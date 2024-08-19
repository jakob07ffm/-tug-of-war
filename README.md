# Tug of War Game

Welcome to the Tug of War game! This README will guide you on how to play, as well as provide an overview of the game mechanics and controls.

## Overview

Tug of War is a competitive game where two players (or one player against AI) compete to pull a marker to their side of the screen. The game is won when a player successfully pulls the marker all the way to their edge of the screen or when the opponent's stamina is depleted.

## How to Play

### Objective

- **Pull the marker to your side**: The goal is to pull the marker to your side of the screen before your opponent does.
- **Manage your stamina**: Each player has a stamina bar that decreases when pulling. Efficiently manage your stamina to avoid exhaustion.

### Controls

- **Player 1 (Left Side)**
  - Press `A` key to pull the marker towards you.
  - Press `S` key to activate a special move (once available).
- **Player 2 (Right Side)**
  - Press `L` key to pull the marker towards you.
  - Press `;` key to activate a special move (once available).
  
- **Other Controls**
  - Press `P` key to pause or resume the game.
  - Press `M` key to mute or unmute the sound.
  - Press `R` key to restart the game after a round is won.
  - Press `Q` key to quit the game.

### Game Features

- **Stamina**: Each player starts with full stamina (100 points). Stamina decreases when pulling the marker and regenerates slowly when not pulling.
  - Green bar indicates high stamina.
  - Red bar indicates low stamina.

- **Power-Ups**: Occasionally, power-ups appear on the screen. Capture them by positioning the marker over the power-up. Types of power-ups include:
  - **Stamina Boost**: Restores some stamina.
  - **Speed Boost**: Temporarily increases the speed of the marker.
  - **Invincibility**: Fully restores stamina temporarily.

- **Weather Effects**: Random weather effects, like wind, can influence the marker's movement.

- **AI Mode**: If AI is enabled (`A` key), Player 2 will be controlled by the computer with a difficulty level of your choice (easy, medium, hard).

- **Special Moves**: Each player can perform a special move that fully restores stamina once per game.

## Winning the Game

- The round is won when a player pulls the marker to their edge of the screen, or when the opponent's stamina is depleted.
- The game displays the winner and the number of rounds each player has won. The first player to win 3 rounds is declared the overall winner.

## Configuration

- **AI Difficulty**: Modify the `ai_difficulty` variable in the code to set AI difficulty. Options are `"easy"`, `"medium"`, and `"hard"`.

- **Sound**: Toggle sound on/off during gameplay by pressing the `M` key.

## Setup and Running the Game

To run the game:
1. Ensure you have Python installed.
2. Install Pygame using `pip install pygame`.
3. Run the game script with `python tug_of_war.py`.

Enjoy the game!
