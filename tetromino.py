import sys


class Grid:
	contents = None
	flagged = []
	def __init__ (self, height, width):
		self.contents = [[' ' for i in range(width)] for j in range(height)]
		self.flagged = [(i,j) for i in range(width) for j in range(height)]
	def reset(self):
		self.contents = [[' ' for j in contents[i]] for i in contents]

	# Returns true if the block is within the constraints of the grid and
	# there are no tetromino pieces in the spot, i.e. the spot contains ' '
	# (empty) or '█' (unformatted, is a ghost)
	def is_free(self, x,y):
		if x >= len(self.contents[0]) or y >= len(self.contents):
			return False
		else:
			return self.contents[y][x] == ' ' or self.contents[y][x] == '█'
	
	# Returns true only if all [x,y] coordinates in blocks are free
	def is_free_blocks(self, blocks):
		if blocks == []:
			return True
		return min([self.is_free(i[0], i[1]) for i in blocks])

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
				print('', end = '')
			for col in row:
				print(col, end = '')
		sys.stdout.flush()
	
	def get_width(self):
		return len(self.contents[0])
	def get_height(self):
		return len(self.contents)
	
	def clearLine(self, line):
		if line < len(self.contents) and line >= 0:
			full = min([i != ' ' for i in self.contents[line]])
			if full:
				# clear line
				self.contents[line] = [' ']*len(self.contents[line])

	def prettyClearLine(self):
		pass


class Tetromino:
	shape = None
	coords = None
	rotation = None
	grid = None
	showGhost = False
	ghost = None

	def __init__(self, shape, grid, rotation):
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

		self.ghost = Ghost(self.shape, grid, rotation)
		self.grid = grid
		self.rotation = rotation
		self.coords = [(grid.get_width()//2) -2, 0]
		
		self.fill()

	def collision(self):
		return self.shape()
		
	def rotate(self, direction):
		if self.can_rotate(direction):
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

	def can_rotate(self, direction):
		# get rotation
		test_rotation = None
		if direction == 'c':
			test_rotation = self.rotation + 1
			if test_rotation > 4:
				test_rotation = 1
		else:
			test_rotation = self.rotation - 1
			if test_rotation < 1:
				test_rotation = 4

		# create collision map for rotated mino
		test_config = self.shape.config(test_rotation)
		# ignore the actual current position of the tetromino
		config = self.shape.config(self.rotation)
		blocks = []
		for row in range(len(config)):
			for col in range(len(config)):
				if test_config[row][col] and not config[row][col]:
					blocks.append([self.coords[0]+col, self.coords[1]+row])

		# test rotated coords
		return self.grid.is_free_blocks(blocks)
		
	def can_go_left(self):
		config = self.shape.config(self.rotation)
		# find rightmost block in each column
		leftblocks = [-1 for i in range(len(config))]
		
		for row in range(len(config)):
			x = self.coords[0]
			for col in config[row]:
				if col:
					if leftblocks[row] == -1:
						leftblocks[row] = x
					else:
						leftblocks[row] = min(leftblocks[row], x)
				x += 1
		

		# check if it can move left
		left = True
		for block_i in range(len(leftblocks)):
			block = leftblocks[block_i]
			if block != -1:
				if not self.grid.is_free(block-1,block_i+self.coords[1]):
					left = False
					break
		return left

	def left(self):
		if self.can_go_left():
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
		if self.can_go_right():
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

		if not drop:
			for i in range(self.coords[0], self.coords[0]+4):
				self.grid.clearLine(i)
		return drop
	
	def drop(self):
		if self.can_drop():
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
		
		if self.showGhost:
			self.ghost.clear()

	# insert only colored tiles into grid
	def fill(self):
		# draw ghost first, and draw tetromino on top of ghost
		if self.showGhost:
			# give the ghost the new coordinates
			self.ghost.setcoords(self.coords.copy())
			# update the ghosts rotation
			self.ghost.setRotation(self.rotation)
			# drop the ghost to the bottom
			self.ghost.drop()
			# fill in the ghost
			self.ghost.fill()
		
		config = self.shape.config(self.rotation)
		y = self.coords[1]
		for row in config:
			x = self.coords[0]
			for col in row:
				if col:
					self.grid.fill(x, y, self.shape.get_block())
				x += 1
			y += 1

	
	def get_pos(self):
		return self.coords.copy()

	def showGhost(self):
		self.showGhost = True
		self.ghost.fill()

	def hideGhost(self):
		self.showGhost = False
		self.ghost.clear()

class Ghost:
	shape = None
	coords = None
	rotation = None
	grid = None
	def __init__(self, shape, grid, rotation):	
		self.shape = shape
		self.grid = grid
		self.coords = [0,0]
		self.rotation = rotation
	
	def setRotation(self, rotation):
		self.rotation = rotation
	
	def setcoords(self, coords):
		self.coords = coords

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

		if not drop:
			for i in range(self.coords[0], self.coords[0]+4):
				self.grid.clearLine(i)
		return drop

	# drop until ghost is at bottom
	def drop(self):
		while self.can_drop():
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
					# use default terminal color for ghost
					self.grid.fill(x, y,'█')
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

	block = u'\u001b[36m█\u001b[0m'


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
