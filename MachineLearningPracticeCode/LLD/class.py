# Classes - Structural blueprint for creating objects, 
# Object - Instance of a class
# Encapsulation - Bundling data and methods
# Inheritance - Deriving new classes from existing ones
# Polymorphism - Ability to take many forms
# Abstraction - Hiding implementation details

class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def start_engine(self):
        return f"{self.make} {self.model} engine started."

    def stop_engine(self):
        return f"{self.make} {self.model} engine stopped."
    

class Tiktoker:
    def __init__(self, name, followers):
        self.name = name
        self.followers = followers

    def create_content(self):
        return f"{self.name} is creating content."

    def gain_followers(self, count):
        self.followers += count
        return f"{self.name} gained {count} followers. Total: {self.followers}"
    
# call Tiktoker
tiktoker1 = Tiktoker("Alice", 1000)
print(tiktoker1.create_content())


class Tic_Tac_Toe:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def print_board(self):
        for row in self.board:
            print("|".join(row))
            print("-" * 5)

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            if self.check_winner():
                print(f"Player {self.current_player} wins!")
                return True
            self.current_player = "O" if self.current_player == "X" else "X"
        else:
            print("Invalid move. Try again.")
        return False

    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != " ":
                return True
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                return True
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return True
        return False

# Tic-Tac-Toe game example
game = Tic_Tac_Toe()
game.print_board()