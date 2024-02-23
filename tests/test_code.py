import datetime

from main.utils import (receive_transactions, get_exec_transaction, get_date, sort_with_date,
                        secret_from_and_to, transaction_path, show_transcriptions)


def test_receive_transactions():
    assert type(receive_transactions()) == list


def test_get_exec_transaction():
    data_test = [{"state": "EXECUTED"},
                 {"state": "CANCELED"},
                 {"state": "EXECUTED"},
                 {}]
    assert type(get_exec_transaction(data_test)) == list
    assert len(get_exec_transaction(data_test)) == 2


def test_get_date():
    assert type(get_date("2018-09-12T21:27:25.241689")) == datetime.date


def test_sort_with_date():
    test_sort = [{"date": "2019-09-12T21:27:25.241689"},
                 {"date": "2018-09-12T21:27:25.241689"},
                 {"date": "2017-09-12T21:27:25.241689"}]
    assert type(sort_with_date(test_sort)) == list
    assert sort_with_date(test_sort) == [{"date": "2019-09-12T21:27:25.241689"},
                                         {"date": "2018-09-12T21:27:25.241689"},
                                         {"date": "2017-09-12T21:27:25.241689"}]


def test_secret_from_and_to():
    assert secret_from_and_to("Счет 90424923579946435907") == "Счет **5907"
    assert secret_from_and_to("Visa Platinum 1246377376343588") == "Visa Platinum 1246 37** **** 3588"


def test_transaction_path():
    card_vs_invoice = {"from": "Visa Platinum 1246377376343588", "to": "Счет 14211924144426031657"}
    invoice_vs_card = {"from": "Счет 14211924144426031657", "to": "Visa Platinum 1246377376343588"}
    none_vs_invoice = {"from": "", "to": "Visa Platinum 1246377376343588"}
    card_vs_none = {"from": "Visa Platinum 1246377376343588", "to": ""}
    assert transaction_path(card_vs_invoice) == "Visa Platinum 1246 37** **** 3588 -> Счет **1657"
    assert transaction_path(invoice_vs_card) == "Счет **1657 -> Visa Platinum 1246 37** **** 3588"
    assert transaction_path(none_vs_invoice) == " -> Visa Platinum 1246 37** **** 3588"
    assert transaction_path(card_vs_none) == "Visa Platinum 1246 37** **** 3588 -> "


def test_show_transcriptions():
    test_dict = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    }
    assert show_transcriptions(test_dict) == ("26.08.2019 Перевод организации\n"
                                              "Maestro 1596 83** **** 5199 -> Счет **9589\n"
                                              "31957.58 руб.\n")
