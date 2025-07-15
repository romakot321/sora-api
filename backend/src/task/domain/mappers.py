from src.task.domain.dtos import TaskResultDTO
from src.task.domain.entities import TaskStatus
from src.integration.domain.dtos import IntegrationTaskResultDTO, IntegrationTaskStatus
from src.task.application.interfaces.task_runner import TResponseData


class IntegrationResponseToDomainMapper:
    def map_one(self, data: IntegrationTaskResultDTO) -> TaskResultDTO:
        return TaskResultDTO(
            external_task_id=data.external_task_id,
            status=self._map_status(data.status),
            result=data.result,
            error=data.error
        )

    def _map_status(self, status: IntegrationTaskStatus) -> TaskStatus:
        if status == IntegrationTaskStatus.queued:
            return TaskStatus.queued
        elif status == IntegrationTaskStatus.started:
            return TaskStatus.started
        elif status == IntegrationTaskStatus.failed:
            return TaskStatus.failed
        elif status == IntegrationTaskStatus.finished:
            return TaskStatus.finished
        raise ValueError(f"Failed to map integration response: Unknown status {status}")

