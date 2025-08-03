from fastapi import APIRouter
from .root import router as root_router
from .user import router as user_router

router = APIRouter()

router.include_router(root_router, tags=["Root"])
router.include_router(user_router, prefix="/users", tags=["Users"])
