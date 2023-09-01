import datetime

from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse

from app.db.repos import PostLikeRepository, PostRepository
from app.schemas import SuccessResponse, PostCreate, PostCreateOut, PostAnalytics
from app.api.depends import get_current_user, get_post_like_repository, get_post_repository
from app.models import User
from app.services import create_post, post_like, post_unlike, get_analytics
from app.exceptions import StartNaviException

router = APIRouter()


@router.post('/',
             response_model=PostCreateOut,
             description='Create post',
             status_code=status.HTTP_201_CREATED)
def create_post_by_user(post_in: PostCreate,
                        user: User = Depends(get_current_user),
                        repo: PostRepository = Depends(get_post_repository)):

    return create_post(repo=repo,
                       title=post_in.title,
                       text=post_in.text,
                       user_id=user.id)


@router.post('/{post_id}/likes/',
             status_code=status.HTTP_200_OK,
             response_model=SuccessResponse,
             description='Like post')
def like_post_by_user(
    post_id: int,
    user: User = Depends(get_current_user),
    repo: PostLikeRepository = Depends(get_post_like_repository)):

    like = post_like(repo=repo, user_id=user.id, post_id=post_id)
    if like:
        return SuccessResponse(detail='You successfully liked post')
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={'message': 'Like already exists'})


@router.delete('/{post_id}/likes/',
               status_code=status.HTTP_200_OK,
               response_model=SuccessResponse,
               description='Like post')
def unlike_post_by_user(
    post_id: int,
    user: User = Depends(get_current_user),
    repo: PostLikeRepository = Depends(get_post_like_repository)):
    try:
        post_unlike(repo=repo, user_id=user.id, post_id=post_id)
    except StartNaviException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'message': e.msg})
    return SuccessResponse(detail='You unliked post')


@router.get('/analytics/',
            status_code=status.HTTP_200_OK,
            response_model=list[PostAnalytics],
            description="Get analytics of likes")
def get_analytics_by_user(
    date_from: datetime.date,
    date_to: datetime.date,
    repo: PostLikeRepository = Depends(get_post_like_repository)
) -> list[PostAnalytics]:
    return get_analytics(repo=repo, date_from=date_from, date_to=date_to)
