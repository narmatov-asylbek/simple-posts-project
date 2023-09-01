import datetime

from sqlalchemy import DateTime, String, ForeignKey, UniqueConstraint, func, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class UserDB(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(200))
    last_login: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True)
    last_request: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True)


class PostDB(Base):
    __tablename__ = 'posts'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    title: Mapped[str] = mapped_column(String(200))
    text: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())


class PostLikeDB(Base):
    __tablename__ = 'post_likes'
    __table_args__ = (UniqueConstraint('user_id', 'post_id'), )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
