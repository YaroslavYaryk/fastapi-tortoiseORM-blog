from fastapi import HTTPException, status

from users.models import User, UserPydantic, UserPydanticLogin
from users.hashing import Hash
from users.schemas import UserSchema
from .jwt_handler import create_access_token
from blog.schemas import Status


def get_user_data_for_token(user):
    return {"id": user.id, "email": user.email}


def get_register_login_response(user, token):
    user_data = get_user_data_for_token(user)
    return {**user_data, "access": token}


async def create_user(user: UserSchema):

    user_obj = await User.create(
        username=user.username, email=user.email, password=Hash.bcrypt(user.password)
    )
    access_token = create_access_token(
        data={"user_data": get_user_data_for_token(user_obj)}
    )
    return get_register_login_response(user_obj, access_token)


async def login(request_user_data):
    user = await UserPydanticLogin.from_queryset(
        User.filter(email=request_user_data.email)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials"
        )
    user_obj = user[0]
    if not Hash.verify(user_obj.password, request_user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Incorrect password"
        )
    access_token = create_access_token(
        data={"user_data": get_user_data_for_token(user_obj)}
    )
    return get_register_login_response(user_obj, access_token)


async def handle_get_all_users():
    return await UserPydantic.from_queryset(User.all())


async def handle_get_one_users(id: int):
    return await UserPydantic.from_queryset_single(User.get(id=id))


async def handle_change_one_user(id, user_data):
    await User.filter(id=id).update(**user_data.dict(exclude_unset=True))
    return await UserPydantic.from_queryset_single(User.get(id=id))


async def handle_delete_one_user(id, current_user):
    current_user_id = current_user["id"]
    if current_user_id != id:
        raise HTTPException(status_code=407, detail=f"Cant delete other user")
    deleted_count = await User.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"user {id} not found")
    return Status(message=f"Deleted user {id}")
