import pickle

import pandas as pd

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
import os

sep = os.sep

df2 = pd.read_csv(f'.{sep}in-game{sep}igrf2.csv')
df2 = df2.sample(frac=1, random_state=918)

data = df2[['apm1', 'pps1', 'vs1', 'apm2', 'pps2', 'vs2', 'time', 'glicko']]
gpm1 = data.apply(lambda x: x['vs1'] * 0.6 - x['apm1'], axis=1)
gpm1.name = 'gpm1'
data = data.join(gpm1)
lpm1 = data.apply(lambda x: +(4 * x['pps1'] * 60 + 9 * x['gpm1']) * 0.1, axis=1)
lpm1.name = 'lpm1'
data = data.join(lpm1)
apl1 = data.apply(lambda x: 0 if x['lpm1'] == 0 else (x['apm1'] / x['lpm1']), axis=1)
apl1.name = 'apl1'
data = data.join(apl1)
app1 = data.apply(lambda x: 0 if x['pps1'] == 0 else (x['apm1'] / x['pps1']) / 60, axis=1)
app1.name = 'app1'
data = data.join(app1)
lpp1 = data.apply(lambda x: 0 if x['pps1'] == 0 else (x['lpm1'] / x['pps1']) / 60, axis=1)
lpp1.name = 'lpp1'
data = data.join(lpp1)
gpl1 = data.apply(lambda x: 0 if x['lpm1'] == 0 else (x['gpm1'] / x['lpm1']), axis=1)
gpl1.name = 'gpl1'
data = data.join(gpl1)




gpm2 = data.apply(lambda x: x['vs2'] * 0.6 - x['apm2'], axis=1)
gpm2.name = 'gpm2'
data = data.join(gpm2)
lpm2 = data.apply(lambda x: +(4 * x['pps2'] * 60 + 9 * x['gpm2']) * 0.1, axis=1)
lpm2.name = 'lpm2'
data = data.join(lpm2)
apl2 = data.apply(lambda x: 0 if x['lpm2'] == 0 else (x['apm2'] / x['lpm2']), axis=1)
apl2.name = 'apl2'
data = data.join(apl2)
app2 = data.apply(lambda x: 0 if x['pps2'] == 0 else (x['apm2'] / x['pps2']) / 60, axis=1)
app2.name = 'app2'
data = data.join(app2)
lpp2 = data.apply(lambda x: 0 if x['pps2'] == 0 else (x['lpm2'] / x['pps2']) / 60, axis=1)
lpp2.name = 'lpp2'
data = data.join(lpp2)
gpl2 = data.apply(lambda x: 0 if x['lpm2'] == 0 else (x['gpm2'] / x['lpm2']), axis=1)
gpl2.name = 'gpl2'
data = data.join(gpl2)

data = data.dropna()

target = data['glicko']

data = data[['apm1', 'pps1', 'vs1', 'gpm1', 'lpm1', 'apl1', 'app1', 'lpp1', 'gpl1', 'apm2', 'pps2', 'vs2', 'gpm2', 'lpm2', 'apl2', 'app2', 'lpp2', 'gpl2', 'time']]

# print(data)
#
# print(target)


data_train, data_test, target_train, target_test = train_test_split(data, target, random_state=918)


lr = Ridge(alpha=0.0001)
poly = PolynomialFeatures(degree=3)
scaler = StandardScaler()
model_lr = Pipeline([('scaler', scaler), ('poly', poly),
                         ('lr', lr)])

model_lr.fit(data_train, target_train)


with open(f'.{sep}model{sep}ML_in_game2.lr', 'wb') as f:
    pickle.dump(model_lr, f)