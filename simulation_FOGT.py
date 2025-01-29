import pygame
import numpy as np
from wave_eqn2d_FOGT import WaveEqn2D

# Konfiguracja symulacji
A = 80
dt = 1
T = 50
freq = 2 * np.pi / T
nx = ny = 200

# Inicjalizacja symulacji
sim = WaveEqn2D(nx, ny, dt=dt, use_mur_abc=True)

# Pozycje przeszkody i źródeł
obstacle_rect = pygame.Rect(80 * 3, 80 * 3, 40 * 3, 40 * 3)
source_positions = [pygame.Rect(ny // 4 * 3, nx // 4 * 3, 6, 6), pygame.Rect(3 * ny // 4 * 3, 3 * nx // 4 * 3, 6, 6)]

# Inicjalizacja Pygame
pygame.init()
scale = 3  # Skalowanie obrazu
width, height = nx * scale, ny * scale
screen = pygame.display.set_mode((width, height + 50))  # Dodatkowe miejsce na przyciski
clock = pygame.time.Clock()

# Przyciski
font = pygame.font.Font(None, 36)
start_button = pygame.Rect(50, height + 10, 100, 30)
reset_button = pygame.Rect(200, height + 10, 100, 30)
running_simulation = False
moving_source = None
moving_obstacle = False


def update(i):
    """Aktualizacja symulacji o jeden krok."""
    if running_simulation:
        for rect in source_positions:
            y, x = rect.y // scale, rect.x // scale
            sim.u[0, y, x] = A * np.sin(i * freq)
        sim.update()
        oy, ox = obstacle_rect.y // scale, obstacle_rect.x // scale
        oh, ow = obstacle_rect.height // scale, obstacle_rect.width // scale
        sim.u[:, oy:oy + oh, ox:ox + ow] = 0  # Zatrzymanie fal na przeszkodzie


def draw():
    """Rysowanie symulacji na ekranie."""
    surface = np.clip(sim.u[0], 0, 40) / 40 * 255  # Normalizacja do 0-255
    surface = np.kron(surface, np.ones((scale, scale)))  # Poprawione skalowanie
    surface = np.stack((surface, surface, 255 - surface), axis=-1)  # Kolor niebieski

    # Dopasowanie rozmiaru do ekranu
    surface = pygame.surfarray.make_surface(surface.astype(np.uint8))
    surface = pygame.transform.scale(surface, (width, height))
    screen.blit(surface, (0, 0))

    # Rysowanie przeszkody w poprawnej pozycji
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(obstacle_rect.y, obstacle_rect.x, obstacle_rect.height, obstacle_rect.width))

    # Rysowanie źródeł jako czarnych kwadratów przed startem
    if not running_simulation:
        for rect in source_positions:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(rect.y, rect.x, rect.height, rect.width))

    # Rysowanie przycisków
    pygame.draw.rect(screen, (0, 255, 0), start_button)
    pygame.draw.rect(screen, (255, 0, 0), reset_button)
    screen.blit(font.render("Start", True, (0, 0, 0)), (start_button.x + 25, start_button.y + 5))
    screen.blit(font.render("Reset", True, (0, 0, 0)), (reset_button.x + 20, reset_button.y + 5))


i = 0
running = True
while running:
    screen.fill((255, 255, 255))  # Czyszczenie ekranu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if start_button.collidepoint(mx, my):
                running_simulation = not running_simulation  # Przełączanie start/stop
            elif reset_button.collidepoint(mx, my):
                sim.u.fill(0)  # Reset symulacji
                i = 0
                running_simulation = False
            elif not running_simulation:
                for idx, rect in enumerate(source_positions):
                    if rect.collidepoint(mx, my):
                        moving_source = idx
                        break
                if obstacle_rect.collidepoint(mx, my):
                    moving_obstacle = True
        elif event.type == pygame.MOUSEBUTTONUP:
            moving_source = None
            moving_obstacle = False
        elif event.type == pygame.MOUSEMOTION and not running_simulation:
            mx, my = event.pos
            if moving_source is not None:
                source_positions[moving_source].x = my
                source_positions[moving_source].y = mx
            if moving_obstacle:
                obstacle_rect.x = my - obstacle_rect.width // 2
                obstacle_rect.y = mx - obstacle_rect.height // 2

    update(i)
    draw()
    pygame.display.flip()
    clock.tick(60)
    i += 1

pygame.quit()
