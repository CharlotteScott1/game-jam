import pygame
import random
import sys
from ant import Ant
from mob import Mob
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600


# Game variables
BASEX = 0
BASEY = 0
# fonts
font = pygame.font.Font('freesansbold.ttf', 20)
# Game variables
BASEX = 150
BASEY = 150
BASERAD = 45
LEAFMULTIPLIER = 0.05

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CIRCLE_COLOR = (0, 255, 0)
GREEN = (55, 153, 35)
BROWN = (77, 39, 39)
NUM_ANTS = 5
NUM_MOBS = 14

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Jam")  # TODO : Change lol


# Clock for controlling frame rate
clock = pygame.time.Clock()


def spawnLeaves(leafPiles):
    """ Return leafPiles"""
    x = random.randint(50+BASERAD, WIDTH-50)
    y = random.randint(50+BASERAD, HEIGHT-30)

    distFromBase = math.sqrt((abs(BASEX - x)**2) + (abs(BASEY-y)**2))
    numLeaves = int(distFromBase * LEAFMULTIPLIER)

    leafPiles += [[pygame.Rect(x, y, max(numLeaves*2.5, 30),
                               max(numLeaves*2, 30)), numLeaves]]

    return leafPiles


def drawLeaves(leafPiles):

    for pile in leafPiles:

        leaf = pygame.image.load("leavesResized.png")
        leaf = pygame.transform.scale(leaf, (pile[0].width, pile[0].height))
        screen.blit(leaf, (pile[0].x, pile[0].y))
        # pygame.draw.rect(
        #   screen, BROWN, (pile[0].x, pile[0].y, pile[0].width, pile[0].height))
        numText = font.render(str(pile[1]), True, WHITE)
        screen.blit(numText, (pile[0].x, pile[0].y))


def pickUpLeaves(ants, leafPiles):
    toPop = []
    for ant in ants:
        if not ant.isCarrying:
            if pygame.Rect.collidelist(pygame.Rect(ant.x, ant.y, 20, 30), list(map(lambda x: x[0], leafPiles))):
                for leaf in leafPiles:
                    if pygame.Rect.colliderect(pygame.Rect(ant.x, ant.y, 20, 30), leaf[0]):
                        leaf[0].width -= 2
                        leaf[0].height -= 2
                        leaf[1] -= 1

                        if leaf[1] < 1:
                            toPop += [leaf]

                        ant.isCarrying = True
                        break

    for leaf in toPop:
        if leaf in leafPiles:
            leafPiles.remove(leaf)
            leafPiles = spawnLeaves(leafPiles)


def depositLeaves(ants, score):
    """returns score"""
    # on collision with base
    # number of leaves carrying = 0
    # score += number of leaves

    for ant in ants:
        if ant.isCarrying:
            if math.sqrt((abs(ant.x - BASEX) ** 2)+(abs(ant.y - BASEY)**2)) < BASERAD:
                ant.isCarrying = False
                score += 1
    return score


# Main game loop

def main():

    leafPiles = []
    # Spawn initial leaves
    score = 0
    for i in range(10):
        leafPiles = spawnLeaves(leafPiles)
    running = True

    bob = Ant("Bob", player_controlled=True)
    ants = [bob]

    for i in range(NUM_ANTS):
        ants.append(Ant(i, following=ants[i]))

    for i, ant in enumerate(ants[:-1]):
        ant.in_trail = ants[i+1]

    mobs = []

    for i in range(NUM_MOBS):
        radius = random.randint(30, 100)
        x, y = random.randint(
            50+radius+BASERAD, WIDTH), random.randint(50+radius+BASERAD, HEIGHT)
        distance = math.sqrt((x - 50) ** 2 + (y - 50) ** 2)
        # Scale speed with distance, minimum speed is 1
        speed = max(1, distance / 1000)
        mobs.append(Mob(i, (x, y), radius, speed=speed))

    while running:
        # Clear screen
        screen.fill(GREEN)
        # Handle events

        if not bob:
            running = False
            break

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
            if ant.distance_to_lead() > 30:
                ant.move_forward()
            if ant.alive:
                ant.draw(screen)
                if ant.following:
                    print(f"{ant.id} following {ant.following.id}")
            # Update display

        for mob in mobs:
            mob.update(ants)
            mob.draw(screen)

        if not bob.alive:
            bob = bob.in_trail

        pickUpLeaves(ants, leafPiles)
        prevScore = score
        score = depositLeaves(ants, score)

        for i in range((score // 5) - (prevScore//5)):
            newAnt = Ant(len(ants)-1, following=ants[-1])
            ants[-1].in_trail = newAnt
            ants += [newAnt]

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Game over screen
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 -
                game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 -
                score_text.get_width() // 2, HEIGHT // 2 + 10))
    ending = True
    while ending:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ending = False

    pygame.quit()


if __name__ == "__main__":
    main()
