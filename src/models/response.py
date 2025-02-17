from pydantic import BaseModel


class Response(BaseModel):
    message: str
    data: dict | list[dict] | None = None
