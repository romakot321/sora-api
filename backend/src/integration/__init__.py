from fastapi import FastAPI

from src.integration.infrastructure.sora.adapter import SoraRestAdapter
from src.integration.infrastructure.sora.dependencies import get_sora_director
from src.integration.infrastructure.sora.llm_provider import get_provider_config
from src.integration.infrastructure.sora.llm_provider.browsers import ChromeBrowser
from src.integration.infrastructure.sora.llm_provider.directors import SoraDirector
from src.integration.infrastructure.sora.task_repository import SoraTaskRepository


def setup_integration(app: FastAPI):
    director = get_sora_director()

    app.sora_director = director