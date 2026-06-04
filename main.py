import pygame
import sys
from game import Game

def main():
    # Initialize Pygame
    pygame.init()
    
    # Game settings
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    
    # Create display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Football Game - Score Goals!")
    
    # Clock for FPS
    clock = pygame.time.Clock()
    
    # Initialize game
    game = Game(WIDTH, HEIGHT)
    
    # Game loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # Reset game
                    game = Game(WIDTH, HEIGHT)
        
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Update game
        if not game.is_game_over():
            game.handle_input(keys)
            game.update(dt)
        else:
            # Allow restart with 'R'
            if keys[pygame.K_r]:
                game = Game(WIDTH, HEIGHT)
        
        # Draw game
        game.draw(screen)
        
        # Update display
        pygame.display.flip()
    
    # Quit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
