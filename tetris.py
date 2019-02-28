import sys, os, time, random, signal,  select, tty, termios, atexit
from tetromino import *
win_rows, win_cols = os.popen('stty size', 'r').read().split()
n = int(win_rows)
m = int(win_cols)
orig_termios = None

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

def enableRawMode():
	global orig_termios
	orig_termios = termios.tcgetattr(sys.stdin)
	raw_termios = termios.tcgetattr(sys.stdin)
	
	raw_termios[3] = raw_termios[3] & ~(termios.ECHO | termios.ICANON)
	raw_termios[6][termios.VMIN] = 0
	raw_termios[6][termios.VTIME] = 0

	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, raw_termios)	
	atexit.register(disableRawMode)

def disableRawMode():
	global orig_termios
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_termios)
	sys.stdout.flush()
	
def check_input():	
	ch_set = []
	ch = os.read(sys.stdin.fileno(), 1)
	while ch != None and len(ch) > 0:
		if ord(ch) == 27:
			ch_set.append('^')
		else:
			ch_set.append(chr(int(ord(ch))))
		if ch_set[0] != '^' or len(ch_set) >= 3:
			break
		ch = os.read(sys.stdin.fileno(), 1)
	ch_set = ''.join(ch_set)
	return ch_set

def main():
	#signal.signal(signal.SIGINT, sig_handler)
	enableRawMode()
	# clear screen
	#print(clr + hom, end = '')
	#for line in grid:
	#	print(''.join(line), end='')
	#	sys.stdout.flush()
	grid = Grid(n,m)
	minos = []
	mino = None
	t = -1
	fr = 100
	mino_oldpos = None
	goal_col = 0
	ghost = None
	while(True):
		t += 1
		#time.sleep(fr)
		
		inp = check_input()
		if inp == 'q':
			sys.exit()
		elif inp == ' ' and mino == None:
			mino = Tetromino(random.choice('LJSZTOI'), grid, random.randint(1,4))
		elif inp == '^[D' and mino != None:
			mino.left()
		elif inp == '^[C' and mino != None:
			mino.right()
		
		if mino != None and t % fr == 0:
			if mino.can_drop():
				mino.drop()	
			else:
				mino = None
			
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
