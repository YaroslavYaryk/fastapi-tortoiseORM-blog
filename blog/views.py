from fastapi import APIRouter, Depends
from typing import List, Union
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError


from .services import (
    handle_post,
    handle_post_like,
    handle_post_comment,
    handle_comment_like,
)
from .models import Post

from .pydantic_schemas import (
    PostCommentUpdatePydantic,
    PostCreatePydantic,
    PostPydantic,
    PostForUserPydantic,
    PostCommentCreatePydantic,
    PostCommentPydantic,
    PostCommentReplyPydantic,
    PostCommentLikePydantic,
)
from .schemas import (
    PostBase,
    PostCommentBase,
    PostCommentReply,
    PostCommentSingle,
    PostSingle,
    Status,
)
from users.oauth2 import get_current_user


router = APIRouter(prefix="/blogs")


@router.get("", response_model=List[PostBase], tags=["blog"])
async def get_all_posts():
    return await handle_post.handle_get_all_posts()


@router.get("/user/{user_id}", response_model=List[PostForUserPydantic], tags=["blog"])
async def get_posts_for_user(id):
    return await handle_post.handle_get_posts_for_user(id)


@router.post("/", response_model=PostPydantic, tags=["blog"])
async def create_post(post: PostCreatePydantic, current_user=Depends(get_current_user)):
    return await handle_post.handle_create_post(post, current_user)


@router.get(
    "/{id}",
    response_model=PostSingle,
    responses={404: {"model": HTTPNotFoundError}},
    tags=["blog"],
)
async def get_one_post(id):
    return await handle_post.handle_get_one_post(id)


@router.put(
    "/{id}",
    response_model=PostPydantic,
    responses={404: {"model": HTTPNotFoundError}},
    tags=["blog"],
)
async def change_one_post(
    id: int, post: PostCreatePydantic, current_user=Depends(get_current_user)
):
    return await handle_post.handle_change_one_post(id, post, current_user)


@router.delete(
    "/{id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    tags=["blog"],
)
async def delete_one_post(id: int, current_user=Depends(get_current_user)):
    return await handle_post.handle_delete_one_post(id)


@router.post(
    "/{id}/like/",
    responses={404: {"model": HTTPNotFoundError}},
    tags=["blog like"],
)
async def press_like_to_blog(id: int, current_user=Depends(get_current_user)):
    return await handle_post_like.handle_press_like_to_blog(id, current_user)


@router.get(
    "/{id}/likes/", responses={404: {"model": HTTPNotFoundError}}, tags=["blog like"]
)
async def get_all_post_likes(id: int):
    return await handle_post_like.handle_get_all_post_likes(id)


@router.post(
    "/{id}/comment/",
    responses={404: {"model": HTTPNotFoundError}},
    tags=["blog comment"],
    response_model=PostCommentPydantic,
)
async def create_comment_to_post(
    id: int, comment: PostCommentCreatePydantic, current_user=Depends(get_current_user)
):
    return await handle_post_comment.handle_create_comment_to_post(
        id, comment, current_user
    )


@router.get(
    "/{id}/comment/",
    responses={404: {"model": HTTPNotFoundError}},
    tags=["blog comment"],
    response_model=List[PostCommentBase],
)
async def get_all_post_comments(id: int):
    return await handle_post_comment.handle_get_all_post_comments(id)


@router.get(
    "/comment/{comment_id}/",
    responses={404: {"model": HTTPNotFoundError}},
    tags=["blog comment"],
    response_model=PostCommentBase,
)
async def get_one_comment(comment_id):
    return await handle_post_comment.handle_get_one_comment(comment_id)


@router.get(
    "/comment/{comment_id}/replies/",
    responses={404: {"model": HTTPNotFoundError}},
    tags=["blog comment"],
    response_model=List[PostCommentReply],
)
async def get_comment_replies(comment_id):
    return await handle_post_comment.handle_get_comment_replies(comment_id)


@router.put(
    "/comment/{comment_id}/",
    responses={404: {"model": HTTPNotFoundError}},
    tags=["blog comment"],
    response_model=PostCommentPydantic,
)
async def edit_comment(
    comment_id,
    comment: PostCommentUpdatePydantic,
    current_user=Depends(get_current_user),
):
    return await handle_post_comment.handle_edit_comment(
        comment_id, comment, current_user
    )


@router.delete(
    "/comment/{comment_id}/",
    responses={404: {"model": HTTPNotFoundError}},
    tags=["blog comment"],
    response_model=Status,
)
async def delete_comment(comment_id, current_user=Depends(get_current_user)):
    return await handle_post_comment.handle_delete_comment(comment_id, current_user)


@router.post(
    "/comment/{id}/like/",
    responses={404: {"model": HTTPNotFoundError}},
    tags=["comment like"],
)
async def press_like_to_comment(id: int, current_user=Depends(get_current_user)):
    return await handle_comment_like.handle_press_like_to_comment(id, current_user)


@router.get(
    "/comment/{id}/likes/",
    responses={404: {"model": HTTPNotFoundError}},
    tags=["comment like"],
    response_model=List[PostCommentLikePydantic],
)
async def get_all_comment_likes(id: int):
    return await handle_comment_like.handle_get_all_comment_likes(id)
