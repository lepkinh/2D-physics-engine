import pygame
import math
import random
from pygame.math import Vector2


pygame.init()
pygame.font.init()

# constant variables
WINDOW_SIZE = (800, 600)
FPS = 60
GRAVITY = Vector2(0, 981.0)  # pixels/s/s
ELASTICITY = 0.7
FRICTION = 0.99

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Circle:
    def __init__(self, pos, radius, color):
        self.pos = Vector2(pos)
        self.velocity = Vector2(0, 0)
        self.radius = radius
        self.color = color
        self.mass = math.pi * radius * radius  # m proportional to area

    def update(self, dt):
        # gravity
        self.velocity += GRAVITY * dt
        
        # friction
        self.velocity *= FRICTION
        
        # position
        self.pos += self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont(None, 24)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        
    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        # draw slider handle
        handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        pygame.draw.circle(screen, WHITE, (int(handle_x), self.rect.centery), 8)
        
    def update(self, mouse_pos):
        if self.dragging:
            x = max(self.rect.left, min(mouse_pos[0], self.rect.right))
            self.value = self.min_val + (x - self.rect.left) / self.rect.width * (self.max_val - self.min_val)
            
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
            handle_rect = pygame.Rect(handle_x - 8, self.rect.y - 4, 16, 16)
            if handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

class PhysicsEngine:
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("2D Physics Engine")
        
        # UI elements
        self.radius_slider = Slider(10, 20, 200, 5, 50, 20)
        self.color_buttons = [
            Button(10, 40, 60, 30, "Red", RED),
            Button(80, 40, 60, 30, "Green", GREEN),
            Button(150, 40, 60, 30, "Blue", BLUE)
        ]
        
        self.circles = []
        self.current_color = RED
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        
    def handle_collisions(self):
        # wall collisions
        for circle in self.circles:
            # bottom surface
            if circle.pos.y + circle.radius > WINDOW_SIZE[1]:
                circle.pos.y = WINDOW_SIZE[1] - circle.radius
                circle.velocity.y *= -ELASTICITY
            
            # top surface
            if circle.pos.y - circle.radius < 0:
                circle.pos.y = circle.radius
                circle.velocity.y *= -ELASTICITY
            
            # right surface
            if circle.pos.x + circle.radius > WINDOW_SIZE[0]:
                circle.pos.x = WINDOW_SIZE[0] - circle.radius
                circle.velocity.x *= -ELASTICITY
            
            # left surface
            if circle.pos.x - circle.radius < 0:
                circle.pos.x = circle.radius
                circle.velocity.x *= -ELASTICITY

        # circle collisions
        for i, circle1 in enumerate(self.circles):
            for circle2 in self.circles[i + 1:]:
                diff = circle1.pos - circle2.pos
                distance = diff.length()
                
                if distance < circle1.radius + circle2.radius:
                    normal = diff / distance
                    relative_velocity = circle1.velocity - circle2.velocity
                    impulse = -2 * relative_velocity.dot(normal) / (1/circle1.mass + 1/circle2.mass)
                    
                    circle1.velocity += (impulse / circle1.mass) * normal * ELASTICITY
                    circle2.velocity -= (impulse / circle2.mass) * normal * ELASTICITY
                    
                    overlap = (circle1.radius + circle2.radius - distance) / 2
                    circle1.pos += normal * overlap
                    circle2.pos -= normal * overlap

    def run(self):
        running = True
        while running:
            time_delta = self.clock.tick(FPS)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # checking UI interaction
                    if mouse_pos[1] > 80:  # below UI area
                        new_circle = Circle(
                            mouse_pos,
                            self.radius_slider.value,
                            self.current_color
                        )
                        self.circles.append(new_circle)
                    else:
                        for button in self.color_buttons:
                            if button.is_clicked(mouse_pos):
                                self.current_color = button.color
                                
                self.radius_slider.handle_event(event)
                
            # update
            mouse_pos = pygame.mouse.get_pos()
            self.radius_slider.update(mouse_pos)
            
            for circle in self.circles:
                circle.update(time_delta)
            
            self.handle_collisions()
            
            # draw
            self.screen.fill(WHITE)
            
            # draw UI
            self.radius_slider.draw(self.screen)
            for button in self.color_buttons:
                button.draw(self.screen)
                
            # draw radius value
            radius_text = self.font.render(f"Radius: {int(self.radius_slider.value)}", True, WHITE)
            self.screen.blit(radius_text, (220, 15))
            
            # draw circles
            for circle in self.circles:
                circle.draw(self.screen)
            
            # draw preview circle
            if mouse_pos[1] > 80:  # dont show preview over UI
                pygame.draw.circle(
                    self.screen,
                    self.current_color,
                    mouse_pos,
                    int(self.radius_slider.value),
                    1  # draw outline only
                )
            
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    engine = PhysicsEngine()
    engine.run()