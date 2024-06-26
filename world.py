import random

import pygame as pg
import math
import sys

from gameObject import *
from gameObject import TILE_HEIGHT, TILE_WIDTH
from items import TILE_HEIGHT, TILE_WIDTH
from settings import *
from items import *
from settings import TILE_HEIGHT, TILE_WIDTH
from game import *
from savesystem import *
from particle import *

class World(GameObject):
    def __init__(self, game):
        self.game = game
        
        self.floor_layer = []
        self.building_layer = []

        self.tile_library = {"empty" :      EmptyTile(self.game, "empty"),
                             "floor" :      Tile(self.game, "floor", "new-sprites/buildings/floor.png"),
                             "counter" :    Counter(self.game, "counter", "new-sprites/buildings/counter.png", sprite_rect=pg.Rect(0, -4*PPU, TILE_WIDTH, 20*PPU), price=10),
                             "seller" :     Seller(self.game, "seller", "new-sprites/buildings/seller.png", hitbox=pg.Vector2(2, 2), sprite_rect=pg.Rect(0, -4*PPU, 2*TILE_WIDTH, 38*PPU), price=1000),
                             "fridge" :     Fridge(self.game, "fridge", "new-sprites/buildings/fridge.png", hitbox=pg.Vector2(2, 1), sprite_rect=pg.Rect(0, -2*TILE_HEIGHT, 2*TILE_WIDTH, 3*TILE_HEIGHT), price=1000),
                             "shop" :       Shop(self.game, "shop", "new-sprites/buildings/shop.png", hitbox=pg.Vector2(2, 1), sprite_rect=pg.Rect(0, -2*TILE_HEIGHT, 2*TILE_WIDTH, 3*TILE_HEIGHT)),
                             "item-shop" :  ItemShop(self.game, "item-shop", "new-sprites/buildings/shop.png", hitbox=pg.Vector2(2, 1), sprite_rect=pg.Rect(0, -2*TILE_HEIGHT, 2*TILE_WIDTH, 3*TILE_HEIGHT)),
                             "chopper" :    Processor(self.game, "chopper", "new-sprites/buildings/Counter with Knife.png", sprite_rect=pg.Rect(0, -4*PPU, TILE_WIDTH, 20*PPU), price=100, pps=0, ppi=0.1),
                             "oven" :       Processor(self.game, "oven", "new-sprites/buildings/oven.png", sprite_rect=pg.Rect(0, -TILE_WIDTH, TILE_WIDTH, 2*TILE_HEIGHT), price=100, pps=0.1, ppi=0),
        }
        
        self.generateWorld()
    
    def generateWorld(self): 
        self.floor_layer = [[self.tile_library["floor"].copy(pg.Vector2(x, y)) for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]
        # self.building_layer = [[self.tile_library["empty"] for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]
        self.building_layer = [[self.tile_library["empty"] for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]

        self.place("shop", pg.Vector2(int(WORLD_WIDTH/2)-1, 0))
        self.place("seller", pg.Vector2(int(WORLD_WIDTH/2)-1, WORLD_HEIGHT - 2))

    def is_legible_tile_placement(self, id:str, pos:pg.Vector2):
        tile = self.tile_library[id].copy(pos)
        for space in tile.get_spaces():
            if self.get(space.x, space.y) != self.tile_library["empty"]:
                return False
        return True

    def destroy(self, pos:pg.Vector2):
        tile = self.get(pos.x, pos.y)
        if tile == self.tile_library["empty"]: return

        for space in tile.get_spaces():
            self.building_layer[int(space.y)][int(space.x)] = self.tile_library["empty"]


    def place(self, id:str, pos:pg.Vector2):
        if not self.is_legible_tile_placement(id, pos):
            return

        tile = self.tile_library[id].copy(pos)

        for space in tile.get_spaces()[1:]:
            self.building_layer[int(space.y)][int(space.x)] = ReferenceTile(self.game, tile, space)
        self.building_layer[int(pos.y)][int(pos.x)] = tile

    def oob(self, x, y):
        return x < 0 or x >= WORLD_WIDTH or y < 0 or y >= WORLD_HEIGHT

    def get(self, x, y):
        if self.oob(x, y): return self.tile_library["empty"]
        else: return self.building_layer[int(y)][int(x)]

    def update(self):
        [[building.update() for building in row] for row in self.building_layer]

    def draw(self):
        [[self.game.world_renderer]]
        [[self.floor_layer[y][x].draw() for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]
        [[self.building_layer[y][x].draw() for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]


class Tile(GameObject):
    def __init__(self, game, id, sprite, pos:pg.Vector2=pg.Vector2(0, 0), hitbox:pg.Vector2=pg.Vector2(1, 1), sprite_rect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)):
        self.id = id
        super().__init__(game, pos, hitbox, sprite, sprite_rect)
    
    def get_spaces(self):
        return sum([[pg.Vector2(self.pos.x + dx, self.pos.y + dy) for dx in range(int(self.hitbox.x))] for dy in range(int(self.hitbox.y))], [])

    def draw(self):
        self.game.world_renderer.draw_object_immediate(self)
    
    def copy(self, pos:pg.Vector2):
        return Tile(self.game, self.id, self.sprite, pos, self.hitbox, self.sprite_rect)


class EmptyTile(GameObject):
    def __init__(self, game, id):
        self.game = game
        self.id = id

    def copy(self):
        return self

class Building(Tile):
    def __init__(self, game, id, sprite, pos:pg.Vector2=pg.Vector2(0, 0), hitbox:pg.Vector2=pg.Vector2(1, 1), sprite_rect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True, price=100):
        super().__init__(game, id, sprite, pos, hitbox, sprite_rect)
        self.isSolid = isSolid
        self.price = price
    
    def interact(self, player):
        print(f"wowww you interacted with the {self.id}!")

    def alt_interact(self, player):
        print(f"wowww you alt interacted with the {self.id}!")
    
    def draw(self):
        self.game.world_renderer.draw_object(self)
    
    def copy(self, pos:pg.Vector2):
        return Building(self.game, self.id, self.sprite, pos, self.hitbox, self.sprite_rect, self.isSolid, self.price)

    def draw_highlighted(self, layer=0):
        highlight = self.sprite.convert_alpha()
        highlight.fill((255, 255, 255), special_flags=pg.BLEND_RGB_ADD)
        highlight.set_alpha(128)
        self.game.world_renderer.draw_object(self, highlight, layer=layer)
    
    def draw_ghost(self, layer=0): 
        ghost = self.sprite.convert_alpha()
        ghost.set_alpha(128)
        self.game.world_renderer.draw_object(self, ghost, self.pos, layer=layer)
    
    def draw_red(self, layer=0):
        highlight = self.sprite.convert_alpha()
        highlight.fill((255, 50, 50), special_flags=pg.BLEND_RGB_ADD)
        highlight.set_alpha(128)
        self.game.world_renderer.draw_object(self, highlight, layer=layer)
    
    def draw_blue(self, layer=0):
        highlight = self.sprite.convert_alpha()
        highlight.fill((50, 100, 255), special_flags=pg.BLEND_RGB_ADD)
        highlight.set_alpha(128)
        self.game.world_renderer.draw_object(self, highlight, layer=layer)


class Shop(Building):
    def __init__(self, game, id, sprite, pos: pg.Vector2 = pg.Vector2(0, 0), hitbox: pg.Vector2 = pg.Vector2(1, 1), sprite_rect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True, price=100):
        super().__init__(game, id, sprite, pos, hitbox, sprite_rect, isSolid, price)
    
    def interact(self, player):
        if self.game.wave_state != BREAK_WAVE:
            self.game.particles.append(DisabledParticle(self.game, self.pos))
            return
        super().interact(player)
        if self.game.state == PLAY_STATE:
            self.game.state = BUY_STATE
    
    def copy(self, pos:pg.Vector2):
        return Shop(self.game, self.id, self.sprite, pos, self.hitbox, self.sprite_rect, self.isSolid, self.price)


class ItemShop(Building):
    def __init__(self, game, id, sprite, pos: pg.Vector2 = pg.Vector2(0, 0), hitbox: pg.Vector2 = pg.Vector2(1, 1), sprite_rect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True, price=100):
        super().__init__(game, id, sprite, pos, hitbox, sprite_rect, isSolid, price)
    
    def interact(self, player):
        super().interact(player)
        if self.game.state == PLAY_STATE:
            self.game.state = BUY_ITEM_STATE
    
    def copy(self, pos:pg.Vector2):
        return ItemShop(self.game, self.id, self.sprite, pos, self.hitbox, self.sprite_rect, self.isSolid, self.price)


class ReferenceTile(Building):
    def __init__(self, game, reference:Building, pos:pg.Vector2, hitbox:pg.Vector2=pg.Vector2(1, 1)):
        super().__init__(game, reference.id, reference.sprite, pos, pg.Vector2(1, 1), reference.sprite_rect, reference.isSolid)
        self.reference = reference
    
    def get_spaces(self):
        return self.reference.get_spaces()

    def draw(self):
        pass
    
    def interact(self, player):
        self.reference.interact(player)

    def draw_highlighted(self, layer=0):
        self.reference.draw_highlighted(layer)
    
    def draw_red(self, layer=0):
        self.reference.draw_red(layer)

    def draw_blue(self, layer=0):
        self.reference.draw_blue(layer)
    
    def draw_ghost(self, layer=0):
        self.reference.draw_ghost(layer)

class Counter(Building):
    def __init__(self, game, id, sprite, pos:pg.Vector2=pg.Vector2(0, 0), hitbox:pg.Vector2=pg.Vector2(1, 1), sprite_rect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True, price=100):
        super().__init__(game, id, sprite, pos, hitbox, sprite_rect, isSolid, price)
        self.item = None

    def interact(self, player):
        if self.item == None and not player.inventory.isEmpty():
            self.item = player.inventory.next()
            player.inventory.pop()
        elif type(self.item) == Package and not player.inventory.isEmpty():
            self.item = self.item.add(player.inventory.next())
            player.inventory.pop()
        elif self.item != None and not player.inventory.isEmpty():
            package = self.game.item_library["package"].copy()
            package.add(self.item)
            package.add(player.inventory.next())
            player.inventory.pop()

            self.item = package
    
    def alt_interact(self, player):
        if self.item != None and not player.inventory.isFull():
            player.inventory.add_item(self.item)
            self.item = None

    def draw(self):
        super().draw()
        if self.item != None:
            self.item.draw(self.pos, z=0.6)
    
    def copy(self, pos: pg.Vector2):
        return Counter(self.game, self.id, self.sprite, pos, self.hitbox, self.sprite_rect, self.isSolid, self.price)


class Seller(Building):
    def __init__(self, game, id, sprite, pos:pg.Vector2=pg.Vector2(0, 0), hitbox:pg.Vector2=pg.Vector2(1, 1), sprite_rect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True, price=100):
        super().__init__(game, id, sprite, pos, hitbox, sprite_rect, isSolid, price)

    def interact(self, player):
        if self.game.wave_state != COOK_WAVE:
            self.game.particles.append(DisabledParticle(self.game, self.pos))
            return
            
        if not player.inventory.isEmpty():
            self.game.particles.append(SellParticle(self.game, self.pos, text=f"+${player.inventory.next().sellprice}"))

            self.game.money_made_today += player.inventory.next().sellprice
            player.inventory.pop()

    def draw(self):
        super().draw()
    
    def copy(self, pos: pg.Vector2):
        return Seller(self.game, self.id, self.sprite, pos, self.hitbox, self.sprite_rect, self.isSolid, self.price)


class Fridge(Building):
    def __init__(self, game, id, sprite, pos: pg.Vector2 = pg.Vector2(0, 0), hitbox: pg.Vector2 = pg.Vector2(1, 1),

            sprite_rect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True, price=100):
        super().__init__(game, id, sprite, pos, hitbox, sprite_rect, isSolid, price)

        self.storage = Storage(self.game, 20)
        for i in range(12):
            self.storage.add(random.choice(["sugar", "butter", "cookie"]))

    def interact(self, player):
        print("opening storage...")
        self.game.state = FRIDGE_STATE
        self.game.storage_menu.set(self.storage)

    def copy(self, pos: pg.Vector2):
        return Fridge(self.game, self.id, self.sprite, pos, self.hitbox, self.sprite_rect, self.isSolid, self.price)
    
    def draw(self):
        super().draw()

class Processor(Building):
    def __init__(self, game, id, sprite, pos: pg.Vector2 = pg.Vector2(0, 0), hitbox: pg.Vector2 = pg.Vector2(1, 1), sprite_rect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True, price=100, pps=0.05, ppi=0.1):
        super().__init__(game, id, sprite, pos, hitbox, sprite_rect, isSolid, price)
        
        self.item = None

        self.progress = 0

        self.pps = pps # process per interaction
        self.ppi = ppi # process per interaction

    def interact(self, player):
        if self.item == None and not player.inventory.isEmpty():
            package = self.game.item_library["package"].copy()
            package = package.add(player.inventory.next(), self.id)
            player.inventory.pop()

            self.item = package
            self.progress = 0

        elif self.item != None:
            if not player.inventory.isEmpty():
                if type(self.item) == Package:
                    self.item = self.item.add(player.inventory.next(), self.id)
                    player.inventory.pop()
                elif self.item != None:
                    package = self.game.item_library["package"].copy()
                    package = package.add(self.item, self.id)
                    package = package.add(player.inventory.next(), self.id)
                    player.inventory.pop()
                    self.item = package

                    self.progress = 0
            
            elif self.progress < 1:
                self.progress += self.ppi
    
    def alt_interact(self, player):
        if self.progress >= 1 and self.item != None and not player.inventory.isFull():
            player.inventory.add_item(self.item)
            self.item = None

    def update(self):
        if self.item != None and self.progress < 1:
            self.progress += self.pps * self.game.DT

    def draw(self):
        super().draw()
        if self.item != None:
            self.item.draw(self.pos, z=0.8)

            # draw the progress bar
            background_bar = pg.Surface((TILE_WIDTH, 8))
            progress_bar = pg.Surface((min(1, self.progress) * TILE_WIDTH, 8))
            progress_bar.fill((0, 255, 0))

            self.game.world_renderer.draw_object(self, background_bar, self.pos, z=0.4)
            self.game.world_renderer.draw_object(self, progress_bar, self.pos, z=0.4)

    
    def copy(self, pos: pg.Vector2):
        return Processor(self.game, self.id, self.sprite, pos, self.hitbox, self.sprite_rect, self.isSolid, self.price, self.pps, self.ppi)
