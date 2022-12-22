from fastapi import APIRouter

from blog import views as post_views
from users import views as user_views

routes = APIRouter()

routes.include_router(post_views.router)
routes.include_router(user_views.router)
