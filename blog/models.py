from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise import Tortoise


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    body = fields.TextField()
    author = fields.ForeignKeyField(
        "models.User", related_name="posts", on_delete="CASCADE"
    )

    def __str__(self):
        return f"Post({self.title}, {self.body}, {self.author})"


class PostLike(Model):
    id = fields.IntField(pk=True)
    post = fields.ForeignKeyField(
        "models.Post", related_name="post_likes", on_delete="CASCADE"
    )
    user = fields.ForeignKeyField(
        "models.User", related_name="like_user", on_delete="CASCADE"
    )

    def __str__(self):
        return f"PostLike({self.id}, {self.post})"


class PostComment(Model):
    id = fields.IntField(pk=True)
    post = fields.ForeignKeyField(
        "models.Post", related_name="post_comments", on_delete="CASCADE"
    )
    user = fields.ForeignKeyField(
        "models.User", related_name="comment_user", on_delete="CASCADE"
    )
    comment = fields.TextField()
    parent = fields.ForeignKeyField(
        "models.PostComment", related_name="comment_children", null=True
    )

    def __str__(self):
        return f"PostComment({self.id}, {self.post}, {self.user}, {self.comment})"


class PostCommentLike(Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField(
        "models.User", related_name="comment_like_user", on_delete="CASCADE"
    )
    comment = fields.ForeignKeyField(
        "models.PostComment", related_name="post_comment_likes", null=True
    )

    def __str__(self):
        return f"PostCommentLike({self.id},  {self.user}, {self.comment})"
