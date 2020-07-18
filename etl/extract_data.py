
import os
import time
from datetime import datetime, timedelta

import csv
import codecs
import requests
import yaml
import pyodbc 

#extract the name of the directory that this file is located in, regardless of the current working directory.
script_dir = os.path.dirname(__file__)

filename_yaml = os.path.join('/run', 'secrets','db_credentials.yaml')

with open(filename_yaml) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

driver = config[config['destination']]['driver']
server = config[config['destination']]['server']
database = config[config['destination']]['database']
user = config[config['destination']]['user']
password = config[config['destination']]['password']

conn = pyodbc.connect("Driver=" + driver + ";"
                      "Server=" + server + ";"
                      "Database=" + database + ";"
                      "uid=" + user + ";"
                      "pwd=" + password + ";")


yesterday_format1 = datetime.strftime(datetime.now() - timedelta(1), '%Y/%m/%d')
yesterday_format2  = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

download_day_format1 = yesterday_format1
download_day_format2 = yesterday_format2
print("Downlaod day:" , download_day_format1)

x = "https://data.tii.ie/Datasets/TrafficCountData/" + download_day_format1 + "/per-site-class-aggr-" + download_day_format2 + ".csv"

print(x)

response = requests.get("https://data.tii.ie/Datasets/TrafficCountData/" + download_day_format1 + "/per-site-class-aggr-" + download_day_format2 + ".csv")

#https://stackoverflow.com/questions/30483977/python-get-yesterdays-date-as-a-string-in-yyyy-mm-dd-format/30484112

#raw_data = response.text
text = codecs.iterdecode(response.iter_lines(), 'utf-8') #response.iter_lines()
reader = csv.reader(text, delimiter=',')


cursor_desc = conn.cursor()
#cursor_desc.execute('SELECT * FROM traffic_daily_aggregates')


next(reader) #skip first row
params = [(row) for row in reader]
#params = [(row) for i, row in enumerate(reader) if i < 100]



cursor_desc.fast_executemany = True
sql = "INSERT INTO traffic_daily_aggregates  VALUES (?, ?, ?, ?, ?, ?)"
t0 = time.time()
cursor_desc.executemany(sql, params)
conn.commit()
print(f'{time.time() - t0:.1f} seconds')

