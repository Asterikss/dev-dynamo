from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Self
from .classes import MSConfig
from dacite import from_dict
import tomllib
import json

@dataclass
class Config:
    ms: MSConfig

    @classmethod
    def from_toml(cls, file_name: str | Path) -> Self:
        with open(file_name, "rb") as toml_file:
            data: dict = tomllib.load(toml_file)
        
        return from_dict(data_class=Config, data=data)

    @classmethod
    def from_json(cls, file_name: str | Path) -> Self:
        with open(file_name) as json_file:
            data: dict = json.load(json_file)
        
        return from_dict(data_class=Config, data=data)