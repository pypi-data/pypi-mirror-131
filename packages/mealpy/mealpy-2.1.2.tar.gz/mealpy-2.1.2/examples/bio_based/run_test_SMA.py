#!/usr/bin/env python
# ------------------------------------------------------------------------------------------------------%
# Created by "Thieu Nguyen" at 20:59, 12/06/2020                                                        %
#                                                                                                       %
#       Email:      nguyenthieu2102@gmail.com                                                           %
#       Homepage:   https://www.researchgate.net/profile/Thieu_Nguyen6                                  %
#       Github:     https://github.com/thieu1995                                                        %
#-------------------------------------------------------------------------------------------------------%

from opfunu.cec_basic.cec2014_nobias import *
from mealpy.bio_based import SMA
from mealpy.problem import Problem
from mealpy.utils.termination import Termination

# Setting parameters

# A - Different way to provide lower bound and upper bound. Here are some examples:

## A1. When you have different lower bound and upper bound for each parameters
problem_dict1 = {
    "obj_func": F5,
    "lb": [-3, -5, 1, -10, ],
    "ub": [5, 10, 100, 30, ],
    "minmax": "min",
    "verbose": True,
}
problem_obj1 = Problem(problem_dict1)

## A2. When you have same lower bound and upper bound for each parameters, then you can use:
##      + int or float: then you need to specify your problem size / number of dimensions (n_dims)
problem_dict2 = {
    "obj_func": F5,
    "lb": -10,
    "ub": 30,
    "minmax": "min",
    "verbose": True,
    "n_dims": 30,  # Remember the keyword "n_dims"
}
problem_obj2 = Problem(problem_dict2)

##      + array: 2 ways
problem_dict3 = {
    "obj_func": F5,
    "lb": [-5],
    "ub": [10],
    "minmax": "min",
    "verbose": True,
    "n_dims": 30,  # Remember the keyword "n_dims"
}
problem_obj3 = Problem(problem_dict3)

n_dims = 100
problem_dict4 = {
    "obj_func": F5,
    "lb": [-5] * n_dims,
    "ub": [10] * n_dims,
    "minmax": "min",
    "verbose": True,
}

## Run the algorithm

### Your parameter problem can be an instane of Problem class or just dict like above
model1 = SMA.BaseSMA(problem_obj1, epoch=100, pop_size=50, pr=0.03)
model1.solve()

model2 = SMA.BaseSMA(problem_dict4, epoch=100, pop_size=50, pr=0.03)
model2.solve()

# B - Test with different Stopping Condition (Termination) by creating an Termination object

## There are 4 termination cases:
### 1. FE (Number of Function Evaluation)
### 2. MG (Maximum Generations / Epochs): This is default in all algorithms
### 3. ES (Early Stopping): Same idea in training neural network (If the global best solution not better an epsilon
###     after K epoch then stop the program
### 4. TB (Time Bound): You just want your algorithm run in K seconds. Especially when comparing different algorithms.

termination_dict1 = {
    "mode": "FE",
    "quantity": 100000  # 100000 number of function evaluation
}
termination_dict2 = {  # When creating this object, it will override the default epoch you define in your model
    "mode": "MG",
    "quantity": 1000  # 1000 epochs
}
termination_dict3 = {
    "mode": "ES",
    "quantity": 30  # after 30 epochs, if the global best doesn't improve then we stop the program
}
termination_dict4 = {
    "mode": "ES",
    "quantity": 60  # 60 seconds = 1 minute to run this algorithm only
}
termination_obj1 = Termination(termination_dict1)
termination_obj2 = Termination(termination_dict2)
termination_obj3 = Termination(termination_dict3)
termination_obj4 = Termination(termination_dict4)

### Pass your termination object into your model as a addtional parameter with the keyword "termination"
model3 = SMA.BaseSMA(problem_dict1, epoch=100, pop_size=50, pr=0.03, termination=termination_obj1)
model3.solve()
### Remember you can't pass termination dict, it only accept the Termination object


