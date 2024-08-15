import pandas as pd


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
# pd.set_option('display.max_colwidth', None)  # Keine Begrenzung der Spaltenbreite

df = pd.read_csv('2780_Wurth_werkstattdb.csv', sep=",", dtype={'postal_code': 'string'})

# df['postal_code'] = df['postal_code'].apply(lambda x: f"{x:05}")

# del df['Unnamed: 0']
# df = df.drop(120, axis=0)
# df = df.drop(119, axis=0)


print(df['postal_code'].dtype)

# df.loc[100, 'phone'] = 'NaN'
# df.loc[100, 'street'] = "Voie Nouvelle Les Latteux"
# df.loc[100, 'postal_code'] = "89400"
# df.loc[100, 'city'] = "MIGENNES"
# df.loc[109, 'street'] = "419 la belle fontaine"
# df['phone'] = df['phone'].str.replace(".", "")



print(df)


# df.to_csv('2831_E.LECLERC_werkstattdb.csv', index=False)