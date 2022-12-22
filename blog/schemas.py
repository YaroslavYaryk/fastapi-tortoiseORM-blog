from pydantic import BaseModel
from typing import List, Optional


class Status(BaseModel):
    message: str


class LikeSchema(BaseModel):
    id: int
    post_id: int
    user_id: int


class CommentSchema(BaseModel):
    id: int
    post_id: int
    user_id: int
    comment: str
    # parent_id: Optional[int] = None


class PostBase(BaseModel):
    id: int
    title: str
    body: str
    author_id: int
    likes: int
    comments: int


class PostSingle(PostBase):
    comments: List[CommentSchema]


class PostCommentSchema(CommentSchema):
    pass


class PostCommentBase(PostCommentSchema):
    replies: int
    likes: int
    parent_id: Optional[int] = None


class PostCommentSingle(PostCommentBase):

    replies: List[CommentSchema]


class PostCommentReply(PostCommentSchema):

    likes: int
