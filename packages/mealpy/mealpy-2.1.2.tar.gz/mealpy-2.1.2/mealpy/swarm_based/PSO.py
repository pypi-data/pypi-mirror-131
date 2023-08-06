#!/usr/bin/env python
# ------------------------------------------------------------------------------------------------------%
# Created by "Thieu Nguyen" at 09:49, 17/03/2020                                                        %
#                                                                                                       %
#       Email:      nguyenthieu2102@gmail.com                                                           %
#       Homepage:   https://www.researchgate.net/profile/Thieu_Nguyen6                                  %
#       Github:     https://github.com/thieu1995                                                        %
#-------------------------------------------------------------------------------------------------------%

import numpy as np
from copy import deepcopy
from mealpy.optimizer import Optimizer


class BasePSO(Optimizer):
    """
        The original version of: Particle Swarm Optimization (PSO)
    """
    ID_VEC = 2      # Velocity
    ID_LOP = 3      # Local position
    ID_LOF = 4      # Local fitness

    def __init__(self, problem, epoch=10000, pop_size=100, c1=2.05, c2=2.05, w_min=0.4, w_max=0.9, **kwargs):
        """
        Args:
            problem ():
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
            c1 (float): [0-2] local coefficient
            c2 (float): [0-2] global coefficient
            w_min (float): Weight min of bird, default = 0.4
            w_max (float): Weight max of bird, default = 0.9
            **kwargs ():
        """
        super().__init__(problem, kwargs)
        self.nfe_per_epoch = pop_size
        self.sort_flag = False

        self.epoch = epoch
        self.pop_size = pop_size
        self.c1 = c1
        self.c2 = c2
        self.w_min = w_min
        self.w_max = w_max

        self.v_max = 0.5 * (self.problem.ub - self.problem.lb)
        self.v_min = -self.v_max

    def create_solution(self):
        """
        Returns:
            The position position with 2 element: index of position/location and index of fitness wrapper
            The general format: [position, [target, [obj1, obj2, ...]]]

        ## To get the position, fitness wrapper, target and obj list
        ##      A[self.ID_POS]                  --> Return: position
        ##      A[self.ID_FIT]                  --> Return: [target, [obj1, obj2, ...]]
        ##      A[self.ID_FIT][self.ID_TAR]     --> Return: target
        ##      A[self.ID_FIT][self.ID_OBJ]     --> Return: [obj1, obj2, ...]
        """
        position = np.random.uniform(self.problem.lb, self.problem.ub)
        fitness = self.get_fitness_position(position=position)
        velocity = np.random.uniform(self.v_min, self.v_max)
        local_pos = deepcopy(position)
        local_fit = deepcopy(fitness)
        return [position, fitness, velocity, local_pos, local_fit]

    def evolve(self, epoch):
        """
        Args:
            epoch (int): The current iteration
        """
        # Update weight after each move count  (weight down)
        w = (self.epoch - epoch) / self.epoch * (self.w_max - self.w_min) + self.w_min
        pop_new = []
        for idx in range(0, self.pop_size):
            agent = deepcopy(self.pop[idx])
            v_new = w * self.pop[idx][self.ID_VEC] + self.c1 * np.random.rand() * \
                    (self.pop[idx][self.ID_LOP] - self.pop[idx][self.ID_POS]) + \
                    self.c2 * np.random.rand() * (self.g_best[self.ID_POS] - self.pop[idx][self.ID_POS])
            # v_new = np.clip(v_new, self.v_min, self.v_max)
            x_new = self.pop[idx][self.ID_POS] + v_new  # Xi(new) = Xi(old) + Vi(new) * deltaT (deltaT = 1)
            pos_new = self.amend_position_random(x_new)
            agent[self.ID_POS] = pos_new
            agent[self.ID_VEC] = v_new
            pop_new.append(agent)
        pop_new = self.update_fitness_population(pop_new)

        for idx in range(0, self.pop_size):
            if self.compare_agent(pop_new[idx], self.pop[idx]):
                self.pop[idx] = deepcopy(pop_new[idx])
                if self.compare_agent(pop_new[idx], [None, self.pop[idx][self.ID_LOF]]):
                    self.pop[idx][self.ID_LOP] = deepcopy(pop_new[idx][self.ID_POS])
                    self.pop[idx][self.ID_LOF] = deepcopy(pop_new[idx][self.ID_FIT])


