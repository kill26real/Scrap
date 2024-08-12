import pandas as pd


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
# pd.set_option('display.max_colwidth', None)  # Keine Begrenzung der Spaltenbreite

df = pd.read_csv('2831_E.LECLERC_werkstattdb.csv', sep=",")

# df['postal_code'] = df['postal_code'].apply(lambda x: f"{x:05}")

# del df['Unnamed: 0']
# df = df.drop(120, axis=0)
# df = df.drop(119, axis=0)


print(df['phone'].dtype)

print(df)

# df_new = df.drop_duplicates()
# #
# df_copy = df_new.copy()
# df_copy['postal_code'] = df_copy['postal_code'].astype('string')
# df_copy['postal_code'] = df_copy['postal_code'].apply(lambda x: '0' + str(x) if len(str(x)) < 5 else x).astype('string')
#
# print(df_copy['postal_code'])
# print('TYPE', df_copy['postal_code'].dtype)
#
#
# df.to_csv('2830_Roady_werkstattdb.csv')