import numpy as np
import heapq

class UCS:
    def __init__(self, screen, font, tile_size):
        self.screen = screen
        self.font = font
        self.tile_size = tile_size

    def Solve(self, board, goal):
        goal_state = set(goal)
        queue = [(0, [], 0, None)]
        queue_num = 0
        paths = {}
        Is_goal = "No"
        full_state = [{
            "state_index": queue_num,
            "state": [],
            "cost": 0,
            "heuristic": None,
            "limit": None,
            "T": None,
            "accept": None,
            "K": None,
            "is_goal": Is_goal
        }]

        while (queue):
            cost, state, index, path = heapq.heappop(queue)
            paths[index] = (path, state)
            if (Is_goal == "Yes"):
                goal_path = []
                i = index
                while i is not None:
                    path_index, path_state = paths[i]
                    goal_path.append(path_state)
                    i = path_index
                goal_path.reverse()

                return full_state, (s for s in goal_path)

            row = len(state)
            if (row >= 8): continue
            for col in range(8):
                if (board.Is_Safe(state, row, col)):
                    new_state = state + [(row, col)]
                    new_cost = cost + self.Count_cost(board, state, row, col)
                    queue_num += 1
                    heapq.heappush(queue, (new_cost, state + [(row, col)], queue_num, index))

                    if (set(new_state) == goal_state): Is_goal = "Yes"
                    else: Is_goal = "No"
                    full_state.append({
                        "state_index": queue_num,
                        "state": new_state,
                        "cost": new_cost,
                        "heuristic": None,
                        "limit": None,
                        "T": None,
                        "accept": None,
                        "K": None,
                        "is_goal": Is_goal
                    })
        return full_state, iter([])

    def Count_cost(self, board, state, row, col):
        board_current = np.zeros((8, 8), dtype=int)
        for (r, c) in state:
            board.PlaceQueenPath(c, r, board_current)

        board_new = board_current.copy()
        board.PlaceQueenPath(col, row, board_new)

        return (np.count_nonzero(board_new)) - (np.count_nonzero(board_current))