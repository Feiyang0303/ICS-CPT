PLAY_STATE = 0
EDIT_STATE = 1

PPU = 3 # PIXELS PER UNIT
UPT = 16 # UNIT PER TILE

TILE_WIDTH = UPT * PPU
TILE_HEIGHT = UPT * PPU

WORLD_WIDTH = 16
WORLD_HEIGHT = 12


MARGIN = TILE_WIDTH

SCREEN_WIDTH = WORLD_WIDTH * TILE_WIDTH + 2*MARGIN
SCREEN_HEIGHT = WORLD_HEIGHT * TILE_HEIGHT + 2*MARGIN


MASTER_VOLUME = 100

BACKGROUND_COLOUR = (33, 33, 35)

PLAYER_HITBOX_HEIGHT = 0.8
PLAYER_HITBOX_WIDTH = 0.8

PLAYER_MAX_SPEED = 8
PLAYER_TIME_TO_MAX = 0.02
PLAYER_ACCELERATION  = PLAYER_MAX_SPEED / PLAYER_TIME_TO_MAX
PLAYER_DECELERATION_TIME = 0.08
PLAYER_DECELERATION = PLAYER_MAX_SPEED / PLAYER_DECELERATION_TIME