from flask import Flask, request

import psycopg

app = Flask(__name__)
CONN = psycopg.connect('dbname=wdb')
CONN.autocommit = True
CUR = CONN.cursor()
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


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


wdb=# \d pwsmeasure
                        Table "public.pwsmeasure"
  Column   |            Type             | Collation | Nullable | Default 
-----------+-----------------------------+-----------+----------+---------
 stationid | integer                     |           | not null | 
 parameter | text                        |           | not null | 
 value     | double precision            |           | not null | 
 unit      | text                        |           |          | 
 timestamp | timestamp without time zone |           |          | now()



"""



@app.route("/weather", methods=['GET', 'POST'])
def storedata():
    units = {'solarradiation': 'W/m2', 'winddir': 'grader', 'humidity': '%', 'indoorhumidity': '%', 'lobatt': '', 'UV': '' }
    # Todo: Same date for all parameters. Check if dateutc == now 
    stationid = request.args.get('ID',None)
    insert = 'insert into pwsmeasure(stationid,parameter,value,unit) values(%s,%s,%s,%s)'
    for key in request.args.keys():
        value = None
        unit = None
        param = key
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
    return('OK')
