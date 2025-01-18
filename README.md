# About this game
This game was made in pygame. It consists of a bunch of little balls that fly around the screen, bouncing off of lines that the user places. For each ball on screen, when it hits a line that has been placed, the angle of reflection is calculated using trignometry to simulate realistic bouncing physics. This lets the user create elaborate systems that balls can bounce around in.

During my first Computer Science semester at USU, I learned how to use python. When I found out about what classes were and how they were different from structs in C, I decided to try and implement that knowledge and expand upon it by making this simple but satisfying game.

## ZIP file
You can just extract Ball-Sound-Game.zip and run that, no python IDE required :)  
However, if you want to peek around at code you can totally do that with the other files using your favorite text editor or python IDE

# Intended play
It is quite fun to place a spawner on one part of the screen, and watching the trajectory of balls, to continue placing new lines for them to bounce off of. You can essentially place as many lines in any configuration you want, which lets you make all sorts of wacky, intricate, crazy bouncing paths for the balls (before they eventually fly off the screen). Try to get as many balls to stay on the screen at once as you can! 

The game will start lagging once you get above several hundred balls. This might be due to me including for loops in multiple different places in the code, for things such as physics, and displaying to the screen. This was just to organize the code to make it more readable, and this project was small enough that I don't think it matters too much.

# Controls
The user uses the mouse and keyboard to place balls, spawners that repeatedly spawn balls in the same location, and lines for the balls to bounce off of.
> - 1 = place ball
> - 2 = begin / end line segment
> - 3 = place spawner
> - 4 = speed up spawner, if mouse is hovering over it
> - 5 = slow down spawner, if mouse is hovering over it
> - 6 = toggle noise on / off
