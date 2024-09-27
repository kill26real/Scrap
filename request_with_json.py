import requests
import json
url = "https://www.autofit.com/api/search/universal_workshops"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://www.autofit.com',
    'Referer': 'https://www.autofit.com/werkstattsuche',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}
payload = {
    "layouts": ["auto_fit"],
    "city": None,
    "open": None,
    "selectedServices": [],
    "limit": 3,
    "offset": 0
}
response = requests.post(url, headers=headers, data=json.dumps(payload))
if response.status_code == 200:
    data = response.json()
    garages = data['data']['workshops']
    print('gefundene garages: ', len(garages))
    print("Erhaltene Daten:")
    print(json.dumps(data, indent=4))
