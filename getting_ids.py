import json
import requests
from pprint import pprint
import sys
import time
import pandas as pd

client_id = '4bb7fae04b544121e40118e90470a1d4'

def get_detailed_info(id):
    fields = 'id,title,main_picture,alternative_titles,start_date,end_date,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,genres,media_type,status,num_episodes,start_season,source,average_episode_duration,rating,studios,related_anime,related_manga,recommendations,statistics'
    # fields = 'id,title,related_anime,related_manga'
    url = f'https://api.myanimelist.net/v2/anime/{id}?fields={fields}'
    response = requests.get(url, headers = {'X-MAL-CLIENT-ID': f'{client_id}'})
    if response.status_code != 200:
        print(f'Problem occured\nStatus code: {response.status_code}', file=sys.stderr)
        return
    return response.json()

def get_ranking_list_ids():
    fields = 'id,title'
    url = f'https://api.myanimelist.net/v2/anime/ranking?ranking_type=all&limit=500&offset=0&fields={fields}'
    list_of_ids = []
    while True:
        response = requests.get(url, headers = {'X-MAL-CLIENT-ID': f'{client_id}'})
        if response.status_code != 200:
            print(f'Problem occured\nStatus code: {response.status_code}\nTrying again', file=sys.stderr)
            time.sleep(0.1)
        else:
            data = response.json()
            for anime in data['data']:
                list_of_ids.append(anime['node']['id'])
            try:
                url = data['paging']['next']
            except:
                print(f'Reached the end', file=sys.stderr)
                break
            time.sleep(0.1)
    return list_of_ids


list_of_ids = get_ranking_list_ids()
pprint(len(list_of_ids))

with open('list_of_ids.txt', 'w') as outfile:
    outfile.write('\n'.join(str(v) for v in list_of_ids))
    # pprint(list_of_ids, outfile)

# for anime in top_anime['data']:
#     list_of_ids.append(anime['node']['id'])

# pprint(list_of_ids)

# detailed_data = []
# for id in list_of_ids:
#     anime_detailed_info = get_detailed_info(id)
#     detailed_data.append(anime_detailed_info)

# with open('data.json', 'w') as outfile:
#     json.dump(detailed_data, outfile)