import requests
import json
import csv

LOCAL_SERVER_URL = 'http://192.168.58.78:5000/receive_data'

def send_data_csv(csv_path):
    """
    Sends data to server in from of a csv file,
    which has to be loaded by the path as parameter
    """
    loaded_csv = load_csv(csv_path)
    json_data = json.dumps(loaded_csv)
    response = send_data_to_server(LOCAL_SERVER_URL, json_data, csv_path)
    analyze_response(response)

def send_data_raw(input_data):
    """
    Sends data to server based on the raw input data,
    should be a list of entries that are in the correct format
    """
    json_data = json.dumps(input_data)
    response = send_data_to_server(LOCAL_SERVER_URL, json_data)
    analyze_response(response)


def send_data_to_server(url, data,csv_path=''):
    try:
        print(csv_path)
        print('sending data to Database please wait and dont close the script')
        response = requests.post(url, json=data)
        # response.raise_for_status() # Raise an exception for HTTP errors
        if response.status_code == 200:
            return response
        elif response.status_code == 400 or response.status_code == 500:
            error_message = response.json().get('message', 'No message provided')
            error_traceback = response.json().get('traceback', 'No traceback available')
            print(f"Error {response.status_code}: {error_message}")
            print(f"Traceback: {error_traceback}")
            return response
        else:
            return response
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")
        return None


def analyze_response(response):
    if response.status_code == 200:
        print("Data successfully transmitted and inserted")
    elif response.status_code == 201:
        response_json = response.json()
        reasons = response_json.get('reason', ['Unknown error'])
        print(reasons)
    elif response.status_code != 500:
        response_json = response.json()
        reasons = response_json.get('reason', ['Unknown error'])
        print('check failure reasons as to why the import didnt succeed')
        # Write the reasons to a CSV file
        with open('failure_reasons.csv', 'w', newline='', encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['reason'])

        with open('failure_reasons.csv', 'a', newline='', encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            for reason in reasons:
                csv_writer.writerow([reason])

def load_csv(path):
    with open(path, 'r',encoding='UTF-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        return list(reader)