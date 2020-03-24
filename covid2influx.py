import pandas as pd
import re
from datetime import datetime

# Province/State,Country/Region,Lat,Long,1/22/20,1/23/20,1/24/20,1/25/20,1/26/20,1/27/20,1/28/20,1/29/20,1/30/20,1/31/20,2/1/20,...,3/22/20
# people,type=Confirmed,Country/Region=US,Province/State=New\ York,Lat=42.1657,Long=-74.9481 value=15793.0 1584835200000000000

out = open('covid-write-points.txt', 'w')

out.write("%s\n" % "# DML")
out.write("%s\n" % "# CONTEXT-DATABASE: covid-19")
out.write("%s\n" % "# CONTEXT-RETENTION-POLICY: autogen")
out.write("%s\n" % "")

types = ['Confirmed', 'Recovered', 'Deaths']

for type in types:
    df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-" + type + ".csv")

    for index, row in df.iterrows():
        for column in df:
            if re.match(r"^[0-9]", df[column].name):
                date_str = df[column].name
                # print(date_str)
                utc_time = datetime.strptime(date_str, "%m/%d/%y")
                epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
                epoch_time_nano = int(epoch_time * 1000 * 1000 * 1000)

                country = str(row['Country/Region']).replace(",", "\,").replace(" ", "\ ")
                state = str(row['Province/State']).replace(",", "\,").replace(" ", "\ ")

                if state in (None, "", 'nan'):
                    state = "*"

                lat = str(row['Lat'])
                long = str(row['Long'])

                value = str(row[date_str])
                # print(value)
                if value not in (None, "", 'nan'):
                    write_point = 'people,type=' + type + ',Country/Region=' + country + ',Province/State=' + state + ',Lat=' + lat + ',Long=' + long + ' value=' + value + ' ' + str(epoch_time_nano)
                    # print(write_point)
                    out.write("%s\n" % write_point)
