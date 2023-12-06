import functools
import os
import typing
from typing import List, Optional, Tuple

import boto3

all_lambda_names: List[str] = None
current_profile_name: Optional[str] = os.getenv('AWS_PROFILE')
current_region_name: Optional[str] = os.getenv('AWS_REGION')
all_cached: typing.Dict[str, typing.Any] = {}


def get_profile() -> Tuple[str, str]:
    global current_region_name, current_profile_name
    if not current_profile_name:
        raise ValueError('no profile selected, cannot proceed')
    region = current_region_name or 'us-east-1'
    return current_profile_name, region


def set_profile(profile: str, region: str):
    global current_region_name, current_profile_name
    current_profile_name = profile
    current_region_name = region


def get_boto3_session():
    profile, region = get_profile()
    return boto3.Session(
        profile_name=profile,
        region_name=region
    )


def discard_caches():
    global all_cached
    all_cached = {}


def with_cache(service: str, name: str):
    def inner_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            global all_cached
            cache_key = f'{service}/{name}'
            cached_value = all_cached.get(cache_key)
            if cached_value is None:
                all_cached[cache_key] = func(*args, **kwargs)
            return all_cached[cache_key]

        return wrapper
    return inner_wrapper
