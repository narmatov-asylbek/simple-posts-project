import datetime

from pydantic import BaseModel


class Post(BaseModel):
    id: int | None = None
    user_id: int | None = None
    title: str | None = None
    text: str | None = None
    created_at: str | None = None


class User(BaseModel):
    id: int | None = None
    username: str
    password: str | None = None
    last_login: datetime.datetime | None = None
    last_request: datetime.datetime | None = None


class PostLike(BaseModel):
    id: int | None = None
    user_id: int
    post_id: int
