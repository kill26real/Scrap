def checkduplicate(output, name, street, plz, city):
    if len(output) == 0:
        return True
    for entry in output:
        if (entry['name'] == name and
            entry['street'] == street and
            entry['postal_code'] == plz and
            entry['city'] == city):
            return False
    return True

# check = checkduplicate(OUTPUT, name, street, plz, city)
# if check and iso2 in valid_countries:
#     print(f'garage {k}')
#     print('search by: ', row_csv[0])
#     print('name: ' + str(name))
#     print('street: ' + street)
#     print('city: ' + city)
#     print('plz: : ' + plz)
#     print('country: ', country)
#     print('services: ' + str(services))
#     print('web: ', web)
#     print('phone: ' + str(phone))
#     print('fax: ', fax)
#     print('email: ' + str(email))
#     print('latitude: ' + str(lat))
#     print('longitude: ' + str(lng))
#     print('------------------------------------------------')
#     k += 1
#     with open('Bosch.csv', 'a', newline='', encoding="utf-8") as csvfile:
#         csv_writer = csv.writer(csvfile)
#         csv_writer.writerow(
#             [name, street, city, plz, contract, country, iso2, phone, fax, web, email, services,
#              lat, lng, garage_id])
#     OUTPUT.append({
#         'abc': 'ID',
#         'country': iso2,
#         'target_groups': 'independent car service',
#         'contracts': contract,
#         'name': name,
#         'street': street,
#         'city': city,
#         'postal_code': plz,
#         'phone': phone,
#         'fax': fax,
#         'web': web,
#         'email': email,
#         'services': services,
#         'latitude': lat,
#         'longitude': lng,
#         'garage_id': garage_id,
#         'contact_title': '',
#         'contact_first_name': firstname,
#         'contact_last_name': lastname,
#         'contact_position': '',
#         'contact_email': '',
#         'source': source
#     })
# send_data_raw(OUTPUT, 'Bosch')
