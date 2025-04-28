from .base import APIModel


class Detail(APIModel):
    detail_id: str


class DetailTikTok(Detail):
    pass
