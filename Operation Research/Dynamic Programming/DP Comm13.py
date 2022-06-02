import matplotlib.pyplot as plt


Demand=[36, 27, 45, 24, 29, 24, 30, 35, 40, 46, 34, 31, 26, 28, 37, 31, 47, 33, 42, 25, 29, 40, 39, 42, 32, 24, 29, 22, 42, 41]
Capacity=80
Day=range(1,len(Demand)+1)

def cost(a):
    if a==0:
        return 0
    else:
        return 300+80*a**0.9

cost_Dict={}
def v(t,s):
    if s>Capacity:   # if left power exceeds capacity, then throw away the power beyond capacity.
        s=Capacity
    if t not in Day:
        return (0,None,None)
    else:
        if (t,s) not in cost_Dict:
            cost_Dict[t,s]=min( (cost(a)+ v(t+1,s+a-Demand[t-1])[0],a,s+a-Demand[t-1]) for a in range(max(0,Demand[t-1]-s),Demand[t-1]+Capacity-s+1))
        return cost_Dict[t,s]

print(v(1,0))

actionArray=[]
minCost,action,state=(0,0,0)
for t in Day:
    minCost,action,state=v(t,state)
    actionArray.append(action)

print("Each day power generation:\n",actionArray)

plt.figure(figsize=(12,8))
plt.xlabel("Day in June",fontsize=15)
plt.xlim(0,31)
plt.ylabel("Power Generation / MWH",fontsize=15)
plt.ylim(-5,150)
plt.title("The amount of power generation at each day in June",fontsize=20)
for a,b in zip(Day,actionArray):
    if b!=0:
        plt.text(a, b+2, (a,b),fontsize=13)
plt.scatter(Day,actionArray)
plt.show()