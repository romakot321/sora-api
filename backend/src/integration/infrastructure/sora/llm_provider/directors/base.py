import threading
from abc import ABC, abstractmethod
from typing import Dict, Any

from src.integration.infrastructure.sora.llm_provider.browsers.base import BaseBrowser


class BaseDirectorProvider(ABC):
    def __init__(self, browser: BaseBrowser, config: Dict[str, Any]):
        self.browser = browser
        self.config = config

    @abstractmethod
    def create_video(self, message: str) -> bool:
        pass

    @abstractmethod
    def update_aspect_ratio(self, aspect_ratio: str) -> bool:
        pass

    @abstractmethod
    def update_resolution(self, resolution: str) -> bool:
        pass

    @abstractmethod
    def update_duration(self, duration: int) -> bool:
        pass

    @abstractmethod
    def update_variation(self, variation: int) -> bool:
        pass

    @abstractmethod
    def download_videos(self, path: str) -> bool:
        pass
