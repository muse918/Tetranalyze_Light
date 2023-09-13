import time

import requests

import os

import pandas as pd

sep = os.sep

if __name__ == '__main__':

    # player_id = 'muse918'
    # if os.path.isfile(f'.{sep}track{sep}{player_id}.csv'):
    #     player_csv = pd.read_csv(f'.{sep}track{sep}{player_id}.csv').tail(5)
    #     ans = ''
    #     for i in player_csv.index:
    #
    #         print(eval(player_csv.loc[i]['game'])['endcontext'][0]['user']['username'])
    #         print(eval(player_csv.loc[i]['playerinfo'])['rating'])
    #         print(eval(player_csv.loc[i]['game'])['endcontext'][0]['wins'])
    #         print(eval(player_csv.loc[i]['game'])['endcontext'][1]['wins'])
    #         print(eval(player_csv.loc[i]['game'])['endcontext'][1]['user']['username'])
    #         print(eval(player_csv.loc[i]['opponent'])['rating'])
    while True:
        track_id = pd.read_csv(f'.{sep}track_list.csv')['user'].tolist()
        for user in track_id:
            responsePlayer = requests.get('https://ch.tetr.io/api/users/' + user).json()
            if not responsePlayer['success']:
                continue
            player_id = responsePlayer['data']['user']['_id']
            player = responsePlayer['data']['user']['league']
            print(user)
            if os.path.isfile(f'.{sep}track{sep}{player_id}.csv'):
                player_csv = pd.read_csv(f'.{sep}track{sep}{player_id}.csv')
                player_log = player_csv['playerinfo'].tolist()
                last_log = eval(player_log[-1])
                if last_log['gamesplayed'] != player['gamesplayed']:
                    missed_game = player['gamesplayed'] - last_log['gamesplayed']
                    responseReplays = requests.get(
                        'https://ch.tetr.io/api/streams/league_userrecent_' + player_id).json()
                    if not responseReplays['success']:
                        continue
                    if len(dict(responseReplays['data'])['records']) < missed_game:
                        missed_game = len(dict(responseReplays['data'])['records'])
                    for i in range(missed_game):
                        game = dict(responseReplays['data'])['records'][missed_game - i - 1]
                        if game['endcontext'][0]['user']['_id'] != player_id:
                            game['endcontext'] = list(reversed(game['endcontext'][:]))
                        opponent_name = game['endcontext'][1]['user']['username']
                        opponent_response = requests.get('https://ch.tetr.io/api/users/' + opponent_name).json()
                        if not opponent_response['success']:
                            continue
                        opponent = opponent_response['data']['user']['league']
                        player_frame = pd.DataFrame({'playerinfo': [player], 'game': [game], 'opponent': [opponent]})
                        player_csv = pd.concat([player_csv, player_frame], ignore_index=True)
                player_csv = player_csv.loc[:, ~player_csv.columns.str.contains('^Unnamed')]
                player_csv.to_csv(f'.{sep}track{sep}{player_id}.csv')

            else:
                responseReplays = requests.get(
                    'https://ch.tetr.io/api/streams/league_userrecent_' + player_id).json()
                if not responseReplays['success']:
                    continue
                if len(dict(responseReplays['data'])['records']) == 0:
                    continue
                game = dict(responseReplays['data'])['records'][0]
                if game['endcontext'][0]['user']['_id'] != player_id:
                    game['endcontext'] = list(reversed(game['endcontext'][:]))
                opponent_name = game['endcontext'][1]['user']['username']
                opponent_response = requests.get('https://ch.tetr.io/api/users/' + opponent_name).json()
                if not opponent_response['success']:
                    continue
                opponent = opponent_response['data']['user']['league']
                player_frame = pd.DataFrame({'playerinfo': [player], 'game': [game], 'opponent': [opponent]})
                player_csv = player_frame
                player_csv = player_csv.loc[:, ~player_csv.columns.str.contains('^Unnamed')]
                player_csv.to_csv(f'.{sep}track{sep}{player_id}.csv')
        time.sleep(60)


def track(name):
    responsePlayer = requests.get('https://ch.tetr.io/api/users/' + name).json()
    if not responsePlayer['success']:
        return False
    player_id = responsePlayer['data']['user']['_id']
    track_id = pd.read_csv(f'.{sep}track_list.csv')['user'].tolist()
    if player_id in track_id:
        return False
    else:
        track_id.append(player_id)
        pd.DataFrame(track_id, columns=['user']).to_csv(f'.{sep}track_list.csv')
        return True


def list_track():
    track_id = pd.read_csv(f'.{sep}track_list.csv')['user'].tolist()
    userlist = []
    for i in track_id:
        responsePlayer = requests.get('https://ch.tetr.io/api/users/' + i).json()
        if not responsePlayer['success']:
            continue
        userlist.append(responsePlayer['data']['user']['username'])
    return userlist


def untrack(name):
    responsePlayer = requests.get('https://ch.tetr.io/api/users/' + name).json()
    if not responsePlayer['success']:
        return False
    player_id = responsePlayer['data']['user']['_id']
    track_id = pd.read_csv(f'.{sep}track_list.csv')['user'].tolist()
    if player_id in track_id:
        track_id.remove(player_id)
        pd.DataFrame(track_id, columns=['user']).to_csv(f'.{sep}track_list.csv')
        return True
    else:
        return False


def show(name, num):
    num = min(num, 10)
    responsePlayer = requests.get('https://ch.tetr.io/api/users/' + name).json()
    if not responsePlayer['success']:
        return None
    player_id = responsePlayer['data']['user']['_id']
    if os.path.isfile(f'.{sep}track{sep}{player_id}.csv'):
        player_csv = pd.read_csv(f'.{sep}track{sep}{player_id}.csv').tail(num)
        ans = ''
        for i in player_csv.index:
            u1_name = eval(player_csv.loc[i]['game'])['endcontext'][0]['user']['username']
            u2_name = eval(player_csv.loc[i]['game'])['endcontext'][1]['user']['username']
            u1_rating = eval(player_csv.loc[i]['playerinfo'])['rating']
            u2_rating = eval(player_csv.loc[i]['opponent'])['rating']
            u1_win = eval(player_csv.loc[i]['game'])['endcontext'][0]['wins']
            u2_win = eval(player_csv.loc[i]['game'])['endcontext'][1]['wins']
            ans += f'{u1_name} ({u1_rating:.2f}TR) VS {u2_name} ({u2_rating:.2f}TR)\n' \
                   f'{u1_win} : {u2_win}' + '\n\n'

            # muse918
            # 24314.292511047643
            # 7
            # 6
            # espergifts
            # 24558.345159543478
        return ans
    else:
        return None
