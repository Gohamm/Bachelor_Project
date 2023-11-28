import pandas as pd
import base64
import requests
from client import RestClient
from datetime import datetime
import json
from sqlalchemy import create_engine, ARRAY, String, Date, Integer


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

def make_api_request(client, url, post_data):
    # convert post_data to JSON format
    json_data = json.dumps(post_data)
    
    # make a single API request
    return client.post(url, json_data)

def handle_api_respone(response):

    print("api response:", response)

    if response["status_code"] == 20000 and response.get("tasks_count", 0) > 0:
        tasks = response.get("tasks", [])

        if tasks and isinstance(tasks, list):
            keyword_data = []

            for task in tasks:
                results = task.get("result", [])

                for result_info in results:
                    keyword = result_info.get("keyword")
                    location_code = result_info.get("location_code")
                    monthly_searches = result_info.get("monthly_searches", [])

                    if monthly_searches:
                        keywords = [keyword]
                        for monthly_search in monthly_searches:
                            date = f"{monthly_search.get('year')}-{monthly_search.get('month'):02d}" if monthly_search else None
                            search_volume = monthly_search.get("search_volume")

                            keyword_entry = {
                                "location_code": location_code,
                                "keywords": keywords,
                                "search_volume": search_volume,
                                "date": date,
                            }
                            keyword_data.append(keyword_entry)

            if keyword_data:
                df_result = pd.DataFrame(keyword_data)
                print("DataFrame columns:", df_result.columns)
                return df_result
            else:
                print("No keyword data found.")
                return None

    else:
        print("Error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
        return None

def append_to_database(df):
    # PostgreSQL connection parameters
    db_params = {
        'host': '34.89.54.138',
        'port': '5432',
        'database': 'bachelordb',
        'user': 'postgres',
        'password': 'andr294567'
    }

    # Connect to the PostgreSQL database
    # Create a connection string for SQLAlchemy
    conn_str = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"

    try:
        # Create a SQLAlchemy engine
        engine = create_engine(conn_str)

        #convert 'date' column to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

        # Convert 'keywords' column from list to concatenated string
        df['keywords'] = df['keywords'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

        # Append DataFrame to PostgreSQL table
        df.to_sql('api_data', con=engine, if_exists='append', index=False, schema='dataforseo', dtype={'keywords': String(), 'search_volume': Integer(), 'date': Date()})
        print("Data appended to PostgreSQL table successfully.")
    except Exception as e:
        print(f"Error appending data to PostgreSQL table: {str(e)}")
    finally:
        # Dispose of the engine to close the database connection
        engine.dispose()

def main():

    # credentials
    login = "andreas_ulrich@hotmail.com"
    password = "f4203e32318d9f9c"

    # specifying the date range to fetch data
    date_from = "2023-06-01"
    date_to = "2023-06-30"

    client = authorize(login, password)

    # API url
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

    # create a dataframe to store api results
    df_result = handle_api_respone(response)

    #print dataframe
    if df_result is not None:
        print("success!")
        print(df_result)

        #append the dataframe to postgres database
        append_to_database(df_result)

if __name__ == "__main__":
    main()


    
    








