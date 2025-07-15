from src.integration import SoraTaskRepository, SoraRestAdapter, ChromeBrowser, SoraDirector, get_provider_config


def get_sora_task_repository():
    return SoraTaskRepository()


def get_sora_rest_adapter():
    return SoraRestAdapter(get_sora_task_repository())


def get_sora_director():
    global _browser
    return SoraDirector(_browser, get_provider_config("sora"))


_browser = ChromeBrowser(get_sora_rest_adapter())
