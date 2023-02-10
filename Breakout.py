import decimal

import sys

import time
from abc import ABC

import pygame
from pygame.locals import *
from GameStage import GameStage
from GameStage import Entity
from utils import load_sound, load_sprite, init_pygame
from pygame.math import Vector2

# Set up constants
WIDTH = 800
HEIGHT = 600
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

position_x = 0


def move_object(position):
    global position_x
    position_x = position
    # print(f"Moving object in direction {direction_x}")


def set_position_x_to_zero():
    global position_x
    position_x = 0


class Breakout:
    def __init__(self):

        self.surface = init_pygame(WIDTH, HEIGHT)
        self.frame_advance = None
        # self.game_stage = GameStage(WIDTH, HEIGHT)
        self.seconds_count = 1
        # self.bat = None
        # self.bat = Bat((WIDTH / 2 - 60, HEIGHT - 20), self.game_stage)
        # self.ball = Ball((345 + self.bat.width/2, 565), self.game_stage)
        # self.ball = Ball((345 + self.bat.width / 2, 565), self.game_stage)
        # self.ball = Ball((345 + self.bat.width / 2, HEIGHT - self.bat.height), self.game_stage)
        # self.game_stage.add_sprite(self.bat)
        # self.game_stage.add_sprite(self.ball)
        self.ball_is_play = False
        self.impacts = []
        self.bat = None
        self.ball = None
        self.init_entities()

    def init_entities(self):
        self.ball = Ball(position=(400 / 2, 565), surface=self.surface)
        self.bat = Bat(position=(WIDTH / 2 - 60, HEIGHT - 20), surface=self.surface)

    def run(self) -> None:
        clock = pygame.time.Clock()

        frame_count = 0.0
        time_passed = 0.0
        self.fps = 0.0

        # Main loop
        while True:
            # calculate fps
            # time_passed += clock.tick(60)
            # frame_count += 1
            # if frame_count % 10 == 0:  # every 10 frames
            #     # nearest integer
            #     self.fps = round((frame_count / (time_passed / 1000.0)))
            #     # reset counter
            #     time_passed = 0
            #     frame_count = 0

            self.seconds_count += 1

            self.surface.fill((10, 10, 10))

            # self.game_stage.screen.fill((10, 10, 10))
            # self.game_stage.update_impacts()
            # self.ball.move()
            self.update()
            self.render()
            self.handle_input(events=pygame.event.get(), callback=move_object)
            self.check_collision()
            # self.game_stage.draw_sprites()
            # self.input(pygame.event.get())
            self.remove_animations()

            # Double buffer draw
            pygame.display.flip()
            clock.tick(60)

    # def input(self, events) -> None:
    #
    #     self.frame_advance = False
    #     for event in events:
    #         if event.type == QUIT:
    #             sys.exit(0)
    #         elif event.type == KEYDOWN:
    #             if event.key == K_ESCAPE:
    #                 sys.exit(0)
    #
    #     is_key_pressed = pygame.key.get_pressed()
    #
    #     if is_key_pressed[pygame.K_LEFT]:
    #         self.bat.move_left()
    #     elif is_key_pressed[pygame.K_RIGHT]:
    #         self.bat.move_right()

    def handle_input(self, events, callback) -> None:

        self.frame_advance = False
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_LEFT]:
            callback(-1)
        elif is_key_pressed[pygame.K_RIGHT]:
            callback(1)

    def check_collision(self) -> None:

        if self.ball.position.y >= 565:

            ball_x, ball_y = self.ball.get_position()
            bat_x, bat_y = self.bat.get_position()

            difference_x = ball_x + self.ball.get_radius() - bat_x

            if not self.ball_is_play:
                if -5 < difference_x < 120:
                    dx, dy = self.ball.get_direction()
                    #check this logic
                    self.ball.direction.x = -dx
                    #self.ball.direction.y = -dy
                    self.ball.sound.play()

                    self.impacts.append(Impact(Vector2(ball_x, ball_y), surface=self.surface))

                    # self.game_stage.add_animations(Impact((self.ball.position.x, self.ball.position.y)))
                    print("Impact! difference {}, ball X:{} and bat X:{} "
                          .format(difference_x, self.ball.position.x, self.bat.position.x))
                else:
                    self.ball_is_play = True
                    print("Finish difference {}, ball X:{} and bat X:{} "
                          .format(difference_x, self.ball.position.x, self.bat.position.x))
            else:
                # Temporary until I do something with the lost match
                self.ball_is_play = False

    def update(self):
        for entity in [self.ball] + [self.bat] + self.impacts:
            entity.update()

    def render(self):
        for entity in [self.ball] + [self.bat] + self.impacts:
            entity.render()

    def remove_animations(self) -> None:
        for i in range(len(self.impacts) - 1, -1, -1):
            if self.impacts[i].time >= 10:
                del self.impacts[i]


