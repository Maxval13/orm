import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker

from models import create_tables, Book, Sale, Shop, Stock, Publisher

password = input('пароль от БД:')

DSN = f'postgresql://postgres:{password}@localhost:5432/client_db'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

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

name_publisher = input("Введите имя издателя для получения информации: ")


def find_sale(name_publisher):
    query = session.query(Stock, Book.title, Shop.name, Sale.price, Sale.date_sale)
    query = query.join(Sale)
    query = query.join(Shop)
    query = query.join(Book)
    query = query.join(Publisher)
    records = query.filter(Publisher.name == name_publisher)

    for c in records:
        print(f'{c[1].ljust(40)} | {c[2].ljust(10)} | {c[3]} | {c[4]}')


find_sale(name_publisher)

session.close()
