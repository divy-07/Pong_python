import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, center, name):
        super().__init__()

        self.center = center
        self.name = name

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.width = SCREEN_WIDTH/100
        self.height = SCREEN_HEIGHT/10

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.center = center

        self.move_speed = 4
        self.score = 0
       
    def move(self, direction):
        self.rect.y += (direction * self.move_speed)

    def reset(self):
        self.rect.center = self.center
