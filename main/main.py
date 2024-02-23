from utils import (receive_transactions, get_exec_transaction, sort_with_date, show_transcriptions)


def main():
    executed_transaction = get_exec_transaction(receive_transactions())
    sorted_transaction = sort_with_date(executed_transaction)
    for i in sorted_transaction:
        print(show_transcriptions(i))


if __name__ == '__main__':
    main()
