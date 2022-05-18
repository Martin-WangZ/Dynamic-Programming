import matplotlib.pyplot as plt


Demand=[36, 27, 45, 24, 29, 24, 30, 35, 40, 46, 34, 31, 26, 28, 37, 31, 47, 33, 42, 25, 29, 40, 39, 42, 32, 24, 29, 22, 42, 41]
Capacity=80
Day=range(1,len(Demand)+1)
High=[61, 48, 76, 38, 48, 39, 52, 63, 71, 85, 59, 47, 45, 45, 57, 51, 75, 52, 72, 47, 47, 76, 62, 77, 50, 41, 53, 34, 64, 75]
# 25 days
PHH=0.5
PNH=0.2
# 5 days
PHC=0.1

def cost(a):
    if a==0:
        return 0
    else:
        return 300+80*a**0.9


costDict = {}


def v(t, s, n, nh):
    if s > Capacity:
        s = Capacity
    if t not in Day:
        return (0, None, None, None, None)
    if (t, s, n, nh) not in costDict:

        if nh == "High":  # high
            # n>=0 not reduce prob for the current day
            no = min((cost(a) + (1 - PHH) * v(t + 1, s + a - Demand[t - 1], n, "Normal")[0] + PHH *
                      v(t + 1, s + a - High[t - 1], n, "High")[0], a,
                      (1 - PHH) * (s + a - Demand[t - 1]) + PHH * (s + a - High[t - 1]), n, nh) for a in
                     range(max(0, High[t - 1] - s), 1 + Capacity + High[t - 1] - s))
            yes = no
            if n > 0:
                yes = min((cost(a) + (1 - PHC) * v(t + 1, s + a - Demand[t - 1], n - 1, "Normal")[0] + PHC *
                           v(t + 1, s + a - High[t - 1], n - 1, "High")[0], a,
                           (1 - PHC) * (s + a - Demand[t - 1]) + PHC * (s + a - High[t - 1]), n - 1, nh) for a in
                          range(max(0, High[t - 1] - s), 1 + Capacity + High[t - 1] - s))

        else:  # normal

            # n>=0
            no = min((cost(a) + (1 - PNH) * v(t + 1, s + a - Demand[t - 1], n, "Normal")[0] + PNH *
                      v(t + 1, s + a - High[t - 1], n, "High")[0], a,
                      (1 - PNH) * (s + a - Demand[t - 1]) + PNH * (s + a - High[t - 1]), n, nh) for a in
                     range(max(0, High[t - 1] - s), 1 + Capacity + High[t - 1] - s))
            yes = no
            if n > 0:
                yes = min((cost(a) + (1 - PHC) * v(t + 1, s + a - Demand[t - 1], n - 1, "Normal")[0] + PHC *
                           v(t + 1, s + a - High[t - 1], n - 1, "High")[0], a,
                           (1 - PHC) * (s + a - Demand[t - 1]) + PHC * (s + a - High[t - 1]), n - 1, nh) for a in
                          range(max(0, High[t - 1] - s), 1 + Capacity + High[t - 1] - s))

        costDict[t, s, n, nh] = min(yes, no)

    return costDict[t, s, n, nh]

print(v(1,0,5,"Normal"))

expStates=[]
nList=[]
nhList=[]
for t in Day:
    if t==1:
        s=0
        n=5
        nh="Normal"
    else:
        vMin=min(v(t,int(s//1),n,"High"),v(t,int(s//1),n,"Normal"))
        s=vMin[2]
        n=vMin[3]
        nh=vMin[4]
    expStates.append(s)
    nList.append(n)
    nhList.append(nh)

print("when to reduce probability: \n",nList) # 19,22,24,27,29

print("High demand or Normal demand at given day:\n",nhList) #    19 22 24 27 29 30

actList=[]
for t in Day:
    a=v(t,int(expStates[t-1]//1),nList[t-1],nhList[t-1])[1]
    actList.append(a)

print("the power should be generate at each day:\n",actList)

plt.figure(figsize=(12,8))
plt.xlabel("Day in June",fontsize=15)
plt.xlim(0,31)
plt.ylabel("Expected Power Generation / MWH",fontsize=15)
plt.ylim(-5,150)
plt.title("The expected amount of power generation at each day in June",fontsize=20)
for a,b in zip(Day,actList):
    if b!=0:
        plt.text(a, b+2, (a,b),fontsize=10)
plt.scatter(Day,actList)
plt.show()


