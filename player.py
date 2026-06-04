import pygame
import math

class Player:
    """Player class with movement, AI, and ball control"""
    
    def __init__(self, x, y, team="blue", player_id=1):
        self.x = x
        self.y = y
        self.team = team  # "blue" or "red"
        self.player_id = player_id
        self.width = 20
        self.height = 20
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.color = (0, 100, 255) if team == "blue" else (255, 50, 50)
        self.kick_range = 40
        self.kick_power = 20
        self.stamina = 100
        self.max_stamina = 100
        
    def handle_input(self, keys):
        """Handle keyboard input for player movement"""
        self.velocity_x = 0
        self.velocity_y = 0
        
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
        if keys[pygame.K_UP]:
            self.velocity_y = -self.speed
        if keys[pygame.K_DOWN]:
            self.velocity_y = self.speed
    
    def update(self, width, height):
        """Update player position with boundary checking"""
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Keep player in bounds
        if self.x - self.width // 2 < 0:
            self.x = self.width // 2
        elif self.x + self.width // 2 > width:
            self.x = width - self.width // 2
            
        if self.y - self.height // 2 < 0:
            self.y = self.height // 2
        elif self.y + self.height // 2 > height:
            self.y = height - self.height // 2
    
    def ai_move(self, ball, width, height, other_players=None):
        """AI movement logic - move towards ball with basic strategy"""
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Move towards ball
        dx = ball.x - self.x
        dy = ball.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Scale velocity to avoid overshooting
            scale = min(self.speed, distance) / distance if distance > 0 else 0
            self.velocity_x = dx * scale / distance if distance > 0 else 0
            self.velocity_y = dy * scale / distance if distance > 0 else 0
    
    def can_kick_ball(self, ball):
        """Check if player can reach the ball"""
        distance = math.sqrt((ball.x - self.x)**2 + (ball.y - self.y)**2)
        return distance < self.kick_range
    
    def kick_ball(self, ball, target_x=None, target_y=None):
        """Kick the ball towards a target or in a direction"""
        if self.can_kick_ball(ball):
            if target_x is None:
                # Default kick direction based on team
                if self.team == "blue":
                    ball.kick(1, 0, self.kick_power)
                else:
                    ball.kick(-1, 0, self.kick_power)
            else:
                # Kick towards target
                dx = target_x - self.x
                dy = target_y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance > 0:
                    ball.kick(dx / distance, dy / distance, self.kick_power)
            return True
        return False
    
    def draw(self, surface):
        """Draw the player on the surface"""
        # Draw player body
        pygame.draw.rect(surface, self.color, 
                        (self.x - self.width // 2, self.y - self.height // 2, 
                         self.width, self.height))
        # Draw player number
        font = pygame.font.Font(None, 16)
        text = font.render(str(self.player_id), True, (255, 255, 255))
        surface.blit(text, (self.x - 5, self.y - 5))
    
    def distance_to(self, x, y):
        """Calculate distance to a point"""
        return math.sqrt((self.x - x)**2 + (self.y - y)**2)
