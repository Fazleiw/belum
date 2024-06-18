import requests
import urllib.parse
import json
import time
import subprocess
import threading

# URL dan headers
url = "https://api.service.gameeapp.com/"
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://telegram.blum.codes',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
}
# Fungsi untuk membaca initData dari file
def read_initdata_from_file(filename):
    initdata_list = []
    with open(filename, 'r') as file:
        for line in file:
            initdata_list.append(line.strip())
    return initdata_list

def get_nama_from_init_data(init_data):
    parsed_data = urllib.parse.parse_qs(init_data)
    if 'user' in parsed_data:
        user_data = parsed_data['user'][0]
        data = ""
        user_data_json = urllib.parse.unquote(user_data)
        user_data_dict = json.loads(user_data_json)
        if 'first_name' in user_data_dict:
            data = user_data_dict['first_name']
        if 'last_name' in user_data_dict:
            data = data + " " + user_data_dict['last_name']
        if 'username' in user_data_dict:
            data = data + " " + f"({user_data_dict['username']})"
        return data
    return None

# Fungsi untuk melakukan start session
def auth(initdata):
    payload = {
        'query': initdata
    }
    try:
        response = requests.post('https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP', json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['token']['access']
    except requests.exceptions.RequestException as error:
        print(f'Error during authentication: {error}')
        raise

def get_tasks(token):
    headers["authorization"] = f'Bearer {token}'
    response = requests.get('https://game-domain.blum.codes/api/v1/tasks', headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def submission(token, task_id):
    headers["authorization"] = f'Bearer {token}'
    response = requests.post(f'https://game-domain.blum.codes/api/v1/tasks/{task_id}/start', headers=headers)
    return response

def claim(token, task_id):
    headers["authorization"] = f'Bearer {token}'
    response = requests.post(f'https://game-domain.blum.codes/api/v1/tasks/{task_id}/claim', headers=headers)
    return response

# Fungsi untuk menjalankan operasi untuk setiap initData
def process_initdata(init_data):
    nama = get_nama_from_init_data(init_data)
    print(nama)
    token = auth(init_data)
    if token:
        tasks = get_tasks(token)
        for task in tasks:
            if "subTask" in task and "id" in task["subTask"]:
                task_id = f'{task["subTask"]["id"]}-{task["id"]}'
            else:
                task_id = task["id"]

            if "submission" not in task or task["status"] != "FINISHED":
                submission_response = submission(token, task_id)
                if submission_response.status_code == 200:
                    print(f"Submission successful for task {task_id}")


                time.sleep(40)
                
                claim_response = claim(token, task_id)
                if claim_response.status_code == 200:
                    print(f"Claim successful for task {task_id}")
                else:
                    print(f"Claim failed for task {task_id}: {claim_response.text}")
            else:
                print(f"Task {task_id} already claimed")
    else:
        print("Authentication failed")

# Main program
def main():
    initdata_file = "initdata.txt"
    initdata_list = read_initdata_from_file(initdata_file)
    threads = []
    
    for init_data in initdata_list:
        thread = threading.Thread(target=process_initdata, args=(init_data.strip(),))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
        subprocess.run(["python3", "gamee.py"])
