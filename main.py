import pygame
import random
import sys
from ant import Ant
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600


# Game variables
BASEX = 0
BASEY = 0
LEAFMULTIPLIER = 0.05


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CIRCLE_COLOR = (0, 255, 0)
GREEN = (55, 153, 35)
BROWN = (77, 39, 39)
NUM_ANTS = 5

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Jam")  # TODO : Change lol


# Clock for controlling frame rate
clock = pygame.time.Clock()


def spawnLeaves(leafPiles):
    """ Return leafPiles"""
    x = random.randint(10, WIDTH)
    y = random.randint(10, HEIGHT)

    distFromBase = math.sqrt((abs(BASEX - x)**2) + (abs(BASEY-y)**2))
    numLeaves = int(distFromBase * LEAFMULTIPLIER)

    leafPiles += [{"x": x, "y": y, "leaves": numLeaves}]

    return leafPiles


def drawLeaves(leafPiles):

    font = pygame.font.Font('freesansbold.ttf', 20)
    for pile in leafPiles:

        pygame.draw.rect(
            screen, BROWN, (pile["x"], pile["y"], pile["leaves"], pile["leaves"]))
        numText = font.render(str(pile["leaves"]), True, WHITE, BROWN)
        screen.blit(numText, (pile["x"], pile["y"]))


def pickUpLeaves():
    # Get collision
    # Sub number of ants from number of leaves
    # update number of leaves carrying
    pass


def depositLeaves():
    # on collision with base
    # number of leaves carrying = 0
    # score += number of leaves
    pass


# Main game loop

def main():

    leafPiles = []
    # Spawn intital leaves
    for i in range(10):
        leafPiles += spawnLeaves(leafPiles)

    running = True

    bob = Ant(player_controlled=True)
    ants = [bob]
    for i in range(NUM_ANTS):
        ants.append(Ant(following=ants[i]))

    while running:
        # Clear screen
        screen.fill(GREEN)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            bob.move_forward()

        if keys[pygame.K_q]:
            bob.turn_left()
        if keys[pygame.K_e]:
            bob.turn_right()

        drawLeaves(leafPiles)

        bob.draw(screen)
        for ant in ants[1:]:
            ant.look_at_lead()
            print(ant.distance_to_lead())
            if ant.distance_to_lead() > 30:
                ant.move_forward()
            ant.draw(screen)
            # Update display

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
