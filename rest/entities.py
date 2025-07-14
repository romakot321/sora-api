from typing import Literal

from pydantic import BaseModel


class TaskGeneration(BaseModel):
    id: str
    url: str
    task_id: str | None = None
    title: str | None = None


class Task(BaseModel):
    id: str
    status: Literal["queued", "succeeded", "failure"]
    generations: list[TaskGeneration]
    prompt: str | None = None
    failure_reason: str | None = None


class TaskFetchResponse(BaseModel):
    task_responses: list[Task]
    last_id: str | None = None


class TaskCreatedResponse(BaseModel):
    id: str