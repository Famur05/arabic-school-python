from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserAddDTO, UserLoginDTO, UserDTO
from app.repositories.user import UserRepository
from app.config.auth import auth, config
from fastapi import Response


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)

    async def create(self, new_user: UserAddDTO) -> dict[str, str | int]:
        user = await self.user_repository.create(new_user)
        return {
            "message": "User created successfully",
            "user_id": user.id,
            "user_name": user.name,
        }

    async def get_all(self) -> list[UserDTO]:
        users = await self.user_repository.get_all()
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return [
            UserDTO(
                id=user.id,
                name=user.name,
                email=user.email,
                password=user.hashed_password,
            )
            for user in users
        ]

    async def get_by_id(self, user_id: int) -> UserDTO:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.hashed_password,
        )

    async def login(
        self, credentials: UserLoginDTO, response: Response
    ) -> dict[str, str | int]:
        user = await self.user_repository.get_by_email_and_password(credentials)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = auth.create_access_token(str(user.id))
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=token,
            httponly=config.JWT_COOKIE_HTTP_ONLY,
            secure=config.JWT_COOKIE_SECURE,
            max_age=config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds(),
        )
        return {
            "message": "User logged in successfully",
            "user_id": user.id,
            "user_name": user.name,
            "token": token,
        }

    async def delete(self, user_id: int) -> dict[str, str | int]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await self.user_repository.delete(user)
        return {
            "message": "User deleted successfully",
            "user_id": user.id,
            "user_name": user.name,
        }
