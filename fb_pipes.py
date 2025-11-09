import pygame
import random

class Pipe:
    def __init__(self, x, y, inverted=False):
        self.surface = pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/pipe-green.png').convert(), (2, 1.65))
        self.rect = self.surface.get_rect(midtop=(x, y))
        if inverted:
            self.rect = self.surface.get_rect(midbottom=(x, y - 250))
            self.surface = pygame.transform.flip(self.surface, False, True)
    
    def move(self):
        self.rect.centerx -= 5

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

class PipeManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pipe_list = []
        self.pipe_heights = [350, 450, 550, 650]
        self.spawn_pipe_event = pygame.USEREVENT
        pygame.time.set_timer(self.spawn_pipe_event, 1000)
        self.scored_pipes = []

    def update(self, event_list, game_active):
        if game_active:
            self._handle_pipe_spawning(event_list)
            self._move_pipes()
        else:
            self.pipe_list.clear()
            self.scored_pipes.clear()


    def draw(self, screen):
        for pipe in self.pipe_list:
            pipe.draw(screen)

    def check_collision(self, bird_rect):
        for pipe in self.pipe_list:
            if bird_rect.colliderect(pipe.rect):
                return True
        return False

    def check_score(self, bird_rect, score):
        if not self.pipe_list:
            return score

        for pipe in self.pipe_list:
            if pipe.rect.centerx < bird_rect.centerx and pipe not in self.scored_pipes:
                 score += 0.5 # Each pipe pair is worth 1 point
                 self.scored_pipes.append(pipe)

        return score


    def _handle_pipe_spawning(self, event_list):
        for event in event_list:
            if event.type == self.spawn_pipe_event:
                random_pipe_pos = random.choice(self.pipe_heights)
                self.pipe_list.append(Pipe(800, random_pipe_pos))
                self.pipe_list.append(Pipe(800, random_pipe_pos, inverted=True))

    def _move_pipes(self):
        for pipe in self.pipe_list:
            pipe.move()
        
        # Remove pipes that have moved off-screen
        self.pipe_list = [pipe for pipe in self.pipe_list if pipe.rect.right > -50]