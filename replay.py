import pygame
import neat
import pickle
import os
import sys

# Import game classes
from bird import Bird
from fb_pipes import PipeManager
from floor import Floor

# --- Game Constants and Setup ---
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 844.8

def play_best_genome(config_path, genome_path="best_model"):
    # --- Load NEAT Configuration ---
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # --- Load the saved genome ---
    for filename in os.listdir(genome_path):
        if filename.endswith(".pkl"):
            with open(os.path.join(genome_path, filename), "rb") as f:
                print(f"Loading genome {filename}...")
                genome = pickle.load(f)

            # --- Create the neural network from the genome ---
            net = neat.nn.FeedForwardNetwork.create(genome, config)

            # --- Pygame Setup ---
            pygame.init()
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            clock = pygame.time.Clock()
            game_font = pygame.font.Font('flappy-bird-assets/04B_19.TTF', 40)
            bg_surface = pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/background-day.png').convert(), (2, 1.65))

            # --- Create Game Objects ---
            bird = Bird(SCREEN_WIDTH, SCREEN_HEIGHT)
            pipe_manager = PipeManager(SCREEN_WIDTH, SCREEN_HEIGHT)
            floor = Floor(SCREEN_WIDTH, 725)
            score = 0
            score_sound = pygame.mixer.Sound('flappy-bird-assets/audio/point.wav')
            score_sound.set_volume(0.12)

            # --- Main Game Loop for Replay ---
            running = True
            while running:
                clock.tick(120)
                event_list = pygame.event.get()
                for event in event_list:
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()
                    
                target_pipe_bottom = None
                target_pipe_top = None
                if len(pipe_manager.pipe_list) > 0:

                    # Find the first pipe relevant to the first bird
                    for k in range(0, len(pipe_manager.pipe_list), 2):
                        bottom_p = pipe_manager.pipe_list[k]

                        if bottom_p.rect.right > bird.rect.left:
                            target_pipe_bottom = bottom_p

                            if k + 1 < len(pipe_manager.pipe_list):
                                target_pipe_top = pipe_manager.pipe_list[k+1]
                            break
                        
                # --- Get Inputs for the Neural Network ---
                # 1. Normalize Bird's Y coordinate
                norm_bird_y = bird.rect.centery / SCREEN_HEIGHT

                # 2. Normalize Bird's vertical velocity
                # Assuming bird_instance.movement is its current vertical speed.
                norm_bird_velocity = bird.movement / 15.0
                norm_bird_velocity = max(-1, min(1, norm_bird_velocity))

                # Defaults if no pipes are visible
                norm_dist_top_pipe_h = 0.5 # Middle of screen top
                norm_dist_bottom_pipe_h = 0.5 # Middle of screen bottom
                norm_next_gap_top_y = 0.5 # Middle of screen top
                norm_next_gap_bottom_y = 0.5 # Middle of screen bottom

                # Use the general target pipes for the generation for simplicity here
                if target_pipe_bottom and target_pipe_top:

                    # Check if this specific pipe is still ahead of the current bird
                    if target_pipe_bottom.rect.right > bird.rect.left:
                        # 2 and 3 setup
                        dist_top_h = (target_pipe_top.rect.bottom - bird.rect.right)
                        dist_bott_h = (target_pipe_bottom.rect.top - bird.rect.right)

                         # 2 and 3 Normalized horizontal distance from bird's right to pipe's top and bottom
                        norm_dist_top_pipe_h = max(0, dist_top_h / SCREEN_WIDTH) 
                        norm_dist_bottom_pipe_h = max(0, dist_bott_h / SCREEN_WIDTH)

                        # 4 Normalized Y position of the top of the gap (bottom edge of the top pipe)
                        norm_next_gap_top_y = target_pipe_top.rect.bottom / SCREEN_HEIGHT

                        # 5 Normalized Y position of the bottom of the gap (top edge of the bottom pipe)
                        norm_next_gap_bottom_y = target_pipe_bottom.rect.top / SCREEN_HEIGHT
                inputs = (
                    norm_bird_y,
                    norm_dist_top_pipe_h,
                    norm_dist_bottom_pipe_h,
                    norm_next_gap_top_y,
                    norm_next_gap_bottom_y
                )
                output = net.activate(inputs)
                if output[0] > 0.5:
                    bird.movement = 0
                    bird.movement -= 7

                # --- Update Game State ---
                bird.movement += bird.gravity
                bird.rect.centery += bird.movement
                bird.animation_index = (bird.animation_index + 1) % len(bird.frames) # Simplified animation
                bird.surface = bird.frames[bird.animation_index]
                pipe_manager.update(event_list, True)
                floor.update()

                # Check for score
                old_score = score
                score = pipe_manager.check_score(bird.rect, score)
                if score > old_score:
                    score_sound.play()

                # Check for collision
                if pipe_manager.check_collision(bird.rect) or bird.rect.top <= -20 or bird.rect.bottom >= 725:
                    print(f"Game Over! Final Score: {int(score)}")
                    running = False # End the game loop
                
                # --- Drawing ---
                screen.blit(bg_surface, (0, 0))
                pipe_manager.draw(screen)
                floor.draw(screen)
                bird.draw(screen)
                score_text = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
                screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))
                pygame.display.update()

            pygame.time.wait(500) # Wait 0.5 second before closing
            pygame.quit()


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_neat.txt') # Use the same config as training
    play_best_genome(config_path)