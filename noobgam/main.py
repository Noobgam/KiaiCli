import logging

from noobgam.kiai_cli import KiaiCli
from noobgam.subcommands.log_groups_picker import LogGroupsPicker
from noobgam.subcommands.log_query import LogQuery
from noobgam.subcommands.profile_switcher import ProfileSwitcher

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('botocore.credentials').disabled = True
    my_cmd = KiaiCli(
        subcommands=[
            ProfileSwitcher(),
            LogGroupsPicker(),
            LogQuery(),
        ],
    )
    my_cmd.cmdloop()