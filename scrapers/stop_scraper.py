import pymysql
import re
import os


conn = pymysql.connect(host=os.getenv('DB_URL'), port=3306, user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), db="dublinbus")
cursor = conn.cursor()
# stops.txt is downloaded from https://www.transportforireland.ie/transitData/PT_Data.html
f = open('stops.txt', 'r')
# read in the first index line
index = f.readline()
while index:
    try:
        index = f.readline()
        content = index.strip('\n').split(',')
        content = list(map(lambda x: x.strip('"'),content))
        stop_id = int(re.sub(r'^....DB0*', '', content[0]))
        name = content[1].split(',')[0]
        lat = float(content[-2])
        lon = float(content[-1])
        cursor.execute("insert into stops values(%s, %s, %s ,%s)", (stop_id, name, lon, lat))
    except:
        # There is a virtual stop on the list
        pass
f.close()
conn.commit()
cursor.close()
conn.close()
