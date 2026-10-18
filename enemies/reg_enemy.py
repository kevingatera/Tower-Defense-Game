import pygame
from enemies.enemy import Enemy
from path import Path

class Reg_Enemy(Enemy):

    def __init__(self, screen):
        super().__init__(health=6, speed=2, image=None, bounty=10, name="Regular", screen=screen) #bounty = 10
        self.position = Path().get_path_points()[0]
        self.current_point_index = 0
        self.reached_end = False
