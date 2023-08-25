import pygame
import random
import math

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Шарики || ??? FPS || 0 Шаров')

default_gravity = 0.5
gravity = default_gravity
physics_enabled = True
collision_enabled = False

class ThrownBall:
    def __init__(self, x, y):
        self.radius = 20
        self.x = x
        self.y = y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.speed = 0
        self.angle = random.uniform(0, math.pi * 2)
    
    def update(self):
        if physics_enabled:
            self.speed += gravity
            self.x += math.cos(self.angle) * self.speed
            self.y += math.sin(self.angle) * self.speed

            if self.y >= screen_height - self.radius:
                self.y = screen_height - self.radius
                self.speed *= -0.8
            if self.x <= left_boundary + self.radius or self.x >= right_boundary - self.radius:
                self.angle = math.pi - self.angle
            if self.y <= top_boundary + self.radius:
                self.y = top_boundary + self.radius
                self.speed *= -0.8
        
        if collision_enabled:
            for ball in balls:
                if ball != self:
                    distance = math.sqrt((self.x - ball.x)**2 + (self.y - ball.y)**2)
                    if distance <= self.radius + ball.radius:
                        angle_between = math.atan2(ball.y - self.y, ball.x - self.x)
                        overlap = self.radius + ball.radius - distance
                        self.x -= math.cos(angle_between) * overlap * 0.5
                        self.y -= math.sin(angle_between) * overlap * 0.5

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

balls = []

def show_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(1000)

def input_gravity():
    global gravity
    gravity_input = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        gravity_value = float(gravity_input)
                        if gravity_value == 0:
                            gravity = default_gravity
                            print(f"Гравитация установлена на дефолтное значение: {gravity}")
                        else:
                            gravity = gravity_value
                            print(f"Гравитация установлена на {gravity}")
                        input_active = False
                    except ValueError:
                        gravity_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    gravity_input = gravity_input[:-1]
                else:
                    gravity_input += event.unicode
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Введите значение гравитации (0 для дефолта):", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(text_surface, text_rect)
        input_surface = font.render(gravity_input, True, (255, 255, 255))
        input_rect = input_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(input_surface, input_rect)
        pygame.display.flip()

def help_menu():
    help_text = [
        "Нажмите G, чтобы ввести значение гравитации",
        "Нажмите H, чтобы отобразить меню справки",
        "Нажмите C, чтобы очистить шарики",
        "Нажмите F, чтобы включить/выключить физику",
        "Нажмите P, чтобы включить/выключить коллизии",
        "Нажмите Q, чтобы выйти из приложения"
    ]
    help_surface = pygame.Surface((screen_width, screen_height))
    help_surface.fill((0, 0, 0))
    font = pygame.font.Font(None, 24)
    for i, line in enumerate(help_text):
        text_surface = font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=(10, 10 + i * 40))
        help_surface.blit(text_surface, text_rect)
    screen.blit(help_surface, (0, 0))
    pygame.display.flip()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                waiting_for_input = False

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                balls.append(ThrownBall(x, y))
                pygame.display.set_caption(f'Шарики || {int(clock.get_fps())} FPS || {len(balls)} Шаров')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                balls = []
                show_message('Шарики отчищены')
                pygame.display.set_caption(f'Шарики || {int(clock.get_fps())} FPS || {len(balls)} Шаров')
            if event.key == pygame.K_f:
                physics_enabled = not physics_enabled
                show_message('Физика включена' if physics_enabled else 'Физика отключена')
            if event.key == pygame.K_p:
                collision_enabled = not collision_enabled
                show_message('Коллизия включена' if collision_enabled else 'Коллизия отключена')
            if event.key == pygame.K_g:
                input_gravity()
            if event.key == pygame.K_h:
                help_menu()

    # Удаление шаров, выходящих за границу экрана
    balls = [ball for ball in balls if 0 <= ball.x <= screen_width and 0 <= ball.y <= screen_height]

    screen.fill((0, 0, 0))

    left_boundary = 0
    right_boundary = screen_width
    top_boundary = 0

    for ball in balls:
        ball.update()
        ball.draw()

    pygame.display.flip()
    pygame.display.set_caption(f'Шарики || {int(clock.get_fps())} FPS || {len(balls)} Шаров')
    clock.tick(60)

pygame.quit()
