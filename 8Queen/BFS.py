from collections import deque

class BFS:
    def __init__(self, screen, font, tile_size):
        self.screen = screen
        self.font = font
        self.tile_size = tile_size

    def Solve(self, board, goal):
        goal_state = set(goal)
        queue = deque([([], 0, None)])
        queue_num = 0
        paths = {}
        full_state = []

        while (queue):
            state, index, path = queue.popleft()
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

            row = len(state)
            if (row >= 8): continue
            for col in range(8):
                if (board.Is_Safe(state, row, col)):
                    queue_num += 1
                    queue.append((state + [(row, col)], queue_num, index))
        return full_state, iter([])