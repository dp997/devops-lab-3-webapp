###### IMPORTED LIBRARIES ######  
from flask import render_template, Flask
from sqlalchemy import create_engine
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

engine_string = f'postgresql+psycopg2://{dbusername}:{password}@{dbhostname}:{dbport}/{dbname}?sslmode=require'
# print(engine_string)
    
engine = create_engine(engine_string)

conn = engine.raw_connection()
cursor = conn.cursor()

###### FLASK SERVER ######


app = Flask(__name__)
@app.route('/')    
def index():    
    cursor.execute(f"SELECT * FROM test_dataset")
    headings = [desc[0] for desc in cursor.description]
    print(headings)
    df = pd.DataFrame(cursor.fetchall(), columns = headings)
    print(df.head(10))
    
    return render_template('table.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

if (__name__ == '__main__'):
    app.run(port = 80)