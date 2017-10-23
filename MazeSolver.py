from tkinter import *
import random

window = Tk()
width, height = 0, 0;
current_x, current_y = 0, 0;
win_x, win_y = 0, 0;
origin_x, origin_y = 0, 0;
maze = [[]]
move = []
index = 0
over = False

#MAIN METHOD
#Open file. Populate Maze list. Print current map. Call surroundings()
#-------------------------------------------------------------------------
def main():
	global window, width, height, maze
	global current_x, current_y, win_x, win_y, origin_x, origin_y
	
	i, j = 0, 0;
	maze_file = 'maze.txt'
	
	#Open maze file, populate maze list
	with open(maze_file, 'r') as f:
		maze = [list(line.strip()) for line in f]
	
	#Set key coordinates (current, exit, entrance), print current position
	for line in maze:
		for c in line:
			if c == 'A':
				origin_x, origin_y = j, i;
				current_x, current_y = origin_x, origin_y;
				coord = Label(window, relief=RAISED, bg='blue', width=3)
				coord.grid(row=i, column=j)
			elif c == 'B':
				win_x, win_y = j, i;
			j = j + 1
			width = j
		j = 0
		i = i + 1
	height = i	
	
	surroundings()
	
	window.title('Maze Simulator')
	window.bind_all('<Key>', key)	#Bind all key presses to execute key method

	
#Check the immediate squares surrounding the bot
#-------------------------------------------------------------------------
def surroundings():
	global current_x, current_y, maze, height, width
	
	up = current_y-1
	down = current_y+1
	left = current_x-1
	right = current_x+1
	poss_mov = 0		#Keeps count of possible moves to display num to console
	
	#Check if the square is within the bounds of the maze
	if (up) >= 0:
		poss_mov = poss_mov + check(up, current_x)
			
	if (down) <= (height - 1):
		poss_mov = poss_mov + check(down, current_x)
			
	if (left) >= 0:
		poss_mov = poss_mov + check(current_y, left)
				
	if (right) <= (width - 1):
		poss_mov = poss_mov + check(current_y, right)
	
	if (up) >= 0 and (left) >= 0:
		check(up, left)
			
	if (up) >= 0 and (right) <= (width - 1):
		check(up, right)
			
	if (down) <= (height - 1) and (left) >= 0:
		check(down, left)
			
	if (down) <= (height - 1) and (right) <= (width - 1):
		check(down, right)

	print('Scanning...\nThere are ' + str(poss_mov) + ' new possible moves\n------------------------------\n')


#Checks to see if the square is a wall or open space, then calls for a map update
#-------------------------------------------------------------------------
def check(y, x):
	global maze
	num = 0
	if (maze[y][x] != '@'):
		if (maze[y][x] != '#'):
			update(y, x, 'floor')
			num = 1		#Marked as a possible move
	else:
		update(y, x, 'wall')
	return num


#Updates the map with the correct environment
#-------------------------------------------------------------------------
def update(y, x, type):
	global window
	if type=='wall':
		coord = Label(window, relief=RAISED, bg='light green', width=3)
		coord.grid(row=y, column=x)
	if type=='floor':
		coord = Label(window, relief=SUNKEN, bg='grey', width=3)
		coord.grid(row=y, column=x)


#Returns the bot to the previous square
#-------------------------------------------------------------------------
def moveback():
	global current_x, current_y, index, move
	if move[index-1] == 'u':
		current_x, current_y = moveto('d', current_x, current_y, True)
	elif move[index-1] == 'd':
		current_x, current_y = moveto('u', current_x, current_y, True)
	elif move[index-1] == 'l':
		current_x, current_y = moveto('r', current_x, current_y, True)
	elif move[index-1] == 'r':
		current_x, current_y = moveto('l', current_x, current_y, True)


#Moves the bot in the specified direction, and updates the move list accordingly
#-------------------------------------------------------------------------
def moveto(dir, x, y, bool):
	global window, move, index, maze
	
	#Update coordinate depending on dir parameter
	new_x, new_y = x, y;
	if dir == 'u':
		new_y = y-1
	elif dir == 'd':
		new_y = y+1
	elif dir == 'l':
		new_x = x-1
	elif dir == 'r':
		new_x = x+1
	
	#Moving back, erase move from list, and mark square as red
	if bool:
		move.pop()
		index = index - 1
		color = 'red'

	#Moving to new square, add move to list, mark square as yellow
	else:
		move.append(dir)
		index = index + 1
		color = 'yellow'
	
	#Move to square, mark previous square accordingly
	for child in window.children.values():
		info = child.grid_info()
		if info['row'] == (y) and info['column'] == x:
			child.config(relief=SUNKEN, bg=color)
		if info['row'] == (new_y) and info['column'] == new_x:
			child.config(relief=RAISED, bg='blue')
	
	#Mark square as already traversed
	maze[y][x] = '#'
	
	return new_x, new_y		#Returns the new position of the bot


#Executes while maze is not over.
#Calculates possible moves, randomly picks one, then calls to move in that direction
#-------------------------------------------------------------------------
def key(event):
	global width, height, maze, over
	global current_x, current_y, win_x, win_y, origin_x, origin_y
	if (not over):
		up = current_y-1
		down = current_y+1
		left = current_x-1
		right = current_x+1
		m, u, d, l, r = 0, 0, 0, 0, 0;
		
		#Assigns a move number if a new move is possible
		#Check for out of bounds, walls, or already marked squares
		if (up) >= 0 and (maze[up][current_x] != '@') and (maze[up][current_x] != '#'):
			m = m + 1
			u = m
		if (down) <= (height - 1) and (maze[down][current_x] != '@') and (maze[down][current_x] != '#'):
			m = m + 1
			d = m
		if (left) >= 0 and (maze[current_y][left] != '@') and (maze[current_y][left] != '#'):
			m = m + 1
			l = m
		if (right) <= (width - 1) and (maze[current_y][right] != '@') and (maze[current_y][right] != '#'):
			m = m + 1
			r = m
		
		#No new moves available, go to previous square
		if m == 0:
			moveback()
			print('>>> Going back\n')
		#Randomly choose one of the move numbers assigned
		else:
			num = random.randint(1,m)
		
			#Move in chosen direction
			if num == u:
				print('>>> Chose to move up\n')
				current_x, current_y = moveto('u', current_x, current_y, False)
			elif num == d:
				print('>>> Chose to move down\n')
				current_x, current_y = moveto('d', current_x, current_y, False)
			elif num == l:
				print('>>> Chose to move left\n')
				current_x, current_y = moveto('l', current_x, current_y, False)
			elif num == r:
				print('>>> Chose to move right\n')
				current_x, current_y = moveto('r', current_x, current_y, False)

		#Check surroundings of new position
		surroundings()

		#Check for non-solvable condition
		if current_x == origin_x and current_y == origin_y:
			print('Back at start...')
			root = Tk()
			root.title('Robot Comm')
			Label(root, text=('The maze no has solutions :('), font='Arial 14 bold', width = 25).grid(row=1, column=1)
			over = True

		#Check for win condition
		if current_x == win_x and current_y == win_y:
			print('Found the exit!!!')
			root = Tk()
			root.title('Robot Comm')
			Label(root, text='I found the exit!!', anchor=W, justify=LEFT, font='Arial 20 bold', width = 20).grid(row=0, column=0)
			over = True


main()
mainloop()
