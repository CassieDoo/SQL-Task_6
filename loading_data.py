import json

from models import Publisher, Book, Shop, Stock, Sale
from database_connection import Session


def add_data():
    with open('fixtures/tests_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for record in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
            }[record.get('model')]
            session.add(model(id=record.get('pk'), **record.get('fields')))
        session.commit()


if __name__ == "__main__":
    add_data()
