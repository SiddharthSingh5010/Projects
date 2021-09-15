import pandas as pd
import json
import requests
import os
import time
import logging
from datetime import datetime

#Defining Logger 
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
logger.addHandler(logging.FileHandler('Extractor.log', 'a'))
print = logger.info

print(os.getcwd())
os.chdir('/home/ec2-user')
print(os.getcwd())


date=datetime.strftime(datetime.today(),format="%d-%m-%Y")
print(date)
data=[]

#Fetching Raw Data using RESTAPI from AviationStack.com
def fetchdata(tries=5,delay=1):
    departures=['DEL','BOM','HYD','BLR','MAA','CCU']
    for dep in departures:
        print("Departure: {}".format(dep))
        params = {
            'access_key': '9503782cf1712aea9acf829e3ebada1c',
            'limit': 100,
            'flight_status':'landed',
            'dep_iata':dep
        }
        success=0
        t=0
        while (success==0 and t<tries):
            try:
                time.sleep(delay)
                api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
                print("Status : {}".format(api_result.status_code))
                api_response = api_result.json()['data']
                data.extend(api_response)
                print("Successful for Departure {}".format(dep))
                success=1
            except requests.ConnectionError as e:
                print("Couldn't make successfull connection to AviationStack.com")
                print("Not successful for Departure {}".format(dep))
                t=t+1
            except KeyError as e:
                print("Key Error has Occurred")
                t=t+1
        if(success==0 and t==tries):
            print('Could not Fetch Data for {} successfully after {} tries. Program exiting.'.format(dep,t))
            exit(0)

fetchdata(5)
df=pd.json_normalize(data)
df=df[['flight_date','flight_status','departure.airport',
    'departure.iata','departure.actual','arrival.airport','arrival.timezone',
    'arrival.iata','arrival.actual','airline.name','airline.iata','flight.number',
    'flight.iata','arrival.estimated','departure.estimated','departure.delay','arrival.delay']]

#NAN Value treatment
df['departure.delay'].fillna(0,inplace=True)
df['arrival.delay'].fillna(0,inplace=True)
df.dropna(inplace=True)

#Splitting Date Time and City Region
df['region']=df['arrival.timezone'].apply(lambda row: row.split('/')[0])
df['city']=df['arrival.timezone'].apply(lambda row: row.split('/')[1])
df['departure_date']=df['departure.actual'].apply(lambda row: row.split('T')[0])
df['departure_time']=df['departure.actual'].apply(lambda row: row.split('T')[1])
df['arrival_date']=df['arrival.actual'].apply(lambda row: row.split('T')[0])
df['arrival_time']=df['arrival.actual'].apply(lambda row: row.split('T')[1])
df['departure_time']=df['departure_time'].apply(lambda row: row.split('+')[0])
df['arrival_time']=df['arrival_time'].apply(lambda row: row.split('+')[0])

#Dropping Unnecssary columns
df.drop('departure.actual',inplace=True,axis=1)
df.drop('departure.estimated',inplace=True,axis=1)
df.drop('arrival.actual',inplace=True,axis=1)
df.drop('arrival.estimated',inplace=True,axis=1)
df.drop('arrival.timezone',inplace=True,axis=1)

#Renaming Columns
df.rename(columns={'flight_date':'Flight Date','flight_status':'Status','departure.airport':'Departure Airport',
                  'departure.iata':'Departure IATA','arrival.airport':'Arrival Airport',
                  'arrival.iata':'Arrival IATA', 'airline.name':'Airline Name','airline.iata':'Airline IATA',
                  'flight.number':'Flight Number','flight.iata':'Flight IATA','departure.delay':'Departure Delay',
                  'region':'Arrival Region','city':'Arrival City','departure_date':'Departure Date','departure_time':'Departure Time',
                  'arrival_date':'Arrival Date','arrival_time':'Arrival Time','arrival.delay':'Arrival Delay'},inplace=True)
df['Date']=date

#SavingFile
filename='Data/Data_{}.csv'.format(date)
if not os.path.exists('Data'):
    os.makedirs('Data')
df.to_csv(filename,index=False)
print("File Successfully save for date {} at {}".format(date,filename))