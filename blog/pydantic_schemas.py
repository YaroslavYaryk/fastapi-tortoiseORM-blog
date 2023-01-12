from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from .models import Post, PostLike, PostComment, PostCommentLike

# initialize models
Tortoise.init_models(["blog.models", "users.models"], "models")


# Post schemas
PostPydantic = pydantic_model_creator(
    Post, name="Post", include=("id", "title", "body", "author_id", "likes", "author_name")
)
PostCreatePydantic = pydantic_model_creator(
    Post, name="PostIn", exclude_readonly=True, exclude=("author_id",)
)  # will exclude {id}
PostPydanticList = pydantic_queryset_creator(Post)

PostForUserPydantic = pydantic_model_creator(
    Post, name="PostForUserPydantic", include=("id", "title", "body")
)


# PostLike schemas
PostLikePydantic = pydantic_model_creator(
    PostLike, name="PostLike", include=("id", "post_id", "user_id")
)
PostLikeCreatePydantic = pydantic_model_creator(
    PostLike, name="PostLikeIn", exclude_readonly=True, exclude=("post_id", "user_id")
)  # will exclude {id}


# PostComment Schemas
PostCommentPydantic = pydantic_model_creator(
    PostComment,
    name="PostComment",
    include=("id", "post_id", "user_id", "comment", "parent_id","user_name"),
)
PostCommentCreatePydantic = pydantic_model_creator(
    PostComment,
    name="PostCommentIn",
    exclude_readonly=True,
    exclude=("post_id", "user_id"),
)  # will exclude {id}

PostCommentUpdatePydantic = pydantic_model_creator(
    PostComment,
    name="PostCommentUpdate",
    exclude_readonly=True,
    include=("comment",),
)  # will exclude {id}

PostCommentReplyPydantic = pydantic_model_creator(
    PostComment,
    name="PostCommentReply",
    include=("id", "user_id", "comment", "post_id"),
)


# PostCommentLike schemas

PostCommentLikePydantic = pydantic_model_creator(
    PostCommentLike, name="PostCommentLike", include=("id", "comment_id", "user_id")
)
