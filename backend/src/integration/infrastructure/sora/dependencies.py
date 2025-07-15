from src.integration.infrastructure.sora.adapter import SoraRestAdapter
from src.integration.infrastructure.sora.llm_provider import get_provider_config
from src.integration.infrastructure.sora.llm_provider.browsers import ChromeBrowser
from src.integration.infrastructure.sora.llm_provider.directors import SoraDirector
from src.integration.infrastructure.sora.task_repository import SoraTaskRepository


def get_sora_task_repository():
    return SoraTaskRepository()


def get_sora_rest_adapter():
    return SoraRestAdapter(get_sora_task_repository())


def get_sora_director():
    global _browser
    return SoraDirector(_browser, get_provider_config("sora"))


_browser = ChromeBrowser(get_sora_rest_adapter())
