from io import BytesIO
from typing import Type
from httpx import AsyncClient
from pydantic import BaseModel
import pytest

from src.task.domain.dtos import TaskCreateDTO


def _fill_dto(dto: Type[BaseModel]) -> dict:
    data = {}
    for name, field in dto.model_fields.items():
        if field.default is not None:
            data[name] = field.default
        elif isinstance(field.annotation, str):
            data[name] = "string"
        elif isinstance(field.annotation, int):
            data[name] = 0
        elif isinstance(field.annotation, BaseModel):
            data[name] = _fill_dto(data[name])
        else:
            data[name] = None
    return data


@pytest.mark.asyncio
async def test_task_create(test_client: AsyncClient):
    data = _fill_dto(TaskCreateDTO)
    resp = await test_client.post("/api/task", json=data)
