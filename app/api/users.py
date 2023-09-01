import datetime

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.exceptions import StartNaviException

from app.schemas import UserCreate, UserCreateOut, UserActivityOut, UserLogin, UserLoginOut
from app.api.depends import get_current_user, get_user_repository
from app.services import create_user, verify_password, create_access_token
from app.models import User
from app.db.repos import UserRepository
from app.constants import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post('/signup/',
             response_model=UserCreateOut,
             description='Registration for user',
             status_code=status.HTTP_201_CREATED)
def user_signup(
    user: UserCreate, repo: UserRepository = Depends(get_user_repository)
) -> UserCreateOut | JSONResponse:
    try:
        created = create_user(repo=repo,
                              username=user.username,
                              password1=user.password1,
                              password2=user.password2)
    except StartNaviException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'message': e.msg})
    return UserCreateOut(username=created.username)


@router.post('/login/',
             response_model=UserLoginOut,
             status_code=status.HTTP_200_OK,
             description='Login for user')
def user_login(
    user_in: UserLogin, repo: UserRepository = Depends(get_user_repository)
) -> UserLoginOut:
    user = repo.get_by_username(username=user_in.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    valid_password = verify_password(plain_password=user_in.password,
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
    return UserLoginOut(access_token=access_token, token_type='bearer')


@router.get('/activity/',
            response_model=UserActivityOut,
            status_code=status.HTTP_200_OK,
            description='Get activity of user')
def get_activity_by_user(user: User = Depends(
    get_current_user)) -> UserActivityOut:
    return UserActivityOut(last_login=user.last_login,
                           last_request=user.last_request)
