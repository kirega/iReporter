import psycopg2 
url =  "dbname='ireporter' host='localhost' port='5432' user='kirega' password='root'"

connection = psycopg2.connect(url)
curr = connection.cursor()
curr.execute("query")
connection.commit() #for saving  functions
connection.close()


