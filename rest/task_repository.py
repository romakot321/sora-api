from rest.entities import Task

_storage = []


class TaskRepository:
    def __init__(self):
        global _storage
        self.storage: list[Task] = _storage

    def create(self, task_id: str) -> Task:
        entity = Task(id=task_id, status="queued", generations=[])
        self.storage.append(entity)
        return entity

    def update(self, task_id: str, data: Task) -> Task:
        for i, task in enumerate(self.storage):
            if task.id == task_id:
                self.storage[i] = Task(**(task.model_dump() | data.model_dump()))
                return self.storage[i]
        raise ValueError(f"Can't find task {task_id}")

    def get_list(self) -> list[Task]:
        return self.storage[:]

    def get_by_id(self, id: str) -> Task:
        for i, task in enumerate(self.storage):
            if task.id == id:
                return task
        raise ValueError(f"Can't find task {id}")