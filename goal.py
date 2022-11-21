import random
import pygame

class Goal:
    def __init__(self, screen_width, screen_height, color):
        self.color = color
        self.size = self.width, self.height = 20, 20
        self.position_x = random.randrange(0, screen_width, self.width) 
        self.position_y = random.randrange(0, screen_height, self.height)
        self.goal_rect = pygame.Rect((0, 0), (self.size))

    def change_pos(self, screen_width, screen_height):
        self.position_x = random.randrange(0, screen_width, self.width) 
        self.position_y = random.randrange(0, screen_height, self.height)

    def get_rect(self):
        return self.goal_rect.move([self.position_x, self.position_y])
