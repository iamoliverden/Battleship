import random


class Player:
    def __init__(self, human=True):
        if human:  # Human
            self.ships = [Ship(3), Ship(2), Ship(2), Ship(1), Ship(1), Ship(1), Ship(1)]
            self.previous_guesses = set()
            self.hits = set()
        else:  # Computer
            self.ships = [Ship(3), Ship(2), Ship(2), Ship(1), Ship(1), Ship(1), Ship(1)]
            self.previous_guesses = set()
            self.hits = set()


class Dots:
    def __init__(self, human=True):
        self.dots = None
        self.ship = None
        if human:  # human
            self.taken_dots = []
            self.ships = []
        else:  # computer
            self.taken_dots = []
            self.ships = []
    def update_dots(self, ship, human=True): # Ship(human=True/False).return_coordinates()
        self.ship = ship
        self.dots = ship.return_coordinates()


        if human:
            self.taken_dots.append(self.dots)
            self.taken_dots.append(self.ships)
        else:
            self.taken_dots.append(self.dots)
            self.taken_dots.append(self.ships)
            






class Ship:
    def __init__(self, size, human=True):
        if human:
            self.size = size
            self.coordinates = []
            self.taken_dots= Dots(human=True).taken_dots
        else:
            self.size = size
            self.coordinates = []
            self.taken_dots = Dots(human=False).taken_dots

    def generate_random_coordinates(self):
        while True:
            orientation = random.choice(["horizontal", "vertical"])
            start_row = random.randint(0, len(self.size) - 1)
            start_col = random.randint(0, len(self.size) - 1)

            valid_coordinates = True

            for i in range(self.size):
                row = start_row + i if orientation == "vertical" else start_row
                col = start_col + i if orientation == "horizontal" else start_col
                candidate_coordinates = (row, col)

                for pair in self.coordinates: #flatten the list to compare
                    if (    pair not in [cell for ship in self.taken_dots for cell in ship]
                            and row < len(self.size)
                            and col < len(self.size)
                            and self.size[row][col] == 0
                            and all(
                                self.size[row + dr][col + dc] == 0
                                for dr in range(-1, 2)
                                for dc in range(-1, 2)
                                if 0 <= row + dr < len(self.size) and 0 <= col + dc < len(self.size)
                    )
                    ):
                        self.coordinates.append((row, col))
                    else:
                        valid_coordinates = False
                        break

    def return_coordinates(self):
        return self.coordinates
        




class Board:
    def __init__(self):
        self.size = board_size
        self.board = [["O"] * self.size for _ in range(self.size)]

    def print_board(self):
        print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i, row in enumerate(self.board):
            print(f"{i + 1} | {' | '.join(map(str, row))} |")


class Map:
    def __init__(self, player):
        self.board = Board().board
        self.player = player  # Human or Computer
        self.coordinates = []

    def place_ships(self):
        for ship in self.player.ships:
            self.seek_location()
            for coordinate in self.coordinates:
                self.board[coordinate[0]][coordinate[1]] = '■'
        return self.board


