from pandas import ExcelWriter
import pandas as pd
import numpy as np
import math

df = pd.read_excel('restoran.xlsx')

ids = np.array(df)
ids = ids[:, [0]]

makanan = np.array(df)
makanan = makanan[:, [0, 2]]

pelayanan = np.array(df)
pelayanan = pelayanan[:, [0, 1]]


def clasificate(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        if x == b:
            return 1
        return (x - a) / (b - a)
    elif b < x <= c:
        if c == x:
            return 1
        return (c - x) / (c - b)
    else:
        return 0


valueMakanan = {}
valuePelayanan = {}

for nilai in pelayanan:
    id = nilai[0]
    poin = nilai[1]

    valuePelayanan[id] = {}

    print("NILAI:",  poin, " ID:", id)

    stp = clasificate(poin, 0, 1, 25)
    print("Sangat tidak puas:", stp)
    valuePelayanan[id]['stp'] = stp

    tp = clasificate(poin, 20, 32.5, 45)
    print("tidak puas:", tp)
    valuePelayanan[id]['tp'] = tp

    cp = clasificate(poin, 40, 52.5, 65)
    print("cukup puas:", cp)
    valuePelayanan[id]['cp'] = cp

    p = clasificate(poin, 60, 72.5, 85)
    print("puas:", p)
    valuePelayanan[id]['p'] = p

    sp = clasificate(poin, 80,  100, 101)
    print("Sangat puas:", sp)
    valuePelayanan[id]['sp'] = sp

    print("---------------")

for nilai in makanan:
    id = nilai[0]
    poin = nilai[1]

    valueMakanan[id] = {}

    print("NILAI:",  poin, " ID:", id)

    ste = clasificate(poin, 0, 1, 3)
    print("Sangat tidak enak:", ste)
    valueMakanan[id]['ste'] = ste

    te = clasificate(poin, 2, 3.5, 5)
    print("tidak enak:", te)
    valueMakanan[id]['te'] = te

    ce = clasificate(poin, 4, 5.5, 7)
    print("cukup enak:", ce)
    valueMakanan[id]['ce'] = ce

    e = clasificate(poin, 6, 7.5, 9)
    print("enak:", e)
    valueMakanan[id]['e'] = e

    se = clasificate(poin, 8,  10, 11)
    print("Sangat enak:", se)
    valueMakanan[id]['se'] = se

    print("---------------")


inferenced = []


def inferenceBuruk(makanan, pelayanan, id):
    if makanan != 0 and pelayanan != 0:
        inferenced.append((id, [min(makanan, pelayanan), 12.5]))


def inferenceStandar(makanan, pelayanan, id):
    if makanan != 0 and pelayanan != 0:
        inferenced.append((id, [min(makanan, pelayanan), 50]))


def inferenceTerbaik(makanan, pelayanan, id):
    if makanan != 0 and pelayanan != 0:
        inferenced.append((id, [min(makanan, pelayanan), 87.5]))


for i in ids:
    id = i[0]
    inferenceBuruk(valueMakanan[id]['ste'], valuePelayanan[id]['stp'], id)
    inferenceBuruk(valueMakanan[id]['ste'], valuePelayanan[id]['tp'], id)
    inferenceBuruk(valueMakanan[id]['ste'], valuePelayanan[id]['cp'], id)
    inferenceBuruk(valueMakanan[id]['ste'], valuePelayanan[id]['p'], id)
    inferenceBuruk(valueMakanan[id]['ste'], valuePelayanan[id]['cp'], id)
    inferenceBuruk(valueMakanan[id]['te'], valuePelayanan[id]['stp'], id)
    inferenceBuruk(valueMakanan[id]['te'], valuePelayanan[id]['tp'], id)
    inferenceBuruk(valueMakanan[id]['te'], valuePelayanan[id]['cp'], id)

    inferenceStandar(valueMakanan[id]['ce'], valuePelayanan[id]['stp'], id)
    inferenceStandar(valueMakanan[id]['ce'], valuePelayanan[id]['tp'], id)
    inferenceStandar(valueMakanan[id]['ce'], valuePelayanan[id]['cp'], id)
    inferenceStandar(valueMakanan[id]['ce'], valuePelayanan[id]['p'], id)
    inferenceStandar(valueMakanan[id]['e'], valuePelayanan[id]['stp'], id)
    inferenceStandar(valueMakanan[id]['e'], valuePelayanan[id]['tp'], id)
    inferenceStandar(valueMakanan[id]['e'], valuePelayanan[id]['cp'], id)
    inferenceStandar(valueMakanan[id]['se'], valuePelayanan[id]['stp'], id)
    inferenceStandar(valueMakanan[id]['se'], valuePelayanan[id]['tp'], id)
    inferenceStandar(valueMakanan[id]['te'], valuePelayanan[id]['p'], id)
    inferenceStandar(valueMakanan[id]['te'], valuePelayanan[id]['sp'], id)

    inferenceTerbaik(valueMakanan[id]['se'], valuePelayanan[id]['cp'], id)
    inferenceTerbaik(valueMakanan[id]['se'], valuePelayanan[id]['p'], id)
    inferenceTerbaik(valueMakanan[id]['se'], valuePelayanan[id]['sp'], id)
    inferenceTerbaik(valueMakanan[id]['e'], valuePelayanan[id]['p'], id)
    inferenceTerbaik(valueMakanan[id]['e'], valuePelayanan[id]['sp'], id)
    inferenceTerbaik(valueMakanan[id]['ce'], valuePelayanan[id]['sp'], id)

defuzzied = []
totalKali = 0.0
totalBagi = 0.0

for i in ids:
    id = i[0]
    for inf in inferenced:
        if id == inf[0]:
            kali = inf[1][0]*inf[1][1]
            totalKali += kali
            totalBagi += inf[1][0]
    if totalKali == 0 or totalBagi == 0:
        defuzzied.append([id, 0])
    else:
        defuzzied.append([id, totalKali/totalBagi])
    totalKali = 0
    totalBagi = 0
dfDeffuzied = pd.DataFrame(defuzzied, columns=['ID', 'VALUE'])


defuzzied.sort(key=lambda x: x[1], reverse=True)
dfResult = pd.DataFrame(defuzzied, columns=['ID', 'POIN'])
dfResult = dfResult.head(10)
dfResult


dfResult
dfResult.to_excel("result.xls")
