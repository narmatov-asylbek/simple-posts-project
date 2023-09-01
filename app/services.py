import datetime

from jose import jwt
from passlib.context import CryptContext

from app.constants import SECRET_KEY, ALGORITHM
from app.exceptions import StartNaviException
from app.db.repos import UserRepository, PostRepository, PostLikeRepository
from app.models import User, PostLike, Post
from app.schemas import PostAnalytics

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict,
                        expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_user(repo: UserRepository, username: str, password1: str,
                password2: str) -> User:
    if password1 != password2:
        raise StartNaviException(msg='password are not equal')

    if repo.user_exists(username=username):
        raise StartNaviException(msg='user with this username already exists')

    hashed = get_password_hash(password1)
    return repo.create(username=username, password=hashed)


def create_post(repo: PostRepository, title: str, text: str,
                user_id: int) -> Post:
    return repo.create(title=title, text=text, user_id=user_id)


def post_like(repo: PostLikeRepository, user_id: int,
              post_id: int) -> PostLike | None:
    if not repo.exists(post_id=post_id, user_id=user_id):
        return repo.create(user_id=user_id, post_id=post_id)


def post_unlike(repo: PostLikeRepository, user_id: int, post_id: int) -> None:
    if not repo.exists(post_id=post_id, user_id=user_id):
        raise StartNaviException(msg="Like or Post doesn't exists")
    repo.delete(post_id=post_id, user_id=user_id)


def get_analytics(repo: PostLikeRepository, date_from: datetime.date,
                  date_to: datetime.date) -> list[PostAnalytics]:
    if date_from:
        date_from = datetime.datetime.combine(date_from, datetime.time.min)

    if date_to:
        date_to = datetime.datetime.combine(date_to, datetime.time.max)

    return repo.get_analytics(date_from=date_from, date_to=date_to)
