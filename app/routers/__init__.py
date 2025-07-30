from fastapi import APIRouter
from .user import router as user_router
from .root import router as root_router

router = APIRouter()

router.include_router(root_router, tags=["Root"])
router.include_router(user_router, prefix="/users", tags=["Users"])
