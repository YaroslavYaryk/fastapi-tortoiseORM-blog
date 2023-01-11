from fastapi import HTTPException

from blog.models import PostComment, PostCommentLike
from blog.schemas import Status
from blog.pydantic_schemas import PostCommentLikePydantic, PostCommentPydantic


async def create_like_to_comment(comment_id, user_id):
    comment_like_obj = await PostCommentLike.create(
        comment_id=comment_id, user_id=user_id
    )
    return await PostCommentLikePydantic.from_tortoise_orm(comment_like_obj)


async def delete_like_to_comment(comment_id, user_id):
    deleted_count = await PostCommentLike.filter(
        comment_id=comment_id, user_id=user_id
    ).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"CommentLike  not found")
    return Status(message=f"Deleted CommentLike")


async def handle_press_like_to_comment(comment_id, user):
    post_like = await PostCommentLike.filter(comment_id=comment_id, user_id=user["id"])
    if post_like:
        return await delete_like_to_comment(comment_id, user["id"])
    else:
        return await create_like_to_comment(comment_id, user["id"])


async def handle_get_all_comment_likes(id):
    return await PostCommentLikePydantic.from_queryset(
        PostCommentLike.filter(comment_id=id)
    )



async def handle_get_comment_likes_for_blog(id):
    comment_queryset = await PostCommentPydantic.from_queryset(PostComment.filter(post_id=id))
    comment_ids = [elem.id for elem in comment_queryset]
    
    return await PostCommentLikePydantic.from_queryset(PostCommentLike.filter(comment__id__in=comment_ids))