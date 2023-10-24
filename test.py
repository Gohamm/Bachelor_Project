import pandas as pd

date_from = "2023-06-01"
date_to = "2023-06-30"
post_data = dict()

#excel sheet connection
file_path = r'c:\Users\Ulrich\Desktop\GBE\Bachelor Project\masterdata_sheet.xlsx'

df = pd.read_excel(file_path, usecols=[0, 1])

print (df)

for index, row in df.iloc[0:].iterrows():
    print("processing row", index)
    post_data[len(post_data)] = {
        'keywords': row[0],
        'location_code': row[1],
        'date_from': date_from,
        'date_to' : date_to
    }

print(post_data)