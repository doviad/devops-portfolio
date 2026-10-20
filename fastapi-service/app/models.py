from pydantic import BaseModel
from typing import Literal

class Server(BaseModel):
    id: int
    name: str
    status: Literal["running", "stopped"]

class ServerCreate(BaseModel):
    name: str
    status: Literal["running", "stopped"]

class ServerUpdate(BaseModel):
    status: Literal["running", "stopped"] | None=None
