import psycopg2

DB_HOST = 'localhost'
DB_USERNAME = 'kirega'
DB_PASS='kirega'
DB_NAME='ireporter_test'
DB_PORT='5432'

URL = "dbname='{}' host='{}' port='{}' user='{}' \
 password='{}'".format(DB_NAME,DB_HOST,DB_PORT,DB_USERNAME,DB_PASS)


table1 = """CREATE TABLE IF NOT EXISTS "User" 
(   id serial PRIMARY KEY,
    first_name varchar(50) NOT NULL,
    last_name  varchar(50) NOT NULL,
    other_names varchar(50) ,
    phonenumber varchar(50) NOT NULL, 
    username varchar(64) NOT NULL,
    email varchar(120) NOT NULL,
    password varchar(128) NOT NULL,
    isAdmin boolean DEFAULT FALSE,
    registeredOn timestamp DEFAULT now()
);"""

table2 = """CREATE TABLE IF NOT EXISTS "Incident" 
(   id serial PRIMARY KEY,
    comment varchar(255) NOT NULL,
    incidentType varchar(25) check(incidentType in ('red-flag', 'intervention')),
    location varchar(50),
    status varchar(50) DEFAULT 'draft' check(status in ('draft','under-investigation','resolved','rejected')), 
    images bytea,
    videos bytea,
    createdOn timestamp DEFAULT now()
);"""
table_queries = [table1,table2]

def connection(url):
    conn = psycopg2.connect(URL)
    return conn

def create_tables(query):
    conn = connection(URL)
    curr = conn.cursor()
    for i in query:
        curr.execute(i)
    conn.commit()

def db_migrate():
    create_tables(table_queries)