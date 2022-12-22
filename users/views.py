from fastapi import APIRouter, Depends
from typing import List
from .models import User, UserCreatePydantic, UserPydantic, UserPydanticList
from .schemas import UserSchema, UserRegisteLoginResponse, UserLoginSchema
from .services import handle_user
from .oauth2 import get_current_user
from blog.schemas import Status

router = APIRouter(prefix="/users")


@router.post("/auth/register/", response_model=UserRegisteLoginResponse, tags=["auth"])
async def register_user(user: UserSchema):
    return await handle_user.create_user(user)


@router.post("/auth/login/", response_model=UserRegisteLoginResponse, tags=["auth"])
async def login_user(user: UserLoginSchema):
    return await handle_user.login(user)


@router.get("/", response_model=List[UserPydantic], tags=["user"])
async def get_all_users():
    return await handle_user.handle_get_all_users()


@router.get("/{id}", response_model=UserPydantic, tags=["user"])
async def get_one_user(id: int, current_user=Depends(get_current_user)):
    return await handle_user.handle_get_one_users(id)


@router.put("/{id}", response_model=UserPydantic, tags=["user"])
async def change_one_user(
    id: int, user_data: UserCreatePydantic, current_user=Depends(get_current_user)
):
    return await handle_user.handle_change_one_user(id, user_data)


@router.delete("/{id}", response_model=Status, tags=["user"])
async def delete_one_user(id: int, current_user=Depends(get_current_user)):
    return await handle_user.handle_delete_one_user(id, current_user)
