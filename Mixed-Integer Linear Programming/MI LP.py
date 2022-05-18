from gurobipy import *
import math
import pandas as pd
import os


# Use pandas to import the csv files as data frames
DATA_PATH="Dataset"
GRID_DATA_PATH=os.path.join(DATA_PATH,"grid.csv")
NODE_DATA_PATH=os.path.join(DATA_PATH,"nodes2.csv")
# import grid and node dataset
arcs=pd.read_csv(GRID_DATA_PATH)
nodes=pd.read_csv(NODE_DATA_PATH)

# all Sets
A = arcs['Arc']
N = nodes['Node']
G = [42,23,46,15]
H = [20,21,30,31,48,49,56,57,70,71,82,83,90,91,106,107,112,113]
T = range(6)

# Comm 1 - Generator data : costs and supply

costs = { 42: 75, 23: 63, 46: 80, 15: 78}
supply = { 42: 403, 23: 834, 46: 830, 15: 616}

# Comm 2 - data: Transmission loss data

loss = 0.001

# Comm 3 - data: Transmission limits and distance(lenth of arc)

upbound = 126

# Calculate lengths of each arc
distance = [math.hypot(
    nodes['X'][arcs['Node1'][a]]-nodes['X'][arcs['Node2'][a]],
    nodes['Y'][arcs['Node1'][a]]-nodes['Y'][arcs['Node2'][a]]) for a in A]


# Comm 4 - data: customer demand at each time period

D = [[nodes['D'+str(t)][n] for t in T] for n in N]

# Comm 6 - data: the number of chosen arcs and increased transimitting ability

num_choosed_arc=3
extra_ability=50


# Comm 7 - data:  gas cost, supply and number of gas station

gas_cost=79
gas_supply=200
gas_generator=1


# Comm 8 - data: Node 45

declined_node=45

# Comm 9 - data: the gas generator only works during four periods.

runnig_period=4


# Comm 10 - data: solar supply, costs and the number of solar farm to be built.

solar_supply={0:0,1:20,2:120,3:110,4:20,5:0}
solar_cost=42
solar_generator=1


# Comm 11 - data: threhold with normal cost , increased costs beyond threhold

thresholds={key:value*0.6 for key,value in supply.items()}
increased_costs={key:value*0.3 for key,value in costs.items()}


# Comm 12 -data : percentage for one period, max number at a period, choose one period to reduce

reduced_percentage=0.1
reduced_limit=9
reduced_period=1

m = Model("Electrigrid")

m.setParam('MIPGap', 0)

# X gives flow on arc a in time period t
X = {(a, t): m.addVar() for a in A for t in T}

# Y gives amount generated at node n in time period t
Y = {(n, t): m.addVar() for n in N for t in T}

# SY gives amount generated at node n in time period t for solar farm

SY = {(n, t): m.addVar() for n in N for t in T}

# EY[n,t]==Y[n,t]-thresholds[n]*E[n,t]

EY = {(n, t): m.addVar() for n in N for t in T if n in supply.keys()}

# CY = costs[n]+increased_costs[n]*E[n,t]

CY = {(n, t): m.addVar() for n in N for t in T if n in supply.keys()}

# TY = thresholds[n]*costs[n]*E[n,t]

TY = {(n, t): m.addVar() for n in N for t in T if n in supply.keys()}

# DY = demand

DY = {(n, t): m.addVar() for n in N for t in T}

# B gives binary value to indicate whether choose as the arc with increased upbound

Bb = {a: m.addVar(vtype=GRB.BINARY) for a in A if a not in H}

# G gives binary value to indicate whether a node is choosed as gas generator. Note: node 45 cannot be generator

Gb = {n: m.addVar(vtype=GRB.BINARY) for n in N if n not in supply.keys() and n != declined_node}

# Tb gives binary value to indicate whether the gas generator  will work at the period.

Tb = {t: m.addVar(vtype=GRB.BINARY) for t in T}

# S gives binary value to indicate whether a node is choosed as solar generator.

Sb = {n: m.addVar(vtype=GRB.BINARY) for n in N}

# E gives binary value to indicate whether the supply at the node exceeds its threshold at period t.

Eb = {(n, t): m.addVar(vtype=GRB.BINARY) for n in N for t in T if n in supply.keys()}

# Rb gives binary value to indicate whether the node will reduce demand at period t

Rb = {(n, t): m.addVar(vtype=GRB.BINARY) for n in N for t in T if n not in supply.keys()}

