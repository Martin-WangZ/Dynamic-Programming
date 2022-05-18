import os
import pandas as pd
import numpy as np
from gurobipy import *

DATA_PATH="Dataset"
GRID_DATA_PATH=os.path.join(DATA_PATH,"grid.csv")
NODE_DATA_PATH=os.path.join(DATA_PATH,"nodes.csv")
# new dataset
New_Node_DATA_PATH=os.path.join(DATA_PATH,"nodes2.csv")
nodes2=pd.read_csv(New_Node_DATA_PATH)
clockPoint=[0,4,8,12,16,20]
#
grid=pd.read_csv(GRID_DATA_PATH)
nodes=pd.read_csv(NODE_DATA_PATH)
Generator_Node=np.array([42,23,46,15])
Generator_Capacity=np.array([403,834,830,616])
Generator_Cost=np.array([75,63,80,78])
No_Bound_Arc=np.array([20,21,30,31,48,49,56,57,70,71,82,83,90,91,106,107,112,113])


# define a function to calculate the distance of each node to adjacent nodes
def disNodeToAdj(node1,node2,nodes2=nodes2):
    x1=nodes[nodes["Node"]==node1]["X"]
    y1=nodes[nodes["Node"]==node1]["Y"]
    x2=nodes[nodes["Node"]==node2]["X"]
    y2=nodes[nodes["Node"]==node2]["Y"]
    x1x2=int(x1)-int(x2)
    y1y2=int(y1)-int(y2)
    disNode1ToNode2=np.sqrt(x1x2**2+y1y2**2)
    return disNode1ToNode2

df = pd.DataFrame(columns=["Arc","Node1","Node2","Distance"])
for index,row in grid.iterrows():
        node1=row["Node1"]
        node2=row["Node2"]
        arc=row["Arc"]
        # calculate distance of two adjacent nodes
        distance=disNodeToAdj(node1,node2,nodes2)
        df=df.append(pd.DataFrame({"Arc":[arc],"Node1":[node1],"Node2":[node2],"Distance":[distance]}),ignore_index=True)

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

m=Model("Electricity Network With Loss and upbound and time")

arcList=df["Arc"]

# build variables for time period 0  0-4
X0={arc:m.addVar() for arc in arcList}
Y0={g:m.addVar() for g in Generator_Node}

# build variables for time period 1  4-8
X1={arc:m.addVar() for arc in arcList}
Y1={g:m.addVar() for g in Generator_Node}

# build variables for time period 2  8-12
X2={arc:m.addVar() for arc in arcList}
Y2={g:m.addVar() for g in Generator_Node}

# build variables for time period 3  12-16
X3={arc:m.addVar() for arc in arcList}
Y3={g:m.addVar() for g in Generator_Node}

# build variables for time period 4  16-20
X4={arc:m.addVar() for arc in arcList}
Y4={g:m.addVar() for g in Generator_Node}

# build variables for time period 5  20-24
X5={arc:m.addVar() for arc in arcList}
Y5={g:m.addVar() for g in Generator_Node}

# Constraint 1: all non-negative and some arcs is not bigger than 126 transmittiong limitation
m.addConstrs((X0[i]>=0 for i in arcList))
m.addConstrs((X0[i]<=126 for i in arcList if i not in No_Bound_Arc))
m.addConstrs((X1[i]>=0 for i in arcList))
m.addConstrs((X1[i]<=126 for i in arcList if i not in No_Bound_Arc))
m.addConstrs((X2[i]>=0 for i in arcList))
m.addConstrs((X2[i]<=126 for i in arcList if i not in No_Bound_Arc))
m.addConstrs((X3[i]>=0 for i in arcList))
m.addConstrs((X3[i]<=126 for i in arcList if i not in No_Bound_Arc))
m.addConstrs((X4[i]>=0 for i in arcList))
m.addConstrs((X4[i]<=126 for i in arcList if i not in No_Bound_Arc))
m.addConstrs((X5[i]>=0 for i in arcList))
m.addConstrs((X5[i]<=126 for i in arcList if i not in No_Bound_Arc))


m.addConstrs((Y0[i]>=0 for i in Generator_Node))
m.addConstrs((Y1[i]>=0 for i in Generator_Node))
m.addConstrs((Y2[i]>=0 for i in Generator_Node))
m.addConstrs((Y3[i]>=0 for i in Generator_Node))
m.addConstrs((Y4[i]>=0 for i in Generator_Node))
m.addConstrs((Y5[i]>=0 for i in Generator_Node))