class PPSO(Optimizer):
    """
        A variant version of PSO: Phasor particle swarm optimization: a simple and efficient variant of PSO
    Link:
        Phasor particle swarm optimization: a simple and efficient variant of PSO
    Notes:
        This code is converted from matlab code (sent from author: Ebrahim Akbari)
    """
    ID_VEC = 2  # Velocity
    ID_LOP = 3  # Local position
    ID_LOF = 4  # Local fitness

    def __init__(self, problem, epoch=10000, pop_size=100, **kwargs):
        """
        Args:
            problem ():
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
            **kwargs ():
        """
        super().__init__(problem, kwargs)
        self.nfe_per_epoch = pop_size
        self.sort_flag = False

        self.epoch = epoch
        self.pop_size = pop_size
        self.v_max = 0.5 * (self.problem.ub - self.problem.lb)
        self.v_min = -self.v_max

        # Dynamic variable
        self.dyn_delta_list = np.random.uniform(0, 2 * np.pi, self.pop_size)

    def create_solution(self):
        position = np.random.uniform(self.problem.lb, self.problem.ub)
        fitness = self.get_fitness_position(position=position)
        velocity = np.random.uniform(self.v_min, self.v_max)
        local_pos = deepcopy(position)
        local_fit = deepcopy(fitness)
        return [position, fitness, velocity, local_pos, local_fit]

    def evolve(self, epoch):
        """
        Args:
            epoch (int): The current iteration
        """
        pop_new = []
        for i in range(0, self.pop_size):
            agent = deepcopy(self.pop[i])
            aa = 2 * (np.sin(self.dyn_delta_list[i]))
            bb = 2 * (np.cos(self.dyn_delta_list[i]))
            ee = np.abs(np.cos(self.dyn_delta_list[i])) ** aa
            tt = np.abs(np.sin(self.dyn_delta_list[i])) ** bb

            v_new = ee * (self.pop[i][self.ID_LOP] - self.pop[i][self.ID_POS]) + tt * (self.g_best[self.ID_POS] - self.pop[i][self.ID_POS])
            v_new = np.minimum(np.maximum(v_new, -self.v_max), self.v_max)
            agent[self.ID_VEC] = deepcopy(v_new)

            x_temp = self.pop[i][self.ID_POS] + v_new
            x_temp = np.minimum(np.maximum(x_temp, self.problem.lb), self.problem.ub)
            agent[self.ID_POS] = x_temp

            self.dyn_delta_list[i] += np.abs(aa + bb) * (2 * np.pi)
            self.v_max = (np.abs(np.cos(self.dyn_delta_list[i])) ** 2) * (self.problem.ub - self.problem.lb)
            pop_new.append(agent)
        # Update fitness for all solutions
        pop_new = self.update_fitness_population(pop_new)

        # Update current position, current velocity and compare with past position, past fitness (local best)
        for idx in range(0, self.pop_size):
            if self.compare_agent(pop_new[idx], self.pop[idx]):
                self.pop[idx] = deepcopy(pop_new[idx])
                if self.compare_agent(pop_new[idx], [None, self.pop[idx][self.ID_LOF]]):
                    self.pop[idx][self.ID_LOP] = deepcopy(pop_new[idx][self.ID_POS])
                    self.pop[idx][self.ID_LOF] = deepcopy(pop_new[idx][self.ID_FIT])


