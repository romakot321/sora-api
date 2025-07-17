import random

from src.integration.infrastructure.sora.adapter import SoraRestAdapter
from src.integration.infrastructure.sora.llm_provider import get_provider_config
from src.integration.infrastructure.sora.llm_provider.browsers.chrome import ChromeBrowser
from src.integration.infrastructure.sora.llm_provider.directors.sora import SoraDirector
from src.integration.infrastructure.sora.task_repository import SoraTaskRepository


def get_sora_task_repository():
    return SoraTaskRepository()


def get_sora_rest_adapter():
    return SoraRestAdapter(get_sora_task_repository())


def get_sora_director():
    global browsers
    browser = random.choice(browsers)
    return SoraDirector(browser, get_provider_config("sora"))


browsers = [ChromeBrowser(get_sora_rest_adapter(), browser_name="chrome"), ChromeBrowser(get_sora_rest_adapter(), browser_name="chrome2"), ChromeBrowser(get_sora_rest_adapter(), browser_name="chrome3")]