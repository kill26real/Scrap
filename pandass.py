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
# df.index = df.iloc[:, 0]  # Setze die erste Spalte als Index

# del df['Unnamed: 0']  # eine Spalte entfernen
# df = df.drop(120, axis=0) # eine Zeile entfernen

# df.loc[100, 'phone'] = '09 69 32 42 52'

# del df['Unnamed: 0']
# df = df.drop(120, axis=0)

# df = df.reset_index(drop=True)


# duplicate_df = df[df.duplicated()]
# print(duplicate_df.sort_values(by='name').head(10))
# print('duplicates: ', len(duplicate_df.sort_values(by='name')))

# df_ohne_duplicate = df.drop_duplicates()
# print(df_ohne_duplicate.sort_values(by='name').head(10))
# print('ohne duplicates', len(df_ohne_duplicate.sort_values(by='name')))





pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
# pd.set_option('display.max_colwidth', None)  # Keine Begrenzung der Spaltenbreite

df = pd.read_csv('3737_Vulco_werkstattdb.csv', sep=",", skipinitialspace=True,  dtype={'postal_code': 'string'})

df['postal_code'] = df['postal_code'].apply(lambda x: f"{x:05}")
df['postal_code'] = df['postal_code'].astype(pd.StringDtype())
df['phone'] = df['phone'].astype(pd.StringDtype())
df['fax'] = df['fax'].astype('string')

df['phone'] = df['phone'].str.replace(" ", "")
df['fax'] = df['fax'].str.replace(" ", "")


print(df)

print('postal type', df['postal_code'].dtype)
print('phone', df['phone'].dtype)
print('fax', df['fax'].dtype)
print('web', df['web'].dtype)
print('name', df['name'].dtype)


# df.to_csv('3737_Vulco_new_werkstattdb.csv', index=False)




