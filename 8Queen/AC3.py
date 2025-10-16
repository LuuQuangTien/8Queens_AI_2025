from collections import deque

class AC3:
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
            next_domain = {r: set(c) for r, c in domain.items()}
            next_domain[row] = {c}
            if (self.AC3(next_domain)):
                new_state = state + [(row, c)]
                result = self.Backtracking(board, new_state, paths, index, next_domain)
                if (result): return result
        return None

    def Constraints(self, A, B, col_A, col_B):
        return (col_A != col_B) and (abs(A - B) != abs(col_A - col_B))

    def AC3(self,domain):
        queue = deque([(i, j) for i in range(8) for j in range(8) if i != j])

        while queue:
            A, B = queue.popleft()
            if(self.Arc_check(domain, A, B)):
                if not(domain[A]): return False
                for i in range(8):
                    if i != A and i != B:
                        queue.append((i, A))
        return True

    def Arc_check(self, domain, A, B):
        removed_domain = set()
        for i in domain[A]:
            if not(any(self.Constraints(A, B, i, j) for j in domain[B])):
                removed_domain.add(i)
        if(removed_domain):
            domain[A] -= removed_domain
            return True
        return False

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