import os
import time

import matplotlib.pyplot as plt

import ML
import ML_in_game
import ML_low

sep = os.sep
path = f'.{sep}temp'
def analyze(match:dict):
    t = list(map(lambda x: x['replays'][0]['frames'] / 60, match['data']))
    apm_1 = match['endcontext'][0]['points']['secondaryAvgTracking']
    pps_1 = match['endcontext'][0]['points']['tertiaryAvgTracking']
    vs_1 = match['endcontext'][0]['points']['extraAvgTracking']['aggregatestats___vsscore']
    apm_2 = match['endcontext'][1]['points']['secondaryAvgTracking']
    pps_2 = match['endcontext'][1]['points']['tertiaryAvgTracking']
    vs_2 = match['endcontext'][1]['points']['extraAvgTracking']['aggregatestats___vsscore']
    game = len(apm_1)
    glicko_1 = []
    glicko_2 = []
    user1 = ML.playerInfoFull(match['endcontext'][0]['user']['_id'])
    user2 = ML.playerInfoFull(match['endcontext'][1]['user']['_id'])
    for i in range(game):
        glicko_1.append(ML_in_game.predictGlicko(apm_1[i], pps_1[i], vs_1[i], t[i]))
        glicko_2.append(ML_in_game.predictGlicko(apm_2[i], pps_2[i], vs_2[i], t[i]))
    u1_glicko = user1['league']['glicko']
    u2_glicko = user2['league']['glicko']
    u1 = user1['username']
    u2 = user2['username']
    plt.cla()
    plt.plot(range(1, game+1), glicko_1, marker='o', label=u1, c='blue')
    plt.plot(range(1, game+1), glicko_2, marker='o', label=u2, c='red')
    plt.axhline(u1_glicko, color='blue', linestyle='--')
    plt.axhline(u2_glicko, color='red', linestyle='--')
    plt.legend()
    plt.xticks(range(1, game+1))
    plt.xlabel('Game')
    plt.ylabel('Glicko')
    plt.title(f'Tetra League: {u1} VS {u2}')

    # plt.yscale('log', base=10)
    t = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    figdir = f'{path}{sep}analyze_match_{t}.png'
    plt.savefig(figdir)
    return figdir


