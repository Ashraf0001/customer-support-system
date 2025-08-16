from app.core.schema import WorkflowSchema, NodeConfig
from app.core.workflow import Workflow
from app.schemas.placeholder_schema import PlaceholderEventSchema
from app.workflows.placeholder_workflow_nodes.initial_node import InitialNode


class PlaceholderWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="",
        event_schema=PlaceholderEventSchema,
        start=InitialNode,
        nodes=[
            NodeConfig(
                node=InitialNode,
                connections=[],
                description="",
                parallel_nodes=[],
            ),
        ],
    )
