import enum

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Date
from sqlalchemy import Enum as SQLAlchemyEnum 

from app.core.database import Base

class AnimeStatus(str, enum.Enum):
    WATCHING = "watching"
    COMPLETED = "completed"
    DROPPED = "dropped"
    PLAN_TO_WATCH = "plan_to_watch"

class MangaStatus(str, enum.Enum):
    READING = "reading"
    COMPLETED = "completed"
    DROPPED = "dropped"
    PLAN_TO_READ = "plan_to_read"

class AnimeLibraryEntry(Base):
    __tablename__ = "anime_library_entries"
    __table_args__ = (UniqueConstraint("user_id", "anime_id", name="uq_user_anime"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    anime_id = Column(Integer, nullable=False)
    status = Column(SQLAlchemyEnum(AnimeStatus), nullable=False)
    current_episode = Column(Integer, default=0)
    start_date = Column(Date, nullable=True)

class MangaLibraryEntry(Base):
    __tablename__ = "manga_library_entries"
    __table_args__ = (UniqueConstraint("user_id", "manga_id", name="uq_user_manga"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    manga_id = Column(Integer, nullable=False)
    status = Column(SQLAlchemyEnum(MangaStatus), nullable=False)
    current_chapter = Column(Integer, default=0)
    start_date = Column(Date, nullable=True)

