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

def extract_keywords_and_locations(df):
    #extract keywords and location codes from the dataframe
    keyword_list = []
    for index, row in df.iterrows():
        keyword_info = {
            'keyword': str(row.iloc[0]),
            'location_code': int(row.iloc[1])
        }
        keyword_list.append(keyword_info)
    return keyword_list

def construct_post_data(keyword_list, date_from, date_to):

    # Create a list to store all keywords within a task
    all_keywords = []

    # Loop through the list of keywords
    for keyword_info in keyword_list:
        # Accumulate all keywords
        all_keywords.append(keyword_info['keyword'])

    # Construct the post_data with all keywords
    post_data = {
        'location_code': int(keyword_list[0]['location_code']),  # Assuming all keywords have the same location_code
        'keywords': all_keywords,
        'date_from': date_from,
        'date_to': date_to
    }

    return [post_data]




    #create a list to store keywords
    #post_data = []

    #create a list to store keywords within a task

    #loop through the dataframe to gather keywords
    #for keyword_info in keyword_list:
        
        #construct the post_data with all keywords
        #task_data = {
        #'location_code': int(keyword_info['location_code']),
        #'keywords': [keyword_info['keyword']],    
        #'date_from': date_from,
        #'date_to': date_to    
        #}
        #post_data.append(task_data)
        

    #return post_data

def make_api_request(client, url, post_data):
    #convert post_data to JSON format
    json_data = json.dumps(post_data)
    
    #make a single API request
    return client.post(url, json_data)

def handle_api_respone(response):

    print("api response:", response)
    #handle the api response
    if response["status_code"] == 20000 and response.get("tasks_count", 0) > 0:
        task = response.get("tasks", [])[0]
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
    url = "https://sandbox.dataforseo.com/v3/keywords_data/google/search_volume/live"

    #excel sheet location
    file_path = file_path = r'c:\Users\Ulrich\Desktop\GBE\Bachelor Project\masterdata_sheet.xlsx'

    df = read_excel_file(file_path)

    #extract keywords and location codes
    keyword_list = extract_keywords_and_locations(df)

    #use the data to construct post_data
    post_data = construct_post_data(keyword_list, date_from, date_to)

    print(post_data)

    response = make_api_request(client, url, post_data)

    df_result = handle_api_respone(response)

    #print dataframe
    if df_result is not None:
        print("success!")
        print(df_result)

if __name__ == "__main__":
    main()


    
    








