import pygame
import random
from Board import Board, State_window
from BFS import BFS
from DFS import DFS
from UCS import UCS
from DLS import DLS
from IDS import IDS
from Greedy import GREEDY
from A_Sao import ASTAR
from Hill_Climbing import HILL
from Simulated_Anealing import SIM
from Beam_Search import BEAM
from Genetic_Algorithm import GENETIC
from Sensorless import SENSORLESS
from Nondeterministic import ANDOR
from Partially_observable import PAR_OBS
from Backtracking import BACKTRACKING
from Forward_Checking import FORWARD_CHECKING
from AC3 import AC3

pygame.init()

#____________Color_______________________
GRAY = (200,200,200)
GREEN = (173, 204, 96)
BLUE = (83, 129, 231)
YELLOW = (221, 217, 29)
WHITE = (255,255,255)
BLACK = (0,0,0)

#____________Display_____________________
screen = pygame.display.set_mode((950, 500))
tile_size = 50
font = pygame.font.Font(None, 35)
screen_width, screen_height = screen.get_size()
window_state = "MENU"
full_state = []

board_left = Board(screen, (0,0,0), 50, 50, tile_size, font)
board_right = Board(screen, (0,0,0), 500, 50, tile_size, font)


running = True

#____________Button_______________________
button_width = 150
button_height = 50

algorithm = None
solver = None

class Button():
    def __init__(self, screen, font, x, y, width, height, text, button_color, text_color):
        self.screen = screen
        self.font = font
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.button_color = button_color
        self.text_color = text_color
        self.clicked = False

    def draw(self, events):
        pressed_color = tuple(int(color * 0.8) for color in self.button_color)
        pressed = False

        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                if (self.rect.collidepoint(pygame.mouse.get_pos())):
                    self.clicked = True
            if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
                if (self.rect.collidepoint(pygame.mouse.get_pos())):
                    pressed = True
                self.clicked = False

        btn_color = pressed_color if (self.clicked) else self.button_color
        pygame.draw.rect(self.screen, btn_color, self.rect)
        btn_txt = self.font.render(self.text, True, self.text_color)
        self.screen.blit(btn_txt, btn_txt.get_rect(center=self.rect.center))
        return pressed

