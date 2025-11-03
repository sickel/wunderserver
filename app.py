from flask import Flask, request

import psycopg
import json

databasename = 'wdb'

app = Flask(__name__)
# To connect using alternative server / username / port, edit connectionstring 
# preferably use ~/.pgpass to set up password for connection

connectionstring = f'dbname={databasename}'
CONN = psycopg.connect(connectionstring)
CONN.autocommit = True
CUR = CONN.cursor()
@app.route("/")
def index():
    return "<p>Wunderground server</p>"

# Example url:
# GET /weatherstation/update?ID=1&PASSWORD=Aaa&tempf=64.9&humidity=56&dewptf=48.9&windchillf=64.9&winddir=187&windspeedmph=1.79&windgustmph=2.24&rainin=0.000&dailyrainin=0.000&weeklyrainin=0.000&monthlyrainin=0.000&yearlyrainin=0.000&totalrainin=0.000&solarradiation=63.47&UV=0&indoortempf=73.9&indoorhumidity=46&absbaromin=30.106&baromin=29.914&temp4f=67.5&humidity4=41&lowbatt=0&dateutc=now&softwaretype=EasyWeatherPro_V5.2.2&action=updateraw&realtime=1&rtfreq=5
"""
tempf 63.9
humidity 56
dewptf 47.8
windchillf 63.9
winddir 163
windspeedmph 0.89
windgustmph 
rainin 0.000
dailyrainin 0.000
weeklyrainin 0.000
monthlyrainin 0.000
yearlyrainin 0.000
totalrainin 0.000
solarradiation 67.25
UV 0
indoortempf 72.9
indoorhumidity 47
absbaromin 30.100
baromin 29.908
temp4f 66.6
humidity4 41
lowbatt 0
dateutc now
softwaretype EasyWeatherPro_V5.2.2
action updateraw
realtime 1
rtfreq 5

The data are sent in imperial units. They are converted to SI before storing

THe system is set up to store data in the database wdb on localhost on port 5432
with the same username as is running the server. Adjustments on the connection
can be done in the connection statement above or in ~/.pgpass

The database need to have a table with (at least) the following fields:

wdb=# \d pwsmeasure
                        Table "public.pwsmeasure"
  Column   |            Type             | Collation | Nullable | Default 
-----------+-----------------------------+-----------+----------+---------
 stationid | integer                     |           | not null | 
 parameter | text                        |           | not null | 
 value     | double precision            |           | not null | 
 unit      | text                        |           |          | 
 timestamp | timestamp without time zone |           |          | now()


The table should be indexed on stationid, parameter and timmestamp. There should also
be a unique key on those three fields. There may be a index on value, it probably would 
never make sense to have an index on unit. 

the extention timescaledb will be helpful for managing the data when the table is growing
larger.




"""



@app.route("/weather", methods=['GET', 'POST'])
def storedata():
    try:
        units = {'solarradiation': 'W/m2', 'winddir': 'grader', 'humidity': '%', 'indoorhumidity': '%', 'lobatt': '', 'UV': '' }
        stationid = request.args.get('ID',None)
        if request.args.get('dateutc',None) == 'now':
            # Using the default now()-value
            insert = 'insert into pwsmeasure(stationid,parameter,value,unit) values(%s,%s,%s,%s)'
        else:
            insert = 'insert into pwsmeasure(stationid,parameter,value,unit,timestamp) values(%s,%s,%s,%s,%s)'
            timestamp = request.args.get('dateutc',None)
            if timestamp is None:
                # No time information is given, something is wrong
                 
        for key in request.args.keys():
            value = None
            unit = None
            param = key
            if request.args.get(key) == -9999:
                print(f"invalid parameter: {param}")
                continue
            if key in['tempf','dewptf','windchillf', 'indoortempf']:
                value = (float(request.args.get(key))-32)*5/9
                unit = 'C'
                param = key[:-1]
            if key.endswith('mph'):
                value = float(request.args.get(key))*1609/3600
                unit = 'm/s'
                param = key[:-3]
            if key.endswith('baromin'):
                value = float(request.args.get(key))*33.8639
                param = key[:-2]
                unit = 'hPa'
            if key.endswith( 'rainin'):
                value = float(request.args.get(key))*25.4
                unit = 'mm'
                param = key[:-2]
            if key in units:
                value = float(request.args.get(key))
                unit = units[key]
            if not (value is None or stationid is None):
                CUR.execute(insert,[stationid,param,value,unit])
    except Exception as e:
        # If anything fails, we just ignore that dataset and log the problems
        with open('error.log','a') as logfile:
            logfile.write('----')
            logfile.write(str(e))
            logfile.write(json.dumps(request.args))
            logfile.write('\n')
    return('OK')


