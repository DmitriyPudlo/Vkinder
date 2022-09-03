import psycopg2
import config_db


class Connector:
    def __init__(self):
        self.conn = psycopg2.connect(database=config_db.DATABASE, user=config_db.USER, password=config_db.PASSWORD)
        self.conn.autocommit = True
        self.cursor_db = self.conn.cursor()

    def add_client(self, client_id):
        sql_add_client = f"INSERT INTO client (client_id)" \
                         f"VALUES ('{client_id}')" \
                         f"ON CONFLICT (client_id) DO NOTHING"
        self.cursor_db.execute(sql_add_client)

    def del_client(self, client_id):
        sql_del_client = f"DELETE FROM client WHERE client_id = {client_id}"
        self.cursor_db.execute(sql_del_client)

    def add_candidate(self, client_id, candidate_id):
        sql_add_candidate = f"INSERT INTO pair (client_id, candidate_id)" \
                            f"VALUES ('{client_id}', '{candidate_id}')" \
                            f"ON CONFLICT (candidate_id) DO NOTHING"
        self.cursor_db.execute(sql_add_candidate)

    def add_photo(self, candidate_id, id_photo):
        sql_add_photo = f"INSERT INTO photo (candidate_id, photo_link)" \
                        f"VALUES ({candidate_id}, {id_photo})"
        self.cursor_db.execute(sql_add_photo)

    def show_candidates(self, client_id):
        sql_show_candidates = f"SELECT candidate_id FROM pair WHERE client_id = {client_id}"
        self.cursor_db.execute(sql_show_candidates)
        candidate_list = self.cursor_db.fetchall()
        return candidate_list

    def show_photo(self, candidate_id):
        sql_show_photo = f"SELECT photo_link FROM photo WHERE candidate_id = {candidate_id}"
        self.cursor_db.execute(sql_show_photo)
        photo_list = self.cursor_db.fetchall()
        return photo_list

    def create_tables(self):
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
        self.cursor_db.execute(sql_create_table)

    def connect_close(self):
        self.conn.close()
