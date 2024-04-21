import pytest


@pytest.fixture
def operation_data():
    return {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.70",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Visa Classic 7510683061365791",
        "to": "Счет 11776614605963066702"
    }


@pytest.fixture
def operation_data_without_from(operation_data):
    operation_data['description'] = 'Открытие вклада'
    del operation_data['from']
    return operation_data
