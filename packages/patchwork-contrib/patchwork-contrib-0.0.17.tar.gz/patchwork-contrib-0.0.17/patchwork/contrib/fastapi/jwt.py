# -*- coding: utf-8 -*-
import uuid
from calendar import timegm
from datetime import datetime
from enum import Enum
from types import MappingProxyType
from typing import Mapping, Any, Union

from jose import jwt, JWTError
from starlette.datastructures import MutableHeaders
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Scope, Receive, Send, Message

from patchwork.contrib.fastapi.settings import JWTConfig
from patchwork.core.utils import cached_property


class TokenState(Enum):
    UNSET = 0
    SET = 1
    MODIFIED = 2


def unix_now():
    return timegm(datetime.utcnow().utctimetuple())


class JWTToken:

    _payload: dict

    def __init__(self, config,  raw: str = None):
        self.config = config

        if raw is not None:
            self._decode(raw)
            self.__state = TokenState.SET
        else:
            self._payload = {}
            self.__state = TokenState.UNSET

    @cached_property
    def payload(self) -> Mapping:
        return MappingProxyType(self._payload)

    @property
    def is_set(self):
        return self._state != TokenState.UNSET

    @property
    def is_modified(self):
        return self._state == TokenState.MODIFIED

    @property
    def _state(self):
        return self.__state

    @_state.setter
    def _state(self, value):
        if self.__state == TokenState.UNSET:
            self._init_token()

        self.__state = value

    @property
    def sub(self):
        """
        Subject of the JWT (the user)
        :return:
        """
        return self.payload.get('sub')

    @property
    def exp(self):
        """
        Time after which the JWT expires
        :return:
        """
        return self.payload.get('exp')

    @property
    def iss(self):
        """
        Issuer of the JWT
        :return:
        """
        return self.payload.get('iss')

    @property
    def aud(self):
        """
        Recipient for which the JWT is intended
        :return:
        """
        return self.payload.get('aud')

    @property
    def nbf(self):
        """
        Time before which the JWT must not be accepted for processing
        :return:
        """
        return self.payload.get('nbf')

    @property
    def iat(self):
        """
        Time at which the JWT was issued; can be used to determine age of the JWT
        :return:
        """
        return self.payload.get('iat')

    @property
    def jti(self):
        """
        Unique identifier; can be used to prevent the JWT from being replayed (allows a token to be used only once)
        :return:
        """
        return self.payload.get('jti')

    def get(self) -> Union[str, None]:
        if not self.is_set:
            return None

        assert self.config.validity is not None, "token validity must be set"

        return jwt.encode(self._payload, self.config.secret, algorithm=self.config.algorithm)

    def update(self, data: dict):
        self._payload.update(data)
        self._state = TokenState.MODIFIED

    def set(self, claim: str, value: Any):
        self._payload[claim] = value
        self._state = TokenState.MODIFIED

    def refresh(self):
        if 'iat' in self._payload:
            self._payload.pop('iat')
        if 'exp' in self._payload:
            self._payload.pop('exp')
        self._state = TokenState.MODIFIED

    def invalidate(self):
        self._payload = {}
        self._state = TokenState.UNSET

    def _init_token(self):
        data = self._payload
        if 'iss' not in data and self.config.issuer is not None:
            data['iss'] = self.config.issuer

        if 'aud' not in data and self.config.audience is not None:
            data['aud'] = self.config.audience

        if 'iat' not in data:
            data['iat'] = unix_now()

        if 'exp' not in data:
            data['exp'] = data['iat'] + self.config.validity

        if 'jti' not in data:
            data['jti'] = str(uuid.uuid4())

    def _decode(self, raw: str = None):

        self._payload = jwt.decode(
            token=raw,
            key=self.config.secret,
            algorithms=[self.config.algorithm],
            audience=self.config.allowed_audience,
            issuer=self.config.allowed_issuer,
            options={
                'require_aud': self.config.allowed_audience is not None,
                'require_iss': self.config.allowed_issuer is not None,
                'require_exp': True
            }
        )


class AccessTokenMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        config: JWTConfig
    ) -> None:
        self.app = app
        self.config = config

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)

        if self.config.cookie_name in connection.cookies:
            data = connection.cookies[self.config.cookie_name]
            try:
                scope["token"] = JWTToken(self.config, data)
            except JWTError:
                scope["token"] = JWTToken(self.config)
        else:
            scope["token"] = JWTToken(self.config)

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                path = scope.get("root_path", "") or self.config.path

                token: JWTToken = scope["token"]
                headers = MutableHeaders(scope=message)
                if not token.is_set:
                    header_value = f"{self.config.cookie_name}=null; " \
                                   f"path={path}; " \
                                   f"expires=Thu, 01 Jan 1970 00:00:00 GMT; " \
                                   f"max-age=0; " \
                                   f"httponly; " \
                                   f"{'secure; ' if self.config.https_only else ''}" \
                                   f"samesite={self.config.samesite.capitalize()}; " \
                                   f"domain={self.config.domain}"
                    headers.append("Set-Cookie", header_value)
                elif token.is_modified:
                    header_value = f"{self.config.cookie_name}={token.get()}; " \
                                   f"path={path}; " \
                                   f"max-age={int(token.exp - unix_now())}; " \
                                   f"httponly; " \
                                   f"{'secure; ' if self.config.https_only else ''}" \
                                   f"samesite={self.config.samesite.capitalize()}; " \
                                   f"domain={self.config.domain}"

                    headers.append("Set-Cookie", header_value)

            await send(message)

        await self.app(scope, receive, send_wrapper)
