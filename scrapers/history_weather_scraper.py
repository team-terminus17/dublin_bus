import pandas as pd
import pymysql
import os


# file is downloaded from https://www.met.ie/climate/available-data/historical-data
df = pd.read_csv('hly175.csv')

df = df[['rain', 'temp', 'rhum']]
time_list = [1060992000+3600*i for i in range(len(df))]
df['timestamp'] = time_list
df = df.drop(df[df['timestamp'] < 1514768400].index)
df = df.drop(df[df['timestamp'] > 1546257600].index)
df = df[['timestamp', 'rain', 'temp', 'rhum']]


conn = pymysql.connect(host=os.getenv('DB_URL'), port=3306, user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), db="dublinbus")
cursor = conn.cursor()
values = df.values.tolist()
s = ','.join(['%s' for _ in range(len(df.columns))])
table_name = 'HistoryWeatherHourly'
cursor.executemany('INSERT INTO {} VALUES ({})'.format(table_name, s), values)
conn.commit()
cursor.close()
conn.close()
