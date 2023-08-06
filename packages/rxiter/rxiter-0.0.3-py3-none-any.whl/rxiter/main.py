import functools
# from typing import AsyncIterable, AsyncIterator

from .tools import SharableAsyncIterable, ReplayAsyncIterable


def share(obj):
    if callable(obj):
        return _async_share_dec(obj)
    elif hasattr(obj, "__aiter__"):
        return _async_share(obj)
    else:
        raise Exception("share can only be applied to an AsyncIterable object.")


def repeat(obj):
    if callable(obj):
        return _async_replay_dec(obj)
    elif hasattr(obj, "__anext__"):
        return _async_replay(obj)
    else:
        raise Exception("repeat can only be applied to an AsyncIterator object.")


def _async_share(async_iterable):
    return SharableAsyncIterable(async_iterable)


def _async_replay(async_iterator):
    return ReplayAsyncIterable(async_iterator)


def _async_share_dec(async_iterable_fn):
    def wrapper(*args, **vargs):
        obj = async_iterable_fn(*args, **vargs)
        if not hasattr(obj, "__aiter__"):
            raise Exception("share can only be applied to an AsyncIterable object.")
        return SharableAsyncIterable(obj)
    return functools.cache(wrapper)


def _async_replay_dec(async_iterator_fn):
    def wrapper(*args, **vargs):
        obj = async_iterator_fn(*args, **vargs)
        if not hasattr(obj, "__anext__"):
            raise Exception("repeat can only be applied to an AsyncIterator object.")
        return ReplayAsyncIterable(obj)
    return functools.cache(wrapper)
