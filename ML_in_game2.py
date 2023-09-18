import math
import os
import pickle

sep = os.sep

with open(f'.{sep}model{sep}ML_in_game2.lr', 'rb') as f:
    model_lr = pickle.load(f)

def map_to_predict(a1, a2, time):
    gpm1 = (a1[2] * 0.6 - a1[0])  # gpm
    lpm1 = ((4 * a1[1] * 60 + 9 * gpm1) * 0.1)  # lpm
    apl1 = (a1[0] / lpm1)  # apl
    app1 = (a1[0] / a1[1] / 60)  # app
    lpp1 = (lpm1 / a1[1] / 60)  # lpp
    gpl1 = (gpm1 / lpm1)  # gpl


    gpm2 = (a2[2] * 0.6 - a2[0])  # gpm
    lpm2 = ((4 * a2[1] * 60 + 9 * gpm2) * 0.1)  # lpm
    apl2 = (a2[0] / lpm2)  # apl
    app2 = (a2[0] / a2[1] / 60)  # app
    lpp2 = (lpm2 / a2[1] / 60)  # lpp
    gpl2 = (gpm2 / lpm2)  # gpl

    return [[a1[0], a1[1], a1[2], gpm1, lpm1, apl1, app1, lpp1, gpl1, a2[0], a2[1], a2[2], gpm2, lpm2, apl2, app2, lpp2, gpl2, time]]







def glicko_to_tr(glicko):
    return 25000 / (1 + 10 ** (
            (1500 - glicko) * math.pi / math.sqrt(2500 * (64 * math.pi ** 2 + 147 * math.log(10, math.e) ** 2))))
def tr_to_glicko(tr):
    if tr >= 25000:
        return 10000
    if tr <= 0:
        return -10000
    return 1500-math.sqrt(2500 * (64 * math.pi ** 2 + 147 * math.log(10, math.e) ** 2))/math.pi*math.log10(25000/tr-1)

def predictTR(apm1, pps1, VS1, apm2, pps2, VS2, time):
    return glicko_to_tr(predictGlicko(apm1, pps1, VS1, apm2, pps2, VS2, time))


def predictGlicko(apm1, pps1, VS1, apm2, pps2, VS2, time):
    return (model_lr.predict(map_to_predict([apm1, pps1, VS1], [apm2, pps2, VS2], time))[0])