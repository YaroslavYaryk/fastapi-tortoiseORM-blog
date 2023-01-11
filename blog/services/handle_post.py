from fastapi import HTTPException

from blog.models import Post, PostLike
from blog.schemas import Status, PostBase
from blog.pydantic_schemas import PostCreatePydantic, PostPydantic, PostForUserPydantic
from users.models import User, UserPydantic



async def handle_create_post(post: PostCreatePydantic, user):
    post_obj = await Post.create(**post.dict(), author_id=user["id"])
    return {
        **(await PostPydantic.from_tortoise_orm(post_obj)).dict(),
        "author_name": (await get_author_by_id(user["id"])).username
    }


async def get_likes_to_post(post_id: int):
    post_likes = await Post.get(id=post_id).prefetch_related(
        "post_likes"
    )  # connect row post_likes as related field to Post table
    return await post_likes.post_likes.all()


async def get_comments_to_post(post_id: int):
    post_likes = await Post.get(id=post_id).prefetch_related(
        "post_comments"
    )  # connect row post_likes as related field to Post table
    return await post_likes.post_comments.all()



async def get_author_by_id(author_id):
    return await UserPydantic.from_queryset_single(User.get(id=author_id))


async def get_author_for_post(post_id):
    post = await PostPydantic.from_queryset_single(Post.get(id=post_id))
    return await get_author_by_id(post.author_id)


async def handle_get_all_posts():
    # a = await get_likes_to_post_all()
    posts = [el.id for el in await PostPydantic.from_queryset(Post.all())]
    posts_result = [
        {**item.dict(), "author_name": (await get_author_by_id(item.author_id)).username} for item in (await PostPydantic.from_queryset(Post.all()))
    ]
    for index, i in enumerate(posts):
        posts_result[index]["likes"] = len(await get_likes_to_post(i))
        posts_result[index]["comments"] = len(await get_comments_to_post(i))
    return posts_result

    return await PostPydantic.from_queryset(Post.all())


async def handle_get_posts_for_user(id):
    return await PostForUserPydantic.from_queryset(Post.filter(author_id=id))


async def handle_get_one_post(id: int):
    post_likes = await get_likes_to_post(id)
    post_comments = await get_comments_to_post(id)
    post = await PostPydantic.from_queryset_single(Post.get(id=id))
    return {**post.dict(), "likes": len(post_likes), "comments": len(post_comments)}


async def handle_change_one_post(id: int, post: PostCreatePydantic, user):
    await Post.filter(id=id).update(
        **post.dict(exclude_unset=True), author_id=user["id"]
    )
    return await PostPydantic.from_queryset_single(Post.get(id=id))


async def handle_delete_one_post(id):
    deleted_count = await Post.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    return Status(message=f"Deleted post {id}", id=id)
