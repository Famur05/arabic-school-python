from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserAddDTO, UserLoginDTO, UserDTO
from app.repositories.user import UserRepository
from app.config.auth import auth, config
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)

    async def create(self, new_user: UserAddDTO) -> dict[str, str | int]:
        hashed_password = pwd_context.hash(new_user.password)
        user = await self.user_repository.create(new_user, hashed_password)
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
                email=user.email
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
        )

    async def login(
        self, credentials: UserLoginDTO, response: Response
    ) -> dict[str, str | int]:
        user = await self.user_repository.get_by_email(credentials.email)
        if not user or not pwd_context.verify(
            credentials.password, user.hashed_password
        ):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        user_info = await self.user_repository.get_user_info_by_user_id(user.id)
        role = user_info.access_role.value

        token = auth.create_access_token(str(user.id), data={"role": role})

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
            "role": role,
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
