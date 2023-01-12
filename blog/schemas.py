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
    user_name:Optional[str]=None
    # parent_id: Optional[int] = None
    

class CommentPostSchema(CommentSchema):
    parent_id: Optional[int] = None
    
    
class CommentLikeSchema(BaseModel):
    id: int
    comment_id: int
    user_id: int
    


class PostBase(BaseModel):
    id: int
    title: str
    body: str
    author_id: int
    likes: Optional[int] = 0
    comments: Optional[int] = 0


class PostBaseList(PostBase):
    author_name:str




class PostSingle(PostBase):
    # comments: List[CommentSchema]
    # likes: List[LikeSchema]
    pass


class PostCommentSchema(CommentSchema):
    pass


class PostCommentBase(PostCommentSchema):
    replies: int
    likes: int
    parent_id: Optional[int] = None
    

class GetCommentBase(PostCommentBase):
    replies: List[CommentSchema]
    likes: List[CommentLikeSchema]=None
    user_name:Optional[str]=None



class PostCommentSingle(PostCommentBase):

    replies: List[CommentSchema]


class PostCommentReply(PostCommentSchema):

    likes: int
