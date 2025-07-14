import json
from loguru import logger
from pydantic import ValidationError

from rest.entities import TaskCreatedResponse, TaskFetchResponse, Task
from rest.task_repository import TaskRepository


class RestAdapter:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def on_task_updated(self, task: Task):
        self.task_repository.update(task.id, task)
        logger.debug(f"Task {task.id} updated")

    def on_task_created(self, task_id: str):
        self.task_repository.create(task_id)
        logger.debug(f"Task {task_id} created")

    def on_tasks_fetch(self, data: dict):
        try:
            tasks_response = TaskFetchResponse.model_validate(data)
        except ValidationError:
            pass
        else:
            if tasks_response.task_responses:
                self.on_task_updated(tasks_response.task_responses[0])

        try:
            created_response = TaskCreatedResponse.model_validate(data)
        except ValidationError:
            pass
        else:
            self.on_task_created(created_response.id)

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