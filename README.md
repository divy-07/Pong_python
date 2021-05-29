# Pong_python
Made using PyGame. I also publish exe versions of this game on my [website](https://divy-07.github.io/). Check that out if you want to play it. I will only be uploading latest versions on here, though you can [play the older version](https://divy-07.github.io/games/pong/) from the website.

The game offers single player and multiplayer option. (Multiplayer is on the same computer)
Additionally, you can choose from 5, 10 or unlimited points game. 

For playing against computer, difficulties include: easy, medium, hard, and impossible. 

### Objective of the game

Both player are paddles that move with arrow keys and WASD.
The objective is to make the other player miss the ball. One miss = one point.
Reach the goal and you win.

### Physics/mechanics

The ball initially starts with slow speed, but as the game continues without anyone scoring, the ball speeds up.
The direction of ball leaving the paddle is determined from how far away from paddle's center it is hit.
So, hit in center and it will go straight. Hit on edge and it goes at an angle(max 55 degree angle).
This means more risk = more reward as angled shots are hard to hit.

Enjoy!

Feel free to use the code and add features using pull requests. 
