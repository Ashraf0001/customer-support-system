from app.core.schema import WorkflowSchema, NodeConfig
from app.core.workflow import Workflow
from app.schemas.customer_support_schema import SupportTicketSchema
from app.workflows.customer_support_nodes.analyze_ticket_node import AnalyzeTicketNode
from app.workflows.customer_support_nodes.classify_ticket_node import ClassifyTicketNode
from app.workflows.customer_support_nodes.generate_response_node import GenerateResponseNode


class CustomerSupportWorkflow(Workflow):
    """Customer support ticket processing workflow.
    
    This workflow processes incoming customer support tickets through
    a series of AI-powered analysis and response generation steps:
    
    1. AnalyzeTicketNode: Analyzes ticket content for classification and sentiment
    2. ClassifyTicketNode: Validates and enhances classification results
    3. GenerateResponseNode: Generates appropriate response based on classification
    
    The workflow follows the lightweight MVP pattern with 3 nodes maximum
    and simple, linear processing flow.
    """
    
    workflow_schema = WorkflowSchema(
        description="Customer support ticket processing workflow for lightweight MVP",
        event_schema=SupportTicketSchema,
        start=AnalyzeTicketNode,
        nodes=[
            NodeConfig(
                node=AnalyzeTicketNode,
                connections=[ClassifyTicketNode],
                description="Analyzes incoming support tickets for classification and sentiment using Ollama"
            ),
            NodeConfig(
                node=ClassifyTicketNode,
                connections=[GenerateResponseNode],
                description="Validates and enhances classification results with business logic"
            ),
            NodeConfig(
                node=GenerateResponseNode,
                connections=[],
                description="Generates helpful responses based on classification using Ollama"
            ),
        ],
    )
