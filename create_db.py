import psycopg2
import config_db

conn_checking_db = psycopg2.connect(user=config_db.USER, password=config_db.PASSWORD)
conn_checking_db.autocommit = True
cursor_db = conn_checking_db.cursor()


def create_db():
    sql_create_database = f'CREATE DATABASE {config_db.DATABASE}'
    cursor_db.execute(sql_create_database)


def check_existing_db():
    sql_db_exists = f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{config_db.DATABASE}'"
    cursor_db.execute(sql_db_exists)
    if not cursor_db.fetchall():
        create_db()


def create_tables():
    sql_create_table = 'CREATE TABLE IF NOT EXISTS client (' \
                       'client_id INT PRIMARY KEY);' \
                       'CREATE TABLE IF NOT EXISTS pair (' \
                       'candidate_id INT unique,' \
                       'client_id INT,' \
                       'FOREIGN KEY (client_id) REFERENCES client (client_id));' \
                       'CREATE TABLE IF NOT EXISTS photo (' \
                       'photo_id SERIAL PRIMARY KEY,' \
                       'candidate_id INT,' \
                       'photo_link VARCHAR(50)' \
                       ')'
    cursor_db.execute(sql_create_table)


if __name__ == '__main__':
    check_existing_db()
    create_tables()
    conn_checking_db.close()
