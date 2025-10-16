import pygame
import numpy as np
from Board import Board
import random

class HILL:
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

    def Solve(self, board, initial_state):
        X = initial_state
        X_cost = self.Heuristic_calc(board, X)
        if(X_cost == 0): Is_goal = "Yes"
        else: Is_goal = "No"
        index = 0
        full_state = [{
             "state_index": index,
             "state": X.copy(),
             "cost": None,
             "heuristic": X_cost,
             "limit": None,
             "T": None,
             "accept": None,
             "K": None,
             "is_goal": Is_goal
        }]

        def Goal_state():
            nonlocal X, X_cost, index, full_state
            while True:
                if X_cost == 0:
                    break

                N = self.Next_state(X)
                N_cost = [self.Heuristic_calc(board, n) for n in N]
                best_N = np.argmin(N_cost)
                if(N_cost[best_N] >= X_cost):
                    print("Khong tim duoc trang thai tot hon")
                    break

                X = N[best_N]
                X_cost = N_cost[best_N]
                index += 1
                if(X_cost == 0):
                    print("Da tim duoc 8 con hau")
                    Is_goal = "Yes"
                else: Is_goal = "No"

                full_state.append({
                    "state_index": index,
                    "state": X.copy(),
                    "cost": None,
                    "heuristic": X_cost,
                    "limit": None,
                    "T": None,
                    "accept": None,
                    "K": None,
                    "is_goal": Is_goal
                })
                yield X
                if(Is_goal == "Yes"): break

        return full_state, Goal_state()