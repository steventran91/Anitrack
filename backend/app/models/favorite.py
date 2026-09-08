import enum
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy import Enum as SQLAlchemyEnum
from app.core.database import Base

class FavoriteType(str, enum.Enum):
    ANIME = "anime"
    MANGA = "manga"
    CHARACTER = "character"

class Favorite(Base):
    __tablename__ = "favorite"
    __table_args__ = (UniqueConstraint("user_id", "item_type", "item_id"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_type = Column(SQLAlchemyEnum(FavoriteType), nullable=False)
    item_id = Column(Integer, nullable=False)