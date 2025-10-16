import random

class ANDOR:
    def __init__(self, screen, font, tile_size):
        self.screen = screen
        self.font = font
        self.tile_size = tile_size
        self.state_counter = 0
        self.Is_goal = "No"

    def OR(self, board, state, full_state, paths, p_index):
        solutions = []
        self.state_counter += 1
        index = self.state_counter
        paths[index] = (p_index, state[:])

        full_state.append({
            "state_index": index,
            "state": state[:],
            "node": "OR",
            "cost": None,
            "heuristic": None,
            "limit": None,
            "T": None,
            "accept": None,
            "K": None,
            "is_goal": self.Is_goal
        })
        paths[index] = (p_index, state[:])

        row = len(state)
        for col in range(8):
            if (board.Is_Safe(state, row, col)):
                new_state = state + [(row, col)]
                result = self.AND(board, new_state, full_state, paths, index)
                solutions.extend(result)
        return solutions

    def AND(self, board, result, full_state, paths, p_index):
        self.state_counter += 1
        index = self.state_counter
        paths[index] = (p_index, result[:])
        Is_goal = "No"
        if(len(result) == 8):
            Is_goal = "Yes"
            self.state_counter += 1
            index = self.state_counter
            full_state.append({
                "state_index": index,
                "state": result[:],
                "node": "AND",
                "cost": None,
                "heuristic": None,
                "limit": None,
                "T": None,
                "accept": None,
                "K": None,
                "is_goal": Is_goal
            })
            return [result]

        full_state.append({
            "state_index": index,
            "state": result[:],
            "node": "AND",
            "cost": None,
            "heuristic": None,
            "limit": None,
            "T": None,
            "accept": None,
            "K": None,
            "is_goal": Is_goal
        })
        return self.OR(board, result, full_state, paths, index)

    def Solve(self, board, goal_state=None):
        paths = {}
        full_state = []
        """initial_state = [(0, i) for i in range(8)]
        initial_node = random.choice(initial_state)""" #sd khi tim giai phap 1 nhanh random


        solutions = self.OR(board, [], full_state, paths, None)
        if not(solutions): return full_state, iter([])

        random_solution = random.choice(solutions)
        goal_index = None
        for node in full_state:
            if node["state"] == random_solution and node["node"] == "OR":
                goal_index = node["state_index"]
                break

        goal_path = []
        i = goal_index
        while i is not None:
            path_index, state = paths.get(i, (None, []))
            goal_path.append(state)
            i = path_index
        goal_path.reverse()

        full_state.append({
            "state_index": None,
            "state": solutions,
            "node": "AND",
            "cost": None,
            "heuristic": None,
            "limit": None,
            "T": None,
            "accept": None,
            "K": None,
            "is_goal": self.Is_goal
        })
        for s in solutions: print(list(s))

        return full_state, (s for s in goal_path)