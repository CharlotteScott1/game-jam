import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CIRCLE_COLOR = (0, 255, 0)

# Circle properties
CIRCLE_RADIUS = 20
CIRCLE_SPEED = 5

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Jam")  # TODO : Change lol

# Clock for controlling frame rate
clock = pygame.time.Clock()

# List to store circles
circles = []


def create_circle():
    x = random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS)
    y = -CIRCLE_RADIUS  # Start above the screen
    return {"x": x, "y": y}

# Main game loop


def main():
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill(BLACK)

        # Add new circles randomly
        if random.random() < 0.02:  # Adjust probability for more/less circles
            circles.append(create_circle())

        # Update and draw circles
        for circle in circles:
            circle["y"] += CIRCLE_SPEED
            pygame.draw.circle(screen, CIRCLE_COLOR,
                               (circle["x"], circle["y"]), CIRCLE_RADIUS)

        # Remove circles that move off the screen
        circles[:] = [circle for circle in circles if circle["y"] -
                      CIRCLE_RADIUS < HEIGHT]

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
