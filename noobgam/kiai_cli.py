import cmd
import logging
import typing
from typing import List, Optional

from noobgam.fetchers.functions import get_lambda_names
from noobgam.subcommands.subcommand import SubCommand


class KiaiCli(cmd.Cmd):
    log_groups_selected: List[str] = []
    log_fields: List[str] = ["@timestamp", "@message"]
    log_parts: List[str] = ["sort @timestamp desc"]
    last_cmd_out: Optional[typing.Any]

    def __init__(self, subcommands: List[SubCommand]):
        super().__init__()
        self.prompt = '@@> '
        for subcommand in subcommands:
            # making sure they're all registered in base class always.
            # the base class is used to show the list of commands / help
            register_subcommand(self, subcommand)
            subcommand.stdout = self.stdout

    def print(self, text: str, add_eol: bool = True):
        if add_eol:
            text += '\n'
        self.stdout.write(text)


    def do_logs(self, line):
        logging.warning(f"Doing {line}")
        pass

    def complete_logs(self, text, line, start_index, end_index):
        return [
            name for name in get_lambda_names()
            if text in name
        ]


def register_subcommand(kiai: KiaiCli, subcommand: SubCommand):
    def do_impl(kiai: KiaiCli, line: str):
        result = subcommand.do(line)
        if result is not None:
            kiai.last_cmd_out = result
        # this is treated as an exit code.
        # return result

    setattr(
        KiaiCli,
        'do_' + subcommand.name,
        do_impl
    )
    setattr(
        KiaiCli,
        'complete_' + subcommand.name,
        subcommand.complete
    )
    default_help = subcommand.get_help()
    if default_help:
        setattr(
            KiaiCli,
            'help_' + subcommand.name,
            lambda _: subcommand.print(subcommand.get_help())
        )
    subcommand.kiai = kiai