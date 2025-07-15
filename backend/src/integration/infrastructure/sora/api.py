import time

from src.integration.domain.entities import SoraGenerateDTO, SoraTask
from src.integration.infrastructure.sora.llm_provider.directors.sora import SoraDirector
from src.integration.infrastructure.sora.task_repository import SoraTaskRepository


def run_sora_generate(director: SoraDirector, dto: SoraGenerateDTO):
    director.update_aspect_ratio(dto.aspect_ratio)
    director.update_duration(dto.duration)
    director.update_resolution(dto.resolution)
    director.update_variation(1)

    director.create_video_safely(dto.prompt)


def wait_for_sora_task_created(task_repository: SoraTaskRepository, dto: SoraGenerateDTO) -> SoraTask:
    for _ in range(60):
        time.sleep(1)

        for task in task_repository.get_list():
            if task.prompt.strip().lower() == dto.prompt.strip().lower():
                return task

    raise TimeoutError()


def wait_for_sora_task_complete(task_repository: SoraTaskRepository, task: SoraTask) -> SoraTask:
    for _ in range(60):
        time.sleep(1)

        task = task_repository.get_by_id(task.id)
        if task.status == 'succeeded' or task.status == 'failed':
            return task

    raise TimeoutError()
