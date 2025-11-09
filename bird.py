import pygame

class Bird:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load bird images and create animation frames
        bird_downflap = pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/redbird-downflap.png').convert_alpha(), (2, 1.65))
        bird_midflap = pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/redbird-midflap.png').convert_alpha(), (2, 1.65))
        bird_upflap = pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/redbird-upflap.png').convert_alpha(), (2, 1.65))
        self.frames = [bird_downflap, bird_midflap, bird_upflap]
        self.animation_index = 0
        self.surface = self.frames[self.animation_index]
        self.rect = self.surface.get_rect(center=(80, self.screen_height / 2))

        # Bird movement physics
        self.gravity = 0.15
        self.movement = 0

        # Flap sound
        self.flap_sound = pygame.mixer.Sound('flappy-bird-assets/audio/wing.wav')
        self.flap_sound.set_volume(0.2)

        # Bird animation timer
        self.flap_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.flap_event, 200)

    def update(self, game_active, event_list):
        if game_active:
            self._apply_gravity()
            self._handle_input(event_list)
            self._animate()
        else:
            self._reset()

    def draw(self, screen):
        rotated_bird = self._rotate()
        screen.blit(rotated_bird, self.rect)

    def _apply_gravity(self):
        self.movement += self.gravity
        self.rect.centery += self.movement

    def _handle_input(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_w):
                self.movement = 0
                self.movement -= 7
                self.flap_sound.play()
            if event.type == self.flap_event:
                self.animation_index = (self.animation_index + 1) % len(self.frames)
                self.surface = self.frames[self.animation_index]


    def _rotate(self):
        return pygame.transform.rotozoom(self.surface, -self.movement * 3, 1)

    def _animate(self):
        new_bird = self.frames[self.animation_index]
        new_bird_rect = new_bird.get_rect(center=(80, self.rect.centery))
        self.surface = new_bird
        self.rect = new_bird_rect


    def _reset(self):
        self.rect.center = (80, self.screen_height / 2)
        self.movement = 0