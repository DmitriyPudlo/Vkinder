import psycopg2


def create_db():
    sql_create_database = 'CREATE DATABASE "vkinder"'
    cursor_db.execute(sql_create_database)


def check_existing_db():
    sql_db_exists = "SELECT datname FROM pg_catalog.pg_database WHERE datname = 'vkinder'"
    cursor_db.execute(sql_db_exists)
    if not cursor_db.fetchall():
        create_db()


def create_tables():
    sql_create_table_client = 'CREATE TABLE IF NOT EXISTS client (' \
                              'client_id INT PRIMARY KEY' \
                              ')'
    sql_create_table_pair = 'CREATE TABLE IF NOT EXISTS pair (' \
                            'candidate_id INT unique,' \
                            'client_id INT,' \
                            'FOREIGN KEY (client_id) REFERENCES client (client_id)' \
                            ')'
    sql_create_table_photo = 'CREATE TABLE IF NOT EXISTS photo (' \
                             'photo_id SERIAL PRIMARY KEY,' \
                             'candidate_id INT,' \
                             'photo_link VARCHAR(50)' \
                             ')'
    cursor.execute(sql_create_table_client)
    cursor.execute(sql_create_table_pair)
    cursor.execute(sql_create_table_photo)


def add_client(client_id):
    sql_add_client = f"INSERT INTO client (client_id)" \
                     f" VALUES ('{client_id}')"
    cursor.execute(sql_add_client)


def del_client(client_id):
    sql_del_client = f"DELETE FROM client WHERE client_id = {client_id}"
    cursor.execute(sql_del_client)


def add_candidate(client_id, candidate_id):
    sql_add_candidate = f"INSERT INTO pair (client_id, candidate_id)" \
                        f"VALUES ('{client_id}', '{candidate_id}')"
    cursor.execute(sql_add_candidate)


def add_photo(candidate_id, link):
    sql_add_photo = f"INSERT INTO photo (candidate_id, photo_link)" \
                    f" VALUES ('{candidate_id,}', '{link}')"
    cursor.execute(sql_add_photo)


def show_candidates(client_id):
    sql_show_candidates = f"SELECT * FROM pair WHERE client_id = {client_id}"
    cursor.execute(sql_show_candidates)
    candidate_list = cursor.fetchall()
    return candidate_list


def show_foto(candidate_id):
    sql_show_photo = f"SELECT * FROM photo WHERE candidate_id = {candidate_id}"
    cursor.execute(sql_show_photo)
    photo_list = cursor.fetchall()
    return photo_list


conn_checking_db = psycopg2.connect(user="postgres", password="postgres")
conn_checking_db.autocommit = True
cursor_db = conn_checking_db.cursor()
check_existing_db()

with psycopg2.connect(database="vkinder", user="postgres", password="postgres") as conn:
    conn.autocommit = True
    cursor = conn.cursor()
    create_tables()
