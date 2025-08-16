from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class SupportTicketSchema(BaseModel):
    """Schema for incoming customer support tickets.
    
    This schema defines the structure for customer support tickets
    in the lightweight MVP. It includes only essential fields needed
    for basic ticket processing and AI response generation.
    """
    
    id: str = Field(..., description="Unique ticket identifier")
    customer_email: str = Field(..., description="Customer email address")
    subject: str = Field(..., min_length=1, max_length=200, description="Ticket subject line")
    content: str = Field(..., min_length=1, max_length=2000, description="Detailed ticket content")
    priority: Optional[str] = Field(default="medium", description="Ticket priority level")
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Ticket creation timestamp",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "ticket_12345",
                "customer_email": "customer@example.com",
                "subject": "Login issues with my account",
                "content": "I'm unable to log into my account. I keep getting an error message saying 'Invalid credentials' even though I'm sure my password is correct.",
                "priority": "high",
            }
        }
    )


class SimpleClassificationSchema(BaseModel):
    """Schema for AI-generated ticket classification.
    
    This schema defines the structure for the AI classification results
    in the lightweight MVP. It includes basic categorization and sentiment.
    """
    
    category: str = Field(..., description="Ticket category (e.g., technical, billing, general)")
    sentiment: str = Field(..., description="Customer sentiment (positive, neutral, negative)")
    urgency: str = Field(..., description="Urgency level (low, medium, high)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="AI confidence score")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "category": "technical",
                "sentiment": "negative",
                "urgency": "high",
                "confidence": 0.85,
            }
        }
    )


class ResponseSchema(BaseModel):
    """Schema for AI-generated responses.
    
    This schema defines the structure for AI-generated responses
    in the lightweight MVP. It includes the response text and metadata.
    """
    
    response_text: str = Field(..., description="AI-generated response text")
    response_type: str = Field(..., description="Type of response (automated, escalation, follow_up)")
    suggested_actions: Optional[list[str]] = Field(default_factory=list, description="Suggested next actions")
    confidence: float = Field(..., ge=0.0, le=1.0, description="AI confidence in the response")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "response_text": "I understand you're having trouble logging into your account. Let me help you resolve this issue. First, please try clearing your browser cache and cookies, then attempt to log in again.",
                "response_type": "automated",
                "suggested_actions": [
                    "Clear browser cache",
                    "Reset password",
                    "Contact support",
                ],
                "confidence": 0.92,
            }
        }
    )


class TicketProcessingResult(BaseModel):
    """Schema for complete ticket processing results.
    
    This schema combines all processing results into a single response
    for the lightweight MVP.
    """
    
    ticket_id: str = Field(..., description="Original ticket ID")
    status: str = Field(..., description="Processing status (completed, failed, processing)")
    classification: Optional[SimpleClassificationSchema] = Field(None, description="AI classification results")
    response: Optional[ResponseSchema] = Field(None, description="AI-generated response")
    processing_time: Optional[float] = Field(None, description="Total processing time in seconds")
    error_message: Optional[str] = Field(None, description="Error message if processing failed")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ticket_id": "ticket_12345",
                "status": "completed",
                "classification": {
                    "category": "technical",
                    "sentiment": "negative",
                    "urgency": "high",
                    "confidence": 0.85,
                },
                "response": {
                    "response_text": "I understand you're having trouble logging into your account...",
                    "response_type": "automated",
                    "suggested_actions": [
                        "Clear browser cache",
                        "Reset password",
                    ],
                    "confidence": 0.92,
                },
                "processing_time": 2.5,
            }
        }
    )

