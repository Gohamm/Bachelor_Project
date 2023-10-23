import pandas as pd

import requests

from restclient import RestClient

login = "andreas_ulrich@hotmail.com"
password = "f4203e32318d9f9c"
date_from = "2023-06-01"
date_to = "2023-06-30"



client = RestClient(login, password)

post_data = dict()



#excel sheet connection
file_path = r'c:\Users\Ulrich\Desktop\GBE\Bachelor Project\masterdata_sheet.xlsx'

df = pd.read_excel(file_path, usecols=[0, 1])

for index, row in df.iloc[1:].iterrows():
    post_data[len(post_data)] = {
        'keywords': row[0],
        'location_code': row[1],
        'date_from': date_from,
        'date_to' : date_to
    }

response = client.post("/v3/keywords_data/google_ads/search_volume/task_post", post_data)

if response["status_code"] == 20000:
    print(response)

else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))


def handleAPIdata(): 
    client = RestClient("login", "password")

    response = client.get("/v3/keywords_data/google_ads/search_volume/tasks_ready")

    
    








