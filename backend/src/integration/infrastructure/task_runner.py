import json
from io import BytesIO

from src.core.config import settings
from src.core.http.client import IHttpClient
from src.integration import SoraTaskRepository, SoraDirector
from src.integration.domain.entities import SoraGenerateDTO
from src.integration.infrastructure.sora.api import run_sora_generate, wait_for_sora_task_created
from src.task.domain.entities import TaskRun
from src.integration.domain.dtos import IntegrationTaskResultDTO, IntegrationTaskStatus
from src.integration.domain.mappers import TaskRunToRequestMapper
from src.integration.domain.schemas import SoraRunResponse, SoraRunRequest
from src.integration.domain.exceptions import IntegrationRequestException
from src.task.application.interfaces.task_runner import ITaskRunner
from src.integration.infrastructure.http_api_client import HttpApiClient


class SoraTaskRunner(ITaskRunner[IntegrationTaskResultDTO]):
    def __init__(self, task_repository: SoraTaskRepository, sora_director: SoraDirector):
        self.task_repository = task_repository
        self.sora_director = sora_director

    async def start(self, data: TaskRun) -> IntegrationTaskResultDTO:
        dto = SoraGenerateDTO(**data.model_dump())
        run_sora_generate(self.sora_director, dto)
        task = wait_for_sora_task_created(self.task_repository, dto)
        return IntegrationTaskResultDTO(status=IntegrationTaskStatus.queued, external_task_id=task.id)

    async def get_result(self, external_task_id: str) -> IntegrationTaskResultDTO | None:
        task = self.task_repository.get_by_id(external_task_id)
        if task.status == 'succeeded' or task.status == 'failed':
            return IntegrationTaskResultDTO(status=IntegrationTaskStatus(task.status), external_task_id=task.id, result=task.generations[0].url if task.generations else None, error=task.failure_reason)
        return None
