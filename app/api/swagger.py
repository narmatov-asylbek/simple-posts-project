import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.depends import get_user_repository
from app.services import create_access_token, verify_password
from app.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db.repos import UserRepository
from app.schemas import UserLoginOut

router = APIRouter()


@router.post("/token", response_model=UserLoginOut)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm,
                         Depends()],
    repo: UserRepository = Depends(get_user_repository)):

    user = repo.get_by_username(username=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    valid_password = verify_password(plain_password=form_data.password,
                                     hashed_password=user.password)
    if not valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
