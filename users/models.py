from tortoise import fields, Tortoise, models
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class User(models.Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    #: This is a username
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=128, null=True)
    is_active = fields.BooleanField(default=True)
    is_admin = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    # class PydanticMeta:
    #     exclude = ["password"]


Tortoise.init_models(["blog.models", "users.models"], "models")
UserPydantic = pydantic_model_creator(User, name="User", exclude=("password",))
UserPydanticLogin = pydantic_model_creator(User, name="UserLogin")
UserCreatePydantic = pydantic_model_creator(
    User, name="UserIn", exclude_readonly=True
)  # will exclude {id}
UserPydanticList = pydantic_queryset_creator(User)