class HPSO_TVAC(PPSO):
    """
        The variant version of PSO:
            Self-organising Hierarchical PSO with Time-Varying Acceleration Coefficients (HPSO_TVAC)
        Link:
            New self-organising hierarchical PSO with jumping time-varying acceleration coefficients
        Note:
            This code is converted from matlab code (sent from author: Ebrahim Akbari)
    """

    def __init__(self, problem, epoch=10000, pop_size=100, ci=0.5, cf=0.0, **kwargs):
        """
        Args:
            problem ():
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
            **kwargs ():
        """
        super().__init__(problem, epoch, pop_size, **kwargs)
        self.nfe_per_epoch = pop_size
        self.sort_flag = False

        self.epoch = epoch
        self.pop_size = pop_size
        self.ci = ci
        self.cf = cf

    def evolve(self, epoch):
        """
        Args:
            epoch (int): The current iteration
        """
        c_it = ((self.cf - self.ci) * ((epoch + 1) / self.epoch)) + self.ci
        pop_new = []
        for i in range(0, self.pop_size):
            agent = deepcopy(self.pop[i])
            idx_k = np.random.randint(0, self.pop_size)
            w = np.random.normal()
            while (np.abs(w - 1.0) < 0.01):
                w = np.random.normal()
            c1_it = np.abs(w) ** (c_it * w)
            c2_it = np.abs(1 - w) ** (c_it / (1 - w))

            #################### HPSO
            v_new = c1_it * np.random.uniform(0, 1, self.problem.n_dims) * (self.pop[i][self.ID_LOP] - self.pop[i][self.ID_POS]) + \
                        c2_it * np.random.uniform(0, 1, self.problem.n_dims) * \
                    (self.g_best[self.ID_POS] + self.pop[idx_k][self.ID_LOP] - 2 * self.pop[i][self.ID_POS])

            np.where(v_new == 0, np.sign(0.5 - np.random.uniform()) * np.random.uniform() * self.v_max, v_new)
            v_new = np.sign(v_new) * np.minimum(np.abs(v_new), self.v_max)
            #########################

            v_new = np.minimum(np.maximum(v_new, -self.v_max), self.v_max)
            x_temp = self.pop[i][self.ID_POS] + v_new
            pos_new = np.minimum(np.maximum(x_temp, self.problem.lb), self.problem.ub)
            agent[self.ID_VEC] = v_new
            agent[self.ID_POS] = pos_new
            pop_new.append(agent)

            # Update fitness for all solutions
        pop_new = self.update_fitness_population(pop_new)

        # Update current position, current velocity and compare with past position, past fitness (local best)
        for idx in range(0, self.pop_size):
            if self.compare_agent(pop_new[idx], self.pop[idx]):
                self.pop[idx] = deepcopy(pop_new[idx])
                if self.compare_agent(pop_new[idx], [None, self.pop[idx][self.ID_LOF]]):
                    self.pop[idx][self.ID_LOP] = deepcopy(pop_new[idx][self.ID_POS])
                    self.pop[idx][self.ID_LOF] = deepcopy(pop_new[idx][self.ID_FIT])


