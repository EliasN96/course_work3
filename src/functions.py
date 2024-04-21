import json  # pragma: nocover

from src.classes import Operation  # pragma: nocover


def get_operations(name):  # pragma: nocover
    operations = []
    with open(name, encoding='utf-8') as n:
        for data in json.load(n):
            if data:
                op = Operation.init_from_dict(data)
                operations.append(op)
        return operations


def filter_operations_by_state(*operations: Operation, state: str):  # pragma: nocover
    filtered_operations: list[Operation] = []
    for op in operations:
        if op.op_state == state:
            filtered_operations.append(op)
    return filtered_operations


def sort_operations_by_date(*operations: Operation):  # pragma: nocover
    return sorted(operations, key=lambda op: op.op_date, reverse=True)
