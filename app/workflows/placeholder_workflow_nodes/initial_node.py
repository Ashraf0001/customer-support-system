from app.core.nodes.base import Node
from app.core.task import TaskContext


class InitialNode(Node):
    def process(self, task_context: TaskContext) -> TaskContext:
        return task_context
