import pygame
import numpy as np
from Board import Board
from collections import deque

class IDS:
    def __init__(self, screen, font, tile_size):
        self.screen = screen
        self.font = font
        self.tile_size = tile_size

    def Solve_DLS(self, board, goal, limit):
        goal_state = set(goal)
        queue = deque([([], 0, None, 0)])
        queue_num = 0
        paths = {}
        full_state = []

        while (queue):
            state, index, path, depth = queue.pop()
            paths[index] = (path, state)
            if (set(state) == goal_state): Is_goal = "Yes"
            else: Is_goal = "No"

            full_state.append({
                "state_index": index,
                "state": state,
                "cost": None,
                "heuristic": None,
                "limit": None,
                "T": None,
                "accept": None,
                "K": None,
                "is_goal": Is_goal
            })

            if (Is_goal == "Yes"):
                goal_path = []
                i = index
                while i is not None:
                    path_index, path_state = paths[i]
                    goal_path.append(path_state)
                    i = path_index
                goal_path.reverse()

                return full_state, (s for s in goal_path)

            if (depth < limit):
                row = len(state)
                if (row < 8):
                    for col in range(8):
                        if (board.Is_Safe(state, row, col)):
                            queue_num += 1
                            queue.append((state + [(row, col)], queue_num, index, depth + 1))

        return full_state, None

    def Solve(self, board, goal, limit):
        final = []
        for i in range(1, limit + 1):
            full_state, DLS = self.Solve_DLS(board, goal, i)
            final.extend(full_state)
            if(DLS is not None):
                return final, (s for s in DLS)
        return final, iter([])