from constants import *
from functions import *
from conversions import *

import pygame as pg


class Pawn(pg.sprite.Sprite):

	def __init__(self, side, position):

		super().__init__()
		# 'black' or 'white'
		self.side = side
		self.type = 'pawn'
		self.name = '{s} {t}'.format(s=self.side, t=self.type)
		# Location on board e.g. 'a8'
		self.position = position

		# Load image and resize to fit board
		image = pg.image.load(
								"img/{s}_{t}.png".format(s=self.side, t=self.type)
							).convert_alpha()
		self.image = pg.transform.smoothscale(image, (PIECE_SIZE, PIECE_SIZE))
		# Create a surface for the image to be on
		self.rect = self.image.get_rect()
		# Retrieve x, y coordinates to place image
		self.rect.x , self.rect.y = pos2xy(position)



# class Rook(pg.sprite.Sprite):

# 	def __init__(self, side, position):

# 		super().__init__()

# 		self.side = side

# 		# Load image and resize to fit board
# 		image = pg.image.load("img/{}_rook.png".format(side)).convert_alpha()
# 		self.image = pg.transform.scale(image, (PIECE_SIZE, PIECE_SIZE))

# 		self.rect = self.image.get_rect()
# 		self.rect.x , self.rect.y = pos2xy(position)

# class Knight(pg.sprite.Sprite):

# 	def __init__(self, side, position):

# 		super().__init__()

# 		self.side = side

# 		# Load image and resize to fit board
# 		image = pg.image.load("img/{}_knight.png".format(side)).convert_alpha()
# 		self.image = pg.transform.scale(image, (PIECE_SIZE, PIECE_SIZE))

# 		self.rect = self.image.get_rect()
# 		self.rect.x , self.rect.y = pos2xy(position)

# class Bishop(pg.sprite.Sprite):

# 	def __init__(self, side, position):

# 		super().__init__()

# 		self.side = side

# 		# Load image and resize to fit board
# 		image = pg.image.load("img/{}_bishop.png".format(side)).convert_alpha()
# 		self.image = pg.transform.scale(image, (PIECE_SIZE, PIECE_SIZE))

# 		self.rect = self.image.get_rect()
# 		self.rect.x , self.rect.y = pos2xy(position)

# class Queen(pg.sprite.Sprite):

# 	def __init__(self, side, position):

# 		super().__init__()

# 		self.side = side

# 		# Load image and resize to fit board
# 		image = pg.image.load("img/{}_queen.png".format(side)).convert_alpha()
# 		self.image = pg.transform.scale(image, (PIECE_SIZE, PIECE_SIZE))

# 		self.rect = self.image.get_rect()
# 		self.rect.x , self.rect.y = pos2xy(position)

# class King(pg.sprite.Sprite):

# 	def __init__(self, side, position):

# 		super().__init__()

# 		self.side = side

# 		# Load image and resize to fit board
# 		image = pg.image.load("img/{}_king.png".format(side)).convert_alpha()
# 		self.image = pg.transform.scale(image, (PIECE_SIZE, PIECE_SIZE))

# 		self.rect = self.image.get_rect()
# 		self.rect.x , self.rect.y = pos2xy(position)