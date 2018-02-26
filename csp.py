import os
import sys
from collections import deque

def GAC():
    q = deque(range(0, n))
    while len(q) > 0:
        i = q.popleft()
        for c in constraints:
            cVariables = c[0]
            if i in cVariables:
                iIndex = cVariables.index(i)
                newIDomain = []
                count = 0
                for d in c:
                    if count != 0:
                        newIDomain.append(d[iIndex])
                    count += 1
                domains[i] = list(set(domains[i]).intersection(set(newIDomain)))

def checkDomains():
    for d in domains:
        if len(d) == 0:
            return 0
    return 1

def checkCoinstr(x, value, constrs):
    cok = 0
    for c in constrs:
        if x in c[0]:
            iIndex = c[0].index(x)
            count = 0
            for d in c:
                if count != 0:
                    #print "iindex:", iIndex, "d[iindex]:", d[iIndex], "value:", value
                    if d[iIndex] == value:
                        cok += 1
                        break
                count += 1
        else:
            cok += 1
    #print "cok:", cok, " m:", m, "val:", value
    if cok == m:
        return 1
    else:
        return 0

def newConstr(constrs, x, v):
    resultConstr = []
    tempList = []
    for c in constrs:
        if x in c[0]:
            iIndex = c[0].index(x)
            count = 0
            tempList.append(c[0])
            for d in c:
                if count != 0:
                    if d[iIndex] == v:
                        tempList.append(d)
                count += 1
            resultConstr.append(tempList)
            tempList = []
        else:
            resultConstr.append(c)
    return resultConstr

def choose(vall):
    imini = -1
    mini = 2000001
    for i in range(0, len(vall)):
        if vall[i] == -1:
            if len(domains[i]) < mini:
                mini = len(domains[i])
                imini = i
    return imini

def dfs(x, val, constr2):
    val2 = list(val)
    temp = domains[x]
    for v in temp:
        t = checkCoinstr(x, v, constr2)
        if t == 1:
            val2[x] = v
            el = choose(val2)
            if el == -1:
                return 1
            constr3 = newConstr(constr2, x, v)
            result = dfs(el, val2, constr3)
            if result == 1:
                return 1
            else:
                continue
        else:
            continue
    return 0

def solve():
    t = checkDomains()
    if t == 0:
        print('0')
    else:
        val = [-1]*n
        el = choose(val)
        result = dfs(el, val, constraints)
        if result == 1:
            print ('1')
        else:
            print('0')

#Prepare
n = 0
m = 0
domains = []
constraints = []
l = []
fd = open(sys.argv[1], "r")
lines = fd.readlines()
counter = 0
for line in lines:
    if counter == 0:
        n = int(line)
    elif counter == 1:
        d = line.split()
        dd = []
        for x in d:
            dd.append(int(x))
        for i in range (0, n):
            domains.append(list(dd))
    else:
        if line in ['\n', '\r\n']:
            constraints.append(list(l))
            l[:] = []
        else:
            ll = line.split()
            lll = []
            for x in ll:
                lll.append(int(x))
            l.append(list(lll))
    counter += 1
constraints.append(l)
m += 1
constraints2 = []
for con in constraints:
    if con != []:
        constraints2.append(con)
constraints = constraints2
m = len(constraints)

if len(constraints[0]) == 0:
    print ('1')
else:
    GAC()
    solve()
