import sqlite3
from sqlite3 import Error


def create_connection():
    connection = None
    try:
        connection = sqlite3.connect("conn\database.db")
    except Error as e:
        print(e)
    return connection


def create_record(connection, record):
    with connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO finance(category, amount) VALUES (:category, :amount)",
                       {'category': record.category, 'amount': record.amount})
            connection.commit()
        except Error as e:
            print(e)


def get_category(connection, category):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM finance WHERE category=:category", {'category': category})
    return cursor.fetchall()


def get_all(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM finance")
    return cursor.fetchall()


def update_amount(connection, id, amount):
    with connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE finance SET amount=:amount WHERE ID=:id", {'id': id, 'amount': amount})
        connection.commit()


def delete_record(connection, id):
    with connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM finance WHERE id=:id", {'id': id})
        connection.commit()
        return 'Record removed'


def sum_cat(connection, category):
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT sum(amount) FROM finance WHERE category=:category", {'category': category})
        return cursor.fetchall()


def cat_overview(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""select category,
         round(cast(amount as float) / cast(sum(amount) over () as float) * 100, 2) as tot_amount 
         from (select category, sum(amount) as amount from finance group by category)""")
        return cursor.fetchall()
