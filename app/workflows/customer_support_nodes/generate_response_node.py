import json
import logging
import time
from typing import Dict, Any

import requests
from app.core.config import settings
from app.core.nodes.base import Node
from app.core.task import TaskContext
from app.services.prompt_loader import PromptManager
from app.schemas.customer_support_schema import ResponseSchema

logger = logging.getLogger(__name__)


class GenerateResponseNode(Node):
    """Generates helpful responses for customer support tickets.
    
    This node uses the classification results to generate appropriate,
    helpful responses for customer support tickets. It uses Ollama with
    Llama 3.1 8B for lightweight, local AI response generation.
    """
    
    def __init__(self):
        self.ollama_url = f"{settings.ollama_base_url}/api/generate"
        self.model = settings.ollama_model
        self.start_time = None
    
    def process(self, task_context: TaskContext) -> TaskContext:
        """Process the response generation workflow.
        
        Args:
            task_context: The task context containing ticket and classification data
            
        Returns:
            Updated TaskContext with generated response
        """
        self.start_time = time.time()
        ticket = task_context.event
        
        logger.info(f"Starting response generation", extra={
            "ticket_id": ticket.id,
            "node": self.node_name,
            "status": "started"
        })
        
        try:
            # Get classification from previous node
            classification_node = task_context.nodes.get("ClassifyTicketNode", {})
            
            if classification_node.get("status") != "completed":
                raise ValueError("Classification node did not complete successfully")
            
            classification = classification_node.get("classification")
            
            # Build the response prompt using the template
            prompt = self._build_response_prompt(ticket, classification)
            
            # Call Ollama API
            response_result = self._call_ollama(prompt)
            
            # Parse the JSON response
            response_data = self._parse_ollama_response(response_result)
            
            # Calculate processing time
            processing_time = time.time() - self.start_time
            
            # Store results in task context
            task_context.nodes[self.node_name] = {
                "status": "completed",
                "response": response_data,
                "processing_time": processing_time,
                "model_used": self.model
            }
            
            logger.info(f"Response generation completed", extra={
                "ticket_id": ticket.id,
                "node": self.node_name,
                "status": "completed",
                "processing_time": processing_time,
                "response_type": response_data.response_type
            })
            
        except Exception as e:
            processing_time = time.time() - self.start_time if self.start_time else 0
            
            logger.error(f"Response generation failed", extra={
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
    
    def _build_response_prompt(self, ticket, classification) -> str:
        """Build the response generation prompt using the Jinja2 template.
        
        Args:
            ticket: The support ticket data
            classification: The classification results
            
        Returns:
            Formatted prompt string
        """
        try:
            return PromptManager.get_prompt(
                "response_generation",
                ticket=ticket,
                classification=classification
            )
        except Exception as e:
            logger.error(f"Failed to build response prompt: {str(e)}")
            # Fallback to simple prompt
            return f"""
            Generate a helpful response for this support ticket:
            
            Subject: {ticket.subject}
            Content: {ticket.content}
            Priority: {ticket.priority}
            Category: {classification.category}
            Sentiment: {classification.sentiment}
            Urgency: {classification.urgency}
            
            Provide response in JSON format:
            {{
              "response_text": "Your helpful response here...",
              "response_type": "automated",
              "suggested_actions": ["action1", "action2"],
              "confidence": 0.9
            }}
            """
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API for response generation.
        
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
                            "temperature": 0.3,
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
        assert last_err is not None
        raise last_err
    
    def _parse_ollama_response(self, response: str) -> ResponseSchema:
        """Parse the JSON response from Ollama.
        
        Args:
            response: Raw response string from Ollama
            
        Returns:
            Parsed ResponseSchema object
            
        Raises:
            ValueError: If response cannot be parsed as JSON
        """
        try:
            # Try to extract JSON from the response
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
            required_fields = ["response_text", "response_type", "confidence"]
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Create ResponseSchema object
            return ResponseSchema(
                response_text=data["response_text"],
                response_type=data["response_type"],
                suggested_actions=data.get("suggested_actions", []),
                confidence=data["confidence"]
            )
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse Ollama response: {str(e)}")
            logger.error(f"Raw response: {response}")
            
            # Return default response on parsing failure
            return ResponseSchema(
                response_text="Thank you for contacting support. We have received your request and will get back to you shortly. If this is urgent, please contact our support team directly.",
                response_type="escalation",
                suggested_actions=["Contact support team", "Check status page"],
                confidence=0.5
            )
