import pygame
import tkinter as tk
from tkinter import ttk
import numpy as np

class Board:
    def __init__(self, screen, color, x, y, size, font):
        self.size = size
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.font = font
        self.grid = np.zeros((8, 8), dtype=int)
        self.attack = np.zeros((8, 8), dtype=int)
    
    def draw(self):
        for row in range(8):
            for col in range(8):
                flag = self.grid[row, col]
                x = self.x + col * self.size
                y = self.y + row * self.size

                if((row + col) % 2 == 0): pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x, y, self.size, self.size))
                else: pygame.draw.rect(self.screen, self.color, pygame.Rect(x, y, self.size, self.size))

                if(flag == 2):
                    queen_star = self.font.render("Q", True, (255, 0, 0))
                    queen_rect = queen_star.get_rect(center=(x + self.size//2, y + self.size//2))
                    self.screen.blit(queen_star, queen_rect)

                if(self.attack[row, col] == 1):
                    surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                    surf.fill((255, 0, 0, 128))
                    self.screen.blit(surf, (x, y))

    Chessboard_Left = np.zeros((8, 8), dtype=int)
    Chessboard_Right = np.zeros((8, 8), dtype=int)

    def CheckPath(self, x, y, board = None):
        if (board is not None):
            grid = board
        else:
            grid = self.grid

        if (np.any(grid[:, x] == 2) or np.any(grid[y, :] == 2)): return False
        if (np.any(np.diagonal(grid, offset=x - y) == 2) or np.any(
            np.diag(np.fliplr(grid), k=(7 - x) - y) == 2)): return False
        return True

    def UpdateBoard(self):
        self.attack = np.zeros_like(self.grid)
        queens = np.argwhere(self.grid == 2)

        for y, x in queens:
            new_grid = np.zeros_like(self.grid)
            new_grid[:, x] = 1
            new_grid[y, :] = 1

            for i in range(-7, 8):
                r1, c1 = y + i, x + i
                r2, c2 = y + i, x - i
                if(0 <= r1 < 8 and 0 <= c1 < 8):
                    new_grid[r1, c1] = 1
                if(0 <= r2 < 8 and 0 <= c2 < 8):
                    new_grid[r2, c2] = 1
            new_grid[y, x] = 0
            self.attack |= new_grid

        return self.attack

    def PlaceQueenPath(self, x, y, board = None, mark_only=False):
        if(board is not None):
            grid = board
        else:
            grid = self.grid

        if(not mark_only and self.grid[y, x] == 2):
            grid[y, x] = 0
            self.UpdateBoard()
            return True

        if(self.CheckPath(x, y, board)):
            if(not mark_only):
                grid[y, x] = 2
                self.UpdateBoard()
            return True
        else:
            if(not mark_only):
                print("Da co con hau tren duong di")
            return False

    def Is_Safe(self, state, row, col):
        for r, c in state:
            if ((c == col) or (abs(r - row) == abs(c - col))):
                return False
        return True

class State_window:
    def __init__(self, full_states, goal_state = None, page_size = 200):
        self.full_states = full_states
        self.goal_state = goal_state
        self.page_size = page_size
        self.current_page = 0
        self.font = ("Arial", 12)

        self.root = tk.Tk()
        self.root.title("Solving Process")
        self.root.geometry("700x500")

        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(frame, columns=("state_index", "queens", "node", "cost",
                                "heuristic", "limit", "T", "accept", "K", "is_goal"), show="headings")

        self.tree.heading("state_index", text="State")
        self.tree.heading("queens", text="Queens position")
        self.tree.heading("node", text="Node")
        self.tree.heading("cost", text="Cost")
        self.tree.heading("heuristic", text="Heuristic")
        self.tree.heading("limit", text="Limit")
        self.tree.heading("T", text="Temperature")
        self.tree.heading("accept", text="Accept")
        self.tree.heading("K", text="Beam width")
        self.tree.heading("is_goal", text="Check goal")

        self.tree.column("state_index", width=50, anchor="center")
        self.tree.column("queens", width=300, anchor="w")
        self.tree.column("node", width=40, anchor="center")
        self.tree.column("cost", width=40, anchor="center")
        self.tree.column("heuristic", width=40, anchor="center")
        self.tree.column("limit", width=40, anchor="center")
        self.tree.column("T", width=40, anchor="center")
        self.tree.column("accept", width=40, anchor="center")
        self.tree.column("K", width=40, anchor="center")
        self.tree.column("is_goal", width=80, anchor="center")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True, side="left")

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side="bottom", fill="x", pady=5)
        self.btn_prev = tk.Button(bottom_frame, text="Previous", command=self.prev_page)
        self.btn_next = tk.Button(bottom_frame, text="Next", command=self.next_page)
        self.btn_prev.pack(side="left", padx=10)
        self.btn_next.pack(side="right", padx=10)

        self.show_page()
        self.root.mainloop()

    def show_page(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        start = self.current_page * self.page_size
        end = min(start + self.page_size, len(self.full_states))

        for i, s in enumerate(self.full_states[start:end], start=start):
            state_index = s.get("state_index", 0)
            state = str(s.get("state", []))
            node = str(s.get("node", []))
            cost = s.get("cost", 0)
            heuristic = s.get("heuristic", 0)
            limit = s.get("limit", 0)
            T = s.get("T", 0)
            accept = s.get("accept", "")
            K = s.get("K", 0)
            is_goal = s.get("is_goal", "")

            self.tree.insert('', 'end', values=(f"State {state_index}", state, node, cost, heuristic, limit, T, accept, K, is_goal))

    def next_page(self):
        if((self.current_page + 1) * self.page_size < len(self.full_states)):
            self.current_page += 1
            self.show_page()

    def prev_page(self):
        if(self.current_page > 0):
            self.current_page -= 1
            self.show_page()