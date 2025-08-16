from contextlib import contextmanager

from app.worker.config import celery_app
from app.database.event import Event
from app.database.support_ticket import SupportTicket
from app.database.repository import GenericRepository
from app.database.session import SessionLocal
from app.workflows.workflow_registry import WorkflowRegistry

"""
Workflow Task Processing Module

This module handles asynchronous processing of workflow events using Celery.
It manages the lifecycle of event processing from database retrieval through
workflow execution and result storage.
"""


@celery_app.task(name="process_incoming_event")
def process_incoming_event(event_id: str):
    """Processes an incoming event through its designated workflow.

    This Celery task handles the asynchronous processing of events by:
    1. Retrieving the event from the database
    2. Determining the appropriate workflow
    3. Executing the workflow
    4. Storing the results

    Args:
        event_id: Unique identifier of the event to process
        workflow_type: Type of workflow to use for processing the event
    """
    session = SessionLocal()
    try:
        # Initialize repository for database operations
        repository = GenericRepository(session=session, model=Event)

        # Retrieve event from database
        db_event = repository.get(id=event_id)
        if db_event is None:
            raise ValueError(f"Event with id {event_id} not found")

        # Execute workflow and store results
        workflow = WorkflowRegistry[db_event.workflow_type].value()
        task_context = workflow.run(db_event.data).model_dump(mode="json")

        db_event.task_context = task_context

        # Update event with processing results
        repository.update(obj=db_event)
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


@celery_app.task(name="process_customer_support_ticket")
def process_customer_support_ticket(ticket_id: str):
    """Processes a customer support ticket through the AI workflow.

    This Celery task handles the asynchronous processing of support tickets by:
    1. Retrieving the ticket from the database
    2. Executing the customer support workflow
    3. Updating the ticket with AI processing results

    Args:
        ticket_id: Unique identifier of the support ticket to process
    """
    session = SessionLocal()
    try:
        # Initialize repository for database operations
        repository = GenericRepository(session=session, model=SupportTicket)

        # Retrieve ticket from database
        db_ticket = repository.get(id=ticket_id)
        if db_ticket is None:
            raise ValueError(f"Support ticket with id {ticket_id} not found")

        # Update status to processing
        db_ticket.status = "processing"
        repository.update(obj=db_ticket)

        # Execute customer support workflow
        workflow = WorkflowRegistry.CUSTOMER_SUPPORT.value()
        
        # Convert database model to schema for workflow
        from app.schemas.customer_support_schema import SupportTicketSchema
        ticket_schema = SupportTicketSchema(
            id=str(db_ticket.id),
            customer_email=db_ticket.customer_email,
            subject=db_ticket.subject,
            content=db_ticket.content,
            priority=db_ticket.priority,
            created_at=db_ticket.created_at
        )
        
        # Run the workflow
        task_context = workflow.run(ticket_schema)
        
        # Extract results from workflow
        analysis_node = task_context.nodes.get("AnalyzeTicketNode", {})
        classification_node = task_context.nodes.get("ClassifyTicketNode", {})
        response_node = task_context.nodes.get("GenerateResponseNode", {})
        
        # Update ticket with AI processing results
        if analysis_node.get("status") == "completed":
            classification_data = analysis_node.get("classification", {})
            db_ticket.category = classification_data.get("category")
            db_ticket.sentiment = classification_data.get("sentiment")
            db_ticket.urgency = classification_data.get("urgency")
            db_ticket.ai_confidence = classification_data.get("confidence")
            db_ticket.processing_time = analysis_node.get("processing_time", 0)
        
        if response_node.get("status") == "completed":
            response_data = response_node.get("response")
            if response_data:
                db_ticket.ai_response = response_data.response_text
                db_ticket.response_type = response_data.response_type
        
        # Update status based on processing results
        if (analysis_node.get("status") == "completed" and 
            response_node.get("status") == "completed"):
            db_ticket.status = "resolved"
        else:
            db_ticket.status = "failed"
            db_ticket.error_message = "AI processing failed"
        
        # Update the ticket in database
        repository.update(obj=db_ticket)
        session.commit()
        
    except Exception as e:
        session.rollback()
        # Update ticket with error information
        if 'db_ticket' in locals():
            db_ticket.status = "failed"
            db_ticket.error_message = str(e)
            repository.update(obj=db_ticket)
            session.commit()
        raise
    finally:
        session.close()
