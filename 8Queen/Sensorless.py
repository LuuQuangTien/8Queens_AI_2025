from random import choice
from collections import deque

class SENSORLESS:
    def __init__(self, screen, font, tile_size):
        self.screen = screen
        self.font = font
        self.tile_size = tile_size

    def Predict(self, board, belief_state, row):
        new_belief_state = []
        for state in belief_state:
            candidates = []
            for col in range(8):
                if(board.Is_Safe(state, row, col)):  candidates.append(state + ((row, col),))
            if(candidates): new_belief_state.append(frozenset(candidates))
        return new_belief_state

    def Prune_superset(self, belief_state, explored):
        pruned_belief_state = []
        for state in belief_state:
            if(any(state.issubset(e) for e in explored)): continue
            pruned_belief_state.append(state)
        return pruned_belief_state

    def Solve(self, board):
        inital_state = frozenset([tuple()])
        queue = deque([(inital_state, 0)])
        explored = [inital_state]
        index = 0
        paths = {}
        full_state = []
        solutions = []

        while(queue):
            belief_state, row = queue.popleft()
            if(row == 8): Is_goal = "Yes"
            else: Is_goal = "No"

            full_state.append({
                "state_index": index,
                "state": [list(s) for s in belief_state],
                "cost": None,
                "heuristic": None,
                "limit": None,
                "T": None,
                "accept": None,
                "K": None,
                "is_goal": Is_goal
            })
            index += 1

            if (Is_goal == "Yes"):
                solutions.extend(list(belief_state))

            if (row >= 8): continue
            new_belief_state = self.Predict(board, belief_state, row)
            new_belief_state = self.Prune_superset(new_belief_state, explored)

            for state in new_belief_state:
                queue.append((state, row + 1))
                explored.append(state)
                paths[state] = belief_state

        if(solutions):
            full_state.append({
                "state_index": index,
                "state": [list(s) for s in solutions],
                "cost": None,
                "heuristic": None,
                "limit": None,
                "T": None,
                "accept": None,
                "K": None,
                "is_goal": Is_goal
            })
            for s in solutions: print(list(s))
        else:
            print("Khong tim duoc trang thai muc tieu")
            return full_state, iter([])

        random_goal = choice(solutions)
        goal_path = [random_goal]
        parent = paths.get(frozenset([random_goal]))
        while parent:
            parent_state = next(iter(parent))
            goal_path.append(parent_state)
            parent = paths.get(parent)
        goal_path.reverse()

        def return_solver():
            for state in goal_path:
                yield list(state)

        return full_state, return_solver()