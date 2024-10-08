# WebOne

![WebOne Game](sprites/cloud.png)

**WebOne** is an interactive two-player game that combines elements of luck and strategy, where each move can earn or lose points.

## Game Description

- **Game Board**: A 10x10 grid, where each cell hides:
  - Mine (-1 point)
  - Empty spot (0 points)
  - Cupcake (+1 point)

- **Objective**: Score more points than your opponent before all cells are revealed.

- **Features**:
  - Multiplayer game over network.
  - Interface built with PySide6.
  - Random distribution of items on the board.

## How to Play

- Players take turns clicking on buttons, trying to find cupcakes while avoiding mines.
- The game automatically decides who goes first.