# -*- coding: utf-8 -*-
from typing import Union

from fastapi import Depends, HTTPException
from jose import JWTError
from starlette import status
from starlette.requests import Request

from patchwork.core import AsyncPublisher
from .settings import is_tortoise_installed


class PublisherWrapper:

    def __init__(self):
        self._publisher = None

    def __call__(self) -> AsyncPublisher:
        from .settings import settings
        if settings.publisher is None:
            raise RuntimeError("unable to use publisher as it's not configured")

        if self._publisher is None:
            self._publisher = settings.publisher.instantiate()
        return self._publisher


get_publisher = PublisherWrapper()


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)


def access_token(request: Request):
    try:
        token = request['token']
    except KeyError:
        raise credentials_exception

    if not token.is_set:
        raise credentials_exception


def optional_access_token(request: Request):
    try:
        token = request['token']
    except KeyError:
        return None

    return token


async def current_user_id(token: access_token = Depends()) -> int:
    try:
        return int(token.sub)
    except (JWTError, TypeError):
        raise credentials_exception


async def optional_current_user_id(token: optional_access_token = Depends()) -> Union[int, None]:
    if not token.is_set:
        return None

    try:
        user_id = token.sub
        if user_id is None:
            return None
        else:
            return int(user_id)
    except JWTError:
        raise credentials_exception


if is_tortoise_installed:
    from tortoise.exceptions import DoesNotExist

    async def current_user(cuid: int = Depends(current_user_id)):
        from .settings import settings
        try:
            return await settings.user_model.type_.get(user_id=cuid)
        except DoesNotExist:
            raise credentials_exception

    async def optional_current_user(cuid: Union[int, None] = Depends(optional_current_user_id)):
        if cuid is None:
            return None

        from .settings import settings
        try:
            return await settings.user_model.type_.get(user_id=cuid)
        except DoesNotExist:
            return None

else:
    async def current_user(*args, **kwargs):
        raise RuntimeError('no supported ORM installed')

    async def optional_current_user(*args, **kwargs):
        raise RuntimeError('no supported ORM installed')
