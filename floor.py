import pygame

class Floor:
    def __init__(self, screen_width, y_pos):
        self.surface = pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/base.png').convert(), (2, 1.65))
        self.rect1 = self.surface.get_rect(topleft=(0, y_pos))
        self.rect2 = self.surface.get_rect(topleft=(screen_width, y_pos))
        self.y_pos = y_pos

    def update(self):
        self.rect1.x -= 1
        self.rect2.x -= 1
        if self.rect1.right <= 0:
            self.rect1.left = self.rect2.right
        if self.rect2.right <= 0:
            self.rect2.left = self.rect1.right

    def draw(self, screen):
        screen.blit(self.surface, self.rect1)
        screen.blit(self.surface, self.rect2)