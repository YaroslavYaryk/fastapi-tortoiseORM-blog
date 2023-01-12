from fastapi import HTTPException

from blog.pydantic_schemas import (
    PostCommentPydantic,
    PostCommentCreatePydantic,
    PostCommentReplyPydantic,
    PostCommentLikePydantic,
)
from blog.models import PostComment
from blog.schemas import Status
from .handle_post import get_author_by_id

async def handle_create_comment_to_post(
    id: int, comment: PostCommentCreatePydantic, current_user: dict
):
    post_comment = await PostComment.create(
        **comment.dict(), post_id=id, user_id=current_user["id"]
    )
    comment =  await PostCommentPydantic.from_tortoise_orm(post_comment)

    return {
        **comment.dict(),
        "user_name": (await get_author_by_id(current_user["id"])).username
    }


async def get_replies_to_comment(comment_id: int):
    comment_replies = await PostComment.get(id=comment_id).prefetch_related(
        "comment_children"
    )  # connect row post_likes as related field to Post table
  
    return [
            {**elem.dict(), "user_name":(await get_author_by_id(elem.user_id)).username} for elem in await PostCommentReplyPydantic.from_queryset(
        comment_replies.comment_children.all()
    )
    ]


async def get_likes_to_comment(comment_id: int):
    comment_likes = await PostComment.get(id=comment_id).prefetch_related(
        "post_comment_likes"
    )  # connect row post_likes as related field to Post table
   
    return await PostCommentLikePydantic.from_queryset(
        comment_likes.post_comment_likes.all()
    )


async def get_likes_to_comment(comment_id: int):
    comment_likes = await PostComment.get(id=comment_id).prefetch_related(
        "post_comment_likes"
    )  # connect row post_likes as related field to Post table
    return await comment_likes.post_comment_likes.all()


async def get_author_for_comment(commentId):
    post = await PostCommentPydantic.from_queryset_single(PostComment.get(id=commentId))
    return await get_author_by_id(post.author_id)



async def handle_get_all_post_comments(id):

    comment_queryset = PostComment.filter(post_id=id, parent_id=None)
    children = [
        el.id for el in await PostCommentPydantic.from_queryset(comment_queryset)
    ]
    comments_result = [
        {**item.dict(), "user_name": (await get_author_by_id(item.user_id)).username}
        for item in (await PostCommentPydantic.from_queryset(comment_queryset))
    ]
    for index, i in enumerate(children):
        comments_result[index]["replies"] = await get_replies_to_comment(i)
        # comments_result[index]["user_name"] = await get_likes_to_comment(i)
    return comments_result

    return await PostCommentPydantic.from_queryset(
        PostComment.filter(post_id=id, parent_id=None)
    )


async def handle_get_one_comment(comment_id):

    comment_replies = await get_replies_to_comment(comment_id)
    comment_likes = await get_likes_to_comment(comment_id)

    comment = await PostCommentPydantic.from_queryset_single(
        PostComment.get(id=comment_id)
    )
    return {
        **comment.dict(),
        "replies": len(comment_replies),
        "likes": len(comment_likes),
    }


async def handle_get_comment_replies(comment_id):
    
    comment_queryset = PostComment.filter(id=comment_id)
    children = [
        el.id for el in await PostCommentPydantic.from_queryset(comment_queryset)
    ]
    comments_result = [
        {**item.dict()}
        for item in (await PostCommentPydantic.from_queryset(comment_queryset))
    ]
    for index, i in enumerate(children):
        comments_result[index]["likes"] = len(await get_likes_to_comment(i))
    return comments_result

    return await get_replies_to_comment(comment_id)


async def handle_edit_comment(comment_id, comment_request, current_user):
    comment_obj = await PostComment.get(id=comment_id)
    comment_obj.comment = comment_request.comment
    await comment_obj.save()

    return await PostCommentPydantic.from_queryset_single(
        PostComment.get(id=comment_id)
    )


async def handle_delete_comment(comment_id, current_user):
    current_user_id = current_user["id"]
    deleted_count = await PostComment.filter(
        id=comment_id, user_id=current_user_id
    ).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=404, detail=f"comment {comment_id} for this user not found"
        )
    return Status(message=f"Deleted comment {comment_id}")
