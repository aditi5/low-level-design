from collections import deque
from abc import ABC, abstractmethod
import random


# Observer Pattern: Abstract class for observers (players)
class PlayerObserver(ABC):
    @abstractmethod
    def update(self, player_id: int, score: int, game_over: bool):
        pass


# Command Pattern: Abstract class for commands (moves)
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# Concrete MoveCommand implementing Command Pattern
class MoveCommand(Command):
    def __init__(self, game, player_id, direction):
        self.game = game
        self.player_id = player_id
        self.direction = direction

    def execute(self):
        return self.game.move(self.player_id, self.direction)


# Player class (Observer Pattern)
class Player(PlayerObserver):
    def __init__(self, player_id):
        self.player_id = player_id
        self.score = 0

    def update(self, player_id, score, game_over):
        if self.player_id == player_id:
            self.score = score
            if game_over:
                print(f"Player {self.player_id} game over with score: {self.score}")
            else:
                print(f"Player {self.player_id} score updated to: {self.score}")


# Ghost class for AI-controlled movement
class Ghost:
    def __init__(self, position):
        self.position = position

    def move(self, directions, width, height):
        # Randomly choose a direction for the ghost
        direction = random.choice(list(directions.values()))
        new_position = (self.position[0] + direction[0], self.position[1] + direction[1])
        # Check bounds to keep ghosts within the grid
        if 0 <= new_position[0] < height and 0 <= new_position[1] < width:
            self.position = new_position


# Pacman Game class (Singleton Pattern)
class PacmanGame:
    _instance = None

    @staticmethod
    def get_instance(width: int, height: int, pellets: list):
        if PacmanGame._instance is None:
            PacmanGame._instance = PacmanGame(width, height, pellets)
        return PacmanGame._instance

    def __init__(self, width: int, height: int, pellets: list):
        self.width = width
        self.height = height
        self.pellets = set(tuple(p) for p in pellets)  # Set of pellet positions
        self.players = {}  # Store players
        self.observers = []  # List of observers (players)
        self.pacmans = {}  # Store positions of each player's Pacman
        self.ghosts = [Ghost((height // 2, width // 2))]  # Initialize ghosts at the center
        self.directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    def add_player(self, player_id: int):
        # Initialize a Pacman for the new player at (0, 0)
        self.players[player_id] = Player(player_id)
        self.pacmans[player_id] = (0, 0)
        self.observers.append(self.players[player_id])

    def notify_observers(self, player_id, score, game_over):
        for observer in self.observers:
            observer.update(player_id, score, game_over)

    def move(self, player_id: int, direction: str) -> int:
        # Get the current position of the player's Pacman
        pacman_position = self.pacmans[player_id]
        delta_row, delta_col = self.directions[direction]
        new_position = (pacman_position[0] + delta_row, pacman_position[1] + delta_col)

        # Check if the new position is out of bounds
        if not (0 <= new_position[0] < self.height and 0 <= new_position[1] < self.width):
            self.notify_observers(player_id, self.players[player_id].score, True)
            return -1  # Game over, Pacman hit the wall

        # Check if Pacman encounters a ghost
        for ghost in self.ghosts:
            if new_position == ghost.position:
                self.notify_observers(player_id, self.players[player_id].score, True)
                return -1  # Game over, Pacman encounters a ghost

        # Check if Pacman eats a pellet
        if new_position in self.pellets:
            self.players[player_id].score += 10  # Increase score for eating a pellet
            self.pellets.remove(new_position)  # Remove the eaten pellet
            self.notify_observers(player_id, self.players[player_id].score, False)

        # Update Pacman's position
        self.pacmans[player_id] = new_position
        return self.players[player_id].score

    def move_ghosts(self):
        # Move all ghosts randomly
        for ghost in self.ghosts:
            ghost.move(self.directions, self.width, self.height)


# Example usage:
game = PacmanGame.get_instance(5, 5, [[1, 2], [3, 3], [0, 4]])
game.add_player(1)
game.add_player(2)

# Player 1 moves
move_command_1 = MoveCommand(game, 1, "R")
print(move_command_1.execute())  # Player 1 moves right

# Player 2 moves
move_command_2 = MoveCommand(game, 2, "D")
print(move_command_2.execute())  # Player 2 moves down

# Move ghosts
game.move_ghosts()


"""
To create a basic Pacman game with similar design patterns and multiplayer support, we'll break down the game into key components and implement a simplified version. The Pacman game mechanics include the following aspects:

Grid-Based Movement: Pacman moves within a grid and collects pellets. Ghosts also move within the grid.
Multiple Players: Support for multiple players (multiple Pacmans) and AI-controlled ghosts.
Observer Pattern: Notify players of game state changes (e.g., score updates, game over).
Command Pattern: Handle movement commands for both players and ghosts.
Singleton Pattern: To ensure only one game instance is running.
Factory Method Pattern: To create different characters (Pacman and Ghosts).


Explanation of the Implementation:
Observer Pattern:

Player class observes the game state and is notified of changes like score updates and game over status.
Command Pattern:

MoveCommand handles movement commands for each player, allowing us to encapsulate and execute player moves.
Singleton Pattern:

PacmanGame uses the singleton pattern to ensure that only one instance of the game is running.
Factory Method Pattern:

Although not explicitly used here, a factory method could be implemented to create different types of characters (Pacman, Ghosts) for a more complex game.
Ghost Movement:

The Ghost class has simple AI for random movement within the grid, keeping them constrained within the game's boundaries.
Multiplayer Support:

The game supports multiple players, with each controlling their own Pacman.
Players can move independently, and the game tracks their scores.
How It Works:
Players issue movement commands using the MoveCommand.
The game processes movements, checks collisions (walls, ghosts), and updates scores when a pellet is eaten.
The game uses an observer pattern to notify players of changes in the game state.
Ghosts move randomly after every player command.
"""