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

objects_saved = 4
objects_parameters = 3 # x_begin, x_end, y
objects_ahead = 1

write_to_files = False
graphic_mode = 0

screen_size = (board_width * sprite_width, board_height * sprite_height)  

# fuzzification = 1. / 1.    

dir = os.path.dirname(__file__)

# sprite, width, height, y

objects_types = [
    {
        'sprite': pygame.image.load(os.path.join(dir, "images/cactus.png")), 
        'width': 73, 
        'height': 47, 
        'y': 0,
        'r': math.sqrt(73**2 + 47**2) / 2,
        'probability': 0.15
    },
    {
        'sprite': pygame.image.load(os.path.join(dir, "images/cactus-small.png")), 
        'width': 24, 
        'height': 46, 
        'y': 0,
        'r': math.sqrt(24**2 + 46**2) / 2,
        'probability': 0.1
    },
    {
        'sprite': pygame.image.load(os.path.join(dir, "images/bird.png")), 
        'width': 42, 
        'height': 26, 
        'y': 75,
        'r': math.sqrt(42**2 + 26**2) / 2,
        'probability': 0.025
    }
]

ground = {
    'sprite': pygame.image.load(os.path.join(dir, "images/ground.png")), 
    'width': 1000, 
    'height': 100, 
    'y': 10
}

dino = {
    'sprite': pygame.image.load(os.path.join(dir, "images/dino.png")), 
    'width': 40, 
    'height': 43, 
    'x': 15,
    'y': 0,
    'r': math.sqrt(40**2 + 43**2) / 2
}

