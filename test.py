import pygame
import numpy as np
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

# Inicjalizacja Pygame
pygame.init()

# Wymiary ekranu
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Oscylator harmoniczny')

# Kolory
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 0, 255)

# Inicjalizacja widgetów
slider = Slider(screen, 100, 540, 200, 10, min=0.01, max=0.4, step=0.01)
output = TextBox(screen, 310, 532, 36, 26, fontSize=15)
sliderm = Slider(screen, 100, 500, 200, 10, min=0.01, max=0.4, step=0.01)
outputm = TextBox(screen, 310, 492, 36, 26, fontSize=15)

# Inicjalizacja czcionki
font = pygame.font.Font(None, 25)

# Stałe
m1, m2 = sliderm.value, sliderm.value  # Masy
k1, k2, k3 = slider.value, slider.value, slider.value  # Stałe sprężyn
omega0 = 3.0  # Częstotliwość naturalna każdej masy (zakładając identyczne masy i sprężyny)
fps = 60
clock = pygame.time.Clock()

# Tablica czasu
t = np.linspace(0, 200, 10000)

# Skalowanie i przesunięcie do wizualizacji
scale = 110
shift_x1 = width // 4
shift_x2 = 3 * width // 4
shift_y = height // 10

# Główna pętla
running = True
time_index = 0
base_wave_y = shift_y  # Początkowa współrzędna y dla fali

# Przechowuje wcześniej rysowane punkty
drawn_points_x1 = []
drawn_points_x2 = []

while running:
    omega_1 = np.sqrt(omega0 ** 2 + 2 * k3 / m1)
    omega_2 = omega0

    # Amplitudy i różnice faz (zakładając pewne warunki początkowe)
    A1_1, A1_2 = 1.0, 0.5  # Amplitudy dla masy m1 w każdym trybie
    A2_1, A2_2 = 1.0, -0.5  # Amplitudy dla masy m2 w każdym trybie

    # Przemieszczenia w funkcji czasu
    x1 = A1_1 * np.cos(omega_1 * t) + A1_2 * np.cos(omega_2 * t)
    x2 = A2_1 * np.cos(omega_1 * t) + A2_2 * np.cos(omega_2 * t)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Wyczyść ekran
    screen.fill(WHITE)

    # Aktualizuj wyświetlaną wartość suwaka
    k1, k2, k3 = slider.getValue(), slider.getValue(), slider.getValue()
    output.setText(str(k1))
    m1, m2 = sliderm.getValue(), sliderm.getValue()
    outputm.setText(str(m1))
    pygame_widgets.update(pygame.event.get())

    # Renderuj i rysuj etykietę
    label_text = font.render('Stała sprężyny (k):', True, BLACK)
    screen.blit(label_text, (100, 480))
    label_text = font.render('Masa (m):', True, BLACK)
    screen.blit(label_text, (100, 520))

    # Aktualizuj pozycje
    pos_x1 = shift_x1 + x1[time_index] * scale
    pos_x2 = shift_x2 + x2[time_index] * scale

    # Rysuj masy
    pygame.draw.circle(screen, RED, (int(pos_x1), shift_y), 20)
    pygame.draw.circle(screen, BLUE, (int(pos_x2), shift_y), 20)

    # Rysuj sprężyny (tylko linie dla uproszczenia)
    pygame.draw.line(screen, GREEN, (0, shift_y), (pos_x1 - 20, shift_y), 5)  # Lewa sprężyna
    pygame.draw.line(screen, BLACK, (pos_x1 + 20, shift_y), (pos_x2 - 20, shift_y), 5)  # Środkowa sprężyna
    pygame.draw.line(screen, PINK, (pos_x2 + 20, shift_y), (width, shift_y), 5)  # Prawa sprężyna

    # Dodaj nowe punkty do listy rysowanych punktów
    drawn_points_x1.append((shift_x1 + x1[time_index] * scale, base_wave_y))
    drawn_points_x2.append((shift_x2 + x2[time_index] * scale, base_wave_y))

    # Usuń punkty, które są poza ekranem
    drawn_points_x1 = [(x, y + 0.2) for x, y in drawn_points_x1 if y < (height-150)]
    drawn_points_x2 = [(x, y + 0.2) for x, y in drawn_points_x2 if y < (height-150)]

    # Rysuj punkty
    for i in range(len(drawn_points_x1) - 1):
        pygame.draw.line(screen, RED, drawn_points_x1[i], drawn_points_x1[i + 1], 1)
        pygame.draw.line(screen, BLUE, drawn_points_x2[i], drawn_points_x2[i + 1], 1)

    # Aktualizuj wyświetlacz
    pygame.display.flip()

    # Zwiększ indeks czasu
    time_index = (time_index + 1) % len(t)

    # Kontroluj liczbę klatek na sekundę
    clock.tick(fps)

pygame.quit()
