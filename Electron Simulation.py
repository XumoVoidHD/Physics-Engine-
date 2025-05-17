import pygame
import math
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WALL_DAMPING = 1

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
k = 8.9875517923e9


def check_collision(c1, c2):
    dx = c1.x - c2.x
    dy = c1.y - c2.y
    distance = math.hypot(dx, dy)
    return distance < c1.radius + c2.radius


class Electrons:
    def __init__(self, name, mass, charge, x, y, radius=10, color=(255, 0, 0)):
        self.name = name
        self.mass = mass
        self.charge = charge
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.color = color
        self.radius = radius

    def update(self, others):
        self.ax = 0
        self.ay = 0
        for other in others:
            if other is not self:
                dx = self.x - other.x
                dy = self.y - other.y
                r_squared = dx ** 2 + dy ** 2
                if r_squared < 1:
                    r_squared = 1
                r = math.sqrt(r_squared)

                force_magnitude = (k * self.charge * other.charge * 1e-12) / r_squared
                unit_dx = dx / r
                unit_dy = dy / r

                self.ax += force_magnitude * unit_dx / self.mass
                self.ay += force_magnitude * unit_dy / self.mass

    def move(self, dt):
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        max_speed = 300
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > max_speed:
            scale = max_speed / speed
            self.vx *= scale
            self.vy *= scale

        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -WALL_DAMPING
        elif self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.vx *= -WALL_DAMPING

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -WALL_DAMPING
        elif self.y + self.radius > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius
            self.vy *= -WALL_DAMPING

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def get_info(self):
        return f"{self.name}: Pos: ({int(self.x)}, {int(self.y)}) Vel: ({int(self.vx)}, {int(self.vy)}) Charge: ({int(self.charge)})"


circles = [Electrons(name=f"p{1}", mass=1, charge=-5e3, x=random.randint(0, 800), y=random.randint(0, 600),
                     color=(255, 255, 255))]

number_of_electrons = int(input("Number of electrons: "))
for i in range(0, number_of_electrons):
    x = Electrons(name=f"e{i}", mass=1, charge=1e4 * random.choice([1]), x=random.randint(0, 800),
                  y=random.randint(0, 600),
                  color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    circles.append(x)

running = True

while running:
    dt = clock.tick(60) / 1000
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for circle in circles:
        circle.update(circles)

    for circle in circles:
        circle.move(dt)
        circle.draw(screen)

    for i, circle in enumerate(circles):
        info_text = font.render(f"{circle.get_info()}", True, (255, 255, 255))
        screen.blit(info_text, (SCREEN_WIDTH - 425, 10 + i * 20))

    pygame.display.update()

pygame.quit()
