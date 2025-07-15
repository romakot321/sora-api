from enum import Enum
from typing import Literal

from pydantic import BaseModel


class IntegrationTaskStatus(str, Enum):
    preprocessing = "preprocessing"
    queued = "queued"
    started = "started"
    succeeded = "succeeded"
    failure = "failure"


class IntegrationTaskRunParamsDTO(BaseModel):
    duration: Literal["5", "10", "15", "20"]
    aspect_ratio: Literal["16:9", "1:1", "9:16", "2:3", "3:2"]
    resolution: Literal["480p", "720p", "1080p"]
    prompt: str


class IntegrationTaskResultDTO(BaseModel):
    status: IntegrationTaskStatus
    external_task_id: str | None = None
    result: str | None = None
    error: str | None = None
