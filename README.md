# MazeSolver-Python
Robotics Project

MazeSolver.py takes input from a maze.txt file, which contains '@' characters (wall/obstacle), '.' (open space), and 'A' (entrance) and 'B' (exit).

This project was to showcase the steps of a simple algorithm developed for the robot to solve the maze.

1. Survey immediate surroundings and update map
2. Move to a new open square if available, otherwise move back
3. Note current position, and check for entrace/exit condition

The initial window displays the robots current knowledge of the maze, which is the squares immediately surrounding it. With each keypress, the robot will move and expand it's view of the maze as it explores it.

Green squares represent walls, whereas gray squares are open space, and white areas are not known to the robot yet.
