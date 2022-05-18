# Operation-Research-With-Python


Tools: Miniconda3 + PyCharm + Gurobi

1. install Gurobi Optimizer ;
2. apply for licence and activate Gurobi with it;
3. copy the file gurobipy under path
   gurobi951\win64\your_current_python_version\lib
   to envs\your_env\Lib;
4. switch env to current env (e.g. ml).


## Linear Programming Requirements:

1. The red nodes on the map show the locations of our generators. Due to various factors, these generators have different capacities and costs for producing electricity, as shown in the following

Generator Node	42	23	46	15 

Capacity (MW)	403	834	830	616

Cost ($/MWh)	75	63	80	78

Please provide us with the optimal cost for meeting the current demand over a whole day from our generators

2. However, we did not mention that our transmission lines actually lose electricity along them. This loss can be estimated as 0.1% per km.

Please provide us with the optimal cost for meeting the current demand over a whole day from our generators

3. We have realised that your proposal will exceed the limits on some of our transmission lines. The following 18 lines can effectively handle any load:

20	21	30	31	48	49	56	57	70

71	82	83	90	91	106	107	112	113

However, all of the other lines have a limit of 126 MW. 

Please provide us with the optimal cost for meeting the current demand over a whole day from our generators.

4. However, in practice demand changes over the day, and we are concerned about how our network will cope with peak demand times. We have broken the day into six time periods: Midnight to 4am, 4am to 8am, 8am to 12pm, 12pm to 4pm, 4pm to 8pm, and 8pm to midnight。 

Please provide us with the optimal total cost over the day for meeting the demand in each of the six time periods from our generators.

5. It is dangerous for us to make large changes to a generator’s output from one time period to another. We have discussed this with our engineers, and they suggest that each generator’s output should not change by more than 177 MW from one time period to another.

Please provide us with the optimal total cost over the day for meeting the demand in each of the six time periods from our generators.

## Mixed-Integer Linear Programming 

6. Going forward, we would like you to ignore our previous limit on changes to generator output across the day, as we think our new planning will help address that issue. You can base your future proposals on your response to our Communication 4 (with a cost of $3301661).

Firstly, we have funds to increase the capacity of three of our transmission lines by 50 MW (to 176 MW). Which lines we should increase?

Please provide us with the optimal total cost over the day for meeting the demand in each of the six time periods from our generators.

7. We also have funds to build a small gas generator at one of the existing nodes on the network, where there is not already a generator. This generator can supply up to 200 MW at a cost of $79/MWh. Where should we build this generator? Note that any existing demand at the node where it is located will still need to be met.

Please provide us with the optimal total cost over the day for meeting the demand in each of the six time periods from our generators

8. Unfortunately the local government has declined our application to build the new generator at Node 45. Could you propose an alternative site we should use? We realise that this may affect your earlier proposal on which transmission lines to upgrade.

Please provide us with the optimal total cost over the day for meeting the demand in each of the six time periods from our generators.

9. We're excited to let you know that we have the go-ahead to build the gas generator. Due to the design of the gas generator, we can only run it during four time periods (16 hours) each day. Given our current demands, which time periods should it be operated? We realise that this may affect your earlier proposals on which transmission lines to upgrade and even where we should build the new gas generator.

Please provide us with the optimal total cost over the day for meeting the demand in each of the six time periods from our generators.

10. In addition to the gas generator, we can also build a solar farm at one of the nodes. This will produce electricity over the day as follows:

Time Period	 0–4	    4–8	   8–12	        12–16	     16–20	    20–24

Supply (MW)	  0         20	   120	         110	       20	       0

The cost of the solar electricity is $42/MWh. Where should we build this solar farm? Note that any existing demand at the node where it is located will still need to be met.

Please provide us with the optimal total cost over the day for meeting the demand in each of the six time periods from our combined generators.

11. The costs we have given you for our original four generators are rather simplistic. In practice, the generators operate efficiently up to 60% of their capacity but after that they become more expensive to run. We estimate this increase in cost to be 30% on top of the original values we gave you.

For example, the generator at Node 42 will run at a cost of $75/MWh when supplying no more than 241.8 MW. Beyond that threshold, it will then cost $97.5/MWh to run.

please provide us with the optimal total cost over the day for meeting the demand in each of the six time periods from our combined generators.

12. To counter the increased costs of peak production, we have been working with customers on a scheme where they will commit to reduce their demand by 10% for one time period each day. We can specify the time periods when this will happen for each node but no more than 9 nodes can be reduced during the same time period.

Please provide us with the optimal total cost over the day for meeting the demand in each of the six time periods from our combined generators.

## Dynamic Programming 

13. We need to supply electricity to a remote region that is not part of our network. A small gas generator will be ideal for this environment, but we are excited to try accompanying it with a new 80 MWh battery. This battery will allow us to have days where we do not need to turn on the generator, a positive outcome for the area.

The forecast daily electricity demands (MWh) for June are as follows:

36, 27, 45, 24, 29, 24, 30, 35, 40, 46, 34, 31, 26, 28, 37, 31, 47, 33, 42, 25, 29, 40, 39, 42, 32, 24, 29, 22, 42, 41

Each night we put in our order for the gas to power the generator for the following day. Effectively, our orders are placed in integer numbers of MWh, x, with a total cost of buying the gas and running the generator for a day of $300+80x0.9 (or $0, when x = 0).

We need to meet the forecast demand each day, either directly from the generator or from the battery. Any surplus electricity will be stored in the battery. Once the battery is at capacity, subsequent gas is wasted.

Suppose our battery is initially empty and can be left empty at the end of the month. How much electricity should we plan to generate for each day in June? Please provide us with the optimal total cost.

14. It turns out that our initial forecasts for June were rather limited. Each day there is in fact a 40% chance that demand will be higher than normal, as follows:

61, 48, 76, 38, 48, 39, 52, 63, 71, 85, 59, 47, 45, 45, 57, 51, 75, 52, 72, 47, 47, 76, 62, 77, 50, 41, 53, 34, 64, 75

The remaining 60% of the time the demand will be as previously forecast. Unfortunately, we do not know whether demand will be high or normal when we order the gas the night before.

Please provide us with the optimal expected total cost.

15. In line with the demand-reduction strategy you helped us with in Communication 12, for this new region in June we have been allocated 5 days for which we can reduce the chance of high demand from 40% to only 10% (with a 90% chance of normal demand instead). We can make this request the night before, around the same time that we order our gas. The days do not have to be consecutive. Given this opportunity, please provide us with the optimal expected total cost.

16. Our forecasters have advised us that high and normal demands tend to come in runs, so if demand is high one day, then there is actually a 50% chance it will be high again the next day, while if it is normal one day then there is only a 20% chance it will be high the next day. Requesting the next day for demand reduction will still reduce this to 10%, regardless of whether it was high or normal the previous day.

Based on this updated forecasting, please provide us with the optimal expected total cost. You can assume May 31st has normal demand.
