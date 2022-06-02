# discrete event simulation with possion distribution

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# define the system class including number of arrival packages, packages in reqular queue and in priority queue respectively
# as well as each worker's state such as busy(denote as 1) or leisure(denote as 0).
class SystemState:
    def __init__(self,arrivalPackages=0,regularQueue=0,priorityQueue=0,flag=0):
        self.arrivalPackages=arrivalPackages
        self.regularQueue=regularQueue
        self.priorityQueue=priorityQueue
        self.flag=flag

# initial system at t=0
initialSystemState=SystemState()


# simulate a process at one unit time
def simulateOnce():
    # get arrived package which is followed by poisson distribution with mean 4
    initialSystemState.arrivalPackages = np.random.poisson(4)
    # whether the package is regular or not is followed by binomial distribution with success 0.9
    # and trial number is arrived package
    regularPackages = np.random.binomial(initialSystemState.arrivalPackages, 0.9)
    priorityPackages = initialSystemState.arrivalPackages - regularPackages
    # sum each Queue
    initialSystemState.regularQueue += regularPackages
    initialSystemState.priorityQueue += priorityPackages
    # initial processing ability
    workers = np.random.exponential(0.5, 9)
    # this is aimed to optimize system. firstly assign work to workers who process package fast.
    sortedworkers = np.sort(workers)[::-1]
    # if priority queue has no package, then we process regular queue
    if initialSystemState.priorityQueue == 0:
        # it is possible that regular queue is also empty because new packages arrived followed by poisson(4)
        # so the number of package arrival may be 0 and last time the packages in regular queue have all been processed
        # if regular queue is empty, just jump to next unit time
        if initialSystemState.regularQueue == 0:
            # some of workers at this unit time must be leisure. so return 0
            return 0
        sumEffective = 0
        numberOfbusy = 0
        for i in range(0, 9):
            tempRegular = initialSystemState.regularQueue
            # sum from 0 to ith workers who process how many packages
            sumEffective += sortedworkers[i]
            # is package enough for processing? if enough, then keep adding new workers
            tempRegular -= sumEffective
            # not enough
            if tempRegular <= 0:
                # numberOfbusy workers' processing ability may overceed packages in regular queue,
                # if so, set regular queue is 0 because it can't be a negative number
                initialSystemState.regularQueue = 0
                break
            # enough
            else:
                numberOfbusy += 1
                continue
        # minus proccessd packages in regular queue
        if initialSystemState.regularQueue == 0:
            # all busy, set flag=1 and count+1
            if numberOfbusy == 9:
                initialSystemState.flag = 1
            else:
                initialSystemState.flag = 0
        # there still are left packages in regular queue after 9 workers processed, which means all busy
        else:
            initialSystemState.regularQueue -= sumEffective
            initialSystemState.flag = 1


    # otherwise, priority has packages so we need firstly process the priority queue then process regular queue
    else:
        sumEffective = 0
        numberOfbusy = 0
        for i in range(0, 9):
            tempPriority = initialSystemState.priorityQueue
            sumEffective += sortedworkers[i]
            # whether or not packages are still in priority queue
            tempPriority -= sumEffective
            # if all packages in priority queue are processed, set priority queue 0 and turn to regular queue
            if tempPriority <= 0:
                tempRegular = initialSystemState.regularQueue
                # np.abs(tempPriority) means how many processing ability left among 9 workers
                # now tempRegular stands for whether packages in regular queue is enough to process or not
                tempRegular -= np.abs(tempPriority)
                # if not enough, set priority queue and regular queue is 0 respectively
                if tempRegular <= 0:
                    initialSystemState.priorityQueue = 0
                    initialSystemState.regularQueue = 0
                    break
                # if enough, add new worker to process and the number of busy workers incease 1
                else:
                    numberOfbusy += 1
                    # if all are busy but still have packages in regular queue,
                    # then minus processed package to get final regular queue
                    if numberOfbusy == 9:
                        initialSystemState.priorityQueue = 0
                        initialSystemState.regularQueue = tempRegular
                    continue
                    # otherwise, there are still package in priority queue which waites to process
            else:
                numberOfbusy += 1
                # if all are busy but still have packages in priority queue,
                # then minus processed package to get final priority queue and regular queue is not processed
                if numberOfbusy == 9:
                    initialSystemState.priorityQueue = tempPriority
                continue

        # check if all busy
        if numberOfbusy == 9:
            initialSystemState.flag = 1
        else:
            initialSystemState.flag = 0
    return initialSystemState.flag

T=2000
count=0
N=50

def proSim(count,T):
    for t in range(0,T):
        flag=simulateOnce()
        count+=flag
    proBusy=count/T
    return proBusy


def fhSim(N, count, T):
    sim = np.array([])
    for i in range(0, N):
        proBusy = proSim(count, T)
        sim = np.append(sim, proBusy)
    proBusyMean = np.mean(sim)
    proBusyStd = np.std(sim)
    CI = [proBusyMean - 1.96 * proBusyStd / np.sqrt(N), proBusyMean + 1.96 * proBusyStd / np.sqrt(N)]
    print("the 95% confident interval  =", CI)


Tsequence = np.arange(0, T + 1)
IsBusyAtT = np.array([0])
ProBusyAtEachT = np.array([0])
countFlag = 0
for i in range(1, T + 1):
    flag = simulateOnce()
    IsBusyAtT = np.append(IsBusyAtT, flag)
    countFlag += flag
    proportionFlag = countFlag / i
    ProBusyAtEachT = np.append(ProBusyAtEachT, proportionFlag)

data={"Tsequence":Tsequence,"IsBusyAtT":IsBusyAtT,"ProBusyAtEachT":ProBusyAtEachT}
Table=pd.DataFrame(data)

print(Table.head(10))

plt.plot(Tsequence,ProBusyAtEachT)
plt.show()