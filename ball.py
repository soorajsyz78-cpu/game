import pygame
import math

class Ball:
    """Ball class with physics simulation for football game"""
    
    def __init__(self, x, y, radius=8):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity_x = 0
        self.velocity_y = 0
        self.friction = 0.98
        self.gravity = 0.3
        
    def update(self, width, height):
        """Update ball position and handle physics"""
        # Apply friction
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        
        # Apply gravity
        self.velocity_y += self.gravity
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Bounce off walls
        if self.x - self.radius < 0:
            self.x = self.radius
            self.velocity_x *= -0.8
        elif self.x + self.radius > width:
            self.x = width - self.radius
            self.velocity_x *= -0.8
            
        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity_y *= -0.8
        elif self.y + self.radius > height:
            self.y = height - self.radius
            self.velocity_y *= -0.8
    
    def kick(self, direction_x, direction_y, power=15):
        """Apply kick force to the ball"""
        magnitude = math.sqrt(direction_x**2 + direction_y**2)
        if magnitude > 0:
            direction_x /= magnitude
            direction_y /= magnitude
            self.velocity_x = direction_x * power
            self.velocity_y = direction_y * power
    
    def draw(self, surface, color=(255, 255, 255)):
        """Draw the ball on the surface"""
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
    
    def distance_to(self, x, y):
        """Calculate distance to a point"""
        return math.sqrt((self.x - x)**2 + (self.y - y)**2)
    
    def reset(self, x, y):
        """Reset ball position and velocity"""
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
