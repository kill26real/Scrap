import re
import os
import csv
from tqdm import tqdm
from fuzzywuzzy import fuzz
import phonenumbers
from db_connector import *
from csv_maker import *
import datetime, time

# erstelle RQ_Company_Profiles_Europe.csv
try:
    get_csv()
except Exception as err:
    print('create csv failed with error: ' + str(err))


# Pfad zum Marken CSV
csv_path = 'RQ_Company_Profiles_Europe.csv'

# Pfad zum Textordner
text_folder = '2023-12_deep'


def load_csv(path):
    with open(path, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        return list(reader)

def fuzzy_search_around(text, search_value, other_value='Town', char_range=50):
    matches = re.finditer(r'\b' + re.escape(search_value.lower()) + r'\b', text.lower())
    
    for match in matches:
        start_pos = max(0, match.start() - char_range)
        end_pos = min(len(text), match.end() + char_range)

        nearby_text = text[start_pos:end_pos]
        similarity_ratio = fuzz.ratio(other_value.lower(), nearby_text.lower())
        
        # You can adjust the threshold based on your requirements
        if similarity_ratio >= 80:
            return True
    
    return False

def search_around(text, search_value, other_value='Town', char_range=50):
    matches = re.finditer(r'\b' + re.escape(search_value.lower()) + r'\b', text.lower())
    for match in matches:
        start_pos = max(0, match.start() - char_range)
        end_pos = min(len(text), match.end() + char_range)

        nearby_text = text[start_pos:end_pos]
        if other_value.lower() in nearby_text.lower():
            return True
    return False

def phone_fixer(text,row_data,fax='Empty'):
    preselect = row_data['Preselect']
    phone_number = row_data['Phone']
    fax_number = row_data['Fax'].replace(' ','')
    return_element = {'phone':'','preselect':'','fax':''}
    for match in phonenumbers.PhoneNumberMatcher(text,''):
        if match:
            parsed_number = phonenumbers.parse(match.raw_string,None)
            match_national = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            match_national = match_national[1:].replace(' ','')
            if match_national == phone_number:
                return_element['phone'] = 'X'
                match_international = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                match_international = match_international[1:3]
                preselect = preselect[3:5]
                if preselect == match_international:
                    return_element['preselect'] = 'X'
            if fax == 'Empty':
                return return_element
            if match_national == fax_number:
                return_element['fax'] = 'X'
    return return_element
    

def search_and_replace_all_fields(text,data):
    # Create a new dictionary to store the modified data
    modified_data = {key: '' for key in data.keys() if key != 'ID_Company'}
    modified_data['street_near_town'] = ''
    if data['ID_Company'] == '279':
        abc =''
    for key, value in data.items():
        search_value = value  # Use the value associated with each key as the search value
        if key == 'ID_Company':
            continue
        if search_value == '' or search_value == 'NULL':
            modified_data[key] = 'Empty'
        elif re.search(r'\b' + re.escape(search_value.lower()) + r'\b', text.lower()):
            modified_data[key] = 'X'
            if key == 'Street' and modified_data['street_near_town'] == '':
                second_search_vlaue = data['Town']
                if search_around(text,search_value,second_search_vlaue,50):
                    modified_data['street_near_town'] = 'X'
            elif key == 'Town' and modified_data['street_near_town'] == '':
                second_search_vlaue = data['Street']
                if search_around(text,search_value,second_search_vlaue,50):
                    modified_data['street_near_town'] = 'X'
        else:
            modified_data[key] = ''

    return modified_data

def write_header():
    with open('output_addressfinder.csv', 'w', newline='', encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile,delimiter=';')
                csv_writer.writerow(['ID_Company','Country','Company_Name_Filter','Street','Postal_code','Fax','Town','Preselect','Phone','Contact Last name','Contact first name','Mail','Internet','street_near_town'])

st = datetime.datetime.fromtimestamp(time.time()).strftime('%m.%d.%Y')
tqdm.write("Loading addresses from csv")
loaded_csv =  load_csv(csv_path)
tqdm.write("Loading last id for addressfinder")
try:
    with open('last_id_addressfinder.txt', 'r') as f:
        last_id = int(f.read())
except FileNotFoundError:
    last_id = None
    write_header()
tqdm.write("Opening addressfinder output")
with open('output_addressfinder.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile,delimiter=';')

    tqdm.write("Processing Crawler information")
    for row in tqdm(loaded_csv):
        folder_id = int(row['ID_Company'])

        # Check if the folder for the current row ID exists
        if str(folder_id) not in os.listdir(text_folder):
            # Logic for missing folders
            with open('output_addressfinder_missing.csv', 'a', newline='', encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                csv_writer.writerow([folder_id])
            continue
        
        # check if ID_Company exist in check table
        conn = open_cae()
        cursor = conn.cursor()
        cursor.execute("select ID_Company from [CAE].[dbo].[tbl_Master Data_Company_address_check] WHERE ID_Company = "+str(folder_id)+";" )                        
        row_cae = cursor.fetchone()
        if row_cae is None:
            cursor = conn.cursor()
            cursor.execute("insert into [CAE].[dbo].[tbl_Master Data_Company_address_check] (ID_Company) values("+str(folder_id)+")" )     
            conn.commit()
        # Process files within the folder
        matching_row = row
        folder_path = os.path.join(text_folder, str(folder_id))
        cursor = conn.cursor()
        for filename in os.listdir(folder_path):
            if not filename.endswith('.txt'):
                continue

            tqdm.write(f"Processing: {filename}")
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                text = f.read()

                result = search_and_replace_all_fields(text,matching_row)
                if result['Street'] == 'X' and result['Town'] == '' or result['Street'] == 'X' and result['Postal_code'] == '': 
                    if result['Town'] == '':
                        if fuzzy_search_around(text,matching_row['Street'],matching_row['Town']):
                            # cursor.execute("update [CAE].[dbo].[tbl_Master Data_Company_address_check] set Town=1,[street_near_town]=1,"\
                            #                 "[street near edit date]='"+str(st)+"',[town edit date]='"+str(st)+"' where ID_Company ="+str(folder_id)+";" )     
                            # conn.commit()
                            result['Town'] = 'X'
                            result['street_near_town'] ='X'
                    elif result['Postal_code'] == '':
                        if fuzzy_search_around(text,matching_row['Street'],matching_row['Postal_code']):
                            result['Postal_code'] = 'X'
                            # cursor.execute("update [CAE].[dbo].[tbl_Master Data_Company_address_check] set [Postal_code]=1,"\
                            #                 "[postal_code edit date]='"+str(st)+"' where ID_Company ="+str(folder_id)+";" )     
                            # conn.commit()
                if result['Town'] == 'X' and result['Street'] == '' or result['Town'] == 'X' and result['Postal_code'] == '': 
                    if result['Street'] == '':
                        if fuzzy_search_around(text,matching_row['Town'],matching_row['Street']):
                            # cursor.execute("update [CAE].[dbo].[tbl_Master Data_Company_address_check] set Street=1,[street_near_town]=1,"\
                            #                 "[street near edit date]='"+str(st)+"',[street edit date]='"+str(st)+"' where ID_Company ="+str(folder_id)+";" )     
                            # conn.commit()
                            result['Street'] = 'X'
                            result['street_near_town'] ='X'
                    elif result['Postal_code'] == '':
                        if fuzzy_search_around(text,matching_row['Town'],matching_row['Postal_code']):
                            # cursor.execute("update [CAE].[dbo].[tbl_Master Data_Company_address_check] set [Postal_code]=1,"\
                            #                 "[postal_code edit date]='"+str(st)+"' where ID_Company ="+str(folder_id)+";" )     
                            # conn.commit()
                            result['Postal_code'] = 'X'
                if result['Postal_code'] == 'X' and result['Street'] == '' or result['Postal_code'] == 'X' and result['Town'] == '': 
                    if result['Street'] == '':
                        if fuzzy_search_around(text,matching_row['Postal_code'],matching_row['Street']):
                            # cursor.execute("update [CAE].[dbo].[tbl_Master Data_Company_address_check] set Street=1,"\
                            #                 "[street edit date]='"+str(st)+"' where ID_Company ="+str(folder_id)+";" )     
                            # conn.commit()
                            result['Street'] = 'X'
                    elif result['Town'] == '':
                        if fuzzy_search_around(text,matching_row['Postal_code'],matching_row['Town']):
                            # cursor.execute("update [CAE].[dbo].[tbl_Master Data_Company_address_check] set [Postal_code]=1,"\
                            #                 "[postal_code edit date]='"+str(st)+"' where ID_Company ="+str(folder_id)+";" )     
                            # conn.commit()
                            result['Postal_code'] = 'X'
                if result['Phone'] == '' or result['Fax'] == '' or result['Preselect'] == '':
                    result_phone_fixer = phone_fixer(text,matching_row,matching_row['Fax'])
                    if result['Phone'] == '':
                        if result_phone_fixer['phone'] == 'X':
                            # cursor.execute("update [CAE].[dbo].[tbl_Master Data_Company_address_check] set Phone=1,"\
                            #                 "[phone edit date]='"+str(st)+"' where ID_Company ="+str(folder_id)+";" )     
                            # conn.commit()
                            result['Phone'] = 'X'
                    if result['Preselect'] == '':
                        if result_phone_fixer['preselect'] == 'X':
                            # cursor.execute("update [CAE].[dbo].[tbl_Master Data_Company_address_check] set Preselect=1,"\
                            #                 "[preselect edit date]='"+str(st)+"' where ID_Company ="+str(folder_id)+";" )     
                            # conn.commit()
                            result['Preselect'] = 'X'
                    if result['Fax'] == '':
                        if result_phone_fixer['fax'] == 'X':
                            # cursor.execute("update [CAE].[dbo].[tbl_Master Data_Company_address_check] set Fax=1,"\
                            #                 "[fax edit date]='"+str(st)+"' where ID_Company ="+str(folder_id)+";" )     
                            # conn.commit()
                            result['Fax'] = 'X'
                result_row = list(result.values())
                for key,value in result.items():
                    if value == 'X':
                        lower_key = key.lower()
                        if key == 'street_near_town':
                            lower_key = 'street near'
                        elif key == 'Company_Name':
                            key = 'Company_Name_Filter'
                            lower_key = 'Company Name'
                        if key == 'Contact_Last_name' or key == 'Conatct_first_name':
                            if key == 'Conatct_first_name':
                                key = 'Contact first name'
                            key = key.replace('_',' ')
                            lower_key = ''
                            key_split = key.split()
                            lower_key = ' '.join(key_split[-2:]).lower()
                            cursor.execute(f"update [CAE].[dbo].[tbl_Master Data_Company_address_check] set [{key}]=1,"\
                                f"[{lower_key} edit date]='"+str(st)+"' where ID_Company ="+str(folder_id)+";" )
                            conn.commit()
                        else:
                            # key = key.replace('_',' ')
                            cursor.execute(f"update [CAE].[dbo].[tbl_Master Data_Company_address_check] set {key}=1,"\
                                f"[{lower_key} edit date]='"+str(st)+"' where ID_Company ="+str(folder_id)+";" )
                            conn.commit()
                writer.writerow([folder_id] + result_row)

            with open('last_id.txt', 'w') as f:
                f.write(str(folder_id))

tqdm.write("Fertig mit der Verarbeitung der Textdateien.")