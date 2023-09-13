import pickle

import requests
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import scipy
import json

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
import math
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
import os

sep = os.sep


with open(f'.{sep}model{sep}ML.lr', 'rb') as f:
    model_lr = pickle.load(f)

print('ML Loaded')
def map_to_predict(a):
    a.append(a[2] * 0.6 - a[0])  # gpm
    a.append((4 * a[1] * 60 + 9 * a[3]) * 0.1)  # lpm
    a.append(a[0] / a[4])  # apl
    a.append(a[0] / a[1] / 60)  # app
    a.append(a[4] / a[1] / 60)  # lpp
    a.append(a[3] / a[4])  # gpl

    return [a]








def glicko_to_tr(glicko):
    return 25000 / (1 + 10 ** (
            (1500 - glicko) * math.pi / math.sqrt(2500 * (64 * math.pi ** 2 + 147 * math.log(10, math.e) ** 2))))
def tr_to_glicko(tr):
    if tr >= 25000:
        return 10000
    if tr <= 0:
        return -10000
    return 1500-math.sqrt(2500 * (64 * math.pi ** 2 + 147 * math.log(10, math.e) ** 2))/math.pi*math.log10(25000/tr-1)

def predictTR(apm, pps, VS):
    return glicko_to_tr(model_lr.predict(map_to_predict([apm, pps, VS]))[0])


def predictGlicko(apm, pps, VS):
    return (model_lr.predict(map_to_predict([apm, pps, VS]))[0])


def predictPlayer(user):
    responsePlayer = requests.get('https://ch.tetr.io/api/users/' + user).json()
    if not responsePlayer['success']:
        return None
    player = responsePlayer['data']['user']['league']
    return predictTR(player['apm'], player['pps'], player['vs'])

def playerInfo(user):
    responsePlayer = requests.get('https://ch.tetr.io/api/users/' + user).json()
    if not responsePlayer['success']:
        return None
    player = responsePlayer['data']['user']['league']
    return player


def playerInfoFull(user):
    responsePlayer = requests.get('https://ch.tetr.io/api/users/' + user).json()
    if not responsePlayer['success']:
        return None
    player = responsePlayer['data']['user']
    return player


def playerId(username):
    responsePlayer = requests.get('https://ch.tetr.io/api/users/' + username).json()
    if not responsePlayer['success']:
        return None
    player = responsePlayer['data']['user']['_id']
    return player

def getDiscordPlayerName(id):
    responsePlayer = requests.get('https://ch.tetr.io/api/users/search/' + id).json()
    if responsePlayer['success']:
        if responsePlayer['data'] == None:
            return None
        return responsePlayer['data']['user']['username']
    else:
        return None

def getDiscordPlayerId(id):
    responsePlayer = requests.get('https://ch.tetr.io/api/users/search/' + str(id)).json()
    if responsePlayer['success']:
        if responsePlayer['data'] == None:
            return None
        return responsePlayer['data']['user']['_id']
    else:
        return None

def getLatestMatch(playerId):
    responseReplays = requests.get('https://ch.tetr.io/api/streams/league_userrecent_' + playerId).json()

    if responseReplays['success']:
        if len(dict(responseReplays['data'])['records']) != 0:
            responseReplays = responseReplays['data']['records'][0]
            replayId = responseReplays['replayid']
            name1 = responseReplays['endcontext'][0]['user']['username']
            apm1 = responseReplays['endcontext'][0]['points']['secondary']
            pps1 = responseReplays['endcontext'][0]['points']['tertiary']
            vs1 = responseReplays['endcontext'][0]['points']['extra']['vs']
            wins1 = responseReplays['endcontext'][0]['wins']
            name2 = responseReplays['endcontext'][1]['user']['username']
            apm2 = responseReplays['endcontext'][1]['points']['secondary']
            pps2 = responseReplays['endcontext'][1]['points']['tertiary']
            vs2 = responseReplays['endcontext'][1]['points']['extra']['vs']
            wins2 = responseReplays['endcontext'][1]['wins']
            return (replayId, ((name1, wins1, apm1, pps1, vs1), (name2, wins2, apm2, pps2, vs2)))
        else:
            return None
    else:
        return None

def getFullLatestMatch(playerId):
    responseReplays = requests.get('https://ch.tetr.io/api/streams/league_userrecent_' + playerId).json()

    if responseReplays['success']:
        if len(dict(responseReplays['data'])['records']) != 0:
            responseReplays = getFullMatchId(responseReplays['data']['records'][0]['replayid'])
            return responseReplays
        else:
            return None
    else:
        return None

def getMatchId(matchId):
    try:
        responseReplays = requests.get('https://inoue.szy.lol/api/replay/' + matchId).json()
    except:
        return None

    if type(responseReplays['endcontext']) == list:
        replayId = matchId
        name1 = responseReplays['endcontext'][0]['user']['username']
        apm1 = responseReplays['endcontext'][0]['points']['secondary']
        pps1 = responseReplays['endcontext'][0]['points']['tertiary']
        vs1 = responseReplays['endcontext'][0]['points']['extra']['vs']
        wins1 = responseReplays['endcontext'][0]['wins']
        name2 = responseReplays['endcontext'][1]['user']['username']
        apm2 = responseReplays['endcontext'][1]['points']['secondary']
        pps2 = responseReplays['endcontext'][1]['points']['tertiary']
        vs2 = responseReplays['endcontext'][1]['points']['extra']['vs']
        wins2 = responseReplays['endcontext'][1]['wins']
        return (replayId, ((name1, wins1, apm1, pps1, vs1), (name2, wins2, apm2, pps2, vs2)))
    else:
        return None


def getFullMatchId(matchId):
    try:
        responseReplays = requests.get('https://inoue.szy.lol/api/replay/' + matchId).json()
    except:
        return None

    if type(responseReplays['endcontext']) == list:
        return responseReplays
    else:
        return None

