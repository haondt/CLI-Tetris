import sys

class Grid:
	contents = None
	flagged = []
	def __init__ (self, height, width):
		self.contents = [[' ' for i in range(width)] for j in range(height)]
		self.flagged = [(i,j) for i in range(width) for j in range(height)]
	def reset(self):
		self.contents = [[' ' for j in contents[i]] for i in contents]

	def is_free(self, x,y):
		if x >= len(self.contents[0]) or y >= len(self.contents):
			return False
		else:
			return self.contents[y][x] == ' '
	
	def free(self, x, y):
		self.contents[y][x] = ' '
		self.flagged += (y,x)

	def fill(self, x, y, block):
		self.contents[y][x] = block
		self.flagged += (y,x)
	
	# TODO: Only draw points in flagged[]
	def draw(self):
		# clear screen
		#print(u'\u001b[2J',end='')
		# home cursor
		print(u'\u001b[H',end = '')

		# print grid contents
		firstrow = True
		for row in self.contents:
			if firstrow:
				firstrow = False
			else:
				print('')
			for col in row:
				print(col, end = '')
		sys.stdout.flush()

class Tetromino:
	shape = None
	coords = [0,0]
	rotation = 1
	grid = None

	def __init__(self, shape, grid):
		if shape == 'I':
			self.shape = I_mino()
		elif shape == 'J':
			self.shape = J_mino()
		elif shape == 'O':
			self.shape = O_mino()
		elif shape == 'S':
			self.shape = S_mino()
		elif shape == 'Z':
			self.shape = Z_mino()
		elif shape == 'T':
			self.shape = T_mino()
		elif shape == 'L':
			self.shape = L_mino()

		self.coords = [0,0]
		self.grid = grid
		self.fill()
	def collision(self):
		return self.shape()
		
	def rotate(self, direction):
		self.clear()

		if direction == 'c':
			self.rotation += 1
			if self.rotation > 4:
				self.rotation = 1
		else:
			self.rotation -= 1
			if self.rotation < 1:
				self.rotation = 4
		self.fill()

	def can_go_left(self):
		return False

	def left(self):
		self.clear()
		self.coords[0] -= 1
		self.fill()

	def can_go_right(self):
		config = self.shape.config(self.rotation)
		# find rightmost block in each column
		rightblocks = [-1 for i in range(len(config))]
		
		for row in range(len(config)):
			x = self.coords[0]
			for col in config[row]:
				if col:
					rightblocks[row] = max(rightblocks[row], x)
				x += 1
		

		# check if it can move right
		right = True
		for block_i in range(len(rightblocks)):
			block = rightblocks[block_i]
			if block != -1:
				if not self.grid.is_free(block+1,block_i+self.coords[1]):
					right = False
					break
		return right
	
	def right(self):
		self.clear()
		self.coords[0] += 1
		self.fill()

	def can_drop(self):
		config = self.shape.config(self.rotation)
		# find bottommost block in each column
		lowblocks = [-1 for i in range(len(config[0]))]

		y = self.coords[1]
		for row in config:
			for col in range(len(row)):
				if row[col]:
					lowblocks[col] = max(lowblocks[col], y)
			y += 1
		

		# check if it can drop
		drop = True
		for block_i in range(len(lowblocks)):
			block = lowblocks[block_i]
			if block != -1:
				if not self.grid.is_free(block_i+self.coords[0], block+1):
					drop = False
					break

		return drop
	
	def drop(self):
		self.clear()
		self.coords[1] += 1
		self.fill()
	
	# remove only colored tiles from grid
	def clear(self):	
		config = self.shape.config(self.rotation)
		y = self.coords[1]
		for row in config:
			x = self.coords[0]
			for col in row:
				if col:
					self.grid.free(x, y)
					
				x += 1
			y += 1

	# insert only colored tiles into grid
	def fill(self):
		config = self.shape.config(self.rotation)
		y = self.coords[1]
		for row in config:
			x = self.coords[0]
			for col in row:
				if col:
					self.grid.fill(x, y, self.shape.get_block())
					
				x += 1
			y += 1

class I_mino:
	configs = {
		1:[
			[1,0,0,0],
			[1,0,0,0],
			[1,0,0,0],
			[1,0,0,0]
		],
		2:[
			[1,1,1,1],
			[0,0,0,0],
			[0,0,0,0],
			[0,0,0,0]
		],
		3:[
			[1,0,0,0],
			[1,0,0,0],
			[1,0,0,0],
			[1,0,0,0]
		],
		4:[
			[1,1,1,1],
			[0,0,0,0],
			[0,0,0,0],
			[0,0,0,0]
		]
	}
	
	block = u'\u001b[34m█\u001b[0m'

	def config(self, rotation):
		return self.configs[rotation]

	def get_block(self):
		return self.block

