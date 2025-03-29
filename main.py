import pygame
import random
import sys
from ant import Ant
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

#fonts
font = pygame.font.Font('freesansbold.ttf', 20)
# Game variables
BASEX = 50
BASEY = 50
BASERAD = 45
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

    leafPiles += [pygame.Rect(x, y, numLeaves, numLeaves)]

    return leafPiles


def drawLeaves(leafPiles):

    for pile in leafPiles:

        pygame.draw.rect(
            screen, BROWN, (pile.x, pile.y, pile.width, pile.height))
        numText = font.render(str(pile.height), True, WHITE, BROWN)
        screen.blit(numText, (pile.x, pile.y))


def pickUpLeaves(ants, leafPiles):

    for ant in ants:
        if not ant.isCarrying:
            if pygame.Rect.collidelist(pygame.Rect(ant.x, ant.y, 10, 20), leafPiles):
                for leaf in leafPiles:
                    if pygame.Rect.colliderect(pygame.Rect(ant.x, ant.y, 10, 20), leaf):
                        leaf.width -= 1
                        leaf.height -= 1

                        ant.isCarrying = True
                        break
    


def depositLeaves(ants, score):
    """returns score"""
    # on collision with base
    # number of leaves carrying = 0
    # score += number of leaves

    for ant in ants:
        if ant.isCarrying:
            if math.sqrt((abs(ant.x - BASEX) **2)+(abs(ant.y - BASEY)**2)) < BASERAD:
                ant.isCarrying = False
                score += 1
    return score

    


# Main game loop

def main():

    leafPiles = []
    score = 0
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

        pygame.draw.circle(screen, BROWN, (BASEX, BASEY), BASERAD)

        scoreText = font.render(str(score), True, WHITE, BROWN)
        screen.blit(scoreText, (BASEX-5, BASEY-10))
        drawLeaves(leafPiles)

        bob.draw(screen)
        for ant in ants[1:]:
            ant.look_at_lead()
            print(ant.distance_to_lead())
            if ant.distance_to_lead() > 30:
                ant.move_forward()
            ant.draw(screen)
            # Update display


        pickUpLeaves(ants, leafPiles)
        score = depositLeaves(ants, score)
        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
