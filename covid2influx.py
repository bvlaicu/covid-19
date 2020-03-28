import pandas as pd
import re
import datetime
from urllib.error import HTTPError

out = open('covid-write-points.txt', 'w')

out.write("%s\n" % "# DML")
out.write("%s\n" % "# CONTEXT-DATABASE: covid-19")
out.write("%s\n" % "# CONTEXT-RETENTION-POLICY: autogen")
out.write("%s\n" % "")

start = datetime.datetime.strptime("01-22-2020", "%m-%d-%Y")
today = datetime.datetime.today()
end = today + datetime.timedelta(days = 2) 
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

for date_obj in date_generated:
    date = date_obj.strftime("%m-%d-%Y")
    # print(date)
    try:
        csv_file = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" + date + ".csv"
        df = pd.read_csv(csv_file)

        for index, row in df.iterrows():
            utc_time = datetime.datetime.strptime(date, "%m-%d-%Y")
            epoch_time = (utc_time - datetime.datetime(1970, 1, 1)).total_seconds()
            epoch_time_nano = int(epoch_time * 1000 * 1000 * 1000)

            if 'Country_Region' in row:
                country = str(row['Country_Region']).replace(",", "\,").replace(" ", "\ ")
            else:
                country = str(row['Country/Region']).replace(",", "\,").replace(" ", "\ ")
            if country == 'Mainland\\ China':
                country = 'China'

            if 'Province_State' in row:
                state = str(row['Province_State']).replace(",", "\,").replace(" ", "\ ")
            else:
                state = str(row['Province/State']).replace(",", "\,").replace(" ", "\ ")
            if state in (None, "", 'nan'):
                state = "*"
            if state == country:
                state = "*"

            if 'Admin2' in row:
                city = str(row['Admin2']).replace(",", "\,").replace(" ", "\ ")
            else:
                city = ""
            if city in (None, "", 'nan'):
                city = "*"

            if 'Lat' in row:
                lat = str(row['Lat'])
            else:
                lat = "*"

            if 'Long_' in row:
                long_ = str(row['Long_'])
            else:
                long_ = "*"

            values = {}
            if 'Confirmed' in row:
                values['Confirmed'] = str(row['Confirmed'])
            else:
                values['Confirmed'] = "0"

            if 'Deaths' in row:
                values['Deaths'] = str(row['Deaths'])
            else:
                values['Deaths'] = "0"

            if 'Recovered' in row:
                values['Recovered'] = str(row['Recovered'])
            else:
                values['Recovered'] = "0"

            if 'Active' in row:
                values['Active'] = str(row['Active'])
            else:
                values['Active'] = "0"

            for type_ in values.keys():
                value = values[type_]
                # print(type_)
                # print(value)
                if value not in (None, "", 'nan'):
                    write_point = 'people,type=' + type_ + ',Country/Region=' + country + ',Province/State=' + state + ',City=' + city + ',Lat=' + lat + ',Long=' + long_ + ' value=' + value + ' ' + str(epoch_time_nano)
                    # print(write_point)
                    out.write("%s\n" % write_point)
    except HTTPError as err:
        if err.code == 404:
            print("File not found:" + csv_file)
        else:
            raise
