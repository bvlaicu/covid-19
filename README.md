Source Covid-19 time series from CSV into InnfluxDB time series

CSV data is sourced from https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series

Instructions:

Install python 3.7 and the pandas python package

```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.7

python3.7 -m pip install pandas
```

Run the sourcing script that pases the CSV source data into InfluxDB write points:

```
python3.7 covid2influx.py
```

Create the InfluxDB database and import the write points
```
IP=<your-influxdb-password>
sudo docker exec addon_a0d7b954_influxdb influx -username homeassistant -password ${IP} -database covid-19 -execute 'DROP DATABASE "covid-19"'
sudo docker exec addon_a0d7b954_influxdb influx -username homeassistant -password ${IP} -database covid-19 -execute 'CREATE DATABASE "covid-19"'
sudo docker cp covid-write-points.txt addon_a0d7b954_influxdb:/
sudo docker exec addon_a0d7b954_influxdb influx -username homeassistant -password ${IP} -database covid-19 -import -path=covid-write-points.txt -precision=ns
```
