import pygame 
from pygame.locals import * # [QUIT, KEYDOWN,K_ESCAPE] etc
from sys import exit  
import numpy as np
import random 
from player import Player
import os

screen_size = (1200,500)  
board_width = 12
board_height = 2

sprite_width = 100
sprite_height = 200

cactus_probability = 0.12
bird_probability = 0.05

dir = os.path.dirname(__file__)


class Dinosaur(object): 

    def __init__(self, player = Player(0)): 
        pygame.init() # init pygame library  
        flag = DOUBLEBUF # double buffer mode 

        self.surface = pygame.display.set_mode(screen_size, flag) 

        self.score = 0

        self.player = player

        self.dino_is_jumping = False
        self.dino_is_alive = True

        self.gamestate = 1 # 1 - run, 2 - init screen (currently not implemented), 0 - exit

        self.dino_sprite = pygame.image.load(os.path.join(dir, "images/dino.png")) 
        self.bird_sprite = pygame.image.load(os.path.join(dir, "images/bird.png")) 
        self.cactus_sprite = pygame.image.load(os.path.join(dir, "images/cactus.png"))

        # self.surface.blit(self.dino_sprite, (10, 280))

        self.loop() # main loop 

    def game_exit(self): 
        exit() 

    def init_board(self):
        self.board = np.zeros((board_width, board_height))

        self.board[0, board_height - 1] = 1 # dinosaur

    def draw_board(self):
        for i in range(board_width):
            for j in range(board_height):
                x = 10 + i * sprite_width
                y = 10 + j * sprite_height

                if self.board[i, j] == 1: # dinosaur
                    self.surface.blit(self.dino_sprite, (x, y))
                elif self.board[i, j] == 2: # cactus
                    self.surface.blit(self.cactus_sprite, (x, y))
                elif self.board[i, j] == 3: # bird
                    self.surface.blit(self.bird_sprite, (x, y))

    def loop(self):
        self.init_board()

        while self.gamestate==1:


            self.surface = pygame.display.set_mode(screen_size) # clear screen
            self.draw_board()

            if self.player.type == 0: # human

                for event in pygame.event.get(): 
                    if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE): 
                        self.gamestate=0

                    if (event.type==KEYDOWN and event.key==K_SPACE): 
                        self.jump()

            elif self.player.type == 1: # computer

                self.player.make_move(self.board)


            pygame.display.flip()

            self.generate_next_board()
            self.check_if_dino_is_alive()
            pygame.time.wait(200)


        if self.player.type == 0: # human
            with open(os.path.join(dir, "results/dino_scores_human.txt"), "a") as myfile:
                myfile.write( "\n" + str(self.score) )

        if self.player.type == 1: # computer
            with open(os.path.join(dir, "results/dino_scores_computer.txt"), "a") as myfile:
                myfile.write( "\n" + str(self.score) )

        print( self.score )

        self.game_exit() 

    def jump(self):
        if self.board[0, 1] == 1:
            self.dino_is_jumping = True
            self.jump_time = 0
            self.board[0, 0] = 1
            self.board[0, 1] = 0

    def check_if_dino_is_alive(self):
        if self.dino_is_alive == True:
            self.score += 1
        elif self.dino_is_alive == False:
            self.gamestate=0

    def generate_next_board(self):
        # scroll board
        for i in range(board_width - 1):
            for j in range(board_height):
                self.board[i, j] = self.board[i + 1, j]

        for j in range(board_height):
            self.board[board_width - 1, j] = 0

        # put back dino and check if still alive
        if (self.dino_is_jumping == True and self.jump_time == 2) or (self.dino_is_jumping == False): # we want to place dino on ground
            if self.board[0, 1] == 0: 
                self.board[0, 1] = 1
                self.jump_time = 0
                self.dino_is_jumping = False
            else:
                self.dino_is_alive = False
        elif (self.dino_is_jumping == True and self.jump_time < 2): # dino is jumping in next iteration
            if self.board[0, 0] == 0:
                self.board[0, 0] = 1
                self.jump_time += 1
            else:
                self.dino_is_alive = False

        # generate new items
        cactus_occurance = random.random()
        if (cactus_probability > cactus_occurance) and self.board[board_width - 2, 0] != 3:
            self.board[board_width - 1, 1] = 2
        else:
            bird_occurance = random.random()
            if (bird_probability > bird_occurance) and self.board[board_width - 2, 1] != 2:
                self.board[board_width - 1, 0] = 3




if __name__ == '__main__': 
    Dinosaur()