This is a simple server with wunderground API. It will collect data sent to <host or ip>:5000/weather and store some of the parameters in a postgresql database.

It is to be run under flask, with 

flask run --host=0.0.0.0

if it is to be accessed by the weather station, but it should preferably be set up to run under a production class server.



Tee system is set up to store data in the database wdb on localhost on port 5432
with the same username as is running the server. Adjustments on the connection
can be done in the connection statement above or in ~/.pgpass

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
