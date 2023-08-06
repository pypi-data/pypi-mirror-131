from pydantic import BaseModel


class Configuration(BaseModel):
    event_id: str
