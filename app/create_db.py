import psycopg2
from passlib.context import CryptContext

from private_db_settings import Settings


def create_db():
    hasher = CryptContext(schemes=['bcrypt'])

    setting: Settings = Settings()
    setting.init_variables()

    conn = psycopg2.connect(
        host=setting.HOST_DB,
        port=setting.PORT,
        database=setting.POSTGRES_DB,
        user=setting.POSTGRES_USER,
        password=setting.POSTGRES_PASSWORD
    )
    cur = conn.cursor()
    cur.execute('CREATE TABLE employee (employee_id serial PRIMARY KEY, name VARCHAR (255) NOT NULL, '
                'surname VARCHAR (255) NOT NULL, salary INTEGER NOT NULL, PROMOTION TIMESTAMP NOT NULL);')
    cur.execute('CREATE TABLE logauth (user_id serial PRIMARY KEY, username VARCHAR (255) NOT NULL, '
                'password VARCHAR (255) NOT NULL, employee_id INTEGER REFERENCES employee(employee_id));')

    cur.execute('INSERT INTO employee (name, surname, salary, PROMOTION) '
                'VALUES (\'Вася\', \'Пупкин\', \'50000\', \'2024-10-10\');')
    cur.execute('INSERT INTO employee (name, surname, salary, PROMOTION) '
                'VALUES (\'Гена\', \'Букин\', \'100000\', \'2023-11-12\');')

    cur.execute(f'INSERT INTO logauth (username, password, employee_id) VALUES (\'Vas\', \'{hasher.hash("sya")}\', 1);')
    cur.execute(f'INSERT INTO logauth (username, password, employee_id) VALUES (\'Gen\', \'{hasher.hash("nna")}\', 2);')

    conn.commit()
    conn.close()
    cur.close()
