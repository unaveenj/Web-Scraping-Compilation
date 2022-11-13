import json
import csv
import pandas as pd
import os
from datetime import datetime
import requests
from tqdm import tqdm

dir = os.getcwd()+"\data"
print(dir)
base_url = "http://www.weather.gov.sg/files/dailydata/DAILYDATA_" #http://www.weather.gov.sg/files/dailydata/DAILYDATA_Station_ID_YYYYMM.csv
links = []
years = []
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
stations = []
dates = []
currentYear = datetime.now().year
for i in range(2019, currentYear+1):
    years.append(str(i))

f= open("stations.json")
data = json.load(f)
for i in data['Station']:
    stations.append(data['Station_ID'][i])
    # print(f"Station: {data['Station'][i]}")
    # print(f"Station_ID: {data['Station_ID'][i]}")

f.close()

for year in years:
    for month in months:
        dates.append(year+month)

for date in dates:
    for station in stations:
        links.append(base_url+station+"_"+date+".csv")
no_links = len(links)

cwd = os.path.abspath(dir)
files = os.listdir(cwd)
file_list = []


for i in tqdm(range(0, no_links), desc="Downloading Weather files"):
    try:
        s = requests.get(links[i], allow_redirects=True).status_code
        if s==200:
            if links[i][-14:] not in files:
                r= requests.get(links[i], allow_redirects=True)
                # print(f"Status code : {s}")
                open(f'data/{links[i][-14:]}', 'wb').write(r.content)
                # print(f"{links[i]} is done downloading....")
            else:
                pass
                # print(f'{links[i][-14:]} exists !')
        else:
            pass
    except:
        pass

# os.system('cmd /k "d:"')
# os.system(f'cmd /k "cd {dir}"')
# os.system('cmd /c "copy *.csv final_output.csv"')

#read the path
#list all the files from the directory

#
# for file in files:
#     file_list.append(cwd+'\\'+file)
# # print(file_list[0])
# df_concat = pd.concat([pd.read_csv(f,encoding = "ISO-8859-1") for f in file_list], ignore_index=True)
# df_concat.to_csv('file_name.csv', index=False)
# print(f"Output Generated at : {os.path.abspath('')}!")