class C_PSO(BasePSO):
    """
        Version: Chaos Particle Swarm Optimization (C-PSO)
        Link
            Improved particle swarm optimization combined with chaos
    """

    def __init__(self, problem, epoch=10000, pop_size=100, c1=1.2, c2=1.2, w_min=0.2, w_max=1.2, **kwargs):
        """
        Args:
            problem ():
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
            c1 (float): [0-2] local coefficient
            c2 (float): [0-2] global coefficient
            w_min (float): Weight min of bird, default = 0.2
            w_max (float): Weight max of bird, default = 1.2
            **kwargs ():
        """
        super().__init__(problem, epoch, pop_size, c1, c2, w_min, w_max, **kwargs)
        self.nfe_per_epoch = pop_size
        self.sort_flag = False

        self.epoch = epoch
        self.pop_size = pop_size
        self.c1 = c1
        self.c2 = c2
        self.w_min = w_min
        self.w_max = w_max

        self.v_max = 0.5 * (self.problem.ub - self.problem.lb)
        self.v_min = -self.v_max
        self.N_CLS = int(self.pop_size / 5)  # Number of chaotic local searches

        # Dynamic variable
        self.dyn_lb = deepcopy(self.problem.lb)
        self.dyn_ub = deepcopy(self.problem.ub)

    def __get_weights__(self, fit, fit_avg, fit_min):
        temp1 = self.w_min + (self.w_max - self.w_min) * (fit - fit_min) / (fit_avg - fit_min)
        if self.problem.minmax == "min":
            output = temp1 if fit <= fit_avg else self.w_max
        else:
            output = self.w_max if fit <= fit_avg else temp1
        return output

    def evolve(self, epoch):
        """
        Args:
            epoch (int): The current iteration
        """
        nfe_epoch = 0
        list_fits = [item[self.ID_FIT][self.ID_TAR] for item in self.pop]
        fit_avg = np.mean(list_fits)
        fit_min = np.min(list_fits)
        pop_new = []
        for i in range(self.pop_size):
            agent = deepcopy(self.pop[i])
            w = self.__get_weights__(self.pop[i][self.ID_FIT][self.ID_TAR], fit_avg, fit_min)
            v_new = w * self.pop[i][self.ID_VEC] + self.c1 * np.random.rand() * (self.pop[i][self.ID_LOP] - self.pop[i][self.ID_POS]) + \
                    self.c2 * np.random.rand() * (self.g_best[self.ID_POS] - self.pop[i][self.ID_POS])
            v_new = np.clip(v_new, self.v_min, self.v_max)
            x_new = self.pop[i][self.ID_POS] + v_new
            agent[self.ID_VEC] = v_new
            agent[self.ID_POS] = x_new
            pop_new.append(agent)

        # Update fitness for all solutions
        pop_new = self.update_fitness_population(pop_new)
        nfe_epoch += self.pop_size

        # Update current position, current velocity and compare with past position, past fitness (local best)
        for idx in range(0, self.pop_size):
            if self.compare_agent(pop_new[idx], self.pop[idx]):
                self.pop[idx] = deepcopy(pop_new[idx])
                if self.compare_agent(pop_new[idx], [None, self.pop[idx][self.ID_LOF]]):
                    self.pop[idx][self.ID_LOP] = deepcopy(pop_new[idx][self.ID_POS])
                    self.pop[idx][self.ID_LOF] = deepcopy(pop_new[idx][self.ID_FIT])

        ## Implement chaostic local search for the best solution
        g_best = self.g_best
        cx_best_0 = (self.g_best[self.ID_POS] - self.problem.lb) / (self.problem.ub - self.problem.lb)  # Eq. 7
        cx_best_1 = 4 * cx_best_0 * (1 - cx_best_0)  # Eq. 6
        x_best = self.problem.lb + cx_best_1 * (self.problem.ub - self.problem.lb)  # Eq. 8
        x_best = self.amend_position_faster(x_best)
        fit_best = self.get_fitness_position(x_best)
        if self.compare_agent([x_best, fit_best], self.g_best):
            g_best = [x_best, fit_best]

        r = np.random.rand()
        bound_min = np.stack([self.dyn_lb, g_best[self.ID_POS] - r * (self.dyn_ub - self.dyn_lb)])
        self.dyn_lb = np.max(bound_min, axis=0)
        bound_max = np.stack([self.dyn_ub, g_best[self.ID_POS] + r * (self.dyn_ub - self.dyn_lb)])
        self.dyn_ub = np.min(bound_max, axis=0)

        pop_new_child = self.create_population(self.pop_size - self.N_CLS)
        self.pop = self.get_sorted_strim_population(self.pop + pop_new_child, self.pop_size)
        nfe_epoch += 1 + (self.pop_size - self.N_CLS)
        self.nfe_per_epoch = nfe_epoch


