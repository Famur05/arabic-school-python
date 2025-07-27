from sqlalchemy import text, insert, select
from datasources.database import async_engine, async_session_maker, Base
from models.user import UserModel, UserInfoModel, Subscription, LanguageLevel
from schemas.user import UserDTO, UserAddDTO
from datasources.database import SessionDep
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Для проверки пароля используйте: pwd_context.verify(plain_password, hashed_password)

async def create_tables():
    async with async_engine.begin() as conn:
        # async_engine.echo = False
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        # async_engine.echo = True


async def create_user(new_user: UserAddDTO, session: SessionDep):
    user = UserModel(
        name=new_user.name,
        email=new_user.email,
        hashed_password=pwd_context.hash(new_user.password)
    )
    session.add(user)
    await session.flush()  # Теперь у user.id есть значения
    user_info = UserInfoModel(
        subscription=Subscription.FREE,
        language_level=LanguageLevel.BEGINNER,
        user_id=user.id,
    )
    session.add(user_info)
    await session.commit()
    return user


async def get_all_users(session: SessionDep):
    res = await session.execute(select(UserModel))
    users = res.scalars().all()
    return users


async def get_user_by_id(user_id: int, session: SessionDep):
    res = await session.execute(select(UserModel).where(UserModel.id == user_id))
    user = res.scalar_one_or_none()
    return user


async def delete_user(user: UserModel, session: SessionDep):
    # await session.flush()
    await session.delete(user)
    await session.commit()


# ---------------------------------


# async def get_data():
#     async with async_session_maker() as session:
#         res = await session.execute(select(UserModel))
#         users = res.scalars().all()
#         result_dto = [UserDTO(id=user.id, name=user.name) for user in users]
#         print(f"{result_dto = }")


# async def update_user(user_id: int, new_name: str):
#     async with async_session_maker() as session:
#         user = await session.get(UserModel, user_id)
#         if user:
#             user.name = new_name
#             await session.commit()
#         else:
#             pass


# Императивный метод вставки данных

# async def insert_data():
#     async with async_engine.connect() as conn:
#         # await conn.execute(text("INSERT INTO users (name) VALUES ('John')"))
#         stmt = insert(users).values(
#             {
#                 "name": "Pavel",
#                 "name": "John",
#             }
#         )
#         await conn.execute(stmt)
#         await conn.commit()


# async def get_data():
#     async with async_engine.connect() as conn:
#         res = await conn.execute(text("SELECT * FROM users"))
#         print(f"{res.all() = }")
