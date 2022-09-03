import psycopg2
import config_db


def create_db(cursor):
    sql_create_database = f'CREATE DATABASE {config_db.DATABASE}'
    cursor.execute(sql_create_database)


def check_existing_db(cursor):
    sql_db_exists = f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{config_db.DATABASE}'"
    cursor.execute(sql_db_exists)
    if not cursor.fetchall():
        create_db(cursor)


def create_tables(cursor):
    sql_create_table = 'CREATE TABLE IF NOT EXISTS client (' \
                       'client_id INT PRIMARY KEY);' \
                       'CREATE TABLE IF NOT EXISTS pair (' \
                       'candidate_id INT unique,' \
                       'client_id INT,' \
                       'FOREIGN KEY (client_id) REFERENCES client (client_id));' \
                       'CREATE TABLE IF NOT EXISTS photo (' \
                       'photo_id SERIAL PRIMARY KEY,' \
                       'candidate_id INT,' \
                       'photo_link INT,' \
                       'FOREIGN KEY (candidate_id) REFERENCES pair (candidate_id));'
    cursor.execute(sql_create_table)


def create_database():
    conn_checking_db = psycopg2.connect(user=config_db.USER, password=config_db.PASSWORD)
    conn_checking_db.autocommit = True
    cursor_db = conn_checking_db.cursor()
    check_existing_db(cursor_db)
    create_tables(cursor_db)
    conn_checking_db.close()
