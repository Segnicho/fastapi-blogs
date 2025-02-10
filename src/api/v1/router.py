from fastapi import APIRouter

from src.api.v1.endpoints import blogs, users

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["Users"])

router.include_router(blogs.router, prefix="/blogs", tags=["Blogs"])
