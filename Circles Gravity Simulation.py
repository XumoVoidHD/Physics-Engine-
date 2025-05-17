import pygame
import math
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)


def check_collision(c1, c2):
    dx = c1.x - c2.x
    dy = c1.y - c2.y
    distance = math.hypot(dx, dy)
    return distance < c1.radius + c2.radius


class Circle:
    def __init__(self, x, y, radius=20, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.color = color
        self.radius = radius

    def move(self, keys, others):

        if keys[pygame.K_a]:
            self.vx = -2
        elif keys[pygame.K_d]:
            self.vx = 2
        else:
            self.vx = 0

        if keys[pygame.K_w] and (self.on_ground() or self.on_top_of_other(others)):
            self.vy = self.jump_strength

        self.vy += self.gravity

        old_x, old_y = self.x, self.y

        self.x += self.vx
        self.y += self.vy

        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))

        if self.y + self.radius > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius
            self.vy = 0

        for other in others:
            if other is not self and check_collision(self, other):
                self.x, self.y = old_x, old_y
                self.vy = 0
                break

    def on_ground(self):
        return self.y + self.radius >= SCREEN_HEIGHT - 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def on_top_of_other(self, others):
        for other in others:
            if other is not self:
                if (
                        abs(self.x - other.x) < self.radius + other.radius and
                        abs((self.y + self.radius) - (other.y - other.radius)) <= 1
                ):
                    return True
        return False

    def get_info(self):
        return f"Pos: ({int(self.x)}, {int(self.y)}) Vel: ({int(self.vx)}, {int(self.vy)})"


circles = [
    Circle(100, 100),
    Circle(200, 150, color=(255, 255, 0)),
    Circle(300, 200, color=(0, 255, 0))
]

running = True
selected_circle = None

while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            for circle in circles:
                dx = circle.x - mouse_x
                dy = circle.y - mouse_y
                if math.hypot(dx, dy) <= circle.radius:
                    selected_circle = circle

    keys = pygame.key.get_pressed()
    for circle in circles:
        if circle is selected_circle:
            circle.move(keys, circles)
        circle.draw(screen)

    for i, circle in enumerate(circles):
        info_text = font.render(f"Circle {i + 1}: {circle.get_info()}", True, (255, 255, 255))
        screen.blit(info_text, (SCREEN_WIDTH - 300, 10 + i * 20))

    pygame.display.update()

pygame.quit()
