import pygame as pg
import math
import sys

from settings import *
from gameObject import *

class Item(GameObject):
    def __init__(self, game, name, image):
        self.game = game
        self.name = name
        self.id = name
        self.spriteRect = pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        self.sprite = pg.transform.scale(pg.image.load(image).convert_alpha(), (TILE_WIDTH, TILE_HEIGHT))

    def draw(self, pos, z=0):
        self.game.world_renderer.draw_object(self, self.sprite, pos, z=z)

# storage
class Storage:
    def __init__(self, game, capacity):
        self.game = game
        self.items = []
        self.capacity = capacity

    def add(self, item):
        print("adding", item)
        if len(self.items) < self.capacity:
            if type(item) is str:
                self.items.append(self.game.item_library[item])
            else:
                self.items.append(self.game.item_library[item.id])


class Inventory:
    MAX = 10

    def __init__(self, game):
        self.game = game
        self.items = []
        self.show_inventory = False

    def toggle_inventory(self):
        self.show_inventory = not self.show_inventory

    def add_item(self, item):
        if len(self.items) < Inventory.MAX:
            if type(item) is str:
                self.items.append(self.game.item_library[item])
            else:
                self.items.append(self.game.item_library[item.id])

    def pop(self):
        if self.items:
            return [self.items.pop()]
        return []

    def isFull(self):
        return len(self.items) >= Inventory.MAX

    def isEmpty(self):
        return len(self.items) == 0

    def next(self):
        if len(self.items) >= 1:
            return self.items[-1]
        return None

    def draw(self):
        for i, item in enumerate(self.items):
            pos = pg.Vector2(self.game.player.pos.x-0.3, self.game.player.pos.y)
            item.draw(pos, z=(i + 3) * 0.6)
