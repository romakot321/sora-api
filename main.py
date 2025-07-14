import time

from llm_provider.browsers.chrome import ChromeBrowser
from llm_provider.directors.sora import SoraDirector
from llm_provider import get_provider_config
from rest.adapter import RestAdapter
from rest.api import run_generate, wait_for_created, wait_for_complete
from rest.dtos import GenerateDTO
from rest.task_repository import TaskRepository

task_repository = TaskRepository()
rest_adapter = RestAdapter(task_repository)

browser = ChromeBrowser(rest_adapter)
director = SoraDirector(browser, get_provider_config("sora"))

dto = GenerateDTO(aspect_ratio="16:9", duration=5, resolution="480p", prompt="Hi!")
run_generate(director, dto)
task = wait_for_created(task_repository, dto)
print("Created", task)
task = wait_for_complete(task_repository, task)
print("Finished", task)