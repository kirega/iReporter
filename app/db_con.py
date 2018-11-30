import psycopg2

DB_HOST = 'localhost'
DB_USERNAME = 'kirega'
DB_PASS='kirega'
DB_NAME='ireporter_test'
DB_PORT='5432'

URL = "dbname='{}' host='{}' port='{}' user='{}' \
 password='{}'".format(DB_NAME,DB_HOST,DB_PORT,DB_USERNAME,DB_PASS)


table1 = 'CREATE TABLE IF NOT EXISTS "User" \
(   id serial PRIMARY KEY,\
    username character varying(64),\
    email character varying(120) ,\
    password_hash character varying(128)\
);'

table_queries = [table1]

def connection(url):
    conn = psycopg2.connect(URL)
    return conn

def create_tables(query):
    conn = connection(URL)
    curr = conn.cursor()
    for i in query:
        curr.execute(i)
    conn.commit()

create_tables(table_queries)