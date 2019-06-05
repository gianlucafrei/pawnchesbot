# Pawnchesbot
School project: An ai playing chess with ony pawn.


## Hot to play
Start the game with `python3 game.py`

```
Select a mode:
1: human    vs. computer
2: computer vs. human
3: computer vs. computer
4: human    vs. human
Enter your choice (1-4): 1
    A   B   C   D   E 
   --------------------
5 | b | b | b | b | b |
   --------------------
4 |   |   |   |   |   |
   --------------------
3 |   |   |   |   |   |
   --------------------
2 |   |   |   |   |   |
   --------------------
1 | w | w | w | w | w |
   --------------------
heuristics for this board: 0
Select your move white
Possible Moves
1: 1A->2A
2: 1B->2B
3: 1C->2C
4: 1D->2D
5: 1E->2E
Enter the number of your move:
```

Then enter the **number** of the move want to play: (1,2,3,...) Just enter for example `3` and press enter.

## How it works

### Alpha-Beta-Pruning

We have implemented a Alpha-Beta-Pruning algorithm. The searched depth is 5 and can be adjusted in to code.
The implementation of the search algorithm can be found in the `alphabeta.py` file.

### Heuristic

We played a bit with different heuristics and found our that the following works best. We start with a value of 0.
For each white piece we check on which rank it is (1 to 5) and add the square of the rank to the value.
For the black pieces we do the same but just subtract the the rank for the value.
Let's make an example with the following board.
```
    A   B   C   D   E 
   --------------------
5 |   | b | b |   | b |
   --------------------
4 | b |   |   | b |   |
   --------------------
3 |   |   | w |   |   |
   --------------------
2 | w |   |   |   |   |
   --------------------
1 |   | w |   | w | w |
   --------------------
```
Because the white A pawn is on the second rank it adds 4 point to the heuristic value. The C pawn adds 9 points to the heuristic output. The B, D, and E pawn each add 1 point to the value. The total points for white are 2+1+9+1+1=14
The black pawns A,B,C,D,E count as 4 1, 1, 4, 1 and therefore subtracts 11 points in total for the heuristic output.
The final output of the heuristic is therefore 14-11=3.
