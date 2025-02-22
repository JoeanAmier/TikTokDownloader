from datetime import datetime

from pydantic import BaseModel, computed_field


class Response(BaseModel):
    message: str
    data: dict | list[dict] | None = None
    params: dict

    @computed_field
    @property
    def time(self) -> str:
        """格式化后的时间字符串"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
