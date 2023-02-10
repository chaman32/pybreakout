import pygame
import inspect

from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import get_random_velocity, load_sound, load_sprite, wrap_position
from abc import ABC, abstractmethod, abstractproperty


class Entity(ABC):

    def __init__(self, position, sprite, sound, surface):
        self.position = Vector2(position)
        self.sprite = sprite
        self.surface = surface
        self.sound = sound
        self.sprite_height = self.sprite.get_height()
        self.sprite_width = self.sprite.get_width()
        self.screen_width, self.screen_height = self.surface.get_size()

    def render(self) -> None:
        self.surface.blit(self.sprite, self.position)

    @abstractmethod
    def update(self) -> None:
        pass

    def remove(self) -> None:
        for i in range(len(self.impacts) - 1, -1, -1):
            if self.impacts[i].time >= 10:
                del self.impacts[i]

    @abstractmethod
    def get_position(self) -> tuple:
        pass

    @abstractmethod
    def get_direction(self) -> tuple:
        pass



class GameStage:
    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_mode((width, height))
        self.screen = pygame.display.get_surface()
        self.sprite_list = []
        self.impacts = []
        self.screen_width, self.screen_height = self.screen.get_size()

    # def draw(self, surface):
    #     blit_position = self.position - Vector2(self.radius)
    #     surface.blit(self.sprite, blit_position)
    #
    # def move(self, surface):
    #     self.position = wrap_position(self.position + self.velocity, surface)
    #
    # def collides_with(self, other_obj):
    #     distance = self.position.distance_to(other_obj.position)
    #     return distance < self.radius + other_obj.radius

    def draw_sprites(self) -> None:
        for sprite in self.sprite_list:
            if sprite.sprite_surface:
                self.screen.blit(sprite.sprite_surface, sprite.position)
        for sprite in self.impacts:
            if sprite.sprite_surface:
                self.screen.blit(sprite.sprite_surface, sprite.position)

    def update_impacts(self) -> None:
        for impact in self.impacts:
            impact.update()

    def add_sprite(self, sprite) -> None:
        self.sprite_list.append(sprite)

    def add_animations(self, sprite) -> None:
        self.impacts.append(sprite)

    def remove_animations(self) -> None:
        for i in range(len(self.impacts) - 1, -1, -1):
            if self.impacts[i].time >= 10:
                del self.impacts[i]
