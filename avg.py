import pandas as pd

import os

sep = os.sep

df2 = pd.read_csv(f'.{sep}tetrlog{sep}last.csv')

data = df2.drop(labels='Unnamed: 0', axis=1)
gpm = data.apply(lambda x: x['vs'] * 0.6 - x['apm'], axis=1)
gpm.name = 'gpm'
data = data.join(gpm)
lpm = data.apply(lambda x: (4 * x['pps'] * 60 + 9 * x['gpm']) * 0.1, axis=1)
lpm.name = 'lpm'
data = data.join(lpm)
apl = data.apply(lambda x: x['apm'] / x['lpm'], axis=1)
apl.name = 'apl'
data = data.join(apl)
app = data.apply(lambda x: x['apm'] / x['pps'] / 60, axis=1)
app.name = 'app'
data = data.join(app)
lpp = data.apply(lambda x: x['lpm'] / x['pps'] / 60, axis=1)
lpp.name = 'lpp'
data = data.join(lpp)
gpl = data.apply(lambda x: x['gpm'] / x['lpm'], axis=1)
gpl.name = 'gpl'
data = data.join(gpl)

print('Avg Loaded')

def avg_range_TR(start, end):
    if end < start:
        return f'범위가 존재하지 않습니다. ({start:.2f} < {end:.2f})'
    mask = (start <= data.rating) & (data.rating <= end)
    df3 = data.loc[mask, :]
    df3 = df3[['apm', 'pps', 'vs', 'gpm', 'lpm', 'apl', 'app', 'lpp', 'gpl']]
    df4 = df3.mean(axis=0)
    all_player = len(data)
    range_player = len(df3)
    if range_player == 0:
        return '플레이어가 존재하지 않습니다.'
    ret = f'TR 범위 : {start:.2f} - {end:.2f}\n'
    ret += f'플레이어 수 : {range_player} ({(range_player / all_player)*100:.2f}%)\n'
    ret += '\n=====평균=====\n\n'

    for i, j in zip(['apm', 'pps', 'vs', 'gpm', 'lpm', 'apl', 'app', 'lpp', 'gpl'], df4):
        ret += f'{i} : {j:.2f}\n'
    return ret


def avg_range_Glicko(start, end):
    if end < start:
        return f'범위가 존재하지 않습니다. ({start:.2f} < {end:.2f})'
    mask = (start <= data.glicko) & (data.glicko <= end)
    df3 = data.loc[mask, :]
    df3 = df3[['apm', 'pps', 'vs', 'gpm', 'lpm', 'apl', 'app', 'lpp', 'gpl']]
    df4 = df3.mean(axis=0)
    all_player = len(data)
    range_player = len(df3)
    if range_player == 0:
        return '플레이어가 존재하지 않습니다.'
    ret = f'Glicko 범위 : {start:.2f} - {end:.2f}\n'
    ret += f'플레이어 수 : {range_player} ({(range_player / all_player)*100:.2f}%)\n'
    ret += '\n=====평균=====\n\n'

    for i, j in zip(['apm', 'pps', 'vs', 'gpm', 'lpm', 'apl', 'app', 'lpp', 'gpl'], df4):
        ret += f'{i} : {j:.2f}\n'
    return ret


def avg_rank(rank):
    if rank.lower() == 'z':
        return 'Z랭크는 분석할 수 없습니다.'
    if rank.lower() not in ['d', 'd+', 'c-', 'c', 'c+', 'b-', 'b', 'b+', 'a-', 'a', 'a+', 's-', 's', 's', 's+', 'ss',
                            'u', 'x']:
        return '유효하지 않은 랭크'
    mask = (data['rank'] == rank.lower())
    df3 = data.loc[mask, :]

    min_rate = df3['rating'].min()
    max_rate = df3['rating'].max()
    all_player = len(data)
    rank_player = len(df3)

    min_glicko = df3['glicko'].min()
    max_glicko = df3['glicko'].max()

    df3 = df3[['apm', 'pps', 'vs', 'gpm', 'lpm', 'apl', 'app', 'lpp', 'gpl']]
    df4 = df3.mean(axis=0)
    ret = f'랭크 : {rank.upper()}\n'
    ret += f'플레이어 수 : {rank_player} ({(rank_player / all_player)*100:.2f}%)\n'
    ret += f'TR 범위 : {min_rate:.2f} - {max_rate:.2f}\n'
    ret += f'Glicko 범위 : {min_glicko:.2f} - {max_glicko:.2f}\n'

    ret += '=====평균=====\n'

    for i, j in zip(['apm', 'pps', 'vs', 'gpm', 'lpm', 'apl', 'app', 'lpp', 'gpl'], df4):
        ret += i + ' : ' + str(round(j, 2)) + '\n'
    return ret


def update():
    global df2
    global data
    df2 = pd.read_csv(f'.{sep}tetrlog{sep}last.csv')

    data = df2.drop(labels='Unnamed: 0', axis=1)
    gpm = data.apply(lambda x: x['vs'] * 0.6 - x['apm'], axis=1)
    gpm.name = 'gpm'
    data = data.join(gpm)
    lpm = data.apply(lambda x: (4 * x['pps'] * 60 + 9 * x['gpm']) * 0.1, axis=1)
    lpm.name = 'lpm'
    data = data.join(lpm)
    apl = data.apply(lambda x: x['apm'] / x['lpm'], axis=1)
    apl.name = 'apl'
    data = data.join(apl)
    app = data.apply(lambda x: x['apm'] / x['pps'] / 60, axis=1)
    app.name = 'app'
    data = data.join(app)
    lpp = data.apply(lambda x: x['lpm'] / x['pps'] / 60, axis=1)
    lpp.name = 'lpp'
    data = data.join(lpp)
    gpl = data.apply(lambda x: x['gpm'] / x['lpm'], axis=1)
    gpl.name = 'gpl'
    data = data.join(gpl)
