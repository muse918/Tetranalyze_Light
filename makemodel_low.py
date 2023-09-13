import pickle

import pandas as pd

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
import os

sep = os.sep

df2 = pd.read_csv(f'.{sep}tetrlog{sep}sum.csv')
df2 = df2.sample(frac=1, random_state=918)

data = df2[['glicko', 'apm', 'pps', 'vs']]
gpm = data.apply(lambda x: x['vs'] * 0.6 - x['apm'], axis=1)
gpm.name = 'gpm'
data = data.join(gpm)
lpm = data.apply(lambda x: +(4 * x['pps'] * 60 + 9 * x['gpm']) * 0.1, axis=1)
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

data = data.dropna()

target = data['glicko']

# data = data[['apm', 'pps', 'vs', 'gpm', 'lpm', 'apl', 'app', 'lpp', 'gpl']]
data = data[['apm', 'pps', 'app']]
# data = data[['apm', 'pps', 'gpm', 'apl', 'app', 'gpl']]

data_train, data_test, target_train, target_test = train_test_split(data, target, random_state=918)


lr = Ridge(alpha=0.0001)
poly = PolynomialFeatures(degree=3)
scaler = StandardScaler()
model_lr = Pipeline([('scaler', scaler), ('poly', poly),
                         ('lr', lr)])

model_lr.fit(data_train, target_train)



with open(f'.{sep}model{sep}ML_low.lr', 'wb') as f:
    pickle.dump(model_lr, f)