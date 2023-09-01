import datetime

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    detail: str


class PostCreateOut(BaseModel):
    user_id: int
    id: int


class PostAnalytics(BaseModel):
    day: datetime.date
    likes: int


class UserCreateOut(BaseModel):
    username: str


class UserLoginOut(BaseModel):
    access_token: str
    token_type: str


class UserActivityOut(BaseModel):
    last_login: datetime.datetime | None
    last_request: datetime.datetime | None


class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str


class UserLogin(BaseModel):
    username: str
    password: str


class PostCreate(BaseModel):
    title: str
    text: str