# according to different time perior to build constraints
def constrFun(node, clock, data=df, nodes2=nodes2):
    # for time period 0
    if clock == 0:
        adjNodes = findAdjNodes(node)
        if node in Generator_Node:
            m.addConstr(
                quicksum(X0[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) - quicksum(
                    X0[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                    row["Node2"] == node) == Y0[node])

            m.addConstr(Y0[node] <= int(Generator_Capacity[Generator_Node == node]))

        if node not in Generator_Node:
            m.addConstr(quicksum(X0[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                                 row["Node2"] == node) - quicksum(
                X0[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) == int(
                nodes2[nodes2["Node"] == node]["D0"]))

    # for time period 1
    if clock == 4:
        adjNodes = findAdjNodes(node)
        if node in Generator_Node:
            m.addConstr(
                quicksum(X1[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) - quicksum(
                    X1[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                    row["Node2"] == node) == Y1[node])

            m.addConstr(Y1[node] <= int(Generator_Capacity[Generator_Node == node]))

        if node not in Generator_Node:
            m.addConstr(quicksum(X1[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                                 row["Node2"] == node) - quicksum(
                X1[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) == int(
                nodes2[nodes2["Node"] == node]["D1"]))

    # for time period 2
    if clock == 8:
        adjNodes = findAdjNodes(node)
        if node in Generator_Node:
            m.addConstr(
                quicksum(X2[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) - quicksum(
                    X2[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                    row["Node2"] == node) == Y2[node])

            m.addConstr(Y2[node] <= int(Generator_Capacity[Generator_Node == node]))

        if node not in Generator_Node:
            m.addConstr(quicksum(X2[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                                 row["Node2"] == node) - quicksum(
                X2[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) == int(
                nodes2[nodes2["Node"] == node]["D2"]))

    # for time period 3
    if clock == 12:
        adjNodes = findAdjNodes(node)
        if node in Generator_Node:
            m.addConstr(
                quicksum(X3[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) - quicksum(
                    X3[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                    row["Node2"] == node) == Y3[node])

            m.addConstr(Y3[node] <= int(Generator_Capacity[Generator_Node == node]))

        if node not in Generator_Node:
            m.addConstr(quicksum(X3[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                                 row["Node2"] == node) - quicksum(
                X3[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) == int(
                nodes2[nodes2["Node"] == node]["D3"]))

    # for time period 4
    if clock == 16:
        adjNodes = findAdjNodes(node)
        if node in Generator_Node:
            m.addConstr(
                quicksum(X4[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) - quicksum(
                    X4[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                    row["Node2"] == node) == Y4[node])

            m.addConstr(Y4[node] <= int(Generator_Capacity[Generator_Node == node]))

        if node not in Generator_Node:
            m.addConstr(quicksum(X4[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                                 row["Node2"] == node) - quicksum(
                X4[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) == int(
                nodes2[nodes2["Node"] == node]["D4"]))

    # for time period 5
    if clock == 20:
        adjNodes = findAdjNodes(node)
        if node in Generator_Node:
            m.addConstr(
                quicksum(X5[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) - quicksum(
                    X5[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                    row["Node2"] == node) == Y5[node])

            m.addConstr(Y5[node] <= int(Generator_Capacity[Generator_Node == node]))

        if node not in Generator_Node:
            m.addConstr(quicksum(X5[row["Arc"]] * (1 - 0.001 * row["Distance"]) for index, row in adjNodes.iterrows() if
                                 row["Node2"] == node) - quicksum(
                X5[row["Arc"]] for index, row in adjNodes.iterrows() if row["Node1"] == node) == int(
                nodes2[nodes2["Node"] == node]["D5"]))

# build constraints for each node at different time period
for clock in clockPoint:
    for node in nodes["Node"]:
        constrFun(node,clock,data=df,nodes2=nodes2)

# set Objective function. each generated energy should multiple 4 hours
m.setObjective(quicksum(Y0[i]*Generator_Cost[Generator_Node==i] for i in Generator_Node)*4+quicksum(Y1[i]*Generator_Cost[Generator_Node==i] for i in Generator_Node)*4+quicksum(Y2[i]*Generator_Cost[Generator_Node==i] for i in Generator_Node)*4+quicksum(Y3[i]*Generator_Cost[Generator_Node==i] for i in Generator_Node)*4+quicksum(Y4[i]*Generator_Cost[Generator_Node==i] for i in Generator_Node)*4+quicksum(Y5[i]*Generator_Cost[Generator_Node==i] for i in Generator_Node)*4,GRB.MINIMIZE)

m.optimize()

print(m.objVal)

