import logging
from typing import Dict, Any

from app.core.nodes.base import Node
from app.core.task import TaskContext
from app.schemas.customer_support_schema import SimpleClassificationSchema

logger = logging.getLogger(__name__)


class ClassifyTicketNode(Node):
    """Processes and validates ticket classification results.
    
    This node takes the raw analysis results from AnalyzeTicketNode
    and converts them into structured classification data. It also
    applies business logic for classification validation and enhancement.
    """
    
    def process(self, task_context: TaskContext) -> TaskContext:
        """Process the ticket classification workflow.
        
        Args:
            task_context: The task context containing analysis results
            
        Returns:
            Updated TaskContext with validated classification
        """
        ticket = task_context.event
        
        logger.info(f"Starting ticket classification", extra={
            "ticket_id": ticket.id,
            "node": self.node_name,
            "status": "started"
        })
        
        try:
            # Get analysis results from previous node
            analysis_node = task_context.nodes.get("AnalyzeTicketNode", {})
            
            if analysis_node.get("status") != "completed":
                raise ValueError("Analysis node did not complete successfully")
            
            # Extract classification data
            raw_classification = analysis_node.get("classification", {})
            
            # Validate and enhance classification
            classification_data = self._validate_classification(raw_classification)
            
            # Apply business logic for classification enhancement
            enhanced_classification = self._enhance_classification(
                classification_data, ticket
            )
            
            # Store results in task context
            task_context.nodes[self.node_name] = {
                "status": "completed",
                "classification": enhanced_classification,
                "original_analysis": raw_classification
            }
            
            logger.info(f"Ticket classification completed", extra={
                "ticket_id": ticket.id,
                "node": self.node_name,
                "status": "completed",
                "category": enhanced_classification.category,
                "sentiment": enhanced_classification.sentiment,
                "urgency": enhanced_classification.urgency
            })
            
        except Exception as e:
            logger.error(f"Ticket classification failed", extra={
                "ticket_id": ticket.id,
                "node": self.node_name,
                "status": "error",
                "error": str(e)
            })
            
            task_context.nodes[self.node_name] = {
                "status": "error",
                "error": str(e)
            }
        
        return task_context
    
    def _validate_classification(self, raw_data: Dict[str, Any]) -> SimpleClassificationSchema:
        """Validate and convert raw classification data to structured format.
        
        Args:
            raw_data: Raw classification data from AI analysis
            
        Returns:
            Validated SimpleClassificationSchema object
        """
        # Validate category
        category = raw_data.get("category", "general").lower()
        valid_categories = [
            "technical", "billing", "general", "feature_request", 
            "bug_report", "account", "security"
        ]
        if category not in valid_categories:
            category = "general"
        
        # Validate sentiment
        sentiment = raw_data.get("sentiment", "neutral").lower()
        valid_sentiments = ["positive", "neutral", "negative"]
        if sentiment not in valid_sentiments:
            sentiment = "neutral"
        
        # Validate urgency
        urgency = raw_data.get("urgency", "medium").lower()
        valid_urgency_levels = ["low", "medium", "high"]
        if urgency not in valid_urgency_levels:
            urgency = "medium"
        
        # Validate confidence
        confidence = raw_data.get("confidence", 0.5)
        if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
            confidence = 0.5
        
        return SimpleClassificationSchema(
            category=category,
            sentiment=sentiment,
            urgency=urgency,
            confidence=confidence
        )
    
    def _enhance_classification(
        self, 
        classification: SimpleClassificationSchema, 
        ticket
    ) -> SimpleClassificationSchema:
        """Apply business logic to enhance classification.
        
        Args:
            classification: Validated classification data
            ticket: Original ticket data
            
        Returns:
            Enhanced classification with business logic applied
        """
        # Adjust urgency based on ticket priority
        if ticket.priority == "high" and classification.urgency == "low":
            classification.urgency = "medium"
        elif ticket.priority == "low" and classification.urgency == "high":
            classification.urgency = "medium"
        
        # Adjust sentiment based on urgency
        if classification.urgency == "high" and classification.sentiment == "positive":
            # High urgency with positive sentiment might indicate sarcasm or frustration
            classification.sentiment = "negative"
        
        # Adjust confidence based on content length
        if len(ticket.content) < 50:
            # Short content might have lower confidence
            classification.confidence = min(classification.confidence, 0.7)
        
        return classification
