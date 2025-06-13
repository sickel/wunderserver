This is a simple server with wunderground API. It will collect data sent to <host or ip>:5000/weather and store some of the parameters in a postgresql database.

It is to be run under flask, with 

flask run --host=0.0.0.0

if it is to be accessed by the weather station, but it should preferably be set up to run under a production class server.

