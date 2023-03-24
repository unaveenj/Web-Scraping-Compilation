import requests
import pandas as pd

#Selected dates
dates = ['2023-02-01',
 '2023-02-02',
 '2023-02-03',
 '2023-02-04',
 '2023-02-05',
 '2023-02-06',
 '2023-02-07',
 '2023-02-08',
 '2023-02-09',
 '2023-02-10',
 '2023-02-11',
 '2023-02-12',
 '2023-02-13',
 '2023-02-14',
 '2023-02-15',
 '2023-02-16',
 '2023-02-17',
 '2023-02-18',
 '2023-02-19',
 '2023-02-20',
 '2023-02-21',
 '2023-02-22',
 '2023-02-23',
 '2023-02-24',
 '2023-02-25',
 '2023-02-26',
 '2023-02-27',
 '2023-02-28']

#Data to append
station = []
value = []
timestamp = []


#Downloading new data
for date in dates:
    url = f"https://api.data.gov.sg/v1/environment/air-temperature?date={date}"
    response = requests.get(url)
    data = response.json()
    for item in data["items"]:
        try:
            timestamp.append(item['timestamp'])
            station.append(item['readings'][5]['station_id'])
            value.append(item['readings'][5]['value'])
            print(f"Air temperature at station {station} on {date}: {value} degrees Celsius")
        except:
            pass

# dictionary of lists
dict = {'Timestamp': timestamp[0:40056], 'Station': station, 'Temp': value}

#output file
df = pd.DataFrame(dict)
df.to_csv("Feb Temp.csv")