class Bat(Entity):
    velocity = Vector2(15, 0)

    def __init__(self, position, surface):
        super().__init__(position, load_sprite("bat0"), None, surface)
        self.old_x = 0

    def update(self) -> None:
        print(f"Position " + str(position_x))
        old_x = self.position.x

        if position_x < 0:
            set_position_x_to_zero()
            self.position.x = self.position.x - self.velocity.x
            if self.position.x <= -6:
                self.position.x = old_x
        if position_x > 0:
            set_position_x_to_zero()
            self.position.x = self.position.x + self.velocity.x
            if self.position.x + self.sprite_width - 6 >= self.screen_width:
                self.position.x = old_x

    def get_position(self) -> tuple:
        return self.position.x, self.position.y

    def get_direction(self) -> tuple:
        return self.direction.x, self.direction.y


# class Bat_old:
#     velocity = Vector2(15, 0)
#
#     def __init__(self, position, game_stage):
#         self.game_stage = game_stage
#         self.sprite_surface = load_sprite("bat0")
#         self.position = Vector2(position)
#         self.width = self.sprite_surface.get_width()
#         self.height = self.sprite_surface.get_height()
#
#     def move_left(self) -> None:
#         old_x = self.position.x
#         self.position.x = self.position.x - self.velocity.x
#         if self.position.x <= -6:
#             self.position.x = old_x
#
#     def move_right(self) -> None:
#         old_x = self.position.x
#         self.position.x = self.position.x + self.velocity.x
#         if self.position.x + self.width - 6 >= self.game_stage.screen_width:
#             self.position.x = old_x


import math


# class BreakoutBall:
#     def __init__(self, x, y, radius, speed, angle):
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.speed = speed
#         self.angle = angle
#         self.dx = math.cos(angle) * speed
#         self.dy = math.sin(angle) * speed
#
#     def move(self):
#         self.x += self.dx
#         self.y += self.dy
#
#     def reflect_horizontally(self):
#         self.dx = -self.dx
#
#     def reflect_vertically(self):
#         self.dy = -self.dy
#
#     def get_position(self):
#         return (self.x, self.y)
#
#     def get_radius(self):
#         return self.radius


class Ball(Entity):

    def __init__(self, position, surface):
        super().__init__(position, load_sprite("ball"), load_sound("bounce"), surface)
        self.radius = self.sprite.get_width() / 2
        self.speed = Vector2(5, 5)
        self.direction = Vector2(-1, -1)

    def update(self) -> None:

        self.position.x += self.direction.x * self.speed.x
        self.position.y += self.direction.y * self.speed.y

        if abs(self.position.x - WIDTH) > WIDTH or WIDTH - (self.position.x + self.radius + 5) <= 0:
            self.direction.x = -self.direction.x
            self.position.x += self.direction.x

        if abs(self.position.y - HEIGHT) > HEIGHT:
            self.direction.y = -self.direction.y
            self.position.y += self.direction.y

    def get_position(self) -> tuple:
        return self.position.x, self.position.y

    def get_direction(self) -> tuple:
        return self.direction.x, self.direction.y

    def get_radius(self):
        return self.radius


# class Ball_old:
#     def __init__(self, position, game_stage):
#         self.game_stage = game_stage
#         self.sprite_surface = load_sprite("ball")
#         self.position = Vector2(position)
#         self.sound = load_sound("bounce")
#         self.radio = self.sprite_surface.get_width() / 2
#         # self.height = self.sprite_surface.get_height()
#         self.dx, self.dy = -1, -1
#         self.speed = 5
#
#     def move(self) -> None:
#
#         self.position.x += self.dx * self.speed
#         self.position.y += self.dy * self.speed
#
#         if abs(self.position.x - WIDTH) > WIDTH or WIDTH - (self.position.x + self.radio + 5) <= 0:
#             self.dx = -self.dx
#             self.position.x += self.dx
#
#         if abs(self.position.y - HEIGHT) > HEIGHT:
#             self.dy = -self.dy
#             self.position.y += self.dy


class Impact_old(Entity):
    def __init__(self, position):
        self.sprite_surface = None
        self.time = 0
        self.position = Vector2(position)

    def update(self) -> None:
        # There are 5 impact sprites numbered 0 to 4. We update to a new sprite every 2 frames.
        self.sprite_surface = load_sprite("impact" + str(self.time // 2))

        # The Game class maintains a list of Impact instances. In Game.update, if the timer for an object
        # has gone beyond 10, the object is removed from the list.
        self.time += 1


class Impact(Entity):

    def __init__(self, position, surface):
        super().__init__(position, load_sprite("blank"), None, surface)

        self.time = 0

    def update(self) -> None:
        # There are 5 impact sprites numbered 0 to 4. We update to a new sprite every 2 frames.
        self.sprite = load_sprite("impact" + str(self.time // 2))

        # The Game class maintains a list of Impact instances. In Game.update, if the timer for an object
        # has gone beyond 10, the object is removed from the list.
        self.time += 1

    def get_position(self) -> tuple:
        pass

    def get_direction(self) -> tuple:
        pass


if __name__ == '__main__':
    game = Breakout()
    game.run()

    # pygame.display.flip()