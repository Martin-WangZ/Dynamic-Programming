import matplotlib.pyplot as plt

Demand=[36, 27, 45, 24, 29, 24, 30, 35, 40, 46, 34, 31, 26, 28, 37, 31, 47, 33, 42, 25, 29, 40, 39, 42, 32, 24, 29, 22, 42, 41]
Capacity=80
Day=range(1,len(Demand)+1)
High=[61, 48, 76, 38, 48, 39, 52, 63, 71, 85, 59, 47, 45, 45, 57, 51, 75, 52, 72, 47, 47, 76, 62, 77, 50, 41, 53, 34, 64, 75]
PH=0.4
PN=0.6

def cost(a):
    if a==0:
        return 0
    else:
        return 300+80*a**0.9

cost_Dict={}
def v(t,s):
    if s>Capacity:
        s=Capacity
    if t not in Day:
        return (0,None)
    else:
        if (t,s) not in cost_Dict:
            cost_Dict[t,s]=min( (cost(a)+ PN*v(t+1,s+a-Demand[t-1])[0]+PH*v(t+1,s+a-High[t-1])[0],a) for a in range(max(0,High[t-1]-s),1+Capacity+High[t-1]-s)                )
        return cost_Dict[t,s]

print(v(1,0))

expStates=[]
def expState(t,s):
    return PN*(v(t,s)[1]+s-Demand[t-1])+PH*(v(t,s)[1]+s-High[t-1])
for t in Day:
    if t==1:
        s=0
    else:
        s=expState(t,s//1)
    expStates.append(s)

# look at the expected action at day t
actList=[]
for t in Day:
    actList.append(v(t,expStates[t-1]//1)[1])


print("the power should be generate at each day \n",actList)

plt.figure(figsize=(15,8))
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