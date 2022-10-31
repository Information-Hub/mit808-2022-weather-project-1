import pandas as pd
import os
import matplotlib.pyplot as plt
import requests
from io import StringIO

def read_from_drive(url):
    url='https://drive.google.com/uc?id=' + url.split('/')[-2]
    df = pd.read_csv(url)
    return df


#convert daily to monthly to get monthly rainfall

from datetime import datetime
def date_convert(d):
    return datetime.strptime(d, '%d-%b-%Y').strftime('%Y-%m-01')




# def read_from_drive(url):
#     file_id = url.split('/')[-2]
#     dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
#     url2 = requests.get(dwn_url).text
#     csv_raw = StringIO(url2)
#     df = pd.read_csv(csv_raw)
#     return df





