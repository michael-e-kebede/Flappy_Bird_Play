import pygame, sys
from bird import Bird
from fb_pipes import PipeManager
from floor import Floor

def score_display(screen, game_state, score, high_score, game_font):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen.get_width() / 2, 100))
        screen.blit(score_surface, score_rect)

    elif game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen.get_width() / 2, 120))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(screen.get_width() / 2, 70))
        screen.blit(high_score_surface, high_score_rect)

def update_high_score(score, high_score):
    return max(score, high_score)

def main():
    pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
    pygame.init()
    screen_width = 576
    screen_height = 844.8
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game_font = pygame.font.Font('flappy-bird-assets/04B_19.TTF', 40)

    # Game State
    game_active = True
    score = 0
    high_score = 0

    # Game Assets
    bg_surface = pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/background-night.png').convert(), (2, 1.65))
    game_over_surface = pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/message.png').convert_alpha(), (2, 1.65))
    game_over_rect = game_over_surface.get_rect(center=(screen_width / 2, screen_height / 2))
    death_sound = pygame.mixer.Sound('flappy-bird-assets/audio/hit.wav')
    death_sound.set_volume(0.2)
    score_sound = pygame.mixer.Sound('flappy-bird-assets/audio/point.wav')
    score_sound.set_volume(0.1)


    # Game Objects
    bird = Bird(screen_width, screen_height)
    pipe_manager = PipeManager(screen_width, screen_height)
    floor = Floor(screen_width, 725)

    while True:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and not game_active:
                    game_active = True
                    score = 0
        
        # Update game objects
        bird.update(game_active, event_list)
        pipe_manager.update(event_list, game_active)
        if game_active:
            floor.update()

        # Draw everything
        screen.blit(bg_surface, (0, 0))
        
        if game_active:
            pipe_manager.draw(screen)
            floor.draw(screen)
            bird.draw(screen)

            # Collision Checks
            if pipe_manager.check_collision(bird.rect) or bird.rect.top <= -100 or bird.rect.bottom >= 725:
                death_sound.play()
                game_active = False
            
            # Score
            old_score = score
            score = pipe_manager.check_score(bird.rect, score)
            if old_score != score:
                score_sound.play()

            score_display(screen, 'main_game', score, high_score, game_font)
        else:
            high_score = update_high_score(score, high_score)
            score_display(screen, 'game_over', score, high_score, game_font)
            screen.blit(game_over_surface, game_over_rect)


        pygame.display.update()
        clock.tick(120)

if __name__ == '__main__':
    main()