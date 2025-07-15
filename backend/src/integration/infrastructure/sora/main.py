from io import BytesIO

from src.integration import get_sora_director
from src.integration.domain.entities import SoraGenerateDTO, SoraGenerateImageDTO
from src.integration.infrastructure.sora.api import run_sora_generate_image, wait_for_sora_task_complete, \
    wait_for_sora_task_created
from src.integration.infrastructure.sora.dependencies import get_sora_task_repository


if __name__ == "__main__":
    task_repository = get_sora_task_repository()
    director = get_sora_director()

    with open("/home/eramir/Downloads/1.png", "rb") as f:
        file = BytesIO(f.read())

    dto = SoraGenerateImageDTO(aspect_ratio="2:3", prompt="Hi!")
    run_sora_generate_image(director, dto, file)

    task = wait_for_sora_task_created(task_repository, dto)
    print("Created", task)
    task = wait_for_sora_task_complete(task_repository, task)
    print("Finished", task)
