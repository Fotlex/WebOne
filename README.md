# WebOne

![WebOne Game](sprites/cloud.png)

**WebOne** is an interactive two-player minesweeper game that combines elements of luck and strategy, where each move can earn or lose points.

## Game Description

- **Game Board**: A 10x10 grid, where each cell hides:
  - Mine (-1 point)
  - Cupcake (+1 point)

- **Objective**: Score more points than your opponent before all non-mine cells are revealed or all 30 mines are hit.

- **Features**:
  - Multiplayer game over network.
  - Interface built with PySide6.
  - Random distribution of mines on the board.
  - Option to place or remove a flag on suspected mine locations.

## How to Play

- Players take turns clicking on buttons, trying to find cupcakes while avoiding mines.
- The game automatically decides who goes first.