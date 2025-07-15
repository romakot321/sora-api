from src.integration.domain.schemas import SoraRunRequest
from src.task.domain.entities import TaskRun


class TaskRunToRequestMapper:
    def map_one(self, task_run: TaskRun, file_id: str) -> SoraRunRequest:
        pass
