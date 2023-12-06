from noobgam.fetchers.cloudwatch import get_log_groups
from noobgam.subcommands.subcommand import SubCommand, debug
from noobgam.utils.completion_utils import complete_text


class LogGroupsPicker(SubCommand):
    def __init__(self):
        self.name = 'log_group'
        self.help = """Allows manipulating log groups. Subcommands: add, list, clear, show
        """

    def do(self, line: str):
        if not line:
            self.print('No command supplied')
            return

        if line.strip() == 'clear':
            self.kiai.log_groups_selected = []
            self.print('Cleared')
            return

        if line.strip() == 'list':
            self.print(str(get_log_groups()))
            return

        if line.strip() == 'show':
            self.print(f'Currently selected log groups: {self.kiai.log_groups_selected}')
            return

        command, rest = line.split(' ', 1)
        if command != 'add':
            self.print(f'Unrecognized command {command}')
            return

        log_groups = rest.split(' ')
        # no validation here.
        self.kiai.log_groups_selected += log_groups

    def complete(self, text: str, line: str, start_index: int, end_index: int):
        if not line.startswith('log_group add'):
            return []

        if not line.endswith(text):
            return []

        return complete_text(
            text,
            line,
            get_log_groups(),
            start_index,
            end_index
        )
