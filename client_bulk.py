from lib.preprocess import preprocess_text, remove_mail_links, remove_numbers
import pandas as pd
import requests

def send_data(data: str):
    url = "http://10.10.144.89:8001/classify"
    response = requests.post(url, json={"data": data})
    if response.status_code == 200:
        return response.json()
    else:
        return "Error: Unable to process data"
    
if __name__ == "__main__":
    dataPath = './data/recent_data.csv'
    #load data
    df = pd.read_csv(dataPath)
    df = df[['Ticket ID', 'Subject', 'Description']]

    #combine subject and description
    df['Text'] = df['Subject'] + ' ' + df['Description']
    df.fillna(' ', inplace=True)
    df['Text']=df['Text'].apply(str)
    df['Text']=df['Text'].apply(preprocess_text)
    df['Text']=df['Text'].apply(remove_mail_links)
    df['Text']=df['Text'].apply(remove_numbers)
    combined = list(df['Text'])

    #api call on the data points iteratively
    category = []
    for text in combined:
        category.append(send_data(text))
    
    #save the category
    df['Category'] = category
    df.to_csv('./data/output.csv', index=False)