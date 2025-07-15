from src.integration.domain.entities import SoraTask

_storage = []


class SoraTaskRepository:
    def __init__(self):
        global _storage
        self.storage: list[SoraTask] = _storage

    def create(self, task_id: str) -> SoraTask:
        entity = SoraTask(id=task_id, status="queued", generations=[])
        self.storage.append(entity)
        return entity

    def update(self, task_id: str, data: SoraTask) -> SoraTask:
        for i, task in enumerate(self.storage):
            if task.id == task_id:
                self.storage[i] = SoraTask(**(task.model_dump() | data.model_dump()))
                return self.storage[i]
        raise ValueError(f"Can't find task {task_id}")

    def get_list(self) -> list[SoraTask]:
        return self.storage[:]

    def get_by_id(self, id: str) -> SoraTask:
        for i, task in enumerate(self.storage):
            if task.id == id:
                return task
        raise ValueError(f"Can't find task {id}")