# C - Test with different training mode (sequential, threading parallelization, processing parallelization)

## + sequential: Default for all algorithm (single core)
## + thread: create multiple threading depend on your chip
## + process: create multiple cores to run your algorithm.
## Note: For windows, your program need the if __nam__ == "__main__" condition to avoid creating infinite processors

model5 = SMA.BaseSMA(problem_dict1, epoch=100, pop_size=50, pr=0.03)
model5.solve(mode='sequential')  # Default

model6 = SMA.BaseSMA(problem_dict1, epoch=100, pop_size=50, pr=0.03)
model6.solve(mode='thread')

if __name__ == "__main__":
    model7 = SMA.BaseSMA(problem_dict1, epoch=100, pop_size=50, pr=0.03)
    model7.solve(mode='process')

# D - Drawing all available figures

## There are 8 different figures for each algorithm.
## D.1: Based on fitness value:
##      1. Global best fitness chart
##      2. Local best fitness chart
## D.2: Based on objective value:
##      3. Global objective chart
##      4. Local objective chart
## D.3: Based on runtime value (runtime for each epoch)
##      5. Runtime chart
## D.4: Based on exploration verse exploration value
##      6. Exploration vs Exploitation chart
## D.5: Based on diversity of population
##      7. Diversity chart
## D.6: Based on trajectory value (1D, 2D only)
##      8. Trajectory chart

model8 = SMA.BaseSMA(problem_dict1, epoch=100, pop_size=50, pr=0.03)
model8.solve()

## You can access them all via object "history" like this:
model8.history.save_global_objectives_chart(filename="hello/goc")
model8.history.save_local_objectives_chart(filename="hello/loc")
model8.history.save_global_best_fitness_chart(filename="hello/gbfc")
model8.history.save_local_best_fitness_chart(filename="hello/lbfc")
model8.history.save_runtime_chart(filename="hello/rtc")
model8.history.save_exploration_exploitation_chart(filename="hello/eec")
model8.history.save_diversity_chart(filename="hello/dc")
model8.history.save_trajectory_chart(list_agent_idx=[3, 5], list_dimensions=[3], filename="hello/tc")


# E - Handling Multi-Objective function and Constraint Method

## To handling Multi-Objective, mealpy is using weighting method which converting multiple objectives to a single target (fitness value)

## Define your objective function, your constraint
def obj_function(solution):
    t1 = solution[0] ** 2
    t2 = ((2 * solution[1]) / 5) ** 2
    t3 = 0
    for i in range(3, len(solution)):
        t3 += (1 + solution[i] ** 2) ** 0.5
    return [t1, t2, t3]


## Define your objective weights. For example:
###  f1: 50% important
###  f2: 20% important
###  f3: 30% important
### Then weight = [0.5, 0.2, 0.3] ==> Fitness value = 0.5*f1 + 0.2*f2 + 0.3*f3
### Default weight = [1, 1, 1]

problem_dict9 = {
    "obj_func": obj_function,
    "lb": [-3, -5, 1, -10, ],
    "ub": [5, 10, 100, 30, ],
    "minmax": "min",
    "verbose": True,
    "obj_weight": [0.5, 0.2, 0.3]  # Remember the keyword "obj_weight"
}
problem_obj9 = Problem(problem_dict9)
model9 = SMA.BaseSMA(problem_obj9, epoch=100, pop_size=50, pr=0.03)
model9.solve()

## To access the results, you can get the results by solve() method
position, fitness_value = model9.solve()

## To get all fitness value and all objective values, get it via "solution" attribute
## A agent / solution format [position, [fitness, [obj1, obj2, ..., obj_n]]]
position = model9.solution[0]
fitness_value = model9.solution[1][0]
objective_values = model9.solution[1][1]


# F - Test with different variants of this algorithm

model10 = SMA.OriginalSMA(problem_obj9, epoch=100, pop_size=50, pr=0.03)
model10.solve()
