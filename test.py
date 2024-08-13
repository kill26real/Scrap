import pandas as pd


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
# pd.set_option('display.max_colwidth', None)  # Keine Begrenzung der Spaltenbreite

df = pd.read_csv('2830_Roady_werkstattdb.csv', sep=",",  dtype={'postal_code': 'string'})

# df['postal_code'] = df['postal_code'].apply(lambda x: f"{x:05}")

# del df['Unnamed: 0']
# df = df.drop(120, axis=0)
# df = df.drop(119, axis=0)


print(df['postal_code'].dtype)

# df.loc[28, 'city'] = "L'Hospitalet de Llobregat"
# df.loc[28, 'street'] = df.loc[28, 'street'].replace(" 'Hospitalet de Llobregat", '')

print(df)


# df.to_csv('3737_Vulco_werkstattdb.csv', index=False)