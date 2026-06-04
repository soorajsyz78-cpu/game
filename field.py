import pygame

class Field:
    """Field class representing the football pitch"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.line_color = (255, 255, 255)
        self.field_color = (34, 139, 34)  # Green
        self.goal_width = 100
        self.goal_height = 150
        
    def draw(self, surface):
        """Draw the football field"""
        # Fill background with field color
        surface.fill(self.field_color)
        
        # Draw center line
        pygame.draw.line(surface, self.line_color, 
                        (self.width // 2, 0), 
                        (self.width // 2, self.height), 2)
        
        # Draw center circle
        pygame.draw.circle(surface, self.line_color, 
                          (self.width // 2, self.height // 2), 50, 2)
        
        # Draw halfway line
        pygame.draw.line(surface, self.line_color, 
                        (0, self.height // 2), 
                        (self.width, self.height // 2), 1)
        
        # Draw goal areas
        self.draw_goal_area(surface, True)   # Left goal
        self.draw_goal_area(surface, False)  # Right goal
        
        # Draw boundary
        pygame.draw.rect(surface, self.line_color, 
                        (0, 0, self.width, self.height), 3)
    
    def draw_goal_area(self, surface, left_side=True):
        """Draw goal area and goal posts"""
        if left_side:
            # Left goal area
            goal_x = 0
            goal_y = (self.height - self.goal_height) // 2
            # Draw penalty area
            pygame.draw.rect(surface, self.line_color, 
                           (0, goal_y, 150, self.goal_height), 2)
            # Draw goal post area
            pygame.draw.rect(surface, (255, 100, 100), 
                           (goal_x, goal_y, 20, self.goal_height))
        else:
            # Right goal area
            goal_x = self.width - 20
            goal_y = (self.height - self.goal_height) // 2
            # Draw penalty area
            pygame.draw.rect(surface, self.line_color, 
                           (self.width - 150, goal_y, 150, self.goal_height), 2)
            # Draw goal post area
            pygame.draw.rect(surface, (100, 100, 255), 
                           (goal_x, goal_y, 20, self.goal_height))
    
    def get_goal_position(self, team="blue"):
        """Get the center position of the opponent's goal"""
        if team == "blue":
            # Blue team shoots at right goal
            return self.width - 10, self.height // 2
        else:
            # Red team shoots at left goal
            return 10, self.height // 2
    
    def check_goal(self, ball):
        """Check if a goal has been scored and return the scoring team"""
        goal_area_y_min = (self.height - self.goal_height) // 2
        goal_area_y_max = goal_area_y_min + self.goal_height
        
        # Check left goal (red team scores)
        if ball.x < 25 and goal_area_y_min < ball.y < goal_area_y_max:
            return "red"
        
        # Check right goal (blue team scores)
        if ball.x > self.width - 25 and goal_area_y_min < ball.y < goal_area_y_max:
            return "blue"
        
        return None
