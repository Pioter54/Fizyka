import pygame
import numpy as np
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Oscylator harmoniczny')

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

slider = Slider(screen, 100, 500, 300, 10, min=0, max=10, step=1)
output = TextBox(screen, 475, 200, 50, 50, fontSize=30)

# Constants
m1, m2 = 1.0, 1.0  # Masses
k1, k2, k3 = slider.getValue(), slider.getValue(), slider.getValue()  # Spring constants
omega0 = 1.0  # Natural frequency of each mass (assuming identical masses and springs)
fps = 60
clock = pygame.time.Clock()

# Time array
t = np.linspace(0, 200, 10000)

# Frequencies for normal modes
omega_1 = np.sqrt(omega0**2 + 2 * k3 / m1)
omega_2 = omega0

# Amplitudes and phase differences (assuming some initial conditions)
A1_1, A1_2 = 1.0, 0.5  # Amplitudes for mass m1 in each mode
A2_1, A2_2 = 1.0, -0.5  # Amplitudes for mass m2 in each mode

# Displacements as a function of time
x1 = A1_1 * np.cos(omega_1 * t) + A1_2 * np.cos(omega_2 * t)
x2 = A2_1 * np.cos(omega_1 * t) + A2_2 * np.cos(omega_2 * t)

# Scale and shift for visualization
scale = 100
shift_x1 = width // 4
shift_x2 = 3 * width // 4
shift_y = height // 2
position_print_height = 50  # Height for position printing

# Main loop
running = True
time_index = 0
base_wave_y = shift_y + position_print_height  # Initial y-coordinate for the wave

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(WHITE)

    # Update positions
    pos_x1 = shift_x1 + x1[time_index] * scale
    pos_x2 = shift_x2 + x2[time_index] * scale

    # Draw masses
    pygame.draw.circle(screen, RED, (int(pos_x1), shift_y), 20)
    pygame.draw.circle(screen, BLUE, (int(pos_x2), shift_y), 20)

    # Draw springs (just lines here for simplicity)
    pygame.draw.line(screen, BLACK, (0, shift_y), (pos_x1 - 20, shift_y), 5)  # Left spring
    pygame.draw.line(screen, BLACK, (pos_x1 + 20, shift_y), (pos_x2 - 20, shift_y), 5)  # Middle spring
    pygame.draw.line(screen, BLACK, (pos_x2 + 20, shift_y), (width, shift_y), 5)  # Right spring

    # Draw position printing (sine-like waves under the masses)
    wave_y = base_wave_y
    for i in range(time_index):
        wave_y = base_wave_y + i // 10  # Move the wave downward over time
        pygame.draw.line(screen, RED, (shift_x1 + x1[i] * scale, wave_y), (shift_x1 + x1[i + 1] * scale, wave_y), 2)
        pygame.draw.line(screen, BLUE, (shift_x2 + x2[i] * scale, wave_y), (shift_x2 + x2[i + 1] * scale, wave_y), 2)

    # Update slider value display
    k1, k2, k3 = slider.getValue(), slider.getValue(), slider.getValue()
    output.setText(str(k1))
    pygame_widgets.update(pygame.event.get())

    # Update display
    pygame.display.flip()

    # Increment time index
    time_index = (time_index + 1) % len(t)

    # Control the frame rate
    clock.tick(fps)

pygame.quit()
