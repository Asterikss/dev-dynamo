from dataclasses import dataclass
from typing import Self
from dacite import from_dict

@dataclass(frozen=True)
class Token:
    access_token: str
    expires_in: int
    ext_expires_in: int
    scope: str
    token_type: str

    @classmethod
    def from_dict(cls, data: dict) -> Self | None:
        try:
            return from_dict(data_class=Token, data=data)
        except Exception as e:
            return None