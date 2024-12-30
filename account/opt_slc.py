
import os, jwt, json, string, secrets, functools

from starlette.responses import RedirectResponse

from db_config.settings import settings
from db_config.storage_config import engine, async_session

from options_select.opt_slc import left_right_first
from auth_privileged.opt_slc import get_privileged_user

from .models import User

key = settings.SECRET_KEY
algorithm = settings.JWT_ALGORITHM
EMAIL_TOKEN_EXPIRY_MINUTES = settings.EMAIL_TOKEN_EXPIRY_MINUTES


async def get_token_visited(request):
    if request.cookies.get("visited"):
        token = request.cookies.get("visited")
        payload = None
        email = None
        off = None
        if token:
            try:
                payload = jwt.decode(token, key, algorithm)
            except jwt.exceptions.InvalidTokenError as err:
                off = err
            if payload is not None:
                email = payload["email"]
            return email, off

async def get_visited_user(request, session):
    while True:
        i = await get_token_visited(request)
        if not i[0]:
            break
        if i[1]:
            break
        result = await left_right_first(session, User, User.email, i[0])
        return result


def on_off_visited():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request, *a, **ka):
            user = await get_token_visited(request)
            if user:
                return await func(request, *a, **ka)
            return RedirectResponse("/account/login")
        return wrapper
    return decorator


def visited():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request, *a, **ka):
            async with async_session() as session:
                user = await get_visited_user(request, session)
            await engine.dispose()
            if user:
                return await func(request, *a, **ka)
            return RedirectResponse("/account/login")
        return wrapper
    return decorator


def auth():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request, *a, **ka):
            async with async_session() as session:
                user = await get_visited_user(request, session)
                if user:
                    return await func(request, *a, **ka)
                prv = await get_privileged_user(request, session)
                if prv:
                    return await func(request, *a, **ka)
                return RedirectResponse("/")
            await engine.dispose()

        return wrapper

    return decorator
