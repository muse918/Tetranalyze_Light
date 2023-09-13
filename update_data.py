import traceback

import pandas as pd
import time
import requests
import os

sep = os.sep

collect_data = True


def update():
    while True:
        try:
            response = requests.get('https://ch.tetr.io/api/users/lists/league/all')
            response.json()
            break
        except Exception as e:
            # print(traceback.format_exc())
            print('err')
    df = pd.DataFrame(response.json()['data']['users'])['league']
    df = df.apply(lambda x: pd.Series(x.values(), index=x.keys()))
    df.to_csv(f'.{sep}tetrlog{sep}last.csv')

    if collect_data:
        t = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        df.to_csv(f'.{sep}tetrlogs{sep}{t}_tetr.csv')
        print('success to make log at', t)

        if os.path.isfile(f'.{sep}tetrlogs{sep}sum.csv'):
            csvsum = pd.read_csv(f'.{sep}tetrlogs{sep}sum.csv')
        else:
            csvsum = pd.DataFrame(
                columns=['gamesplayed', 'gameswon', 'rating', 'glicko', 'rd', 'rank', 'bestrank', 'apm', 'pps', 'vs',
                         'decaying'])

        df_m = pd.read_csv(f'.{sep}tetrlogs{sep}' + t + '_tetr.csv').drop(labels='Unnamed: 0', axis=1)
        csvsum = pd.concat([csvsum, df_m])
        csvsum = csvsum.drop(labels='Unnamed: 0', axis=1).drop_duplicates()
        csvsum.to_csv(f'.{sep}tetrlogs{sep}sum.csv')

    print('success')