rect_BFS = Button(screen, font, 62.5, 100, button_width, button_height, "BFS", GREEN, BLACK)
rect_DFS = Button(screen, font, button_width + 62.5*2, 100, button_width, button_height, "DFS", GREEN, BLACK)
rect_UCS = Button(screen, font, 62.5, 100 + (button_height + 15), button_width, button_height, "UCS", GREEN, BLACK)
rect_DLS = Button(screen, font, button_width + 62.5*2, 100 + (button_height + 15), button_width, button_height, "DLS", GREEN, BLACK)
rect_IDS = Button(screen, font, 62.5, 100 + (button_height + 15)*2, button_width, button_height, "IDS", GREEN, BLACK)
rect_GREEDY = Button(screen, font, button_width + 62.5*2, 100 + (button_height + 15)*2, button_width, button_height, "GREEDY", GREEN, BLACK)
rect_ASTAR = Button(screen, font, (screen_width // 4) - (button_width // 2) , 100 + (button_height + 15)*3, button_width, button_height, "A*", GREEN, BLACK)

rect_HILL = Button(screen, font, (screen_width // 2) + 25, 100, button_width, button_height, "HILL", YELLOW, BLACK)
rect_SIM = Button(screen, font, (screen_width // 2) + (button_width + 50), 100, button_width, button_height, "SIMULATE", YELLOW, BLACK)
rect_BEAM = Button(screen, font, (screen_width // 2) + 25, 100 + (button_height + 15), button_width, button_height, "BEAM", YELLOW, BLACK)
rect_GENETIC = Button(screen, font, (screen_width // 2) + (button_width + 50), 100 + (button_height + 15), button_width, button_height, "GENETIC", YELLOW, BLACK)

rect_SENSORLESS = Button(screen, font, (screen_width // 2) + 25, 100 + (button_height + 15)*2, button_width, button_height, "KNT", BLUE, BLACK)
rect_AND_OR = Button(screen, font, (screen_width // 2) + (button_width + 50), 100 + (button_height + 15)*2, button_width, button_height, "AND/OR", BLUE, BLACK)
rect_PARTIALLY_OBSERBABLE = Button(screen, font, (screen_width // 2) + 25, 100 + (button_height + 15)*3, button_width, button_height, "NT1P", BLUE, BLACK)

rect_BACKTRACKING = Button(screen, font, (screen_width // 2) + (button_width + 50), 100 + (button_height + 15)*3, button_width, button_height, "BACKTRACKING", YELLOW, BLACK)
rect_FORWARD_CHECKING = Button(screen, font, (screen_width // 2) + 25, 100 + (button_height + 15)*4, button_width, button_height, "FORWARD", YELLOW, BLACK)
rect_AC3 = Button(screen, font, (screen_width // 2) + (button_width + 50), 100 + (button_height + 15)*4, button_width, button_height, "AC3", YELLOW, BLACK)

button = {
        BFS: rect_BFS, DFS: rect_DFS, UCS: rect_UCS, DLS: rect_DLS, IDS: rect_IDS,
        GREEDY: rect_GREEDY, ASTAR: rect_ASTAR,
        HILL: rect_HILL, SIM: rect_SIM, BEAM: rect_BEAM, GENETIC: rect_GENETIC,
        SENSORLESS: rect_SENSORLESS, ANDOR: rect_AND_OR, PAR_OBS: rect_PARTIALLY_OBSERBABLE,
        BACKTRACKING: rect_BACKTRACKING, FORWARD_CHECKING: rect_FORWARD_CHECKING, AC3: rect_AC3
    }
def select_sort_screen(screen, events):
    pygame.display.set_caption("8 Queens")
    background = pygame.Surface((screen_width, screen_height))

    background.fill(WHITE, pygame.Rect(0, 0, screen_width // 2, screen_height))
    pygame.draw.rect(background, WHITE, pygame.Rect(0, 0, screen_width // 2, 100))
    informed_text =  font.render("Uninformed/Informed", True, BLACK)
    informed_rect = informed_text.get_rect(center=pygame.Rect(0, 0, screen_width // 2, 100).center)
    background.blit(informed_text, informed_rect)

    background.fill(GRAY, pygame.Rect(screen_width // 2, 0, screen_width // 2, screen_height))
    pygame.draw.rect(background, GRAY, pygame.Rect(screen_width // 2, 0, screen_width // 2, 100))
    local_text = font.render("Local", True, BLACK)
    local_rect = local_text.get_rect(center=pygame.Rect(screen_width // 2, 0, screen_width // 2, 100).center)
    background.blit(local_text, local_rect)

    screen.blit(background, (0, 0))

while(running):
    events = pygame.event.get()
    screen.fill(GRAY)

    if(window_state == "MENU"):
        select_sort_screen(screen, events)
        for alg, rect in button.items():
            if(rect.draw(events)):
                algorithm = alg(screen, font, tile_size)
                window_state = "SOLVE"

    elif(window_state == "SOLVE"):
        board_left.draw()
        board_right.draw()

        solve_button = pygame.Rect(50, 460, 350, 30)
        pygame.draw.rect(screen, WHITE, solve_button)
        button_text = font.render("Solve", True, BLACK)
        screen.blit(button_text, button_text.get_rect(center=solve_button.center))

        if(solver is not None):
            state = next(solver, None)
            if (state is None):
                solver = None
                state_window = State_window(full_state, goal_state)
            else:
                board_left.grid[:, :] = 0
                for (r, c) in state:
                    board_left.grid[r, c] = 2
                board_left.UpdateBoard()
                pygame.time.delay(200)

        for event in events:
            if(event.type == pygame.MOUSEBUTTONDOWN):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row = (mouse_y - 50) // tile_size

                if((0 <= row < 8) and (500 <= mouse_x < 500 + 8 * tile_size)):
                    col = (mouse_x - 500) // tile_size
                    if(0 <= col < 8):
                        if (board_right.grid[row, col] == 2):
                            board_right.grid[row, col] = 0
                            board_right.UpdateBoard()
                        else: board_right.PlaceQueenPath(col, row)
                if(solve_button.collidepoint(mouse_x, mouse_y)):
                    goal_state = [(r, c) for r in range(8) for c in range(8) if board_right.grid[r, c] == 2]
                    full_state.clear()
                    if(isinstance(algorithm, DLS)):
                        full_state, solver = algorithm.Solve(board_right, goal_state, limit = 8)
                    elif(isinstance(algorithm, IDS)):
                        full_state, solver = algorithm.Solve(board_right, goal_state, limit = 8)
                    elif(isinstance(algorithm, HILL)):
                        random_initial = [(r, random.randint(0, 7)) for r in range(8)]
                        full_state, solver = algorithm.Solve(board_right, random_initial)
                    elif(isinstance(algorithm, SIM)):
                        random_initial = [(r, random.randint(0, 7)) for r in range(8)]
                        full_state, solver = algorithm.Solve(board_right, random_initial, T = 10, alpha = 0.99)
                    elif(isinstance(algorithm, BEAM)):
                        full_state, solver = algorithm.Solve(board_right, K = 3)
                    elif(isinstance(algorithm, GENETIC)):
                        states = [[(r, random.randint(0, 7)) for r in range(8)] for _ in range(100)]
                        random_initial = [(state, algorithm.Heuristic_calc(board_right, state)) for state in states]
                        full_state, solver = algorithm.Solve(board_right, random_initial,  mutation_prob = 0.2)
                    elif(isinstance(algorithm, SENSORLESS)):
                        full_state, solver = algorithm.Solve(board_right)
                    elif(isinstance(algorithm, PAR_OBS)):
                        full_state, solver = algorithm.Solve(board_right, hint = (0, 1))
                    elif(isinstance(algorithm, BACKTRACKING)):
                        full_state, solver = algorithm.Solve(board_right)
                    elif(isinstance(algorithm, FORWARD_CHECKING)):
                        full_state, solver = algorithm.Solve(board_right)
                    elif(isinstance(algorithm, AC3)):
                        full_state, solver = algorithm.Solve(board_right)
                    else:
                        full_state, solver = algorithm.Solve(board_right, goal_state)
    for event in events:
        if(event.type == pygame.QUIT):
            running = False

    pygame.display.flip()
pygame.quit()