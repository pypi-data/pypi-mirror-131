# -*- coding: utf-8 -*-
import pytest

from patchwork.contrib.fastapi import JWTToken
from patchwork.contrib.fastapi import JWTConfig


@pytest.mark.asyncio
async def test_jwt_usage():

    config = JWTConfig(
        secret='secret',
        validity=100
    )

    token = JWTToken(config)
    assert not token.is_set
    assert not token.is_modified

    token.set('sub', 'user')
    assert token.is_set
    assert token.is_modified

    raw = token.get()

    restored_token = JWTToken(config, raw)
    assert restored_token.is_set
    assert not restored_token.is_modified

    old_exp = restored_token.exp

    restored_token.update({
        'sub': 'foo'
    })

    assert restored_token.exp == old_exp, "changing token data should not affect expiration time"
    assert restored_token.is_modified

    restored_token.invalidate()
    assert not restored_token.is_set

    assert restored_token.get() is None
