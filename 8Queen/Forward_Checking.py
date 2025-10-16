class FORWARD_CHECKING:
    def __init__(self, screen, font, tile_size):
        self.screen = screen
        self.font = font
        self.tile_size = tile_size
        self.num = 0
        self.full_state = []

    def Backtracking(self, board, state, paths, path_index, domain):
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
        for c in domain[row]:
            next_domain = self.Forward_checking(domain, row, c)
            if(next_domain):
                new_state = state + [(row, c)]
                result = self.Backtracking(board, new_state, paths, index, next_domain)
                if(result): return result
        return None

    def Forward_checking(self, domain, row, col):
        next_domain = {r: set(c) for r, c in domain.items()}
        for r in range(row + 1, 8):
            if(col in next_domain[r]): next_domain[r].remove(col)
            if((col + (r - row)) in next_domain[r]): next_domain[r].remove((col + (r - row)))
            if((col - (r - row)) in next_domain[r]): next_domain[r].remove((col - (r - row)))
            if not(next_domain[r]): return None

        return next_domain

    def Solve(self, board):
        self.full_state = []
        self.index = 0
        paths = {}
        domain = {r: set(range(8)) for r in range(8)}
        result = self.Backtracking(board, [], paths, None, domain)

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