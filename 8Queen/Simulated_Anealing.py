import numpy as np
import random

class SIM:
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

    def Solve(self, board, initial_state, T, alpha):
        X = initial_state
        X_cost = self.Heuristic_calc(board, X)
        if (X_cost == 0): Is_goal = "Yes"
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
            nonlocal X, X_cost, index, T
            yield X
            while True:
                N = self.Next_state(X)
                neighbor = random.choice(N)
                N_cost = self.Heuristic_calc(board, neighbor)

                delta = N_cost - X_cost
                accept = None
                if delta <= 0:
                    X = neighbor
                    X_cost = N_cost
                    accept = "Yes"
                else:
                    P = np.exp(-delta / T)
                    if random.random() < P:
                        X = neighbor
                        X_cost = N_cost
                        accept = "Yes"
                    else: accept = "No"

                index += 1
                if(X_cost == 0): Is_goal = "Yes"
                else: Is_goal = "No"

                full_state.append({
                    "state_index": index,
                    "state": X.copy(),
                    "cost": None,
                    "heuristic": X_cost,
                    "limit": None,
                    "T": T,
                    "accept": accept,
                    "K": None,
                    "is_goal": Is_goal
                })
                T *= alpha
                if T < 1e-5:
                    print("Nhiet do qua lanh, khong tim duoc muc tieu")
                    break

                if(Is_goal == "Yes"):
                    print("Da tim duoc 8 con hau")
                    break
            yield X

        return full_state, Goal_state()

#T = 10
#alpha = 0.99