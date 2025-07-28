from fastapi import APIRouter, HTTPException
from schemas.user import UserAddDTO, UserLoginDTO
from queries import user as user_crud
from datasources.database import SessionDep
from fastapi import Depends
from config.auth import auth

router = APIRouter()


@router.post("/", summary="Register a new user")
async def create_user(new_user: UserAddDTO, session: SessionDep):
    user = await user_crud.create_user(new_user, session)
    return {
        "message": "User created successfully",
        "user_id": user.id,
        "user_name": user.name,
    }


@router.get("/", summary="Get all users")
async def get_all_users(session: SessionDep):
    users = await user_crud.get_all_users(session)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return {"message": "Users found", "users": users}


@router.get("/{user_id}", summary="Get user by id")
async def get_user_by_id(user_id: int, session: SessionDep):
    user = await user_crud.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User found", "user_id": user.id, "user_name": user.name}


# @router.get("/me", summary="Get current user")
# async def get_me(user=Depends(auth.get_current_user)):
#     return {"message": "Authenticated!", "user": user}

@router.post("/login", summary="Login a user")
async def login(credentials: UserLoginDTO, session: SessionDep):
    user = await user_crud.get_user_by_email_and_password(credentials, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "User logged in successfully", "user_id": user.id, "user_name": user.name}


@router.delete("/{user_id}", summary="Delete user by id")
async def delete_user(user_id: int, session: SessionDep):
    user = await user_crud.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user_crud.delete_user(user, session)
    return {"message": "User deleted successfully", "user_id": user.id, "user_name": user.name}
