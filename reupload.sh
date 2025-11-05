#1 /bin/bash

while read line 
do
    a=
    date0=$(echo $line |awk '{print $4}' | tr [ \ )
    date=$(echo $date0 | tr / \ )
    date=$(date -d"$date" +%Y%m%d)
    time=$(echo $line |awk '{print $5}' | tr ] \ )
    url=$(echo $line |awk '{print $7}' )
    
    echo Date: $date 
    echo Time: $time 
    timestamp=${date}T$time
    echo Timestamp: $timestamp
    url=${url/dateutc=now/dateutc="$timestamp"}
    echo URL:  $url
    wget "http://localhost:5000$url"
done < "$1"
