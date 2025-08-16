from enum import Enum

from app.workflows.placeholder_workflow import PlaceholderWorkflow
from app.workflows.customer_support_workflow import CustomerSupportWorkflow


class WorkflowRegistry(Enum):
    PLACEHOLDER = PlaceholderWorkflow
    CUSTOMER_SUPPORT = CustomerSupportWorkflow
