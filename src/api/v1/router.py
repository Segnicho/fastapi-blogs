from fastapi import APIRouter

from src.api.v1.endpoints import blogs, users, auth

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["Users"])

router.include_router(blogs.router, prefix="/blogs", tags=["Blogs"])

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
