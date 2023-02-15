import json
import os
from dotenv import load_dotenv

import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import or_

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f"{self.id}: ({self.name})"


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="book")

    def __str__(self):
        return f"{self.id}: ({self.title})"


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f"{self.id}: ({self.name})"


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

    def __str__(self):
        return f"{self.id}: ({self.count})"


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref="sale")

    def __str__(self):
        return f"{self.id}: ({self.price}, {self.date_sale}, {self.count})"


load_dotenv()

drivername = os.getenv("DRIVERNAME")
username = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database = os.getenv("DATABASE")

DSN = f"{drivername}://{username}:{password}@{host}:{port}/{database}"
engine = sqlalchemy.create_engine(DSN)


def create_tables(engine):
    Base.metadata.create_all(engine)


create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

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

x = input("Введите имя или идентификатор издателя: ")
susq1 = session.query(Publisher).filter(or_(Publisher.id == x, Publisher.name == x)).subquery()
subq2 = session.query(Book).join(susq1, Book.id_publisher == susq1.c.id).subquery()
subq3 = session.query(Stock).join(subq2, Stock.id_book == subq2.c.id).subquery()
for c in session.query(Shop).join(subq3, Shop.id == subq3.c.id_shop).all():
    print(c)
session.close()
