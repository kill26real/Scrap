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


# with open('2830_Roady_werkstattdb.csv', mode='r', newline='', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         print(row)

# iloc

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

df = pd.read_csv('2830_Roady_werkstattdb.csv',sep=",")

# df.columns = df.iloc[0]  # Setze die erste Zeile als Spaltennamen
# df.index = df.iloc[:, 0]  # Setze die erste Spalte als Index

print('with duplicates: ', len(df))
# print(df.head())


duplikate_df = df[df.duplicated()]
# print(duplikate_df.sort_values(by='name').head(10))
print('duplicates: ', len(duplikate_df.sort_values(by='name')))

df_ohne_duplikate = df.drop_duplicates()
# print(df_ohne_duplikate.sort_values(by='name').head(10))
print('ohne duplicates', len(df_ohne_duplikate.sort_values(by='name')))