class CL_PSO(Optimizer):
    """
        Version: Comprehensive Learning Particle Swarm Optimization (CL-PSO)
        Link
            Comprehensive Learning Particle Swarm Optimizer for Global Optimization of Multimodal Functions
    """
    ID_VEC = 2
    ID_LOP = 3
    ID_LOF = 4

    def __init__(self, problem, epoch=10000, pop_size=100, c_local=1.2, w_min=0.4, w_max=0.9, max_flag=7, **kwargs):
        """
        Args:
            problem ():
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
            c1 (float): [0-2] local coefficient
            c2 (float): [0-2] global coefficient
            w_min (float): Weight min of bird, default = 0.2
            w_max (float): Weight max of bird, default = 1.2
            max_flag (int): Number of times, default = 7
            **kwargs ():
        """
        super().__init__(problem, kwargs)
        self.nfe_per_epoch = pop_size
        self.sort_flag = False

        self.epoch = epoch
        self.pop_size = pop_size
        self.c_local = c_local  # Local coefficient
        self.w_min = w_min  # [0-1] -> [0.4-0.9]      Weight of bird
        self.w_max = w_max
        self.max_flag = max_flag

        self.v_max = 0.5 * (self.problem.ub - self.problem.lb)
        self.v_min = -self.v_max

        # Dynamic variable
        self.flags = np.zeros(self.pop_size)

    def create_solution(self):
        position = np.random.uniform(self.problem.lb, self.problem.ub)
        fitness = self.get_fitness_position(position=position)
        velocity = np.random.uniform(self.v_min, self.v_max)
        local_pos = deepcopy(position)
        local_fit = deepcopy(fitness)
        return [position, fitness, velocity, local_pos, local_fit]

    def evolve(self, epoch):
        """
        Args:
            epoch (int): The current iteration
        """
        wk = self.w_max * (epoch / self.epoch) * (self.w_max - self.w_min)
        pop_new = []
        for i in range(0, self.pop_size):
            agent = deepcopy(self.pop[i])
            if self.flags[i] >= self.max_flag:
                self.flags[i] = 0
                agent = self.create_solution()

            pci = 0.05 + 0.45 * (np.exp(10 * (i + 1) / self.pop_size) - 1) / (np.exp(10) - 1)

            vec_new = deepcopy(self.pop[i][self.ID_VEC])
            for j in range(0, self.problem.n_dims):
                if np.random.rand() > pci:
                    vj = wk * self.pop[i][self.ID_VEC][j] + self.c_local * np.random.rand() * \
                         (self.pop[i][self.ID_LOP][j] - self.pop[i][self.ID_POS][j])
                else:
                    id1, id2 = np.random.choice(list(set(range(0, self.pop_size)) - {i}), 2, replace=False)
                    if self.compare_agent(self.pop[id1], self.pop[id2]):
                        vj = wk * self.pop[i][self.ID_VEC][j] + self.c_local * np.random.rand() *\
                             (self.pop[id1][self.ID_LOP][j] - self.pop[i][self.ID_POS][j])
                    else:
                        vj = wk * self.pop[i][self.ID_VEC][j] + self.c_local * np.random.rand() * \
                             (self.pop[id2][self.ID_LOP][j] - self.pop[i][self.ID_POS][j])
                vec_new[j] = vj
            vec_new = np.clip(vec_new, self.v_min, self.v_max)
            pos_new = self.pop[i][self.ID_POS] + vec_new
            pos_new = self.amend_position_faster(pos_new)
            agent[self.ID_VEC] = vec_new
            agent[self.ID_POS] = pos_new
            pop_new.append(agent)
        pop_new = self.update_fitness_population(pop_new)

        # Update current position, current velocity and compare with past position, past fitness (local best)
        for idx in range(0, self.pop_size):
            if self.compare_agent(pop_new[idx], self.pop[idx]):
                self.pop[idx] = deepcopy(pop_new[idx])
                if self.compare_agent(pop_new[idx], [None, self.pop[idx][self.ID_LOF]]):
                    self.pop[idx][self.ID_LOP] = deepcopy(pop_new[idx][self.ID_POS])
                    self.pop[idx][self.ID_LOF] = deepcopy(pop_new[idx][self.ID_FIT])
                    self.flags[idx] = 0
                else:
                    self.flags[idx] += 1
