import pygame

class Player:
    def __init__(self, screen_width, screen_height, color):
        self.color = color
        self.speed = [0, 0]
        self.size = 20, 20
        self.position = screen_width / 2, screen_height / 2
        self.body_rect = pygame.Rect((0, 0), self.size)
        self.body_rect.center = self.position
        self.visited_rects = []

    def set_speed(self, new_speed):
        self.speed = new_speed

    def move(self):
        self.visited_rects.append(self.body_rect)
        self.body_rect = self.body_rect.move(self.speed)

    def get_coords(self):
        return (self.body_rect.x, self.body_rect.y)

    def get_rect(self):
        return self.body_rect

    def get_visited_rects(self):
        return self.visited_rects
