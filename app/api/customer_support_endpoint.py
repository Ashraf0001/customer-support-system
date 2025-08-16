import json
import logging
import time
from http import HTTPStatus
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.worker.config import celery_app
from app.database.support_ticket import SupportTicket
from app.database.repository import GenericRepository
from app.database.session import db_session
from app.schemas.customer_support_schema import SupportTicketSchema, TicketProcessingResult
from app.workflows.workflow_registry import WorkflowRegistry

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/tickets", response_model=TicketProcessingResult)
def submit_support_ticket(
    ticket_data: SupportTicketSchema,
    session: Session = Depends(db_session),
) -> Response:
    """Submit a customer support ticket for processing.
    
    This endpoint receives support tickets, stores them in the database,
    and queues them for asynchronous AI processing. It implements
    a non-blocking pattern to ensure API responsiveness.
    
    Args:
        ticket_data: The support ticket data, validated against SupportTicketSchema
        session: Database session injected by FastAPI dependency
        
    Returns:
        Response: 202 Accepted response with task ID and ticket information
        
    Raises:
        HTTPException: If ticket submission fails
    """
    start_time = time.time()
    
    logger.info(f"Received support ticket submission", extra={
        "ticket_id": ticket_data.id,
        "customer_email": ticket_data.customer_email,
        "subject": ticket_data.subject
    })
    
    try:
        # Store ticket in database
        repository = GenericRepository(
            session=session,
            model=SupportTicket,
        )
        
        # Create database model instance (let DB generate UUID id)
        db_ticket = SupportTicket(
            customer_email=ticket_data.customer_email,
            subject=ticket_data.subject,
            content=ticket_data.content,
            priority=ticket_data.priority,
            status="open"
        )
        
        # Save to database
        repository.create(obj=db_ticket)
        
        # Queue processing task
        task_id = celery_app.send_task(
            "process_customer_support_ticket",
            args=[str(db_ticket.id)],
        )
        
        processing_time = time.time() - start_time
        
        logger.info(f"Support ticket queued for processing", extra={
            "ticket_id": str(db_ticket.id),
            "task_id": str(task_id),
            "processing_time": processing_time
        })
        
        # Return acceptance response
        return Response(
            content=json.dumps({
                "message": "Support ticket submitted successfully",
                "ticket_id": str(db_ticket.id),
                "task_id": str(task_id),
                "status": "processing",
                "processing_time": processing_time
            }),
            status_code=HTTPStatus.ACCEPTED,
            media_type="application/json"
        )
        
    except Exception as e:
        processing_time = time.time() - start_time
        
        logger.error(f"Support ticket submission failed", extra={
            "ticket_id": ticket_data.id,
            "error": str(e),
            "processing_time": processing_time
        })
        
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit support ticket: {str(e)}"
        )


@router.get("/tickets/{ticket_id}", response_model=Dict)
def get_ticket_status(
    ticket_id: str,
    session: Session = Depends(db_session),
) -> Dict:
    """Get the status and results of a support ticket.
    
    Args:
        ticket_id: The unique identifier of the ticket
        session: Database session injected by FastAPI dependency
        
    Returns:
        Dict: Ticket information including processing results
        
    Raises:
        HTTPException: If ticket not found
    """
    try:
        repository = GenericRepository(
            session=session,
            model=SupportTicket,
        )
        
        # Retrieve ticket from database
        ticket = repository.get(id=ticket_id)
        
        if not ticket:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Ticket with id {ticket_id} not found"
            )
        
        # Convert to dictionary for response
        ticket_data = ticket.to_dict()
        
        logger.info(f"Retrieved ticket status", extra={
            "ticket_id": ticket_id,
            "status": ticket.status
        })
        
        return ticket_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve ticket status", extra={
            "ticket_id": ticket_id,
            "error": str(e)
        })
        
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve ticket status: {str(e)}"
        )


@router.get("/tickets", response_model=list[Dict])
def list_tickets(
    limit: int = 10,
    offset: int = 0,
    status: Optional[str] = None,
    customer_email: Optional[str] = None,
    session: Session = Depends(db_session),
) -> list[Dict]:
    """List support tickets with pagination.
    
    Args:
        limit: Maximum number of tickets to return
        offset: Number of tickets to skip
        session: Database session injected by FastAPI dependency
        
    Returns:
        list[Dict]: List of ticket information
    """
    try:
        # Build query with optional filters
        query = session.query(SupportTicket)
        if status:
            query = query.filter(SupportTicket.status == status)
        if customer_email:
            query = query.filter(SupportTicket.customer_email.ilike(f"%{customer_email}%"))
        tickets = (
            query.order_by(SupportTicket.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        # Convert to list of dictionaries
        ticket_list = [ticket.to_dict() for ticket in tickets]
        
        logger.info(f"Retrieved ticket list", extra={
            "count": len(ticket_list),
            "limit": limit,
            "offset": offset
        })
        
        return ticket_list
        
    except Exception as e:
        logger.error(f"Failed to retrieve ticket list", extra={
            "error": str(e)
        })
        
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve ticket list: {str(e)}"
        )


@router.post("/tickets/{ticket_id}/retry", response_model=Dict)
def retry_ticket(
    ticket_id: str,
    session: Session = Depends(db_session),
) -> Dict:
    """Retry processing a failed ticket.

    Sets the ticket back to processing and re-queues the Celery task.
    """
    try:
        repository = GenericRepository(session=session, model=SupportTicket)
        ticket = repository.get(id=ticket_id)
        if not ticket:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Ticket with id {ticket_id} not found",
            )

        ticket.status = "processing"
        ticket.error_message = None
        repository.update(obj=ticket)

        task_id = celery_app.send_task(
            "process_customer_support_ticket", args=[str(ticket.id)]
        )

        return {
            "message": "Ticket re-queued for processing",
            "ticket_id": str(ticket.id),
            "task_id": str(task_id),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Failed to retry ticket: {str(e)}",
        )
