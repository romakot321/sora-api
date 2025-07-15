from fastapi import FastAPI

from src.integration.infrastructure.sora.dependencies import get_sora_director


def setup_integration(app: FastAPI):
    director = get_sora_director()

    app.sora_director = director