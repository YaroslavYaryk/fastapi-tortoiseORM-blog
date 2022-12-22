from tortoise.contrib.fastapi import register_tortoise


def register_db(app):

    register_tortoise(
        app,
        db_url="asyncpg://postgres:proshnik31@localhost/django-blog",
        modules={"models": ["blog.models", "users.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
