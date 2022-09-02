import psycopg2
import config_db


def add_client(client_id):
    sql_add_client = f"INSERT INTO client (client_id)" \
                    f" VALUES ('{client_id}')"
    cursor_db.execute(sql_add_client)


def del_client(client_id):
    sql_del_client = f"DELETE FROM client WHERE client_id = {client_id}"
    cursor_db.execute(sql_del_client)


def add_candidate(client_id, candidate_id):
    sql_add_candidate = f"INSERT INTO pair (client_id, candidate_id)" \
                        f"VALUES ('{client_id}', '{candidate_id}')"
    cursor_db.execute(sql_add_candidate)


def add_photo(candidate_id, id_photo):
    sql_add_photo = f"INSERT INTO photo (candidate_id, photo_link)" \
                    f" VALUES ('{candidate_id,}', '{id_photo}')"
    cursor_db.execute(sql_add_photo)


def show_candidates(client_id):
    sql_show_candidates = f"SELECT * FROM pair WHERE client_id = {client_id}"
    cursor_db.execute(sql_show_candidates)
    candidate_list = cursor_db.fetchall()
    return candidate_list


def show_photo(candidate_id):
    sql_show_photo = f"SELECT * FROM photo WHERE candidate_id = {candidate_id}"
    cursor_db.execute(sql_show_photo)
    photo_list = cursor_db.fetchall()
    return photo_list


def create_db(cursor):
    sql_create_database = f'CREATE DATABASE {config_db.DATABASE}'
    cursor.execute(sql_create_database)


def check_existing_db(cursor):
    sql_db_exists = f"SELECT datname FROM pg_catalog.pg_database WHERE datname = {config_db.DATABASE}"
    cursor.execute(sql_db_exists)
    if not cursor.fetchall():
        print(cursor.fetchall())
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
                       'photo_link INT' \
                       ')'
    cursor.execute(sql_create_table)


if __name__ == '__main__':
    conn = psycopg2.connect(database=config_db.DATABASE, user=config_db.USER, password=config_db.PASSWORD)
    conn.autocommit = True
    cursor_db = conn.cursor()
    check_existing_db(cursor_db)
    create_tables(cursor_db)
    conn.close()
