import os.path
import random
import traceback

import requests
import pandas as pd

import util

sep = os.sep

if os.path.isfile(f'.{sep}in-game{sep}igrf2.csv'):
    c = pd.read_csv(f'.{sep}in-game{sep}igrf2.csv', index_col=0)
else:
    c = pd.DataFrame(columns=['apm1', 'pps1', 'vs1', 'apm2', 'pps2', 'vs2', 'time', 'glicko'])
try:
    response = requests.get('https://ch.tetr.io/api/users/lists/league/all')
    response = response.json()
    if not response['success']:
        raise Exception
    userlist = list(map(lambda x:x['_id'], response['data']['users']))
    wglk = list(map(lambda x: 2.5**(x['league']['glicko']/1000), response['data']['users']))
    print(wglk)
    userlist = reversed(util.weighted_shuffle(userlist, wglk))
    # random.shuffle(userlist)
    x = 0
    for i in userlist:
        try:
            x+=1
            print(i)
            responseReplayID = requests.get('https://ch.tetr.io/api/streams/league_userrecent_' + i).json()
            if responseReplayID['success']:
                if len(dict(responseReplayID['data'])['records']) != 0:
                    responseReplayID = responseReplayID['data']['records'][0]
                else:
                    continue
            else:
                continue
            matchId = responseReplayID['replayid']
            while True:
                try:
                    responseReplay = requests.get('https://inoue.szy.lol/api/replay/' + matchId).json()
                    break
                except KeyboardInterrupt as e:
                    print(c)
                    print('Stop')
                    c.loc[:, ~c.columns.str.contains('^Unnamed')].to_csv(f'.{sep}in-game{sep}igrf2.csv')
                    print('saved')
                    print(e)
                except: pass
            responseUser = requests.get('https://ch.tetr.io/api/users/' + i).json()
            glk = responseUser['data']['user']['league']['glicko']

            t = list(map(lambda j: j['replays'][0]['frames'] / 60, responseReplay['data']))
            if responseReplay['endcontext'][0]['user']['_id'] == i:
                apm1 = responseReplay['endcontext'][0]['points']['secondaryAvgTracking']
                pps1 = responseReplay['endcontext'][0]['points']['tertiaryAvgTracking']
                vs1 = responseReplay['endcontext'][0]['points']['extraAvgTracking']['aggregatestats___vsscore']
                apm2 = responseReplay['endcontext'][1]['points']['secondaryAvgTracking']
                pps2 = responseReplay['endcontext'][1]['points']['tertiaryAvgTracking']
                vs2 = responseReplay['endcontext'][1]['points']['extraAvgTracking']['aggregatestats___vsscore']
            else:
                apm1 = responseReplay['endcontext'][1]['points']['secondaryAvgTracking']
                pps1 = responseReplay['endcontext'][1]['points']['tertiaryAvgTracking']
                vs1 = responseReplay['endcontext'][1]['points']['extraAvgTracking']['aggregatestats___vsscore']
                apm2 = responseReplay['endcontext'][0]['points']['secondaryAvgTracking']
                pps2 = responseReplay['endcontext'][0]['points']['tertiaryAvgTracking']
                vs2 = responseReplay['endcontext'][0]['points']['extraAvgTracking']['aggregatestats___vsscore']
            print(list(zip(apm1, pps1, vs1, apm2, pps2, vs2, t, [glk] * len(t))))
            c = pd.concat([c, pd.DataFrame(list(zip(apm1, pps1, vs1, apm2, pps2, vs2, t, [glk] * len(t))), columns=['apm1', 'pps1', 'vs1', 'apm2', 'pps2', 'vs2', 'time', 'glicko'])])
            if x%50 == 0:
                c.loc[:, ~c.columns.str.contains('^Unnamed')].to_csv(f'.{sep}in-game{sep}igrf2.csv')
                print('saved')
        except Exception as e:
            # print(c)
            # print('Error')
            print(e)
            print(traceback.format_exc())
except Exception as e:
    print(c)
    print('Error')
except KeyboardInterrupt as e:
    print(c)
    print('Stop')
    c.loc[:, ~c.columns.str.contains('^Unnamed')].to_csv(f'.{sep}in-game{sep}igrf2.csv')
    print('saved')
    print(e)
