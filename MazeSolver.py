from tkinter import *
import random

maze_file = 'maze.txt'

window = Tk()
width, height = 0, 0;
x, y =0, 0;
xwin, ywin = 0, 0;
xorigin, yorigin = 0, 0;
maze = [[]]
move = []
index = 0
over = False

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def main():
	global window, maze_file, maze
		
	with open(maze_file, 'r') as f:
		maze = [list(line.strip()) for line in f]
	
	print_maze()
	
	window.title('Maze Simulator')
	window.bind_all('<Key>', key)

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def print_maze():
	global window, width, height, maze
	global x, y, xwin, ywin, xorigin, yorigin
	i, j = 0, 0;
	
	for line in maze:
		for c in line:
			if c == 'A':
				x, y = j, i;
				xorigin, yorigin = x, y;
				coord = Label(window, relief=RAISED, bg='red', width=3)
				coord.grid(row=i, column=j)
			elif c == 'B':
				xwin, ywin = j, i;
			j = j + 1
			width = j
		j = 0
		i = i + 1

	height = i	
	
	surroundings()

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def key(event):
	global width, height, maze, over
	global x, y, xwin, ywin, xorigin, yorigin
	if (not over):
		m, a, b, c, d = 0, 0, 0, 0, 0;
		if (y - 1) >= 0 and (maze[y-1][x] != '@') and (maze[y-1][x] != '#'):
					m = m + 1
					a = m
				
		if (y + 1) <= (height - 1) and (maze[y+1][x] != '@') and (maze[y+1][x] != '#'):
					m = m + 1
					b = m
				
		if (x - 1) >= 0 and (maze[y][x-1] != '@') and (maze[y][x-1] != '#'):
					m = m + 1
					c = m
					
		if (x + 1) <= (width - 1) and (maze[y][x+1] != '@') and (maze[y][x+1] != '#'):
					m = m + 1
					d = m
		
		if m == 0:
			moveback()
			print('>>> Going back\n')

		else:
			r = random.randint(1,m)
		
			if r == a:
				print('>>> Chose to move up\n')
				x, y = moveup(x, y, False)
			elif r == b:
				print('>>> Chose to move down\n')
				x, y = movedown(x, y, False)
			elif r == c:
				print('>>> Chose to move left\n')
				x, y = moveleft(x, y, False)
			elif r == d:
				print('>>> Chose to move right\n')
				x, y = moveright(x, y, False)

		surroundings()

		if x == xorigin and y == yorigin:
			print('Back at start...')
			root = Tk()
			root.title('Robot Comm')
			Label(root, text=('The maze no has solutions :('), font='Arial 14 bold', width = 25).grid(row=1, column=1)
			over = True

		if x == xwin and y == ywin:
			print('Found the exit!!!')
			root = Tk()
			root.title('Robot Comm')
			Label(root, text='I found the exit!!', anchor=W, justify=LEFT, font='Arial 20 bold', width = 20).grid(row=0, column=0)
			Label(root, text='Let me show you the path', font='Arial 16 bold', width = 25).grid(row=1, column=0)
			trace()
			over = True

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def surroundings():
	global x, y, maze, height, width
	m = 0
	if (y - 1) >= 0:
		if (maze[y-1][x] != '@'):
			if (maze[y-1][x] != '#'):
				discover(x, y-1, 'floor')
				m = m + 1
		else:
			discover(x, y-1, 'wall')
			
	if (y + 1) <= (height - 1):
		if (maze[y+1][x] != '@'):
			if (maze[y+1][x] != '#'):
				discover(x, y+1, 'floor')
				m = m + 1
		else:
			discover(x, y+1, 'wall')
			
	if (x - 1) >= 0:
		if (maze[y][x-1] != '@'):
			if (maze[y][x-1] != '#'):
				discover(x-1, y, 'floor')
				m = m + 1
		else:
			discover(x-1, y, 'wall')
				
	if (x + 1) <= (width - 1):
		if (maze[y][x+1] != '@'):
			if (maze[y][x+1] != '#'):
				discover(x+1, y, 'floor')
				m = m + 1
		else:
			discover(x+1, y, 'wall')
	
	if (y - 1) >= 0 and (x - 1) >= 0:
		if (maze[y-1][x-1] != '@'):
			if (maze[y-1][x-1] != '#'):
				discover(x-1, y-1, 'floor')
		else:
			discover(x-1, y-1, 'wall')
			
	if (y - 1) >= 0 and (x + 1) <= (width - 1):
		if (maze[y-1][x+1] != '@'):
			if (maze[y-1][x+1] != '#'):
				discover(x+1, y-1, 'floor')
		else:
			discover(x+1, y-1, 'wall')
			
	if (y + 1) <= (height - 1) and (x - 1) >= 0:
		if (maze[y+1][x-1] != '@'):
			if (maze[y+1][x-1] != '#'):
				discover(x-1, y+1, 'floor')
		else:
			discover(x-1, y+1, 'wall')
			
	if (y + 1) <= (height - 1) and (x + 1) <= (width - 1):
		if (maze[y+1][x+1] != '@'):
			if (maze[y+1][x+1] != '#'):
				discover(x+1, y+1, 'floor')
		else:
			discover(x+1, y+1, 'wall')

	print('Scanning...\nThere are ' + str(m) + ' new possible moves\n------------------------------\n')

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def discover(x, y, type):
	global window
	if type=='wall':
		coord = Label(window, relief=RAISED, bg='light green', width=3)
		coord.grid(row=y, column=x)
	if type=='floor':
		coord = Label(window, relief=SUNKEN, bg='grey', width=3)
		coord.grid(row=y, column=x)

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def moveback():
	global x, y, index, move
	if move[index-1] == 'u':
		x, y = movedown(x, y, True)
	elif move[index-1] == 'd':
		x, y = moveup(x, y, True)
	elif move[index-1] == 'l':
		x, y = moveright(x, y, True)
	elif move[index-1] == 'r':
		x, y = moveleft(x, y, True)

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def moveup(x, y, bool):
	global window, move, index, maze
	if bool:
		move.pop()
		index = index - 1
	else:
		move.append('u')
		index = index + 1
	for child in window.children.values():
		info = child.grid_info()
		if info['row'] == (y-1) and info['column'] == x:
			child.config(relief=RAISED, bg='red')
		if info['row'] == (y) and info['column'] == x:
			child.config(relief=SUNKEN, bg='grey')
	maze[y][x] = '#'
	y = y - 1
	return x, y

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def movedown(x, y, bool):
	global window, move, index, maze
	if bool:
		move.pop()
		index = index - 1
	else:
		move.append('d')
		index = index + 1
	for child in window.children.values():
		info = child.grid_info()
		if info['row'] == (y) and info['column'] == x:
			child.config(relief=SUNKEN, bg='grey')
		if info['row'] == (y+1) and info['column'] == x:
			child.config(relief=RAISED, bg='red')
	maze[y][x] = '#'
	y = y + 1
	return x, y

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def moveleft(x, y, bool):
	global window, move, index, maze
	if bool:
		move.pop()
		index = index - 1
	else:
		move.append('l')
		index = index + 1
	for child in window.children.values():
		info = child.grid_info()
		if info['row'] == (y) and info['column'] == (x-1):
			child.config(relief=RAISED, bg='red')
		if info['row'] == (y) and info['column'] == x:
			child.config(relief=SUNKEN, bg='grey')
	maze[y][x] = '#'
	x = x - 1
	return x, y

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def moveright(x, y, bool):
	global window, move, index, maze
	if bool:
		move.pop()
		index = index - 1
	else:
		move.append('r')
		index = index + 1
	for child in window.children.values():
		info = child.grid_info()
		if info['row'] == (y) and info['column'] == x:
			child.config(relief=SUNKEN, bg='grey')
		if info['row'] == (y) and info['column'] == (x+1):
			child.config(relief=RAISED, bg='red')
	maze[y][x] = '#'
	x = x + 1
	return x, y

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def trace():
	global window, move, index, x, y
	
	print(str(len(move)) + ' moves: ')
	print(move)
	
	while index > 0:
		if move[index-1] == 'u':
			y = y + 1
		elif move[index-1] == 'd':
			y = y - 1
		elif move[index-1] == 'l':
			x = x + 1
		elif move[index-1] == 'r':
			x = x - 1
		index = index - 1
		
		for child in window.children.values():
			info = child.grid_info()
			if info['row'] == (y) and info['column'] == x:
				child.config(bg='yellow')

main()
mainloop()