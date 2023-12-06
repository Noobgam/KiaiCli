from noobgam.fetchers.cloudwatch import get_log_groups
from noobgam.subcommands.subcommand import SubCommand, debug


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

        # this breaks autocompletion.
        delimeter = line[-len(text) - 1]
        if delimeter in '/-':
            return []

        debug(f'Completing [{text}] in line [{line}]')
        debug(f'delim {delimeter}')
        return [
            name for name in get_log_groups()
            if text in name
        ]
