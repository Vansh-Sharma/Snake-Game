# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 17:02:57 2021

@author: Vansh
"""
import pygame as py
import random
from random import randint
import time

"""
TODO
Add Back Button on Loss
Change Graphic of Snake and Food
DeBug and Smoothen
"""

class Player():
    x = [0]
    y = [0]
    length = 1
    direction = 0
    updateCountMax = 2
    updateCount = 0
    def __init__(self, x, y):
        self.x[0] = x
        self.y[0] = y
        for i in range(0, 2000):
            self.x.append(0)
            self.y.append(0)
        self.x[1] = 10
        self.x[2] = 20
    def update(self):
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
            self.updateCount = 0
            if self.direction == 0:
                if self.x[0] > 799:
                    self.x[0] = 0
                self.x[0] = self.x[0] + 10
            if self.direction == 1:
                if self.x[0] < 1:
                    self.x[0] = 800
                self.x[0] = self.x[0] - 10
            if self.direction == 2:
                if self.y[0] > 599:
                    self.y[0] = 0
                self.y[0] = self.y[0] + 10
            if self.direction == 3:
                if self.y[0] < 1:
                    self.y[0] = 600
                self.y[0] = self.y[0] - 10
    def moveLeft(self):
        self.direction = 1
    def moveRight(self):
        self.direction = 0
    def moveDown(self):
        self.direction = 2
    def moveUp(self):
        self.direction = 3
    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image,(self.x[i], self.y[i]))
    
class Food():
    def __init__(self):
        self.food_color = (0,0,0)
        self.food_needed = True
        self.food_x = random.randint(30,770)
        self.food_y = random.randint(30, 570)
    def generate(self):
        if (self.food_needed):
            self.food_x = random.randint(30,770)
            self.food_y = random.randint(30, 570)
            self.food_needed = False
    def on_init(self):
        self.food_image = py.image.load("blackForFood.jfif").convert()
        self.food_image = py.transform.scale(self.food_image, (20,20))
    

class App():
    def __init__(self):
        self.running = True
        self.snake = Player(240, 240)
        self.food = Food()
        self.score = 0
    def movement(self):
        keys = py.key.get_pressed()
        if keys[py.K_LEFT]:
            self.snake.moveLeft()
        if keys[py.K_RIGHT]:
            self.snake.moveRight()
        if keys[py.K_UP]:
            self.snake.moveUp()
        if keys[py.K_DOWN]:
            self.snake.moveDown()
        self.screen.fill(self.screen_background)
    def score_display(self):
        py.font.init()
        self.font = py.font.SysFont('Comic Sans MS', 25)
        self.score_text = self.font.render(f"Score: {self.score}", True, (0,255,0),(0,0,0))
        self.score_rect = self.score_text.get_rect()
    def on_init(self):
        self.screen = py.display.set_mode((800,600))
        self.screen_background  = (255,165,0)
        self.snake_color = (255,255,255)
        self.image_surf = py.image.load("greenForSnake.jfif").convert()
        self.image_surf = py.transform.scale(self.image_surf, (30,30))
    def on_loop(self):
        self.snake.update()
        for i in range(0,self.snake.length):
            if self.isCollision(self.food.food_x,self.food.food_y, self.snake.x[i], self.snake.y[i], 30):
                self.food.food_x = randint(30,570)
                self.food.food_y = randint(30, 570)
                self.snake.length = self.snake.length + 4
                self.score = self.score + 1
        for i in range(2, self.snake.length):
            if self.isCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i], 0):
                self.loss_screen()
        
        pass
    
    def loss_screen(self):
       
        self.run = True
        while self.run:
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.run = False
                    py.quit()
            #self.screen.blit(self.screen_background, (0,0))
            py.font.init()
            self.font = py.font.SysFont('comicsans', 40)
            self.loss_text = self.font.render("Game Over", True, (0,255,0),(0,0,0))
            self.loss_rect = self.loss_text.get_rect()
            self.screen.blit(self.loss_text, (330,200))
            py.display.flip()
            

    def on_render(self):
        self.screen.fill(self.screen_background)
        self.snake.draw(self.screen, self.image_surf)
        self.screen.blit(self.food.food_image, (self.food.food_x, self.food.food_y))
        self.screen.blit(self.score_text, self.score_rect)
        py.display.flip()
    def isCollision(self, x1, y1, x2, y2, size):
        if x1 >= x2 and x1 <= x2 + size:
            if y1 >= y2 and y1 <= y2+size:
                return True
        return False
    def isRunning(self):
        py.init()
        self.on_init()
        self.food.on_init()
        while self.running:
            py.event.pump()
            py.time.delay(8)
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
            self.movement()
            self.on_loop()
            self.score_display()
            self.on_render()
            self.food.generate()
            py.display.update()
        py.quit()
            
if __name__ == "__main__":
    theApp = App()
    theApp.isRunning()
        
    