import json
import typing
from typing import List, TypedDict


class CloudWatchField(TypedDict):
    field: str
    value: typing.Any


def format_to_table(field_names: List[str], rows: List[List[CloudWatchField]]):
    table_values = [field_names]

    for row in rows:
        current_row_cells = []
        raw_message: typing.Optional[str] = next((field['value'] for field in row if field['field'] == '@message'), None)
        parsed_message: typing.Optional[dict] = None
        if raw_message:
            # rough, but should do for now.
            lidx = raw_message.find('{')
            ridx = raw_message.rfind('}')
            if lidx != -1 and ridx != -1:
                parsed_message = json.loads(raw_message[lidx:(ridx + 1)])

        for field_name in field_names:
            current_val = next(
                (field['value'] for field in row if field['field'] == field_name),
                None
            )
            if current_val is None and parsed_message:
                parts = field_name.split('.')
                node = parsed_message
                for part in parts:
                    node = node.get(part)
                    if not node:
                        break
                current_val = node

            if current_val is None:
                current_val = 'null'

            current_row_cells.append(current_val)
        table_values.append(current_row_cells)

    from tabulate import tabulate
    result = tabulate(table_values, headers='firstrow', tablefmt='fancy_grid')
    return result

