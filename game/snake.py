from collections import deque
from abc import ABC, abstractmethod


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


# Snake Game class (Singleton Pattern)
class SnakeGame:
    _instance = None

    @staticmethod
    def get_instance(width: int, height: int, food: list):
        if SnakeGame._instance is None:
            SnakeGame._instance = SnakeGame(width, height, food)
        return SnakeGame._instance

    def __init__(self, width: int, height: int, food: list):
        self.width = width
        self.height = height
        self.food = deque(food)  # Queue of food positions
        self.players = {}  # Store players with their snakes
        self.observers = []  # List of observers (players)
        self.snakes = {}  # Store snakes for each player
        self.directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    def add_player(self, player_id: int):
        # Initialize a snake for the new player at (0, 0)
        self.players[player_id] = Player(player_id)
        self.snakes[player_id] = {
            'body': deque([(0, 0)]),
            'body_set': {(0, 0)},
            'score': 0
        }
        self.observers.append(self.players[player_id])

    def notify_observers(self, player_id, score, game_over):
        for observer in self.observers:
            observer.update(player_id, score, game_over)

    def move(self, player_id: int, direction: str) -> int:
        snake = self.snakes[player_id]
        snake_body = snake['body']
        snake_set = snake['body_set']

        # Get the current head of the snake
        head_row, head_col = snake_body[0]

        # Calculate the new head position based on the direction
        delta_row, delta_col = self.directions[direction]
        new_head = (head_row + delta_row, head_col + delta_col)

        new_head_row, new_head_col = new_head

        # Check if the new head position is out of bounds
        if not (0 <= new_head_row < self.height and 0 <= new_head_col < self.width):
            self.notify_observers(player_id, snake['score'], True)
            return -1  # Game over, snake hit the wall

        # Check if the new head hits another snake's body (excluding the tail because it moves)
        if new_head in snake_set and new_head != snake_body[-1]:
            self.notify_observers(player_id, snake['score'], True)
            return -1  # Game over, snake hit itself

        # Check if the new head is at the food position
        if self.food and new_head == tuple(self.food[0]):
            # Snake eats the food, increase score
            snake['score'] += 1
            self.food.popleft()  # Remove the eaten food
            # Don't pop the tail because the snake grows
        else:
            # Move the snake: add the new head and remove the tail
            tail = snake_body.pop()
            snake_set.remove(tail)  # Remove tail from the set

        # Add the new head to the snake's body
        snake_body.appendleft(new_head)
        snake_set.add(new_head)  # Add new head to the set

        # Notify observers about the updated score
        self.notify_observers(player_id, snake['score'], False)
        return snake['score']


# Example usage:
game = SnakeGame.get_instance(3, 2, [[1, 2], [0, 1]])
game.add_player(1)
game.add_player(2)

# Player 1 moves
move_command_1 = MoveCommand(game, 1, "R")
print(move_command_1.execute())  # Player 1 moves right

# Player 2 moves
move_command_2 = MoveCommand(game, 2, "D")
print(move_command_2.execute())  # Player 2 moves down

"""
Explanation of Patterns:
Observer Pattern:

Player class implements PlayerObserver to receive updates about the game state (score changes, game over).
Singleton Pattern:

The SnakeGame class uses the singleton pattern to ensure only one instance of the game is running.
Command Pattern:

MoveCommand handles player movements, allowing commands to be executed independently for each player.
Multiplayer Support:

The game now supports multiple players, each having their own snake.
The move method handles player-specific movements, checking for collisions and score updates.

"""
