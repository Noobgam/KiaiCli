from typing import List

from noobgam.caches.common import with_cache, get_boto3_session


@with_cache(service='cw', name='get_log_groups')
def get_log_groups() -> List[str]:
    logs_client = get_boto3_session().client('logs')
    log_group_names = []

    paginator = logs_client.get_paginator('describe_log_groups')

    for page in paginator.paginate():
        for log_group in page['logGroups']:
            log_group_names.append(log_group['logGroupName'])

    return log_group_names