from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import UserModel, UserInfoModel, AccessRole, Subscription, LanguageLevel
from app.schemas.user import UserAddDTO, UserLoginDTO


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, new_user: UserAddDTO, hashed_password: str) -> UserModel:
        user = UserModel(
            name=new_user.name, email=new_user.email, hashed_password=hashed_password
        )
        self.session.add(user)
        await self.session.flush()
        user_info = UserInfoModel(
            access_role=AccessRole.USER,
            subscription=Subscription.FREE,
            language_level=LanguageLevel.BEGINNER,
            user_id=user.id,
        )
        self.session.add(user_info)
        await self.session.commit()
        return user

    async def get_all(self) -> list[UserModel]:
        result = await self.session.execute(select(UserModel))
        users = result.scalars().all()
        return users

    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_info_by_user_id(self, user_id: int) -> Optional[UserInfoModel]:
        result = await self.session.execute(
            select(UserInfoModel).where(UserInfoModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalar_one_or_none()

    async def delete(self, user: UserModel) -> None:
        await self.session.delete(user)
        await self.session.commit()
