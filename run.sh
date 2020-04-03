#!/bin/bash
set -e

. $HOME/.bash_profile

cd "$(dirname "$0")"

python3.7 covid2influx.py 

sudo docker exec addon_a0d7b954_influxdb influx -username homeassistant -password ${IP} -database covid-19 -execute 'DROP DATABASE "covid-19"'
sudo docker exec addon_a0d7b954_influxdb influx -username homeassistant -password ${IP} -database covid-19 -execute 'CREATE DATABASE "covid-19"' 
sudo docker cp covid-write-points.txt addon_a0d7b954_influxdb:/ 
sudo docker exec addon_a0d7b954_influxdb influx -username homeassistant -password ${IP} -database covid-19 -import -path=covid-write-points.txt -precision=ns

