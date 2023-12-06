from typing import List

from noobgam.subcommands.subcommand import debug


# this is an odd way to complete partial things with / and -
def complete_text(text: str, line: str, options: List[str], start_index: int, end_index: int):

    debug(f'Completing [{text}] in line [{line}]')

    token_separator = line.rfind(" ")
    full_token = line[(token_separator + 1):end_index]

    debug(f'Full token: {full_token}')

    filtered_options = [
        option_name for option_name in options
        if full_token in option_name
    ]

    debug(f'filtered_options: {filtered_options}')
    return [
        option[(start_index - token_separator - 1):] for option in filtered_options
    ]
