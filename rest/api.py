import time

from llm_provider.directors import SoraDirector
from rest.dtos import GenerateDTO
from rest.entities import Task
from rest.task_repository import TaskRepository


def run_generate(director: SoraDirector, dto: GenerateDTO):
    director.update_aspect_ratio(dto.aspect_ratio)
    director.update_duration(dto.duration)
    director.update_resolution(dto.resolution)
    director.update_variation(1)

    director.create_video_safely(dto.prompt)


def wait_for_created(task_repository: TaskRepository, dto: GenerateDTO) -> Task:
    for _ in range(60):
        time.sleep(1)

        for task in task_repository.get_list():
            if task.prompt == dto.prompt:
                return task

    raise TimeoutError()


def wait_for_complete(task_repository: TaskRepository, task: Task) -> Task:
    for _ in range(60):
        time.sleep(1)

        task = task_repository.get_by_id(task.id)
        if task.status == 'succeeded' or task.status == 'failed':
            return task

    raise TimeoutError()
