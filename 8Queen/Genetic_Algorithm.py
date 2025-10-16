import pygame
import numpy as np
from Board import Board
import random

class GENETIC:
    def __init__(self, screen, font, tile_size):
        self.screen = screen
        self.font = font
        self.tile_size = tile_size

    def Heuristic_calc(self, board, state):
        heuristic = 0
        for i in range(8):
            row, col = state[i]
            if not (board.Is_Safe(state[:i], row, col)):
                heuristic += 1
        return heuristic

    def Next_state(self, state):
        N = []
        for row, col in state:
            for c in range(8):
                if (c != col):
                    new_state = state.copy()
                    new_state[row] = (row, c)
                    N.append(new_state)
        return N

    def Mutation(self, child, mutation_prob):
        new_child = child.copy()
        if (random.random() < mutation_prob):
            row, col = random.randint(0, 7), random.randint(0, 7)
            new_child[row] = (row, col)
        return new_child

    def Solve(self, board, initial_state, mutation_prob):
        population = sorted(initial_state, key=lambda x: x[1])
        best_state, best_heuristic = population[0]
        index = 0
        if(best_heuristic == 0): Is_goal = "Yes"
        else: Is_goal = "No"
        full_state = [{
            "state_index": index,
            "state": best_state,
            "cost": None,
            "heuristic": best_heuristic,
            "limit": None,
            "T": None,
            "accept": None,
            "K": None,
            "is_goal": Is_goal
        }]

        for i in range(1000):
            (parent1, _), (parent2, _) = population[:2]
            child1 = parent1[:4] + parent2[4:]
            child2 = parent2[:4] + parent1[4:]

            child1 = self.Mutation(child1, mutation_prob)
            child2 = self.Mutation(child2, mutation_prob)

            next_gen = [(child1, self.Heuristic_calc(board, child1)), (child2, self.Heuristic_calc(board, child2))]
            population = sorted(next_gen + population[:2], key=lambda x: x[1])
            index += 1
            if (best_heuristic == 0): Is_goal = "Yes"
            else: Is_goal = "No"
            best_state, best_heuristic = population[0]
            full_state.append({
                "state_index": index,
                "state": best_state.copy(),
                "cost": None,
                "heuristic": best_heuristic,
                "limit": None,
                "T": None,
                "accept": None,
                "K": None,
                "is_goal": Is_goal
            })

            if (Is_goal == "Yes"):
                print("Da tim duoc 8 con hau")
                return full_state, iter([best_state])

        print("Khong tim duoc trang thai cuoi cung")
        return full_state, iter([])
