class BACKTRACKING:
    def __init__(self, screen, font, tile_size):
        self.screen = screen
        self.font = font
        self.tile_size = tile_size
        self.num = 0
        self.full_state = []

    def Backtracking(self, board, state, paths, path_index):
        self.num += 1
        index = self.num
        if (len(state) == 8): Is_goal = "Yes"
        else: Is_goal = "No"

        self.full_state.append({
            "state_index": index,
            "state": state[:],
            "cost": None,
            "heuristic": None,
            "limit": None,
            "T": None,
            "accept": None,
            "K": None,
            "is_goal": Is_goal
        })
        paths[index] = (path_index, state[:])
        if(Is_goal == "Yes"): return state, index

        row = len(state)
        for c in range(8):
            if(board.Is_Safe(state, row, c)):
                new_state = state + [(row, c)]
                result = self.Backtracking(board, new_state, paths, index)
                if(result): return result
        return None

    def Solve(self, board):
        self.full_state = []
        self.index = 0
        paths = {}
        result = self.Backtracking(board, [], paths, None)

        if(result):
            _, goal_index = result
            goal_path = []
            i = goal_index
            while(i is not None):
                path_i, state = paths[i]
                goal_path.append(state)
                i = path_i
            goal_path.reverse()
            return self.full_state, (s for s in goal_path)

        return self.full_state, iter([])