import time
from io import BytesIO
from uuid import uuid4

from src.integration.domain.entities import SoraGenerateDTO, SoraTask, SoraGenerateImageDTO
from src.integration.infrastructure.sora.file_repository import FileRepository
from src.integration.infrastructure.sora.llm_provider.directors.sora import SoraDirector
from src.integration.infrastructure.sora.task_repository import SoraTaskRepository


def run_sora_generate_video(director: SoraDirector, dto: SoraGenerateDTO, file: BytesIO | None):
    director.update_type("Video")

    if file:
        filename = str(uuid4())
        FileRepository.write(filename, file.read())
        director.upload_file(str(FileRepository.storage_path / filename))

    director.update_aspect_ratio(dto.aspect_ratio)
    director.update_duration(dto.duration)
    director.update_resolution(dto.resolution)
    director.update_variation(1)

    director.create_video_safely(dto.prompt)


def run_sora_generate_image(director: SoraDirector, dto: SoraGenerateImageDTO, file: BytesIO | None):
    director.update_type("Image")

    if file:
        filename = str(uuid4()) + ".png"
        FileRepository.write(filename, file.read())
        director.upload_file(str(FileRepository.storage_path / filename))

    director.update_aspect_ratio(dto.aspect_ratio)

    director.create_image(dto.prompt)


def wait_for_sora_task_created(task_repository: SoraTaskRepository, dto: SoraGenerateDTO | SoraGenerateImageDTO) -> SoraTask:
    for _ in range(60):
        time.sleep(1)

        for task in task_repository.get_list():
            if not task.prompt:
                continue
            if task.prompt.strip().lower() == dto.prompt.strip().lower():
                return task

    raise TimeoutError()


def wait_for_sora_task_complete(task_repository: SoraTaskRepository, task: SoraTask) -> SoraTask:
    for _ in range(60 * 5):
        time.sleep(1)

        task = task_repository.get_by_id(task.id)
        if task.status == 'succeeded' or task.status == 'failed':
            return task

    raise TimeoutError()