class T_mino:
	configs = {
		1:[
			[0,1,0,0],
			[1,1,1,0],
			[0,0,0,0],
			[0,0,0,0]
		],
		2:[
			[1,0,0,0],
			[1,1,0,0],
			[1,0,0,0],
			[0,0,0,0]
		],
		3:[
			[1,1,1,0],
			[0,1,0,0],
			[0,0,0,0],
			[0,0,0,0]
		],
		4:[
			[0,1,0,0],
			[1,1,0,0],
			[0,1,0,0],
			[0,0,0,0]
		]
	}

	block = u'\u001b[35m█\u001b[0m'
	

	def config(self, rotation):
		return self.configs[rotation]

	def get_block(self):
		return self.block

class O_mino:
	configs = {
		1:[
			[1,1,0,0],
			[1,1,0,0],
			[0,0,0,0],
			[0,0,0,0]
		],
		2:[
			[1,1,0,0],
			[1,1,0,0],
			[0,0,0,0],
			[0,0,0,0]
		],
		3:[
			[1,1,0,0],
			[1,1,0,0],
			[0,0,0,0],
			[0,0,0,0]
		],
		4:[
			[1,1,0,0],
			[1,1,0,0],
			[0,0,0,0],
			[0,0,0,0]
		]
	}

	block = u'\u001b[33m█\u001b[0m'
	

	def config(self, rotation):
		return self.configs[rotation]

	def get_block(self):
		return self.block

class J_mino:
	configs = {
		1:[
			[0,1,0,0],
			[0,1,0,0],
			[1,1,0,0],
			[0,0,0,0]
		],
		2:[
			[1,0,0,0],
			[1,1,1,0],
			[0,0,0,0],
			[0,0,0,0]
		],
		3:[
			[1,1,0,0],
			[1,0,0,0],
			[1,0,0,0],
			[1,0,0,0]
		],
		4:[
			[1,1,1,0],
			[0,0,1,0],
			[0,0,0,0],
			[0,0,0,0]
		]
	}

	block = u'\u001b[38;5;25m█\u001b[0m'


	def config(self, rotation):
		return self.configs[rotation]

	def get_block(self):
		return self.block

class L_mino:
	configs = {
		1:[
			[1,0,0,0],
			[1,0,0,0],
			[1,1,0,0],
			[0,0,0,0]
		],
		2:[
			[1,1,1,0],
			[1,0,0,0],
			[0,0,0,0],
			[0,0,0,0]
		],
		3:[
			[1,1,0,0],
			[0,1,0,0],
			[0,1,0,0],
			[0,0,0,0]
		],
		4:[
			[0,0,1,0],
			[1,1,1,0],
			[0,0,0,0],
			[0,0,0,0]
		]
	}

	block = u'\u001b[38;5;208m█\u001b[0m'


	def config(self, rotation):
		return self.configs[rotation]

	def get_block(self):
		return self.block

class S_mino:
	configs = {
		1:[
			[0,1,1,0],
			[1,1,0,0],
			[0,0,0,0],
			[0,0,0,0]
		],
		2:[
			[1,0,0,0],
			[1,1,0,0],
			[0,1,0,0],
			[0,0,0,0]
		],
		3:[
			[0,1,1,0],
			[1,1,0,0],
			[0,0,0,0],
			[0,0,0,0]
		],
		4:[
			[1,0,0,0],
			[1,1,0,0],
			[0,1,0,0],
			[0,0,0,0]
		]
	}

	block = u'\u001b[32m█\u001b[0m'


	def config(self, rotation):
		return self.configs[rotation]
	
	def get_block(self):
		return self.block

class Z_mino:
	configs = {
		1:[
			[1,1,0,0],
			[0,1,1,0],
			[0,0,0,0],
			[0,0,0,0]
		],
		2:[
			[0,1,0,0],
			[1,1,0,0],
			[1,0,0,0],
			[0,0,0,0]
		],
		3:[
			[1,1,0,0],
			[0,1,1,0],
			[0,0,0,0],
			[0,0,0,0]
		],
		4:[
			[0,1,0,0],
			[1,1,0,0],
			[1,0,0,0],
			[0,0,0,0]
		]
	}

	block = u'\u001b[31m█\u001b[0m'
	

	def config(self, rotation):
		return self.configs[rotation]
	def get_block(self):
		return self.block