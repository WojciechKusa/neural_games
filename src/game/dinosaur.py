import pygame 
from pygame.locals import * # [QUIT, KEYDOWN,K_ESCAPE] etc
from sys import exit  
import numpy as np
import random 
import math
from player import Player
import os

board_width = 10
board_height = 2

sprite_width = 100
sprite_height = 100

screen_size = (board_width * sprite_width, board_height * sprite_height)  

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

        self.dino_y = 0
        self.jumpStartTime = 0
        self.dino_is_alive = True

        self.gamestate = 1 # 1 - run, 2 - init screen (currently not implemented), 0 - exit

        self.dino_sprite = pygame.image.load(os.path.join(dir, "images/dino.png")) 
        self.bird_sprite = pygame.image.load(os.path.join(dir, "images/bird.png")) 
        self.cactus_sprite = pygame.image.load(os.path.join(dir, "images/cactus.png"))
        self.ground_sprite = pygame.image.load(os.path.join(dir, "images/ground.png"))

        self.objects = []   # [x, z]

        self.v_ox = 2.5
        self.v_oy = 400
        self.g = 410
        self.dt = 50
        self.dt_y = 600
        self.framesSinceGeneration = 0 


        self.loop() # main loop 

    def game_exit(self): 
        exit() 

    def init_board(self):
        self.board = np.zeros((board_width, board_height))

        self.board[0, board_height - 1] = 1 # dinosaur

    def draw_board(self):

        background = pygame.Surface(self.surface.get_size())
        background = background.convert()
        background.fill((247, 247, 247))

        self.surface.blit(background, (0, 0))
        self.surface.blit(self.ground_sprite, (0, sprite_height))
        self.surface.blit(self.dino_sprite, (0, sprite_height - self.dino_y * 50))

        for i in range(len(self.objects)):
            x = self.objects[i][0] * sprite_width
            y = (1 - self.objects[i][1]) * sprite_height

            if y >= 1:
                self.surface.blit(self.cactus_sprite, (x, y))
            else:
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
            pygame.display.set_caption("%f" % (self.score))

            self.generate_next_board()
            self.check_if_dino_is_alive()

            if self.score % 50 == 0:
                self.v_ox = self.v_ox * 1.1
                self.dt_y = self.dt_y / 1.05

            pygame.time.wait(self.dt)


        if self.player.type == 0: # human
            with open(os.path.join(dir, "results/dino_scores_human.txt"), "a") as myfile:
                myfile.write( "\n" + str(self.score) )

        if self.player.type == 1: # computer
            with open(os.path.join(dir, "results/dino_scores_computer.txt"), "a") as myfile:
                myfile.write( "\n" + str(self.score) )

        print( self.score )

        self.game_exit() 

    def jump(self):
        if self.dino_y < 0.01:
            self.jumpStartTime = self.dt / self.dt_y
            self.dino_y = -self.g * self.jumpStartTime * self.jumpStartTime + self.v_oy * self.jumpStartTime  
            self.dino_y = self.dino_y / 50  

    def check_if_dino_is_alive(self):
        if self.dino_is_alive == True:
            self.score += 1
        elif self.dino_is_alive == False:
            self.gamestate=0

    def generate_next_board(self):
        # scroll board
        onBoard = []

        for i in range(len(self.objects)):
            self.objects[i][0] -= self.v_ox * self.dt / 1000
            if self.objects[i][0] > -1:
                onBoard.append(self.objects[i])

        self.objects = onBoard

        if self.dino_y > 0.01:
            self.jumpStartTime += self.dt / self.dt_y
            self.dino_y = -self.g * self.jumpStartTime * self.jumpStartTime + self.v_oy * self.jumpStartTime 
            self.dino_y = self.dino_y / 50

        if self.dino_y < 0:
            self.dino_y = 0

        self.framesSinceGeneration = self.framesSinceGeneration + 1

        if self.framesSinceGeneration > 15:
            if (cactus_probability > random.random()):
                self.objects.append([11, 0])
                self.framesSinceGeneration = 0
            elif (bird_probability > random.random()):
                self.objects.append([11, 1])
                self.framesSinceGeneration = 0

        for i in range(len(self.objects)):
            dx = self.objects[i][0] 
            dy = self.objects[i][1] - self.dino_y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < 0.5:
                self.dino_is_alive = False


if __name__ == '__main__': 
    Dinosaur()