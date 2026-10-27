import jwt
from urllib.parse import parse_qs
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

User = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):

        query_string = scope["query_string"].decode()
        query_params = parse_qs(query_string)

        token = query_params.get("token")

        scope["user"] = AnonymousUser()

        if token:
            token = token[0]

            try:
                decoded = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )

                user = await database_sync_to_async(
                    User.objects.get
                )(id=decoded["user_id"])

                scope["user"] = user

            except Exception as e:
                print("JWT ERROR:", e)

        return await super().__call__(scope, receive, send)