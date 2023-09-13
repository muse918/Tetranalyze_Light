import requests

response = requests.get('https://ch.tetr.io/api/streams/40l_global')
sprintdata = response.json()['data']['records']
sprintdataname = []
for i in sprintdata:
    sprintdataname.append(i['user']['username'])


response = requests.get('https://ch.tetr.io/api/streams/blitz_global')
blitzdata = response.json()['data']['records']
blitzdataname = []
for i in sprintdata:
    blitzdataname.append(i['user']['username'])

response = requests.get('https://ch.tetr.io/api/users/lists/league/all')
users = response.json()['data']['users']
user_country_dict = dict()
for i in users:
    user_country_dict[i['username']] = i['country']
print('Country_Rank Loaded')
def sprint(username:str):
    rank = 0
    try:
        country = user_country_dict[username]
    except:
        user = requests.get(f'https://ch.tetr.io/api/users/{username.lower()}').json()
        if not user['success']:
            return None
        country = user['data']['user']['country']
    if country is None:
        return -1
    if username not in sprintdataname:
        return -2

    for i in sprintdataname:
        try:
            if user_country_dict[i] == country:
                rank += 1
        except:
            if requests.get(f'https://ch.tetr.io/api/users/{i}').json()['data']['user']['country'] == country:
                rank += 1
        if i == username.lower():
            break
    return rank, country

def blitz(username:str):
    rank = 0
    try:
        country = user_country_dict[username]
    except:
        user = requests.get(f'https://ch.tetr.io/api/users/{username.lower()}').json()
        if not user['success']:
            return None
        country = user['data']['user']['country']
    if country is None:
        return -1
    if username not in blitzdataname:
        return -2
    for i in blitzdataname:
        try:
            if user_country_dict[i] == country:
                rank += 1
        except:
            if requests.get(f'https://ch.tetr.io/api/users/{i}').json()['data']['user']['country'] == country:
                rank += 1
        if i == username.lower():
            break
    return rank, country

def update():
    response = requests.get('https://ch.tetr.io/api/streams/40l_global')
    sprintdata = response.json()['data']['records']
    global sprintdataname
    sprintdataname = []
    for i in sprintdata:
        sprintdataname.append(i['user']['username'])


    response = requests.get('https://ch.tetr.io/api/streams/blitz_global')
    blitzdata = response.json()['data']['records']
    global blitzdataname
    blitzdataname = []
    for i in blitzdata:
        blitzdataname.append(i['user']['username'])

    response = requests.get('https://ch.tetr.io/api/users/lists/league/all')
    users = response.json()['data']['users']
    user_country_dict = dict()
    for i in users:
        user_country_dict[i['username']] = i['country']
    print('country_loaded')