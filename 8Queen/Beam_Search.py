import heapq

class BEAM:
    def __init__(self, screen, font, tile_size):
        self.screen = screen
        self.font = font
        self.tile_size = tile_size

    def Solve(self, board, K):
        queue_num = 0
        queue = [(0, queue_num, [], None)]
        paths = {}
        Is_goal = "No"
        full_state = [{
            "state_index": queue_num,
            "state": [],
            "cost": None,
            "heuristic": 0,
            "limit": None,
            "T": None,
            "accept": None,
            "K": K,
            "is_goal": Is_goal
        }]

        while(queue):
            selected_states = []
            while(queue):
                h, index, state, path = heapq.heappop(queue)
                paths[index] = (path, state)
                if(Is_goal == "Yes"):
                    goal_path = []
                    i = index
                    while i is not None:
                        path_index, path_state = paths[i]
                        goal_path.append(path_state)
                        i = path_index
                    goal_path.reverse()

                    return full_state, (s for s in goal_path)

                row = len(state)
                if row < 8:
                    for col in range(8):
                        if board.Is_Safe(state, row, col):
                            queue_num += 1
                            new_state = state + [(row, col)]
                            h_new = self.Heuristic_calc(board, new_state)
                            heapq.heappush(selected_states, (h_new, queue_num, new_state, index))

                            if(len(state) == 8 and self.Heuristic_calc(board, state) == 0): Is_goal = "Yes"
                            else: Is_goal = "No"
                            full_state.append({
                                "state_index": queue_num,
                                "state": new_state,
                                "cost": None,
                                "heuristic": h_new,
                                "limit": None,
                                "T": None,
                                "accept": None,
                                "K": K,
                                "is_goal": Is_goal
                            })
            queue = []
            for i in range(min(K, len(selected_states))):
                heapq.heappush(queue, heapq.heappop(selected_states))
        print("Khong tin duoc trang thai muc tieu, hay tang do rong K")
        return full_state, iter([])

    def Heuristic_calc(self, board, state):
        heuristic = 0
        for i in range(len(state)):
            row, col = state[i]
            if not (board.Is_Safe(state[:i], row, col)):
                heuristic += 1
        return heuristic