class Dinosaur(object): 

    def __init__(self, player, fuzzification): 
        player.prepare("results/reactions.txt", objects_ahead)
        self.surface = None

        if graphic_mode:
            pygame.init() # init pygame library  
            flag = DOUBLEBUF # double buffer mode 
            self.surface = pygame.display.set_mode(screen_size, flag) 

        self.score = 0

        self.player = player

        self.jumpStartTime = 0
        self.dino_is_alive = True

        self.gamestate = 1 # 1 - run, 2 - init screen (currently not implemented), 0 - exit

        self.objects = []   # [x, type]
        self.archive = []   # Save users reactions

        self.v_ox = 3.5
        self.v_oy = 400
        self.g = 410
        self.dt = 50
        self.dt_y = 600
        self.framesSinceGeneration = 0 
        self.fuzzification = fuzzification

        self.saveAfterLanding = []
        self.lastSavedScore = -1

        self.loop() # main loop 

    def game_exit(self): 
        exit() 

    def init_board(self):
        self.board = []
        for i in range(board_height):
            self.board.append([0] * board_width)

    def draw_board(self):

        background = pygame.Surface(self.surface.get_size())
        background = background.convert()
        background.fill((247, 247, 247))

        self.surface.blit(background, (0, 0))
        self.surface.blit(ground['sprite'], (0, ground['height']))
        self.surface.blit(dino['sprite'], (dino['x'], screen_size[1] - dino['height'] - ground['y'] - dino['y'] * dino['height']))

        for i in range(len(self.objects)):
            obj = objects_types[self.objects[i][1]]

            x = self.objects[i][0]
            y = screen_size[1] - obj['height'] - ground['y'] - obj['y']

            self.surface.blit(objects_types[self.objects[i][1]]['sprite'], (x, y))


    def loop(self):
        self.init_board()

        while self.gamestate == 1:

            if graphic_mode:
                self.surface = pygame.display.set_mode(screen_size) 
                self.draw_board()

            self.init_board()

            if graphic_mode:
                for event in pygame.event.get(): 
                    if event.type==QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
                        self.gamestate=0

            if self.player.type == 0 and graphic_mode: # human

                for event in pygame.event.get(): 

                    if (event.type == KEYDOWN and event.key == K_SPACE): 
                        self.jump()

                    if (event.type == KEYDOWN and event.key == K_q):
                        self.big_jump()

            elif self.player.type == 1: # computer

                if len(self.objects) > objects_ahead:
                    position = []

                    for obj in range(objects_ahead):

                        obj_data = objects_types[self.objects[obj][1]]

                        position.append(self.objects[obj][0] + (random.random() - 0.5) * self.fuzzification * obj_data['width'])
                        position.append(self.objects[obj][0] + obj_data['width'] + (random.random() - 0.5) * self.fuzzification * obj_data['width'])
                        position.append(obj_data['y'])

                    response = self.player.make_move(position)

                    if response > 0.3 and response <= 1:
                        self.jump()
                    elif int(round(response)) > 1:
                        self.big_jump()

            if graphic_mode:
                pygame.display.flip()
                pygame.display.set_caption("Score: %d" % (self.score))

            self.generate_next_board()
            self.check_if_dino_is_alive()

            if self.score % 15 == 0 and self.score != self.lastSavedScore:
                jumping = 0
                if (dino['y'] > 0.01 and self.dt_y == 400):
                    jumping = 1
                elif (dino['y'] > 0.01 and self.dt_y == 600):
                    jumping = 2

                self.archive.append(self.currentBoard1D(jumping))
                self.lastSavedScore = self.score

            if graphic_mode:
                pygame.time.wait(int(self.dt / 10))

        if write_to_files:

            if self.player.type == 0: # human
                with open(os.path.join(dir, "results/dino_scores_human.txt"), "a") as myfile:
                    myfile.write( "\n" + str(self.score) )

            if self.player.type == 1: # computer
                with open(os.path.join(dir, "results/dino_scores_computer.txt"), "a") as myfile:
                    myfile.write( "\n" + str(self.score) )
                    
            if len(self.archive) > 0:
                self.archive.pop()
            
                with open(os.path.join(dir, "results/2objects.txt"), "a") as myfile:
                    for i in range(len(self.archive)):
                        myfile.write(";".join(str(x) for x in self.archive[i]) + "\n")

        #print('Final score: ' + str(self.score))
        if graphic_mode:
            self.game_exit() 

    def jump(self):
        if dino['y'] < 0.01:
            self.dt_y = 400
            self.jumpStartTime = self.dt / self.dt_y
            dino['y'] = -self.g * self.jumpStartTime * self.jumpStartTime + self.v_oy * self.jumpStartTime  
            dino['y'] = dino['y'] / 50  
            
            if self.lastSavedScore != self.score:
                self.saveAfterLanding = self.currentBoard1D(True)

    def big_jump(self):
        if dino['y'] < 0.01:
            self.dt_y = 600
            self.jumpStartTime = self.dt / self.dt_y
            dino['y'] = -self.g * self.jumpStartTime * self.jumpStartTime + self.v_oy * self.jumpStartTime  
            dino['y'] = dino['y'] / 50  
            
            if self.lastSavedScore != self.score:
                self.saveAfterLanding = self.currentBoard1D(True)


    def check_if_dino_is_alive(self):
        if self.dino_is_alive == True:
            self.score += 1
        elif self.dino_is_alive == False:
            self.gamestate=0

    def generate_next_board(self):
        onBoard = []

        for i in range(len(self.objects)):
            self.objects[i][0] -= self.v_ox * self.dt / 10
            if self.objects[i][0] > -50:
                onBoard.append(self.objects[i])

        self.objects = onBoard

        if dino['y'] > 0.01:
            self.jumpStartTime += self.dt / self.dt_y
            dino['y'] = -self.g * self.jumpStartTime * self.jumpStartTime + self.v_oy * self.jumpStartTime 
            dino['y'] = dino['y'] / 50

        
        if dino['y'] < 0:
            dino['y'] = 0

            if len(self.saveAfterLanding) > 1:
                self.archive.append(self.saveAfterLanding)
                self.saveAfterLanding = []
                self.lastSavedScore = self.score

        self.framesSinceGeneration = self.framesSinceGeneration + self.v_ox

        if self.framesSinceGeneration > 40:
            for index, obj in enumerate(objects_types):
                if obj['probability'] > random.random():
                    self.objects.append([1050, index])
                    self.framesSinceGeneration = 0
                    break
            
        for obj in self.objects:
            obj_data = objects_types[obj[1]]

            x = obj[0] + obj_data['width'] / 2
            y = obj_data['height'] - obj_data['y']

            dino_x = dino['x'] + dino['width'] / 2
            dino_y = dino['height'] - dino['y'] * dino['height']

            distance = math.sqrt((x - dino_x)**2 + (y - dino_y)**2)
            minDistance = (obj_data['r'] + dino['r']) * .75

            if distance < minDistance:
                self.dino_is_alive = False
        

    def currentBoard1D(self, jumped):

        jumping = 0
        if ((dino['y'] > 0.01 or jumped == 1) and self.dt_y == 400):
            jumping = 1
        elif ((dino['y'] > 0.01 or jumped == 1) and self.dt_y == 600):
            jumping = 2

        current = [board_width * 1.1] * (objects_parameters * objects_saved + 1)

        for i in range(len(self.objects)):
            if i >= objects_saved:
                continue

            obj = objects_types[self.objects[i][1]]

            current[i * objects_parameters] = self.objects[i][0]
            current[i * objects_parameters + 1] = self.objects[i][0] + obj['width']
            current[i * objects_parameters + 2] = obj['y']

        current[objects_parameters * objects_saved] = jumping

        return current

    def getScore(self):
        return self.score

if __name__ == '__main__':
    for i in range(100): 
        score = 0
        for j in range(10):
            score += Dinosaur(Player(1), 1.0 / (i + 1)).getScore()
            
        print(str(1.0 / (i + 1)) + ': ' + str(score / 10))