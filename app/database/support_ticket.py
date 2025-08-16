import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from app.database.session import Base


class SupportTicket(Base):
    """Database model for storing customer support tickets.
    
    This model follows the lightweight MVP pattern with essential fields only.
    It stores both the original ticket data and the AI processing results.
    """
    
    __tablename__ = "support_tickets"
    
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        doc="Unique ticket identifier"
    )
    
    # Essential ticket fields
    customer_email = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Customer email address for identification"
    )
    subject = Column(
        String(200),
        nullable=False,
        doc="Ticket subject line"
    )
    content = Column(
        Text,
        nullable=False,
        doc="Detailed ticket content"
    )
    priority = Column(
        String(20),
        default="medium",
        doc="Ticket priority level (low, medium, high)"
    )
    
    # Status tracking
    status = Column(
        String(20),
        default="open",
        doc="Ticket status (open, processing, resolved, closed)"
    )
    
    # AI processing results
    category = Column(
        String(50),
        nullable=True,
        doc="AI-classified ticket category"
    )
    sentiment = Column(
        String(20),
        nullable=True,
        doc="AI-detected customer sentiment"
    )
    urgency = Column(
        String(20),
        nullable=True,
        doc="AI-assessed urgency level"
    )
    ai_response = Column(
        Text,
        nullable=True,
        doc="AI-generated response text"
    )
    response_type = Column(
        String(30),
        nullable=True,
        doc="Type of AI response (automated, escalation, follow_up)"
    )
    
    # Processing metadata
    processing_time = Column(
        Float,
        nullable=True,
        doc="Total processing time in seconds"
    )
    ai_confidence = Column(
        Float,
        nullable=True,
        doc="AI confidence score for classification/response"
    )
    error_message = Column(
        Text,
        nullable=True,
        doc="Error message if processing failed"
    )
    
    # Timestamps
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        doc="Ticket creation timestamp"
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        doc="Last update timestamp"
    )
    
    def __repr__(self):
        return f"<SupportTicket(id={self.id}, subject='{self.subject}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "id": str(self.id),
            "customer_email": self.customer_email,
            "subject": self.subject,
            "content": self.content,
            "priority": self.priority,
            "status": self.status,
            "category": self.category,
            "sentiment": self.sentiment,
            "urgency": self.urgency,
            "ai_response": self.ai_response,
            "response_type": self.response_type,
            "processing_time": self.processing_time,
            "ai_confidence": self.ai_confidence,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
