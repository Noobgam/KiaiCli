from typing import List

from noobgam.caches.common import get_boto3_session, with_cache


@with_cache(service='lambda', name='get_all_lambda_names')
def get_lambda_names() -> List[str]:
    lambda_client = get_boto3_session().client('lambda')

    function_names = []

    paginator = lambda_client.get_paginator('list_functions')

    for page in paginator.paginate():
        for function in page['Functions']:
            function_names.append(function['FunctionName'])

    return function_names