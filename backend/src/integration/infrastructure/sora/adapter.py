import json

from loguru import logger
from pydantic import ValidationError

from src.integration.domain.entities import SoraTask, SoraTaskFetchResponse, SoraTaskCreatedResponse
from src.integration.infrastructure.sora.task_repository import SoraTaskRepository


class SoraRestAdapter:
    def __init__(self, task_repository: SoraTaskRepository):
        self.task_repository = task_repository

    def on_task_updated(self, task: SoraTask):
        self.task_repository.update(task.id, task)
        logger.debug(f"SoraTask {task.id} updated")

    def on_task_created(self, task_id: str):
        self.task_repository.create(task_id)
        logger.debug(f"SoraTask {task_id} created")

    def on_tasks_fetch(self, data: dict):
        try:
            tasks_response = SoraTaskFetchResponse.model_validate(data)
        except ValidationError as e:
            print(e)
            pass
        else:
            if tasks_response.task_responses:
                return self.on_task_updated(tasks_response.task_responses[0])

        try:
            created_response = SoraTaskCreatedResponse.model_validate(data)
        except ValidationError as e:
            print(e)
            pass
        else:
            return self.on_task_created(created_response.id)

        logger.error("Failed to proceed on_tasks_fetch: Unexpected data: " + str(data)[:1000])

    def cdp_network_response_received_callback(self, message: dict, response_body: dict | None):
        if "params" not in message or "requestId" not in message.get('params', {}):
            return
        url = message["params"]["response"]["url"]
        mime_type = message["params"]["response"]["headers"].get("content-type", "")
        if "https://sora.chatgpt.com/backend/video_gen" not in url:
            return
        if "application/json" not in mime_type:
            return
        response_body = response_body["body"]
        if isinstance(response_body, str) or isinstance(response_body, bytes):
            response_body = json.loads(response_body)
        self.on_tasks_fetch(response_body)
