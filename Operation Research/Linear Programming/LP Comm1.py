import os
import pandas as pd
import numpy as np
from gurobipy import *



DATA_PATH= "Dataset"
GRID_DATA_PATH=os.path.join(DATA_PATH,"grid.csv")
NODE_DATA_PATH=os.path.join(DATA_PATH,"nodes.csv")
# import grid and node dataset
grid=pd.read_csv(GRID_DATA_PATH)
nodes=pd.read_csv(NODE_DATA_PATH)

Generator_Node=np.array([42,23,46,15])
Generator_Capacity=np.array([403,834,830,616])
Generator_Cost=np.array([75,63,80,78])

Total_Capacity=np.sum(Generator_Capacity)
Total_Demand=np.sum(nodes["Demand"])

# Total Capacity is bigger than Total_Demand so the problem has feasible solution
print("Total Capacity(MW):",Total_Capacity)
print("Total_Demand(MW):",Total_Demand)

m = Model("Electricity Network")

# each variable Y = the power at generator node
Lg=len(Generator_Node)
Y={index:m.addVar() for index in range(Lg)}

m.addConstrs((Y[i]>=0 for i in range(Lg)))
m.addConstrs((Y[i]<=Generator_Capacity[i] for i in range(Lg)))

# add supple and demand constraints
m.addConstr(quicksum(Y[i] for i in range(Lg))==Total_Demand)

# build objective function
m.setObjective(quicksum(Generator_Cost[i]*Y[i]*24 for i in range(Lg)),GRB.MINIMIZE)

m.optimize()

print(m.objVal)




