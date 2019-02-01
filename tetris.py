import sys, os, time, random, signal, curses
from tetromino import *
curses.initscr()
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

def sig_handler(signum, frame):
	if signum == signal.SIGINT:
		print(clr + hom, end = '')
		sys.stdout.flush()
		curses.curs_set(1)
		curses.endwin()
		sys.exit()

def main():
	signal.signal(signal.SIGINT, sig_handler)
	# clear screen
	#print(clr + hom, end = '')
	#for line in grid:
	#	print(''.join(line), end='')
	#	sys.stdout.flush()
	grid = Grid(n,m)
	minos = []
	mino = None
	t = -1	
	fr = 0.000
	curses.curs_set(0)
	mino_oldpos = None
	goal_col = 0
	while(True):
		t += 1
		time.sleep(fr)
		
		if mino == None:
			mino = Tetromino(random.choice('LJSZTOI'), grid, random.randint(1,4))
			goal_col = random.randint(1,int(win_cols))
		else:
			mino.drop()	
			if mino.get_pos()[0] < goal_col:
				mino.right()
			elif mino.get_pos()[0] > goal_col:
				mino.left()
			
			if mino_oldpos == mino.get_pos():
				mino = None
			else:
				mino_oldpos = mino.get_pos()
			#if random.random() < 0.5:
			#	if random.random() < 0.5:
			#		mino.rotate('c')
			#	else:
			#		mino.rotate('cc')

		grid.draw()
		
		#print(esc + u'10CX', end = '')
		#sys.stdout.flush()
		#time.sleep(0.1)
		#print(csrL + ' ' + csrL)

main()
