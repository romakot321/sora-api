from pathlib import Path

from src.core.config import settings


class FileRepository:
    storage_path = Path(settings.STORAGE_PATH)

    @classmethod
    def write(cls, filename: str, body: bytes):
        with open(cls.storage_path / filename, "wb") as file:
            file.write(body)

    @classmethod
    def read(cls, filename: str) -> bytes | None:
        if not (cls.storage_path / filename).exists():
            return None
        with open(cls.storage_path / filename, "rb") as file:
            return file.read()