from fastapi import FastAPI, status, HTTPException
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

app = FastAPI()

servers = [
    {"id": 1, "name": "web-01", "status": "running"},
    {"id": 2, "name": "db-01", "status": "running"},
    {"id": 3, "name": "worker-01", "status": "stopped"},
]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/servers", response_model=list[Server])
def get_servers(name: str | None=None, status: Literal["running", "stopped"] | None = None):
    
    result = servers
    if name is not None:
        result = [s for s in result if s["name"] == name]
    if status is not None:
        result = [s for s in result if s["status"] == status]

    return result

@app.get("/servers/{server_id}", response_model=Server)
def get_server(server_id: int):
    for server in servers:
        if server["id"] == server_id:
            return server
    raise HTTPException(status_code=404, detail="Server not found")

@app.post("/servers", response_model=Server, status_code=status.HTTP_201_CREATED)
def create_server(new_server: ServerCreate):
    name_check = any(server["name"] == new_server.name for server in servers)

    if name_check is True:
        raise HTTPException(
            status_code=409,
            detail="Server with this name already exists"
        )   
    
    new_id = max(server["id"] for server in servers) + 1
    
    server = {
        "id": new_id,
        "name": new_server.name,
        "status": new_server.status
    }

    servers.append(server)
    return server

@app.delete("/servers/{server_id}", response_model=Server)
def remove_server(server_id: int):
    for server in servers:
        if server["id"] == server_id:
            servers.remove(server)
            return server
    raise HTTPException(status_code=404, detail="Server not found")

@app.patch("/servers/{server_id}", response_model=Server)
def update_server(server_id: int, update: ServerUpdate):
    for server in servers:
        if server["id"] == server_id:
            if update.status is not None:
                server["status"] = update.status
                return server
    raise HTTPException( status_code=404, detail="Server not found")
