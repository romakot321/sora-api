from typing import Literal

from pydantic import BaseModel


class SoraTaskGeneration(BaseModel):
    id: str
    url: str
    task_id: str | None = None
    title: str | None = None


class SoraTask(BaseModel):
    id: str
    status: Literal["queued", "succeeded", "failure", "preprocessing"]
    generations: list[SoraTaskGeneration]
    prompt: str | None = None
    failure_reason: str | None = None


class SoraTaskFetchResponse(BaseModel):
    task_responses: list[SoraTask]
    last_id: str | None = None


class SoraTaskCreatedResponse(BaseModel):
    id: str


class SoraGenerateDTO(BaseModel):
    duration: Literal[5, 10, 15, 20]
    aspect_ratio: Literal["16:9", "1:1", "9:16", "2:3", "3:2"]
    resolution: Literal["480p", "720p", "1080p"]
    prompt: str