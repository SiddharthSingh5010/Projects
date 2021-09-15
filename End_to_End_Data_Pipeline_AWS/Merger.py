import glob
import os
import pandas as pd
from datetime import datetime

print(os.getcwd())
os.chdir('/home/ec2-user')
print(os.getcwd())

date=datetime.strftime(datetime.today(),format="%d-%m-%Y")
print(date)
#Reading CSV Files 
print("Reading files in /Data")
file_list=glob.glob("Data/*.csv")

#Creating Merged DataFrame
df_final=pd.DataFrame(columns=pd.read_csv(file_list[0]).columns)
for file in file_list:
    df=pd.read_csv(file)
    df_final=pd.concat([df_final,df],axis=0,ignore_index=True)

#Dropping Duplicates
print("Dropping Duplicates")
df_final.drop_duplicates(inplace=True)

#Saving Final File
df_final.to_csv("Data_Final.csv")
print("Successfully Saved file Data_Final.csv")