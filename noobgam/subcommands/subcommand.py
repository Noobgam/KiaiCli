import abc
from typing import Optional

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from noobgam.kiai_cli import KiaiCli


def debug(text):
    text = str(text)
    with open('a.txt', 'a') as f:
        f.write(text + '\n')


class SubCommand(abc.ABC):
    name: str
    help: Optional[str] = None
    kiai: 'KiaiCli'

    @abc.abstractmethod
    def do(self, line: str):
        pass

    @abc.abstractmethod
    def complete(self, text: str, line: str, start_index: int, end_index: int):
        pass

    def get_help(self) -> Optional[str]:
        # can be overriden to be dynamic if you want, will default to helper in the field.
        return self.help

    def print(self, text: str, add_eol: bool = True):
        return self.kiai.print(text, add_eol)


