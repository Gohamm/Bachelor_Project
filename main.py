import pandas as pd
import base64
import requests
from client import RestClient
import time
import json


def authorize(login, password):
    #auth using RestClient class
    return RestClient(login, password)

def read_excel_file(file_path):
    #read excel file and return dataframe
    return pd.read_excel(file_path, usecols=[0 ,1])

def construct_post_data(df, date_from, date_to):
    #create a list to store keywords
    post_data = {}

    #loop through the dataframe to gather keywords
    for index, row in df.iterrows():
        
        #construct the post_data with all keywords
        keyword_data = {
        'location_code': int(row[1]),
        'keywords': [str(row[0])],     
        'date_from': date_from,
        'date_to' : date_to
        }
        post_data[str(index)] = keyword_data

    return post_data

def make_api_request(client, url, post_data):
    #convert post_data to JSON format
    json_data = json.dumps(post_data)

    #make a single API request
    return client.post(url, json_data)

def handle_api_respone(response):

    print("api response:", response)
    #handle the api response
    if response["status_code"] == 20000 and response.get("tasks_count", 0) > 0:
        task = response["tasks"][0]
        if task["status_code"] == 20000:
            result = task.get("result", [])
            if result and isinstance(result, list):
                #extract and return a dataframe from the response
                keyword_data = []
                for keyword_info in result:

                    date_info = keyword_info.get('monthly_searches', [])[0]
                    date = f"{date_info.get('year')}-{date_info.get('month'):02d}" if date_info else None
                    
                    keyword_entry = {
                        'location_code': keyword_info.get('location_code'),
                        'keywords': [keyword_info.get('keyword')],
                        'search_volume': keyword_info.get('search_volume'),
                        'date': date
                    }
                    keyword_data.append(keyword_entry)

                df_result = pd.DataFrame(keyword_data)
                return df_result[['location_code', 'keywords', 'search_volume', 'date']]
                
                #return pd.DataFrame(response['result'][1:], columns=response['result'][0])
    else:
        print("Error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
        return None

def main():
    login = "andreas_ulrich@hotmail.com"
    password = "f4203e32318d9f9c"
    date_from = "2023-06-01"
    date_to = "2023-06-30"

    client = authorize(login, password)

    #API credentials
    credentials = "YW5kcmVhc191bHJpY2hAaG90bWFpbC5jb206ZjQyMDNlMzIzMThkOWY5Yw=="
    url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"

    #excel sheet location
    file_path = file_path = r'c:\Users\Ulrich\Desktop\GBE\Bachelor Project\masterdata_sheet.xlsx'

    df = read_excel_file(file_path)
    post_data = construct_post_data(df, date_from, date_to)

    print(post_data)

    response = make_api_request(client, url, post_data)

    df_result = handle_api_respone(response)

    #print dataframe
    if df_result is not None:
        print("success!")
        print(df_result)

if __name__ == "__main__":
    main()


    
    








