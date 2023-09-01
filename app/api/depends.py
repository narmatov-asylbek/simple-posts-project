from typing import Annotated, Generator

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.constants import SECRET_KEY, ALGORITHM
from app.db.engine import SessionLocal
from app.db.repos import PostLikeRepository, PostRepository, UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user_repository(session: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(session)


def get_post_like_repository(session: Session = Depends(
    get_db)) -> PostLikeRepository:
    return PostLikeRepository(session)


def get_post_repository(session: Session = Depends(get_db)) -> PostRepository:
    return PostRepository(session)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    repo: UserRepository = Depends(get_user_repository)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = repo.get_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user
