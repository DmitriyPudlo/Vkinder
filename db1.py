import psycopg2
import config_db

conn = psycopg2.connect(database="vkinder", user="postgres", password="postgres")
cursor = conn.cursor()

