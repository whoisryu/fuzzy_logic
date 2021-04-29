import pandas as pd
import numpy as np
import math

df = pd.read_excel(
    'https://raw.githubusercontent.com/whoisryu/Fuzzy_Logic/master/restoran.xlsx')
df.head()

ids = np.array(df)
ids = ids[:, [0]]
idDf = pd.DataFrame(ids)
idDf.head()

makanan = np.array(df)
makanan = makanan[:, [0, 2]]
makananDf = pd.DataFrame(makanan)
makananDf.head()

pelayanan = np.array(df)
pelayanan = pelayanan[:, [0, 1]]
pelayananDf = pd.DataFrame(pelayanan)
pelayananDf.head()


def clasificate(x, a, b, c):
    if a <= x <= b:
        nilai = (x - a) / (b - a)
        return nilai
    elif b <= x <= c:
        if b == x:
            nilai = 1
            return nilai
        nilai = (c - x) / (c - b)
        return nilai
    else:
        nilai = 0
        return nilai


valueMakanan = {}
valuePelayanan = {}


for nilai in pelayanan:
    id = nilai[0]
    poin = nilai[1]

    valuePelayanan[id] = {}

    print("POIN: ",  poin)

    stp = clasificate(poin, 0, 12.5, 25)
    print("Sangat tidak puas:", stp)
    valuePelayanan[id][0] = stp

    tp = clasificate(poin, 20, 32.5, 45)
    print("tidak puas:", tp)
    valuePelayanan[id][1] = tp

    cp = clasificate(poin, 40, 52.5, 65)
    print("cukup puas:", cp)
    valuePelayanan[id][2] = cp

    p = clasificate(poin, 60, 72.5, 85)
    print("puas:", p)
    valuePelayanan[id][3] = p

    sp = clasificate(poin, 80,  92.5, 100)
    print("Sangat puas:", sp)
    valuePelayanan[id][4] = sp

    print("---------------")

for nilai in makanan:
    id = nilai[0]
    poin = nilai[1]

    valueMakanan[id] = {}

    print("NILAI: ",  poin)

    ste = clasificate(poin, 0, 1.5, 3)
    print("Sangat tidak enak:", ste)
    valueMakanan[id][0] = ste

    te = clasificate(poin, 2, 3.5, 5)
    print("tidak enak:", te)
    valueMakanan[id][1] = te

    ce = clasificate(poin, 4, 5.5, 7)
    print("cukup enak:", ce)
    valueMakanan[id][2] = ce

    e = clasificate(poin, 6, 7.5, 9)
    print("enak:", e)
    valueMakanan[id][3] = e

    se = clasificate(poin, 8,  9, 10)
    print("Sangat enak:", se)
    valueMakanan[id][4] = se

    print("---------------")

minValue = 0
tempList = []
rankList = []
for id in ids:
    for i in range(5):
        for j in range(5):
            minValue = min(valueMakanan[id[0]][i], valuePelayanan[id[0]][j])
            tempList.append(minValue)
    rankList.append((id[0], max(tempList)))


# take second element for sort
def takeSecond(elem):
    return elem[1]


rankList.sort(key=takeSecond, reverse=True)

dfResult = pd.DataFrame(rankList, columns=['ID', 'POIN'])
dfResult
