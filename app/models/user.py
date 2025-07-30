from datetime import datetime
from sqlalchemy import TIMESTAMP, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.datasources.database import Base
from typing import Annotated
import enum

intpk = Annotated[int, mapped_column(primary_key=True)]


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)


class Subscription(enum.Enum):
    FREE = "free"
    PRO = "pro"
    PREMIUM = "premium"

class LanguageLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class UserInfoModel(Base):
    __tablename__ = "user_info"

    id: Mapped[intpk]
    subscription: Mapped[Subscription]
    language_level: Mapped[LanguageLevel]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


# Императивный метод создания таблицы
# metadata = MetaData()

# users_table = Table(
#     "users",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(255), nullable=False),
# )