class PlayerInput:
    def __init__(self, player):
        self.guess_col = None
        self.guess_row = None
        self.player = player  # Human or Computer
        self.size = Board().size  # 6
        self.board = Map(player).place_ships()
        self.previous_guesses = player.previous_guesses  # set()
        self.ship_coordinates = Map(player).coordinates  # [(0, 0), (0, 1), (0, 2)]
        self.flat_ship_coordinates = [cell for ship in self.ship_coordinates for cell in ship]
        self.hits = player.hits  # set()

    def take_input(self):
        self.guess_col = int(input("Guess Col (1-6): ")) - 1
        self.guess_row = int(input("Guess Row (1-6): ")) - 1

    def is_valid_guess(self, guess):
        return guess[0] in range(self.size) and guess[1] in range(self.size) and guess not in self.previous_guesses

    def is_hit(self, guess, ship_coordinates, human=True):
        if human:
            # go through each ship in ship_coordinates (embedded lists) and return the ship that contains the guess
            for ship in ship_coordinates:
                if guess in ship:
                    self.board[self.guess_row][self.guess_col] = "X"
                    print(f"You hit a {len(ship)}! Arrr!")
                    # add guess to previous_guesses
                    return True
                else:
                    self.board[self.guess_row][self.guess_col] = "T"
                    print("You missed! Blimey!")
                    self.previous_guesses.add(guess)
                    return False
        else:
            # go through each ship in ship_coordinates (embedded lists) and return the ship that contains the guess
            for ship in ship_coordinates:
                if guess in ship:
                    self.board[self.guess_row][self.guess_col] = "X"
                    print(f"Computer hit your {len(ship)} mast ship! Oh no!")
                    # add guess to previous_guesses
                    return True
                else:
                    self.board[self.guess_row][self.guess_col] = "T"
                    print("Computer missed! Hip Hip!")
                    self.previous_guesses.add(guess)
                    return False

    def fleet_sunk(self, hits, flat_ship_coordinates, human=True):
        if human:
            if hits.difference(flat_ship_coordinates) == 0:
                print("You sunk all the ships! Aye, Aye, Captain!")
                return True
            else:
                print("You still have enemy ships to sink. ")
                return False
        else:
            if hits.difference(flat_ship_coordinates) == 0:
                print("Computer sunk all your ships! You lost!")
                return True
            else:
                print("Computer still has enemy ships to sink. Keep playing!")
                return False


class Game:
    def __init__(self, debug=True):
        self.debug = debug
        self.human_player = Player(human=True)
        self.computer_player = Player(human=False)
        self.human_ships_coordinates = Map(self.human_player).coordinates
        self.computer_ships_coordinates = Map(self.computer_player).coordinates
        self.process_input_human = PlayerInput(self.human_player)
        self.process_input_computer = PlayerInput(self.computer_player)
        self.human_board = self.process_input_human.board
        self.computer_board = self.process_input_computer.board

    def debug_print_ships(self):
        if self.debug:
            print("Player Ships:")
            for ship in self.human_ships_coordinates:
                print(f"Size: {ship.size}, Coordinates: {ship.coordinates}")
            print("\nComputer Ships:")
            for ship in self.computer_ships_coordinates:
                print(f"Size: {ship.size}, Coordinates: {ship.coordinates}")

    def play(self):
        print("Welcome to Battleship!")

        # Debugging: Print initial ship positions
        self.debug_print_ships()

        while True:
            # Human's turn
            while True:
                try:
                    print(Game().human_board)
                    Game().process_input_human.take_input()
                    guess = (self.process_input_human.guess_row, self.process_input_human.guess_col)

                    if (self.process_input_human.is_valid_guess(guess) and
                            not self.process_input_human.is_hit(guess, self.human_ships_coordinates, human=True)):
                        break
                    else:
                        print("Invalid guess. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            self.human_player.previous_guesses.add(guess)
            self.human_player.hits.add(guess)

            # check if hit or miss
            self.process_input_human.is_hit(guess, self.process_input_human.ship_coordinates, human=True)
            # print the board
            print(self.human_board)
            # check if the fleet is sunk
            if self.process_input_human.fleet_sunk(self.process_input_human.hits,
                                                   self.process_input_human.flat_ship_coordinates, human=True):
                break

            # Computer's turn
            while True:
                print(self.computer_board)
                guess = (random.randint(0, self.computer_board.size - 1),
                         random.randint(0, self.computer_board.size - 1))

                if not (self.process_input_computer.is_hit(guess,
                                                           self.computer_ships_coordinates, human=False)
                        and guess not in self.process_input_computer.previous_guesses):
                    break

            self.computer_player.previous_guesses.add(guess)
            self.computer_player.hits.add(guess)

            # check if hit or miss
            self.process_input_computer.is_hit(guess, self.process_input_computer.ship_coordinates, human=False)
            # print the board
            self.computer_board.print_board()
            # check if the fleet is sunk
            if self.process_input_computer.fleet_sunk(self.process_input_computer.hits,
                                                      self.process_input_computer.flat_ship_coordinates, human=False):
                break

            # Debugging: Print ship positions after each round
            self.debug_print_ships()


if __name__ == "__main__":
    board_size = 6
    game = Game(debug=True)
    game.play()

Board().print_board()
