from src.core.http.client import AsyncHttpClient
from src.integration.infrastructure.sora.dependencies import get_sora_task_repository, get_sora_director
from src.integration.infrastructure.task_runner import SoraTaskRunner
from src.task.application.interfaces.task_runner import ITaskRunner


def get_integration_task_runner() -> ITaskRunner:
    sora_task_repository = get_sora_task_repository()
    sora_director = get_sora_director()
    return SoraTaskRunner(sora_task_repository, sora_director)
