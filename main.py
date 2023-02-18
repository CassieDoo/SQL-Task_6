from models import Publisher, Book, Shop, Stock, Sale
from database_connection import Session

session = Session()


def get_shops(input_string):
    if input_string.isdigit():
        query = session.query(Shop).\
            join(Stock, Shop.id == Stock.id_shop). \
            join(Book, Stock.id_book == Book.id). \
            join(Publisher, Book.id_publisher == Publisher.id). \
            filter(Publisher.id == int(input_string)).all()
    else:
        query = session.query(Shop). \
            join(Stock, Shop.id == Stock.id_shop). \
            join(Book, Stock.id_book == Book.id). \
            join(Publisher, Book.id_publisher == Publisher.id). \
            filter(Publisher.name == str(input_string)).all()

    publishers_list = []
    for record in query:
        publishers_list.append(str(record))
    return publishers_list


if __name__ == "__main__":
    input_string = input("Введите имя или идентификатор издателя: ")


print('\n'.join(get_shops(input_string)))

session.close()
