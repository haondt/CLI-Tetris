import sys, os, time, random
from tetromino import *
win_rows, win_cols = os.popen('stty size', 'r').read().split()
n = int(win_rows)
m = int(win_cols)
grid = [[' ' for i in range(m)] for j in range(n)]
for i in range(m):
	grid[0][i] = '-'
	grid[n-1][i] = '-'
for i in range(n):
	grid[i][0] = '|'
	grid[i][m-1] = '|'
grid[0][0] = '+'
grid[0][m-1] = '+'
grid[n-1][0] = '+'
grid[n-1][m-1] = '+'


# \u001b[ -> escape character
# 2J -> clear screen
# H -> home cursor
esc = u'\u001b['
clr = esc + u'2J'
hom = esc + u'H'
linclr = esc + u'2K'
csrL = esc + u'1D'
csrR = esc + u'1C'
csrU = esc + u'1A'
csrD = esc + u'1B'

def main():
	# clear screen
	#print(clr + hom, end = '')
	#for line in grid:
	#	print(''.join(line), end='')
	#	sys.stdout.flush()
	grid = Grid(n,m)
	minos = []
	minos.append(Tetromino('J', grid))
	t = -1	
	fr = 0.00001
	while(True):
		t += 1
		time.sleep(fr)
		
		
		for mino in minos:
			if mino.can_drop():
				mino.drop()
			if mino.can_go_right():
				mino.right()
		if (t+1) % 10 == 0:
			minos.append(Tetromino(random.choice('LJSZTOI'), grid))

		grid.draw()
		
		#print(esc + u'10CX', end = '')
		#sys.stdout.flush()
		#time.sleep(0.1)
		#print(csrL + ' ' + csrL)

main()