# build objective function
m.setObjective(quicksum(4 * (TY[n, t] + EY[n, t] * CY[n, t]) for n in N for t in T if n in supply.keys()) + quicksum(
    4 * gas_cost * Y[n, t] for n in N for t in T if n not in supply.keys()) + quicksum(
    4 * solar_cost * SY[n, t] for n in N for t in T), GRB.MINIMIZE)

# choose three arcs to increased their upbound

m.addConstr(quicksum(Bb[a] for a in A if a not in H) == num_choosed_arc)

# choose a non-generator node as gas generator.Note: node 45 cannot be generator

m.addConstr(quicksum(Gb[n] for n in N if n not in supply.keys() and n != declined_node) == gas_generator)

# choose four running periods within six periods

m.addConstr(quicksum(Tb[t] for t in T) == runnig_period)

# choose one of nodes to be solar farm

m.addConstr(quicksum(Sb[n] for n in N) == solar_generator)

# cannot reduce demand at same period over 9 nodes at each period.

m.addConstrs((quicksum(Rb[n, t] for n in N if n not in supply.keys()) <= reduced_limit for t in T))

# choose one period to redue

m.addConstrs((quicksum(Rb[n, t] for t in T) == reduced_period for n in N if n not in supply.keys()))

for t in T:

    for a in A:  # for arc constraint
        # constrain maximum flow on arc a
        if a not in H:
            m.addConstr(X[a, t] <= upbound + Bb[a] * extra_ability)

    for n in N:  # for node constraint
        # balance flow at each node, taking into account loss on inflow arcs,
        # adding amount generated to LHS and demand amount to RHS

        # inflow + supply = outflow + demand :

        # supply node: inflow + supply = outflow + 0
        # demand node : inflow + 0 = outflow + demand

        # SY[n,t]*S[n] means solar supply at that node
        m.addConstr(
            quicksum(X[a, t] * (1 - loss * distance[a]) for a in A if arcs['Node2'][a] == n) + Y[n, t] + SY[n, t] ==
            quicksum(X[a, t] for a in A if arcs['Node1'][a] == n) + DY[n, t])

        # Demand at the node to be changed to generator still need to be met
        # so we cannot set the demand at the node as 0

        #  SY is constrained by supply at solar node

        m.addConstr(SY[n, t] <= solar_supply[t] * Sb[n])

        if n in supply:

            # Y is constrained by supply at generator nodes

            m.addConstr(Y[n, t] <= supply[n])

            # E[n,t]=0 : not exceed ; E[n,t]=1: exceed

            m.addConstr(Y[n, t] - thresholds[n] <= supply[n] * Eb[n, t])

            # exceeded power or not

            m.addConstr(EY[n, t] == Y[n, t] - thresholds[n] * Eb[n, t])

            m.addConstr(CY[n, t] == costs[n] + increased_costs[n] * Eb[n, t])

            # basic cost

            m.addConstr(TY[n, t] == thresholds[n] * costs[n] * Eb[n, t])

            # if it's generator, then DY[n,t]==D[n][t]=0

            m.addConstr(DY[n, t] == D[n][t])

        # if the node is not chooesd as gas generator, then G[n]=0 so that the constraint is Y[n,t]==0
        # otherwise, the constraint is Y[n,t]< gas_supply = 200

        else:
            # set node 45 as 0 because it cannot be gas generator
            if n == declined_node:
                m.addConstr(Y[n, t] == 0)

            else:
                # select four periods to run the gas generator through multiplying Tb[t]
                m.addConstr(Y[n, t] <= gas_supply * Gb[n] * Tb[t])

            # if it's not generator, then the demand will be:
            m.addConstr(DY[n, t] == D[n][t] - D[n][t] * reduced_percentage * Rb[n, t])

m.optimize()
print("Minimum cost = $", m.objVal)

for n in N:
    if Sb[n].x == 1:
        print("solar farm build at:", n)

for t in T:
    if Tb[t].x == 1:
        print("work period:", t)

for a in A:
    if a not in H:
        if Bb[a].x == 1:
            print("changed arc :", a)
for n in N:
    if n not in supply.keys() and n != declined_node:
        if Gb[n].x == 1:
            print("gas generator:", n)

for n in N:
    for t in T:
        if n in supply.keys() and Eb[n, t].x == 1:
            print("exceed node and time period:", (n, t))

for n in N:
    for t in T:
        if n not in supply.keys() and Rb[n, t].x == 1:
            print("reduced node and time period:", (n, t))

