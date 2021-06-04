import pygame
import math

class Ball(pygame.sprite.Sprite):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH):
        super().__init__()

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.width = SCREEN_WIDTH/100
        self.height = SCREEN_WIDTH/100

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.center = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)

        self.default_speed = 8
        self.speed = self.default_speed
        self.x_speed = -1 * self.speed
        self.y_speed = 0

        self.wall_bounce = True
        self.player_bounce = True

    def update(self):
        self.rect.x += self.x_speed

        if ((self.rect.top >= 0) and (self.rect.bottom <= self.SCREEN_HEIGHT)) or not self.wall_bounce:
            self.rect.y += self.y_speed
        elif self.wall_bounce:
            self.y_speed *= -1
            self.wall_bounce = False

        if self.rect.center[1] > (self.SCREEN_HEIGHT/3) and self.rect.center[1] < (self.SCREEN_HEIGHT*(2/3)):
            self.wall_bounce = True

        if self.rect.center[0] > (self.SCREEN_WIDTH/3) and self.rect.center[0] < (self.SCREEN_WIDTH*(2/3)):
            self.player_bounce = True
    
    def new_speed(self, player_y, rally, player_height, max_angle):
        self.speed += (rally*(1/4))
        distance = self.rect.center[1] - player_y
        angle = (max_angle*(abs(distance))/(player_height/2))
        if distance == 0:
            distance = 0.01
        old_x_speed = self.x_speed
        self.x_speed = (self.speed*math.cos(math.radians(angle))) * (-old_x_speed/abs(old_x_speed))
        self.y_speed = self.speed*math.sin(math.radians(angle)) * (distance/abs(distance))
    
    def reset(self):
        self.rect.center = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        self.y_speed = 0
        self.x_speed = self.speed * (self.x_speed / abs(self.x_speed))
        self.speed = self.default_speed
