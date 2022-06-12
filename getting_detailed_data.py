import json
import requests
from pprint import pprint
import sys
import time
import pandas as pd

start_time = time.time()

client_id = '4bb7fae04b544121e40118e90470a1d4'

with open('list_of_ids.txt') as f:
    list_of_ids = f.read().splitlines()

def get_detailed_info(id):
    fields = 'id,title,main_picture,alternative_titles,start_date,end_date,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,genres,media_type,status,num_episodes,start_season,source,average_episode_duration,rating,studios,related_anime,related_manga,recommendations,statistics'
    url = f'https://api.myanimelist.net/v2/anime/{id}?fields={fields}'
    while True:
        response = requests.get(url, headers = {'X-MAL-CLIENT-ID': f'{client_id}'})
        if response.status_code != 200:
            print(f'Problem occured\nStatus code: {response.status_code}\nID: {id}\nTrying again', file=sys.stderr)
            time.sleep(0.1)
        else:
            data = response.json()
            break
    return data

list_of_animes = []

i = 0
error_occured = False

for id in list_of_ids:
    try:
        time.sleep(0.1)
        list_of_animes.append(get_detailed_info(id))
        i = i + 1
    except:
        print(f'Unexpected error occured at index: {i}, id: {id}\nSaving and exiting', file=sys.stderr)
        error_occured = True
        break

with open('anime_data.json', 'w') as outfile:
    json.dump(list_of_animes, outfile)

end_time = time.time()
elapsed_time = end_time - start_time

if error_occured is False:
    print(f'Completed without issues\nParsed animes: {i}', file=sys.stderr)

print(f'Elapsed time: {elapsed_time} s', file=sys.stderr)