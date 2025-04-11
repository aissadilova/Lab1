import psycopg2
import csv

con = psycopg2.connect(
    dbname='Phonebook',
    user='postgres',
    password='postgres',
    host='localhost',
    )

cur = con.cursor()


cur.execute(
    'CREATE TABLE IF NOT EXISTS phone_book ('
    'id SERIAL PRIMARY KEY,'
    'username varchar(50),'
    'phone varchar(50)'
    ')'
)

con.commit() #1

def insert_from_consol():
    name=input("Enter name:")
    telephone=input("Enter telephone:")
    cur.execute(
        'INSERT INTO phone_book(username, phone) VALUES(%s, %s)', (name, telephone)
    ) 
    con.commit()
    print('Inserted new phone from consol')


def insert_from_csv():
    with open('phones.csv', 'r') as file:
        reader=csv.reader(file)
        for row in reader:
            cur.execute(
                'INSERT INTO phone_book(username, phone) VALUES(%s, %s)', (row[0], row[1])
            )
        con.commit()
        print('Inserted new phone from csv')
    #2
def update(name, new_name=None, new_phone=None):
    if new_name:
        cur.execute(
            'UPDATE phone_book SET username = %s WHERE username = %s', (new_name, name)
        )
    if new_phone:
        cur.execute(
            'UPDATE phone_book SET phone = %s WHERE username = %s', (new_phone, name)
        )
#3
def get_user_by_name(name):
    cur.execute(
        'SELECT *FROM phone_book WHERE username = %s', (name)
    )
    user = cur.fetchone()
    print(user[0], user[1], user[2])

def get_user_by_phone(phone):
    cur.execute(
        'SELECT *FROM phone_book WHERE phone = %s', (phone)
    )
    user = cur.fetchone()
    print(user[0], user[1], user[2]) #4

def delete(name):
    cur.execute(
        'DELETE FROM phone_book WHERE username = %s', (name)
    )
    con.commit() #5\

insert_from_consol()