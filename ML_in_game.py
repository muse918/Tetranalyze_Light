import math
import os
import pickle

sep = os.sep

with open(f'.{sep}model{sep}ML_in_game.lr', 'rb') as f:
    model_lr = pickle.load(f)

def map_to_predict(a, time):
    gpm = (a[2] * 0.6 - a[0])  # gpm
    lpm = ((4 * a[1] * 60 + 9 * gpm) * 0.1)  # lpm
    apl = (a[0] / lpm)  # apl
    app = (a[0] / a[1] / 60)  # app
    lpp = (lpm / a[1] / 60)  # lpp
    gpl = (gpm / lpm)  # gpl

    return [[a[0], a[1], a[2], gpm, lpm, apl, app, lpp, gpl, time]]







def glicko_to_tr(glicko):
    return 25000 / (1 + 10 ** (
            (1500 - glicko) * math.pi / math.sqrt(2500 * (64 * math.pi ** 2 + 147 * math.log(10, math.e) ** 2))))
def tr_to_glicko(tr):
    if tr >= 25000:
        return 10000
    if tr <= 0:
        return -10000
    return 1500-math.sqrt(2500 * (64 * math.pi ** 2 + 147 * math.log(10, math.e) ** 2))/math.pi*math.log10(25000/tr-1)

def predictTR(apm, pps, VS, time):
    return glicko_to_tr(predictGlicko(apm, pps, VS, time))


def predictGlicko(apm, pps, VS, time):
    return (model_lr.predict(map_to_predict([apm, pps, VS], time))[0])