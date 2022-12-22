TORTOISE_ORM = {
    "connections": {"default": "asyncpg://postgres:proshnik31@localhost/django-blog"},
    "apps": {
        "models": {
            "models": ["blog.models", "users.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
