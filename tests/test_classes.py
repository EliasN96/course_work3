from datetime import datetime

from src.classes import Payment, Operation


def test_init_payment_from_str():
    payment = Payment.init_from_payment('Maestro 7810846596785568')
    assert payment.name == 'Maestro'
    assert payment.number == '7810846596785568'


def test_safe_payment_for_amount():
    payment = Payment(name='Счет', number='90424923579946435907')
    assert payment.safe() == 'Счет **5907'


def test_safe_payment_for_card_number():
    payment = Payment(name='Visa Classic', number='2842878893689012')
    assert payment.safe() == 'Visa Classic 2842 87** **** 9012'


def test_split_card_number_by_blocks():
    card_number = '2842878893689012'
    result = Payment.split_card_number_by_blocks(card_number)
    assert result == '2842 8788 9368 9012'


def test_init_operation_from_dict(operation_data_without_from):
    op = Operation.init_from_dict(operation_data_without_from)

    assert op.op_id == 939719570
    assert op.op_state == "EXECUTED"
    assert op.op_date == datetime(2018, 6, 30, 2, 8, 58, 425572)
    assert op.op_amount.value == 9824.70
    assert op.op_amount.currency_name == 'USD'
    assert op.op_amount.currency_code == 'USD'
    assert op.op_description == 'Открытие вклада'
    assert op.op_to.name == 'Счет'
    assert op.op_to.number == '11776614605963066702'
    assert op.op_from is None


def test_safe_operation_with_from(operation_data):
    op = Operation.init_from_dict(operation_data)
    expected_result = (
        '30.06.2018 Перевод организации\n'
        'Visa Classic 7510 68** **** 5791 -> Счет **6702\n'
        '9824.70 USD'
    )

    assert op.safe() == expected_result


def test_safe_operation_without_from(operation_data_without_from):
    op = Operation.init_from_dict(operation_data_without_from)

    expected_result = (
        '30.06.2018 Открытие вклада\n'
        'Счет **6702\n'
        '9824.70 USD'
    )

    assert op.safe() == expected_result

