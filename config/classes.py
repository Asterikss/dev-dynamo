from dataclasses import dataclass

@dataclass(frozen=True)
class MSURLConfig:
    mails: str
    auth: str
    token: str
    calendar_events: str

@dataclass(frozen=True)
class MSConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    scope: str
    tenant_id: str
    url: MSURLConfig
