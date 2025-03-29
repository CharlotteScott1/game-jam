import pygame
import math


class Ant:
    def __init__(self, id, x=150, y=150, following=None, in_trail=None, player_controlled=False):
        """Initialize the ant's position."""
        self.id = id
        self.x = x
        self.y = y
        self.heading = 0
        self.speed = 1
        self.following: Ant = following
        self.in_trail: Ant = in_trail
        self.player_controlled = player_controlled
        self.colour = (255, 0, 0)
        self.alive = True

        self.isCarrying = False

    def move_forward(self):
        """Move the ant forward based on its heading."""
        radians = math.radians(-self.heading)
        self.x += self.speed * math.cos(radians)
        self.y -= self.speed * math.sin(radians)

    def turn_left(self):
        """Turn left"""
        self.heading -= 5

    def turn_right(self):
        """Turn Right"""
        self.heading += 5

    def get_position(self):
        """Return the current position of the ant."""
        return self.x, self.y

    def draw(self, screen):
        """Draw the ant's current position."""

        ant_image = pygame.image.load("ant.png")
        ant_image = pygame.transform.scale(ant_image, (25, 25))
        ant_image = ant_image.convert_alpha()

        # Change the color of the PNG
        colorized_image = pygame.Surface(ant_image.get_size(), pygame.SRCALPHA)
        colorized_image.fill((255, 0, 0))
        ant_image.blit(colorized_image, (0, 0),
                       special_flags=pygame.BLEND_RGBA_MULT)

        rotated_image = pygame.transform.rotate(ant_image, -self.heading - 90)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect.topleft)

        # If the ant is carrying something, draw a leaf nearby
        if self.isCarrying:
            leaf_image = pygame.image.load("leaf.png")
            leaf_image = pygame.transform.scale(leaf_image, (15, 15))
            leaf_image = pygame.transform.rotate(leaf_image, 180)
            leaf_image = leaf_image.convert_alpha()

            # Position the leaf slightly above the ant
            leaf_rect = leaf_image.get_rect(center=(self.x, self.y - 20))
            screen.blit(leaf_image, leaf_rect.topleft)

    def look_at_lead(self):
        """Update the position of the next ant in the sequence"""
        if self.following:
            dx = self.following.x - self.x
            dy = self.following.y - self.y
            angle_to_next = math.degrees(math.atan2(-dy, dx))
            self.heading = -angle_to_next

    def distance_to_lead(self):
        """Calculate the distance between two ants."""
        if self.following:
            return math.sqrt((self.following.x - self.x) ** 2 + (self.following.y - self.y) ** 2)
        return 0

    def remove(self):
        """Remove this ant from the chain."""

        if self.following:
            self.following.in_trail = self.in_trail

        if self.in_trail:
            self.in_trail.following = self.following

        self.following = None
        self.alive = False
