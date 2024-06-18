import requests
import time
import threading

def authenticate(init_data):
    url = 'https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP'
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
    payload = {
        'query': init_data
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['token']['access']
    except requests.exceptions.RequestException as error:
        print(f'Error during authentication: {error}')
        raise

def play(auth_token):
    url = 'https://game-domain.blum.codes/api/v1/game/play'
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
        'authorization': f'Bearer {auth_token}',
    }
    response = requests.post(url, headers=headers)
    return response

def claim(auth_token, game_id):
    url = 'https://game-domain.blum.codes/api/v1/game/claim'
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
        'authorization': f'Bearer {auth_token}',
    }
    json_data = {
        'gameId': game_id,
        'points': 200,
    }
    response = requests.post(url, headers=headers, json=json_data)
    return response

def process_init_data(init_data):
    while True:
        try:
            
            auth_token = authenticate(init_data)
            play_response = play(auth_token)
            game_id = play_response.json().get("gameId")
            
            if game_id:
                print('berhasil di :',init_data)
                print(f"Game ID: {game_id}")
                time.sleep(30)
                claim_response = claim(auth_token, game_id)
                print(claim_response)
            else:
                print('error di : ',init_data)
                print("Failed to get game ID")
                break
        
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def main():
    with open('initdata.txt', 'r') as file:
        init_data_list = [line.strip() for line in file]

    threads = []
    for init_data in init_data_list:
        thread = threading.Thread(target=process_init_data, args=(init_data,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()