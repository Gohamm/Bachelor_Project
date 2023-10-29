import pandas as pd
import base64
import requests
from client import RestClient



login = "andreas_ulrich@hotmail.com"
password = "f4203e32318d9f9c"
date_from = "2023-06-01"
date_to = "2023-06-30"


#authorization
client = RestClient(login, password)

print(client)

post_data = dict()
#API credentials
credentials = "YW5kcmVhc191bHJpY2hAaG90bWFpbC5jb206ZjQyMDNlMzIzMThkOWY5Yw=="

url = "https:///v3/keywords_data/google_ads/search_volume/live?"

headers = {"Authorization": f"Basic {credentials}"}



#excel sheet connection
file_path = r'c:\Users\Ulrich\Desktop\GBE\Bachelor Project\masterdata_sheet.xlsx'

df = pd.read_excel(file_path, usecols=[0, 1])

for index, row in df.iloc[0:].iterrows():
    post_data[len(post_data)] = {
        'location_code': row[1],
        'keywords': row[0],     
        'date_from': date_from,
        'date_to' : date_to
    }

print(post_data)

response = client.post(url, post_data)

if response["status_code"] == 20000:
    print(response)

else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))




    
    








