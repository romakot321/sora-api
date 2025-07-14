from typing import Literal

from pydantic import BaseModel


class GenerateDTO(BaseModel):
    duration: Literal[5, 10, 15, 20]
    aspect_ratio: Literal["16:9", "1:1", "9:16", "2:3", "3:2"]
    resolution: Literal["480p", "720p", "1080p"]
    prompt: str