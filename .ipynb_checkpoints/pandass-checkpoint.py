import csv
import requests
import json
import datetime, time
import urllib3
import re
from bs4 import BeautifulSoup
from lxml import etree
import sys
import html
import pandas as pd

# df.columns = df.iloc[0]  # Setze die erste Zeile als Spaltennamen

# del df['Unnamed: 0']  # eine Spalte entfernen
# df = df.drop(120, axis=0) # eine Zeile entfernen

# df.loc[100, 'phone'] = '09 69 32 42 52'

# with open('2830_Roady_n_row_werkstattdb.csv', 'w', newline='', encoding="utf-8") as csvfile:
#    csv_writer = csv.writer(csvfile)
#    csv_writer.writerow(
#        ['abc', 'country', 'target_groups', 'contracts', 'name', 'street', 'city', 'postal_code', 'phone',
#         'fax', 'web', 'email', 'services', 'latitude', 'longitude', 'garage_id', 'sources'])



pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
# pd.set_option('display.max_colwidth', None)  # Keine Begrenzung der Spaltenbreite

df = pd.read_csv('3737_Vulco_werkstattdb.csv',sep=",")

df['postal_code'] = df['postal_code'].apply(lambda x: f"{x:05}")

del df['Unnamed: 0']
# df = df.drop(120, axis=0)

df['phone'].astype(str)

# df.index = df.iloc[:, 0]  # Setze die erste Spalte als Index

df = df.reset_index(drop=True)


print(df)


df.to_csv('2830_Roady_werkstattdb.csv', index=False)




