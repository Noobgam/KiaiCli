import time
from typing import List

from noobgam.caches.common import get_boto3_session
from noobgam.subcommands.subcommand import SubCommand, debug
from noobgam.utils.log_formatter import format_to_table


class LogQuery(SubCommand):
    def __init__(self):
        self.name = 'log'
        self.help = """Allows querying logs, for now just adding filters and querying
        """

    def _get_log_fields(self) -> List[str]:
        # should autodetect it from the results in the future.
        return self.kiai.log_fields or ['@timestamp', '@message']

    def _create_fields_query_part(self):
        return "fields " + ", ".join(self.kiai.log_fields)

    def _create_request_parts(self) -> List[str]:
        return self.kiai.log_parts

    def _create_query(self):
        fields = self._create_fields_query_part()
        parts = self._create_request_parts()
        return '\n  | '.join([fields] + parts)

    def do(self, line: str):
        if line.startswith('fields '):
            fields = line[7:].split(' ')
            self.kiai.log_fields = fields
            self.print(f'Current query config:\n {self._create_query()}')
            return
        if line.strip() == 'parts clear':
            self.kiai.log_parts = []
            self.print(f'Current query config:\n {self._create_query()}')
            return
        if line.startswith('parts add '):
            self.kiai.log_parts.append(
                line[len('parts add '):]
            )
            self.print(f'Current query config:\n {self._create_query()}')
            return


        logs_client = get_boto3_session().client('logs')
        end_time = int(time.time())
        # last 5 min hardcoded for now
        start_time = end_time - 3600 * 12
        query = self._create_query()
        self.print('Executing query:\n' + query)
        response = logs_client.start_query(
            logGroupNames=self.kiai.log_groups_selected,
            startTime=start_time,
            endTime=end_time,
            queryString=query
        )
        query_id = response['queryId']
        while True:
            time.sleep(1)
            debug('Polling')
            result = logs_client.get_query_results(
                queryId=query_id
            )
            # check this.
            if 'error' in result:
                break
            if 'results' in result:
                break
            debug(str(result))
        if 'error' in result:
            self.print(result['error'])
            return None
        else:
            table = format_to_table(self._get_log_fields(), result['results'])
            self.print(table)
            return result['results']


    def complete(self, text: str, line: str, start_index: int, end_index: int):
        # we can discover log group schema here, but don't bother right now.
        return []

