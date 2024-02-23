import json
import os.path
from datetime import date


def receive_transactions():
    """Возвращает список всех транзакций из файла json"""
    with open(os.path.join("..", "operations.json")) as file:
        transaction = json.load(file)
    return transaction


def get_exec_transaction(transaction_list: list):
    """Возвращает список проведенных транзакций"""
    exec_transaction = []
    for i in transaction_list:
        if i.get('state', None) == 'EXECUTED':
            exec_transaction.append(i)
    return exec_transaction


def get_date(date_: str):
    """Возвращает дату из строки в datetime.date формате """
    only_date = date_.split('T')
    date_format = date.fromisoformat(only_date[0])
    return date_format


def sort_with_date(data: list):
    """Сортирует список транзакций по дате"""
    sort_data = sorted(data, key=lambda x: get_date(x['date']), reverse=True)
    return sort_data[:5]


def secret_from_and_to(data: str):
    """Скрывает номер счета или карты"""
    operation_data = data.split()[-1]
    operation_name = " ".join(data.split()[:-1])
    if operation_name == 'Счет':
        operation_data = "**" + operation_data[-4:]
    else:
        operation_data = "".join(operation_data[:4] + " " + operation_data[4:6]
                                 + "**" + " " + "*" * 4 + " " + operation_data[-4:])
    masked_number = "".join(operation_name + " " + operation_data)
    return masked_number


def transaction_path(transaction: dict):
    """
    Возвращает строку от кого перевод и куда
    """
    from_ = transaction.get('from')
    to = transaction.get('to')
    if from_:
        from_ = secret_from_and_to(from_)
    if to:
        to = secret_from_and_to(to)
    return f"{from_} -> {to}"


def show_transcriptions(transaction: dict):
    """Выводит информацию об транзакции"""
    date_transaction = date.strftime(get_date(transaction['date']), '%d.%m.%Y')
    description = transaction['description']
    path_transaction = transaction_path(transaction)
    amounts = transaction['operationAmount']['amount'] + ' ' + transaction['operationAmount']['currency']['name']
    return (f"{date_transaction} {description}\n"
            f"{path_transaction}\n"
            f"{amounts}\n")
