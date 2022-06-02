# import dataset
import os
import pandas as pd
import numpy as np
from gurobipy import *


DATA_PATH= "Dataset"
GRID_DATA_PATH=os.path.join(DATA_PATH,"grid.csv")
NODE_DATA_PATH=os.path.join(DATA_PATH,"nodes.csv")
grid=pd.read_csv(GRID_DATA_PATH)
nodes=pd.read_csv(NODE_DATA_PATH)
Generator_Node=np.array([42,23,46,15])
Generator_Capacity=np.array([403,834,830,616])
Generator_Cost=np.array([75,63,80,78])
# unbounded arc
No_Bound_Arc=np.array([20,21,30,31,48,49,56,57,70,71,82,83,90,91,106,107,112,113])


# define a function to calculate the distance of each node to their adjacent nodes
def disNodeToAdj(node1,node2,nodes=nodes):
    x1=nodes[nodes["Node"]==node1]["X"]
    y1=nodes[nodes["Node"]==node1]["Y"]
    x2=nodes[nodes["Node"]==node2]["X"]
    y2=nodes[nodes["Node"]==node2]["Y"]
    x1x2=int(x1)-int(x2)
    y1y2=int(y1)-int(y2)
    disNode1ToNode2=np.sqrt(x1x2**2+y1y2**2)
    return disNode1ToNode2

# replace coordinatives X,Y with distance
df = pd.DataFrame(columns=["Arc","Node1","Node2","Distance"])
for index,row in grid.iterrows():
        node1=row["Node1"]
        node2=row["Node2"]
        arc=row["Arc"]
        # calculate distance of two adjacent nodes
        distance=disNodeToAdj(node1,node2,nodes)
        df=df.append(pd.DataFrame({"Arc":[arc],"Node1":[node1],"Node2":[node2],"Distance":[distance]}),ignore_index=True)

# given a node, get all adjacent nodes
def findAdjNodes(nodeIndex,df=df):
    adjNodes=pd.DataFrame(columns=["Arc","Node1","Node2","Distance"])
    for index,row in df.iterrows():
        node1=row["Node1"]
        node2=row["Node2"]
        if node1==nodeIndex or node2==nodeIndex:
            adjArc=row["Arc"]
            distance=row["Distance"]
            adjNodes=adjNodes.append(pd.DataFrame({"Arc":[adjArc],"Node1":[node1],"Node2":[node2],"Distance":[distance]}),
                                     ignore_index=True)
    return adjNodes

m=Model("Electricity Network With Loss and upbound")

# add variables X for the amount of electricity transmitting on arc
# variable Y for the amount of generated electricity
arcList=df["Arc"]
X={arc:m.addVar() for arc in arcList}
Y={g:m.addVar() for g in Generator_Node}


# Constraint 1: all variables should be non-negative and there is upbound for some arcs according to the communication
m.addConstrs((X[i]>=0 for i in arcList))
m.addConstrs((Y[i]>=0 for i in Generator_Node))
# compared to communication 2, i just add the constraints here. another codes are all same as communication 2
m.addConstrs((X[i]<=126 for i in arcList if i not in No_Bound_Arc));


# same code as that in communication 2.
def constrFun(node, data=df, nodes=nodes):
    adjNodes = findAdjNodes(node)
    if node in Generator_Node:
        m.addConstr(quicksum(X[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) - quicksum(
            X[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
            row["Node2"] == node) == Y[node])

        m.addConstr(Y[node] <= int(Generator_Capacity[Generator_Node == node]))

    if node not in Generator_Node:
        m.addConstr(quicksum(X[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                             row["Node2"] == node) - quicksum(
            X[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) == int(
            nodes[nodes["Node"] == node]["Demand"]))

# build constraints for each node
for node in nodes["Node"]:
    constrFun(node,data=df,nodes=nodes)

# set Objective function
m.setObjective(quicksum(Y[i]*Generator_Cost[Generator_Node==i]*24 for i in Generator_Node),GRB.MINIMIZE)

m.optimize()

print(m.objVal)
