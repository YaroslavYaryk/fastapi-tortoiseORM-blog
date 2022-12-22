from fastapi import HTTPException

from blog.models import PostLike
from blog.schemas import Status
from blog.pydantic_schemas import PostLikeCreatePydantic, PostLikePydantic


async def create_like_to_post(post_id, user_id):
    post_like_obj = await PostLike.create(post_id=post_id, user_id=user_id)
    return await PostLikePydantic.from_tortoise_orm(post_like_obj)


async def delete_like_to_post(post_id, user_id):
    deleted_count = await PostLike.filter(post_id=post_id, user_id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"PostLike  not found")
    return Status(message=f"Deleted PostLike")


async def handle_press_like_to_blog(post_id, user):
    post_like = await PostLike.filter(post_id=post_id, user_id=user["id"])
    if post_like:
        return await delete_like_to_post(post_id, user["id"])
    else:
        return await create_like_to_post(post_id, user["id"])


async def handle_get_all_post_likes(id):
    return await PostLikePydantic.from_queryset(PostLike.filter(post_id=id))
