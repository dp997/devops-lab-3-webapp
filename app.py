###### IMPORTED LIBRARIES ######  
from flask import render_template, Flask, g
import psycopg2
import os
import urllib
import boto3
import pandas as pd
###### SQL CONNECTION ######
print("Imported packages")

dbhostname = os.environ['DBHOSTNAME']
dbport = os.environ['DBPORT']
dbusername = os.environ['DBUSERNAME']
dbname = os.environ['DBNAME']
region = os.environ['REGION']

rds = boto3.client('rds', region_name=region)

print("Connected to AWS")



password = rds.generate_db_auth_token(DBHostname = dbhostname,
                                      Port = dbport,
                                      DBUsername = dbusername,
                                      Region = region)
                       
password = urllib.parse.quote(password)

def get_db_connection():
    conn = psycopg2.connect(host=dbhostname,
                            database=dbname,
                            user=dbusername,
                            password=password)
    return conn



###### FLASK SERVER ######

app = Flask(__name__)

@app.route('/')    
def index(): 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM test_dataset")
    headings = [desc[0] for desc in cursor.description]
    print(headings)
    df = pd.DataFrame(cursor.fetchall(), columns = headings)
    conn.close()
    return render_template('table.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

if (__name__ == '__main__'):
    app.run(host = "0.0.0.0", port = 80)