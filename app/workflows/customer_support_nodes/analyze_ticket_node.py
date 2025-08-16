import json
import logging
import time
from typing import Dict, Any

import requests
from app.core.config import settings
from app.core.nodes.base import Node
from app.core.task import TaskContext
from app.services.prompt_loader import PromptManager

logger = logging.getLogger(__name__)


class AnalyzeTicketNode(Node):
    """Analyzes incoming support tickets for classification and sentiment.
    
    This node processes customer support tickets to extract key information
    such as intent classification, sentiment analysis, and priority scoring.
    It uses Ollama with Llama 3.1 8B for lightweight, local AI processing.
    """
    
    def __init__(self):
        self.ollama_url = f"{settings.ollama_base_url}/api/generate"
        self.model = settings.ollama_model
        self.start_time = None
    
    def process(self, task_context: TaskContext) -> TaskContext:
        """Process the ticket analysis workflow.
        
        Args:
            task_context: The task context containing the ticket data
            
        Returns:
            Updated TaskContext with analysis results
            
        Raises:
            OllamaConnectionError: If unable to connect to Ollama service
            InvalidTicketDataError: If ticket data is malformed
        """
        self.start_time = time.time()
        ticket = task_context.event
        
        logger.info(f"Starting ticket analysis", extra={
            "ticket_id": ticket.id,
            "node": self.node_name,
            "status": "started"
        })
        
        try:
            # Build the prompt using the template
            prompt = self._build_analysis_prompt(ticket)
            
            # Call Ollama API
            classification_result = self._call_ollama(prompt)
            
            # Parse the JSON response
            classification_data = self._parse_ollama_response(classification_result)
            
            # Calculate processing time
            processing_time = time.time() - self.start_time
            
            # Store results in task context
            task_context.nodes[self.node_name] = {
                "status": "completed",
                "classification": classification_data,
                "processing_time": processing_time,
                "model_used": self.model
            }
            
            logger.info(f"Ticket analysis completed", extra={
                "ticket_id": ticket.id,
                "node": self.node_name,
                "status": "completed",
                "processing_time": processing_time,
                "category": classification_data.get("category"),
                "sentiment": classification_data.get("sentiment")
            })
            
        except Exception as e:
            processing_time = time.time() - self.start_time if self.start_time else 0
            
            logger.error(f"Ticket analysis failed", extra={
                "ticket_id": ticket.id,
                "node": self.node_name,
                "status": "error",
                "error": str(e),
                "processing_time": processing_time
            })
            
            task_context.nodes[self.node_name] = {
                "status": "error",
                "error": str(e),
                "processing_time": processing_time
            }
        
        return task_context
    
    def _build_analysis_prompt(self, ticket) -> str:
        """Build the analysis prompt using the Jinja2 template.
        
        Args:
            ticket: The support ticket data
            
        Returns:
            Formatted prompt string
        """
        try:
            return PromptManager.get_prompt(
                "ticket_analysis",
                ticket=ticket
            )
        except Exception as e:
            logger.error(f"Failed to build analysis prompt: {str(e)}")
            # Fallback to simple prompt
            return f"""
            Analyze this support ticket:
            Subject: {ticket.subject}
            Content: {ticket.content}
            Priority: {ticket.priority}
            
            Provide classification in JSON format:
            {{
              "category": "technical",
              "sentiment": "negative",
              "urgency": "high",
              "confidence": 0.85,
              "reasoning": "Brief explanation"
            }}
            """
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API for ticket analysis.
        
        Args:
            prompt: The formatted prompt to send to Ollama
            
        Returns:
            Raw response from Ollama
            
        Raises:
            requests.RequestException: If API call fails
        """
        backoffs = [2, 4, 8]
        last_err: Exception | None = None
        for attempt, delay in enumerate([0] + backoffs, start=1):
            try:
                response = requests.post(
                    self.ollama_url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "top_p": 0.9,
                        },
                    },
                    timeout=60 if attempt == 1 else 30,
                )
                if response.status_code != 200:
                    raise requests.RequestException(
                        f"Ollama API returned status {response.status_code}: {response.text}"
                    )
                result = response.json()
                return result.get("response", "")
            except requests.RequestException as e:
                last_err = e
                logger.error(f"Ollama API call failed (attempt {attempt}): {str(e)}")
                if delay:
                    try:
                        import time as _t
                        _t.sleep(delay)
                    except Exception:
                        pass
        # All attempts failed
        assert last_err is not None
        raise last_err
    
    def _parse_ollama_response(self, response: str) -> Dict[str, Any]:
        """Parse the JSON response from Ollama.
        
        Args:
            response: Raw response string from Ollama
            
        Returns:
            Parsed classification data
            
        Raises:
            ValueError: If response cannot be parsed as JSON
        """
        try:
            # Try to extract JSON from the response
            # Sometimes LLMs include markdown formatting
            if "```json" in response:
                # Extract JSON from markdown code block
                start = response.find("```json") + 7
                end = response.find("```", start)
                json_str = response[start:end].strip()
            elif "```" in response:
                # Extract JSON from code block
                start = response.find("```") + 3
                end = response.find("```", start)
                json_str = response[start:end].strip()
            else:
                # Try to find JSON in the response
                json_str = response.strip()
            
            # Parse the JSON
            data = json.loads(json_str)
            
            # Validate required fields
            required_fields = ["category", "sentiment", "urgency", "confidence"]
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            return data
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse Ollama response: {str(e)}")
            logger.error(f"Raw response: {response}")
            
            # Return default classification on parsing failure
            return {
                "category": "general",
                "sentiment": "neutral",
                "urgency": "medium",
                "confidence": 0.5,
                "reasoning": "Default classification due to parsing error"
            }
