from datetime import datetime


class Payment:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __repr__(self):  # pragma: nocover
        return f'Payment(name={self.name}, number={self.number})'

    @classmethod
    def init_from_payment(cls, payment):
        *name, number = payment.split(' ')
        return cls(
            ' '.join(name),
            number
        )

    def safe(self):
        if self.name.lower() == 'счет':
            safe_number = self.get_safe_account()
        else:
            safe_number = self.get_safe_card_number()
            safe_number = self.split_card_number_by_blocks(safe_number)
        return f'{self.name} {safe_number}'

    def get_safe_account(self):
        return '*' * 2 + self.number[-4:]

    def get_safe_card_number(self):
        start, middle, end = self.number[:6], self.number[6:-4], self.number[-4:]
        safe_card_number = start + "*" * len(middle) + end
        return safe_card_number

    @staticmethod
    def split_card_number_by_blocks(card_number):
        return f'{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}'


class Amount:
    def __init__(self, value, currency_name, currency_code):
        self.value = value
        self.currency_name = currency_name
        self.currency_code = currency_code

    def __repr__(self):  # pragma: nocover
        return f'Amount(value={self.value}, currency_name={self.currency_name})'


class Operation:
    def __init__(
            self,
            op_id,
            op_state,
            op_date,
            op_amount,
            op_description,
            op_to,
            op_from=None
    ):
        self.op_id = op_id
        self.op_state = op_state
        self.op_date = op_date
        self.op_amount = op_amount
        self.op_description = op_description
        self.op_to = op_to
        self.op_from = op_from

    def __repr__(self):  # pragma: nocover
        return (
            f'Operation('
            f'id={self.op_id}, description={self.op_description}, state={self.op_state}, date={self.op_date}, '
            f'amount={self.op_amount}, from={self.op_from}, to={self.op_to}'
        )

    @classmethod
    def init_from_dict(cls, data):
        return cls(
            op_id=int(data['id']),
            op_state=data['state'],
            op_date=datetime.fromisoformat(data['date']),
            op_amount=Amount(
                value=float(data['operationAmount']['amount']),
                currency_name=data['operationAmount']['currency']['name'],
                currency_code=data['operationAmount']['currency']['code']
            ),
            op_description=data['description'],
            op_to=Payment.init_from_payment(data['to']),
            op_from=Payment.init_from_payment(data['from']) if 'from' in data else None
        )

    def safe(self):
        lines = [
         f'{self.op_date.strftime("%d.%m.%Y")} {self.op_description}'
        ]
        if self.op_from:
            lines.append(f'{self.op_from.safe()} -> {self.op_to.safe()}')
        else:
            lines.append(f'{self.op_to.safe()}')
        lines.append(f'{self.op_amount.value:.2f} {self.op_amount.currency_name}')
        return '\n'.join(lines)
