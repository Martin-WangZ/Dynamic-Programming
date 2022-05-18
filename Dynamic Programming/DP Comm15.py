import matplotlib.pyplot as plt


Demand=[36, 27, 45, 24, 29, 24, 30, 35, 40, 46, 34, 31, 26, 28, 37, 31, 47, 33, 42, 25, 29, 40, 39, 42, 32, 24, 29, 22, 42, 41]
Capacity=80
Day=range(1,len(Demand)+1)
High=[61, 48, 76, 38, 48, 39, 52, 63, 71, 85, 59, 47, 45, 45, 57, 51, 75, 52, 72, 47, 47, 76, 62, 77, 50, 41, 53, 34, 64, 75]
# 25 days
PH=0.4
PN=0.6
# 5 days
PHC=0.1
PNC=0.9

def cost(a):
    if a==0:
        return 0
    else:
        return 300+80*a**0.9

costDict={}
def v(t,s,n):
    if s>Capacity:  # if left power exceeds capacity, then throw away the power beyond capacity
        s=Capacity
    if t not in Day:
        return (0,None,None,None)
    if (t,s,n) not in costDict:
        no=min((cost(a)+PN*v(t+1,s+a-Demand[t-1],n)[0]+PH*v(t+1,s+a-High[t-1],n)[0],a,PN*(s+a-Demand[t-1])+PH*(s+a-High[t-1]),n) for a in range(max(0,High[t-1]-s),1+Capacity+High[t-1]-s))
        yes=no
        if n>0:
            yes=min((cost(a)+PNC*v(t+1,s+a-Demand[t-1],n-1)[0]+PHC*v(t+1,s+a-High[t-1],n-1)[0],a,PNC*(s+a-Demand[t-1])+PHC*(s+a-High[t-1]),n-1) for a in range(max(0,High[t-1]-s),1+Capacity+High[t-1]-s))
        costDict[t,s,n]=min(yes,no)
    return costDict[t,s,n]

print(v(1,0,5))

expStates=[]
nList=[]
for t in Day:
    if t==1:
        s=0
        n=5
    else:
        s=v(t,int(s//1),n)[2]
        n=v(t,int(s//1),n)[3]
    expStates.append(s)
    nList.append(n)

print("when to reduce probability: \n",nList)  # day 10,19,22,24,29 will reduce

# get action at each day
actList=[]
for t in Day:
    a=v(t,expStates[t-1]//1,nList[t-1])[1]
    actList.append(a)


print("the power should be generate at each day \n",actList)

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

