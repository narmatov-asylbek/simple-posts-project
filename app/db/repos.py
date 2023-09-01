import datetime
from collections import defaultdict

from sqlalchemy.orm import Session
from sqlalchemy import exists, select, func, delete

from app.db.models import UserDB, PostDB, PostLikeDB
from app.models import User, PostLike, Post
from app.schemas import PostAnalytics


class UserRepository:

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, username: str, password: str) -> User:
        user_db = UserDB(username=username, password=password)
        self._session.add(user_db)
        self._session.commit()
        self._session.refresh(user_db)
        return User(id=user_db.id, username=user_db.username)

    def user_exists(self, username: str) -> bool:
        stmt = select(exists(UserDB)).where(UserDB.username == username)
        return self._session.execute(stmt).scalar() or False

    def get_by_username(self, username: str) -> User | None:
        user_db = self._session.execute(
            select(UserDB).where(UserDB.username == username)).scalar()
        if not user_db:
            return None
        return User(id=user_db.id,
                    username=user_db.username,
                    password=user_db.password,
                    last_login=user_db.last_login,
                    last_request=user_db.last_request)


class PostRepository:

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, title: str, text: str, user_id: int) -> Post:
        post_db = PostDB(title=title, text=text, user_id=user_id)
        self._session.add(post_db)
        self._session.commit()
        self._session.refresh(post_db)
        return Post(id=post_db.id,
                    user_id=post_db.user_id,
                    title=post_db.title)


class PostLikeRepository:

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, post_id: int, user_id: int) -> PostLike:
        self._session.add(PostLikeDB(user_id=user_id, post_id=post_id))
        self._session.commit()
        return PostLike(post_id=post_id, user_id=user_id)

    def delete(self, post_id: int, user_id: int) -> None:
        self._session.execute(
            delete(PostLikeDB).where(PostLikeDB.post_id == post_id,
                                     PostLikeDB.user_id == user_id))

    def exists(self, post_id: int, user_id: int) -> bool:
        return self._session.execute(
            select(exists(PostLikeDB)).where(PostLikeDB.user_id == user_id,
                                             PostLikeDB.post_id
                                             == post_id)).scalar() or False

    def get_analytics(self, date_from: datetime.datetime,
                      date_to: datetime.datetime) -> list[PostAnalytics]:
        stmt = (select(
            func.date(PostLikeDB.created_at).label('date'),
            func.count(PostLikeDB.id).label('likes_count')).group_by(
                func.date(PostLikeDB.created_at)))

        if date_from:
            stmt = stmt.where(PostLikeDB.created_at >= date_from)

        if date_to:
            stmt = stmt.where(PostLikeDB.created_at <= date_to)

        likes = self._session.execute(stmt).all()

        mapper = defaultdict(lambda: 0)
        for date, count in likes:
            mapper[date] += count
        return [PostAnalytics(day=k, likes=v) for k, v in mapper.items()]
