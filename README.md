This is a simple server with wunderground API. It will collect data sent to <host or ip>:5000/weather and store some of the parameters in a postgresql database.

create the table described below in the database and adjust hostname, username and possibly database in app.py


It can be run under flask, with 

flask run --host=0.0.0.0

if it is to be accessed by the weather station, but it should preferably be set up to run under a production class server.



The system is set up to store data in the database wdb on a given server on port 5432
password can also be added to the connection string or in ~/.pgpass  

The database need to have a table with (at least) the following fields:

```
wdb=# \d pwsmeasure
                        Table "public.pwsmeasure"
  Column   |            Type             | Collation | Nullable | Default 
-----------+-----------------------------+-----------+----------+---------
 stationid | integer                     |           | not null | 
 parameter | text                        |           | not null | 
 value     | double precision            |           | not null | 
 unit      | text                        |           |          | 
 timestamp | timestamp without time zone |           |          | now()

Indexes:
    "pwsmeasure_idx" UNIQUE, btree (stationid, parameter, "timestamp")
Not-null constraints:
    "pwsmeasure_stationid_not_null" NOT NULL "stationid"
    "pwsmeasure_parameter_not_null" NOT NULL "parameter"
    "pwsmeasure_value_not_null" NOT NULL "value"
Access method: heap
```

The table should be indexed on stationid, parameter and timestamp. There should also
be a unique key on those three fields. There may be a index on value, it probably would 
never make sense to have an index on unit. 

The extention timescaledb will be helpful for managing the data when the table is growing
larger.
```
create table pwsmeasure(
  stationid integer not null,
  parameter text not null,
  value double precision not null,
  unit text,
  timestamp timestamp not null default now());

alter table pwsmeasure add primary key (stationid, parameter,timestamp);
```

To set it up with apache:
- make a directory, e.g. /var/www/wunderserver
the directory should be writeable by the account running apache

edit wunderserver.conf to adjust it to the diretory mentioned above and set the right port (If it is to run on 
the same port as another flask server, those two apps conf files has to be combined)

copy app.py and wunderserver.wsgi to the directory

make sure there is a .pgpass file in /var/www with login info, i.e. a line on the form

hostname:database:port:username:password

any part except password may be a wildcard.


 

