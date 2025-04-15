# Chezz-AI-Bot
Developed a Chess AI using Python that determines the most optimal move to play, by utilizing a best-first search algorithm. This algorithm takes in a heuristic evaluation function which sorts all potential moves and boards based on factors a variety of factors such as piece value and potential captures.

## How to run
`./run <board.txt>` where `board.txt` is a valid board file in the format:
`w 0 60000 0
{
a1: 'wF',
a2: 'wP',
a7: 'bP',
a8: 'bF',
b1: 'wN',
b2: 'wP',
b7: 'bP',
b8: 'bN',
c1: 'wC',
c2: 'wP',
c7: 'bP',
c8: 'bC',
d1: 'wQ',
d2: 'wP',
d7: 'bP',
d8: 'bQ',
e1: 'wK',
e2: 'wZ',
e7: 'bZ',
e8: 'bK',
f1: 'wB',
f2: 'wP',
f7: 'bP',
f8: 'bB',
g1: 'wN',
g2: 'wP',
g7: 'bP',
g8: 'bN',
h1: 'wR',
h2: 'wP',
h7: 'bP',
h8: 'bR'
}`

