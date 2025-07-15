from io import BytesIO
from uuid import UUID

from fastapi import File, Depends, APIRouter, UploadFile, BackgroundTasks

from src.task.api.dependencies import HttpClientDepend, TaskUoWDepend, TaskRunnerDepend
from src.task.application.use_cases.create_task import CreateTaskUseCase
from src.task.application.use_cases.get_task import GetTaskUseCase
from src.task.application.use_cases.run_image_task import RunImageTaskUseCase
from src.task.application.use_cases.run_task import RunTaskUseCase
from src.task.domain.dtos import TaskReadDTO, TaskCreateDTO, TaskImageCreateDTO

router = APIRouter()


@router.post("/video", response_model=TaskReadDTO)
async def create_and_run_video_task(
        uow: TaskUoWDepend,
        http_client: HttpClientDepend,
        runner: TaskRunnerDepend,
        background_tasks: BackgroundTasks,
        data: TaskCreateDTO = Depends(TaskCreateDTO.as_form),
        file: UploadFile | None = File(None),
):
    task = await CreateTaskUseCase(uow).execute(data)
    file_buffer = None
    if file is not None:
        file_buffer = BytesIO(await file.read())
    background_tasks.add_task(RunTaskUseCase(uow, runner, http_client).execute, task.id, data, file_buffer)
    return task


@router.post("/image", response_model=TaskReadDTO)
async def create_and_run_image_task(
        uow: TaskUoWDepend,
        http_client: HttpClientDepend,
        runner: TaskRunnerDepend,
        background_tasks: BackgroundTasks,
        data: TaskImageCreateDTO = Depends(TaskImageCreateDTO.as_form),
        file: UploadFile | None = File(None),
):
    task = await CreateTaskUseCase(uow).execute(data)
    file_buffer = None
    if file is not None:
        file_buffer = BytesIO(await file.read())
    background_tasks.add_task(RunImageTaskUseCase(uow, runner, http_client).execute, task.id, data, file_buffer)
    return task


@router.get("/{task_id}", response_model=TaskReadDTO)
async def get_task(task_id: UUID, uow: TaskUoWDepend):
    return await GetTaskUseCase(uow).execute(task_id)
