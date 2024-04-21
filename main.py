from src.functions import get_operations, filter_operations_by_state, sort_operations_by_date
from src.classes import Operation


def main():
    operations = get_operations('operations.json')
    operations = filter_operations_by_state(*operations, state='EXECUTED')
    operations = sort_operations_by_date(*operations)

    for op in operations[:5]:
        print(op)


if __name__ == "__main__":
    main()
