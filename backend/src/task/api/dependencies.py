from typing import Annotated

from fastapi import Depends

from src.core.http.client import IHttpClient
from src.core.http.dependencies import get_http_client
from src.integration.api.dependencies import get_integration_task_runner
from src.task.application.interfaces.task_runner import ITaskRunner
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.infrastructure.db.unit_of_work import TaskUnitOfWork


def get_task_uow() -> ITaskUnitOfWork:
    return TaskUnitOfWork()


def get_task_runner() -> ITaskRunner:
    return get_integration_task_runner()


TaskUoWDepend = Annotated[ITaskUnitOfWork, Depends(get_task_uow)]
TaskRunnerDepend = Annotated[ITaskRunner, Depends(get_task_runner)]
HttpClientDepend = Annotated[IHttpClient, Depends(get_http_client)]
