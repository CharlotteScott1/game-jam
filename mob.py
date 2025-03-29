import random
import pygame
import math


class Mob:
    def __init__(self, name, center, radius, speed):
        self.name = name
        self.center = center  # (x_center, y_center)
        self.radius = radius
        self.speed = speed
        self.x = center[0]
        self.y = center[1]
        self.heading = 0
        self.target = None
        self.path = (random.uniform(self.center[0] - self.radius, self.center[0] + self.radius - 3),
                     random.uniform(self.center[1] - self.radius, self.center[1] + self.radius - 3))
        self.next_hunt = 0

    def update(self, ants):
        if any(self.is_ant_inside(ant.x, ant.y) for ant in ants) and pygame.time.get_ticks() > self.next_hunt:

            self.find_target(ants)
            self.track_target()
        else:
            self.target = None
            self.move_randomly()

        if self.target:
            self.check_collision_with_target()

    def move_randomly(self):
        if not self.target:
            px, py = self.path
            dx, dy = px - self.x, py - self.y
            distance = (dx**2 + dy**2)**0.5

            if distance < 5:  # If close to the current path target, pick a new one
                self.path = (
                    random.uniform(
                        self.center[0] - self.radius, self.center[0] + self.radius),
                    random.uniform(
                        self.center[1] - self.radius, self.center[1] + self.radius)
                )
            else:
                # Move towards the current path target
                dx, dy = dx / distance * self.speed, dy / distance * self.speed
                self.x += dx
                self.y += dy

    def track_target(self):
        if self.target:
            dx, dy = self.target.x - self.x, self.target.y - self.y
            self.heading = math.atan2(dy, dx)
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 1:  # Move towards the target if not already close
                dx, dy = dx / distance * self.speed, dy / distance * self.speed
                self.x += dx
                self.y += dy

    def check_collision_with_target(self):
        if self.target:
            dx, dy = self.target.x - self.x, self.target.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < 5:  # Assuming 5 is the collision threshold
                self.target.remove()
                self.target = None
                self.next_hunt = pygame.time.get_ticks() + 20000  # 20 seconds in milliseconds

    def is_ant_inside(self, ant_x, ant_y):
        distance = math.sqrt(
            (ant_x - self.center[0])**2 + (ant_y - self.center[1])**2)
        return distance <= self.radius

    def find_target(self, ants):
        if pygame.time.get_ticks() < self.next_hunt:
            return
        best_ant = None
        closest = float("inf")
        for ant in ants:
            if self.is_ant_inside(ant.x, ant.y):
                dist = math.sqrt((ant.x - self.x)**2 + (ant.y - self.y)**2)
                if dist < closest:
                    closest = dist
                    best_ant = ant
        self.target = best_ant
        if not best_ant:
            self.target = None

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(
            self.x), int(self.y)), 5)

    def debug(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (int(
            self.center[0]), int(self.center[1])), self.radius, 1)
