import pygame
from ball import Ball
from player import Player
from field import Field

class Game:
    """Main game class managing game state and logic"""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.field = Field(width, height)
        self.ball = Ball(width // 2, height // 2)
        
        # Initialize blue team (player controlled)
        self.players_blue = [
            Player(width // 4, height // 2, "blue", 1),
            Player(width // 4 - 80, height // 3, "blue", 2),
            Player(width // 4 - 80, 2 * height // 3, "blue", 3),
        ]
        
        # Initialize red team (AI controlled)
        self.players_red = [
            Player(3 * width // 4, height // 2, "red", 1),
            Player(3 * width // 4 + 80, height // 3, "red", 2),
            Player(3 * width // 4 + 80, 2 * height // 3, "red", 3),
        ]
        
        self.controlled_player = self.players_blue[0]
        self.score_blue = 0
        self.score_red = 0
        self.game_time = 0
        self.game_duration = 90  # 90 seconds
        self.kick_pressed = False
        self.last_goal_scorer = None
        self.goal_timer = 0
        
    def handle_input(self, keys):
        """Handle player input"""
        self.controlled_player.handle_input(keys)
        
        # Handle ball kick
        space_pressed = keys[pygame.K_SPACE]
        if space_pressed and not self.kick_pressed:
            # Kick towards opponent goal
            if self.controlled_player.team == "blue":
                target = self.field.get_goal_position("blue")
            else:
                target = self.field.get_goal_position("red")
            
            self.controlled_player.kick_ball(self.ball, target[0], target[1])
            self.kick_pressed = True
        elif not space_pressed:
            self.kick_pressed = False
    
    def update(self, dt):
        """Update game state"""
        # Update time
        self.game_time += dt
        
        # Update controlled player
        self.controlled_player.update(self.width, self.height)
        
        # Update AI players (red team)
        for player in self.players_red:
            player.ai_move(self.ball, self.width, self.height, self.players_red)
            player.update(self.width, self.height)
            
            # AI kick logic - kick ball if close enough
            if player.can_kick_ball(self.ball):
                # Randomly decide to kick (gives it an action chance)
                import random
                if random.random() > 0.7:
                    target = self.field.get_goal_position("red")
                    player.kick_ball(self.ball, target[0], target[1])
        
        # Update blue players that aren't controlled
        for i, player in enumerate(self.players_blue):
            if i > 0:  # Skip controlled player
                player.ai_move(self.ball, self.width, self.height, self.players_blue)
                player.update(self.width, self.height)
        
        # Update ball
        self.ball.update(self.width, self.height)
        
        # Handle ball-player interactions
        self.check_ball_player_interactions()
        
        # Check for goals
        scorer = self.field.check_goal(self.ball)
        if scorer and self.goal_timer == 0:
            if scorer == "blue":
                self.score_blue += 1
            else:
                self.score_red += 1
            self.last_goal_scorer = scorer
            self.goal_timer = 30  # 0.5 second timer at 60 FPS
            self.reset_after_goal(scorer)
        
        # Decrement goal timer
        if self.goal_timer > 0:
            self.goal_timer -= 1
    
    def check_ball_player_interactions(self):
        """Check collisions between ball and players"""
        all_players = self.players_blue + self.players_red
        
        for player in all_players:
            if player.can_kick_ball(self.ball):
                # Simple physics: push ball away if close
                dx = self.ball.x - player.x
                dy = self.ball.y - player.y
                distance = (dx**2 + dy**2)**0.5
                
                if distance < player.kick_range and distance > 0:
                    # Add some push to the ball
                    self.ball.velocity_x += (dx / distance) * 1.5
                    self.ball.velocity_y += (dy / distance) * 1.5
    
    def reset_after_goal(self, scorer):
        """Reset game after a goal is scored"""
        # Reset ball to center
        self.ball.reset(self.width // 2, self.height // 2)
        
        # Reset players to starting positions
        self.players_blue[0].x = self.width // 4
        self.players_blue[0].y = self.height // 2
        
        self.players_blue[1].x = self.width // 4 - 80
        self.players_blue[1].y = self.height // 3
        
        self.players_blue[2].x = self.width // 4 - 80
        self.players_blue[2].y = 2 * self.height // 3
        
        self.players_red[0].x = 3 * self.width // 4
        self.players_red[0].y = self.height // 2
        
        self.players_red[1].x = 3 * self.width // 4 + 80
        self.players_red[1].y = self.height // 3
        
        self.players_red[2].x = 3 * self.width // 4 + 80
        self.players_red[2].y = 2 * self.height // 3
    
    def is_game_over(self):
        """Check if game time is up"""
        return self.game_time >= self.game_duration
    
    def get_winner(self):
        """Get the winning team"""
        if self.score_blue > self.score_red:
            return "Blue Team Wins!"
        elif self.score_red > self.score_blue:
            return "Red Team Wins!"
        else:
            return "Tie Game!"
    
    def draw(self, surface):
        """Draw the entire game"""
        # Draw field
        self.field.draw(surface)
        
        # Draw ball
        self.ball.draw(surface)
        
        # Draw players
        for player in self.players_blue:
            player.draw(surface)
        for player in self.players_red:
            player.draw(surface)
        
        # Draw UI
        self.draw_ui(surface)
    
    def draw_ui(self, surface):
        """Draw game UI elements"""
        font_large = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 24)
        
        # Draw score
        score_text = font_large.render(f"{self.score_blue} - {self.score_red}", True, (255, 255, 255))
        surface.blit(score_text, (self.width // 2 - 70, 20))
        
        # Draw time
        remaining_time = max(0, self.game_duration - self.game_time)
        time_text = font_small.render(f"Time: {int(remaining_time)}s", True, (255, 255, 255))
        surface.blit(time_text, (10, 10))
        
        # Draw instructions
        instructions = [
            "ARROW KEYS: Move",
            "SPACE: Kick",
            "R: Restart",
            "ESC: Quit"
        ]
        y_offset = self.height - 100
        for instruction in instructions:
            inst_text = font_tiny.render(instruction, True, (255, 255, 255))
            surface.blit(inst_text, (10, y_offset))
            y_offset += 25
        
        # Draw game over message
        if self.is_game_over():
            # Semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            
            winner = self.get_winner()
            game_over_text = font_large.render("GAME OVER", True, (255, 255, 0))
            winner_text = font_large.render(winner, True, (0, 255, 0))
            restart_text = font_small.render("Press R to Restart", True, (255, 255, 255))
            
            surface.blit(game_over_text, (self.width // 2 - 200, self.height // 2 - 80))
            surface.blit(winner_text, (self.width // 2 - 200, self.height // 2))
            surface.blit(restart_text, (self.width // 2 - 150, self.height // 2 + 80))
