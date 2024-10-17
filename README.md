# ChessBot
A bot, that controls the mouse and plays moves by itself, based on Stockfish engine, on any online chess website.

I made a video about it [here](https://www.youtube.com/watch?v=1EPdyAZ48c8).

[<img src="https://i.ytimg.com/vi/1EPdyAZ48c8/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLAsKrrzhghv1peaqaX3mBXmvU8xxw">](https://www.youtube.com/watch?v=1EPdyAZ48c8)

Do not ever use it against real players. It's only for educational purposes. The bot lacks many features to make it more usable in some actual botting context and playing multiple games fast and reliably.

---
### How to use it?

After installing used dependencies:

1. Set up an online chess board visible on screen (only works when the board is viewed from the perspective of a white player)
2. Run the script and let it control your mouse without obstructing the board.
3. Let it run until the game ends. I don't think the script knows when the game ended, so just stop the script after.

---
### Features:
- Size and coordinates of the board shouldn't matter much, up to a point. Pieces should be clearly recognizable.
- Works only on a specified piece design.
- User has to manually input which side it plays as.
- It only works from the board orientation of a white player.
- Script doesnt have memory of past board states, so it can't determine repetitions or lack of castling rights.
- It uses a light version of Stockfish engine from a few years ago to make the decisions.