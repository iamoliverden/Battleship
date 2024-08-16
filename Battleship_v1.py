<<<<<<< HEAD
<<<<<<< HEAD
'''
# create the board class
Battleship. Game.

designed and written by Oliver Den
Toronto, 2023

To terminate the game at any moment, enter 912, 912 as coordinates.
'''


# create the board class

class Board:
    def __init__(self, board_size=6, human=True):
        if human:
            self.size = board_size
            self.board = [["O"] * self.size for _ in range(self.size)]
        else:
            self.size = board_size
            self.board = [["O"] * self.size for _ in range(self.size)]

    def print_board(self):
        print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i, row in enumerate(self.board):
            print(f"{i + 1} | {' | '.join(map(str, row))} |")


# Create an instance of the Board class

clean_board_human = Board(board_size=6, human=True)
clean_board_computer = Board(board_size=6, human=False)
# %%
# create a ship class

import random


class Ship:
    def __init__(self, size, human=True):
        if human:
            self.board_size = Board().size
            self.size = size
            self.coordinates = []
            self.taken_dots = dots_human.taken_dots
            self.neighbouring_dots = dots_human.neighboring_dots
        else:
            self.board_size = Board().size
            self.size = size
            self.coordinates = []
            self.taken_dots = dots_computer.taken_dots
            self.neighbouring_dots = dots_computer.neighboring_dots

    def generate_random_coordinates(self):
        while True:
            orientation = random.choice(["horizontal", "vertical"])
            start_row = random.randint(0, self.board_size)
            start_col = random.randint(0, self.board_size)

            valid_coordinates = True
            candidate_coordinates = []

            for i in range(self.size):
                row = start_row + i if orientation == "vertical" else start_row
                col = start_col + i if orientation == "horizontal" else start_col

                # Check if the coordinates are within the valid range
                if not (0 <= row < self.board_size and 0 <= col < self.board_size):
                    valid_coordinates = False
                    break

                candidate_coordinates.append((row, col))

            if any(coord in [cell for ship in self.taken_dots for cell in ship] for coord in
                   candidate_coordinates) or any(
                    coord in [cell for neighbor in self.neighbouring_dots for cell in neighbor] for coord in
                    candidate_coordinates):
                valid_coordinates = False
            else:
                self.coordinates.extend(candidate_coordinates)
                break  # Exit the while loop if valid coordinates are found

        if not valid_coordinates:
            # If checks fail, start over with an empty list of candidates
            self.coordinates = []
            self.generate_random_coordinates()

    def return_coordinates(self):
        return self.coordinates


# %%
# create a ship catalogue

class CatalogueOfShips:
    ship_masts = [3, 2, 2, 1, 1, 1, 1]

    def __init__(self, human=True):
        if human:
            self.ship_objects = []
        else:
            self.ship_objects = []

    def return_masts(self):
        return self.ship_masts


# fixed ship lists

human_ship_catalogue = CatalogueOfShips(human=True)
computer_ship_catalogue = CatalogueOfShips(human=False)


# %%
# create the player class - final version

class Player:
    def __init__(self, human=True):
        if human:  # Human
            self.previous_guesses = []
            self.hits = []
        else:  # Computer
            self.previous_guesses = []
            self.hits = []


# Create an instance of the Player class

human_player = Player(human=True)
computer_player = Player(human=False)


# %%
# create class Dots to store the coordinates of the ships and the dots that have been taken
class Dots:
    def __init__(self, human=True):
        if human:
            self.taken_dots = []
            self.neighboring_dots = []
        else:
            self.taken_dots = []
            self.neighboring_dots = []

    def update_dots_taken(self, coordinates):
        self.taken_dots = coordinates

    def update_ships(self, ships):
        self.ships = ships


# Create an instance of the Dots class

dots_human = Dots(human=True)
dots_computer = Dots(human=False)


# %%
# create a class that generates ships

class ShipGenerator:
    def __init__(self, human=True):
        # Initialize with a list of masts from CatalogueOfShips
        self.masts = CatalogueOfShips().return_masts()

        # Use self.human to track whether it's a human ship generator
        self.human = human

    def generate_list_of_ships(self):
        for mast in self.masts:
            # Create a Ship object based on the mast
            self.ship = Ship(mast, human=self.human)

            # Generate random coordinates for the ship
            self.ship.generate_random_coordinates()
            self.ship_coordinates_return = self.ship.return_coordinates()

            # Add the ship to the appropriate ship_catalogue
            if self.human:
                human_ship_catalogue.ship_objects.append(self.ship)
                dots_human.taken_dots.append(self.ship_coordinates_return)
            else:
                computer_ship_catalogue.ship_objects.append(self.ship)
                dots_computer.taken_dots.append(self.ship_coordinates_return)

            # define the list of neighbouring dots
            if self.human:
                neighbors = []
                for x, y in self.ship_coordinates_return:
                    neighbors.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

                # Remove diagonally attached neighbors
                neighbors = [(x, y) for x, y in neighbors if (x, y) not in self.ship_coordinates_return]
                dots_human.neighboring_dots.append(neighbors)
            else:
                neighbors = []
                for x, y in self.ship_coordinates_return:
                    neighbors.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

                # Remove diagonally attached neighbors
                neighbors = [(x, y) for x, y in neighbors if (x, y) not in self.ship_coordinates_return]
                dots_computer.neighboring_dots.append(neighbors)


# initialize the ship generator for human

gen = ShipGenerator(human=True)
gen.generate_list_of_ships()

# and computer

gen = ShipGenerator(human=False)
gen.generate_list_of_ships()


# %%
# create a class that allocates ships to the board

class ShipAllocator:
    def __init__(self, human=True):
        self.human = human
        self.human_board_start = clean_board_human
        self.computer_board_start = clean_board_computer

    def allocate_ships(self):
        if self.human:
            for ship in human_ship_catalogue.ship_objects:
                for row, col in ship.coordinates:
                    self.human_board_start.board[row][col] = '■'
            else:
                for ship in computer_ship_catalogue.ship_objects:
                    for row, col in ship.coordinates:
                        self.computer_board_start.board[row][col] = '■'


# Create an instance of the ShipAllocator class

ship_allocator_human = ShipAllocator(human=True)
ship_allocator_human.allocate_ships()
ship_allocator_computer = ShipAllocator(human=False)
ship_allocator_computer.allocate_ships()

# create variables

human_board_next = ShipAllocator(human=True).human_board_start
computer_board_next = ShipAllocator(human=False).computer_board_start


# %%
# create a class that creates ship lists for the human and computer

class FreeRadicals:
    def active_human_ships(self):
        self.active_human_ships = [coordinate for sublist in dots_human.taken_dots for coordinate in sublist]
        return self.active_human_ships

    def active_computer_ships(self):
        self.active_computer_ships = [coordinate for sublist in dots_computer.taken_dots for coordinate in sublist]
        return self.active_computer_ships


# Creating an instance of the class
free_radicals_instance = FreeRadicals()

# Calling the instance methods to get the lists
active_human_ships = free_radicals_instance.active_human_ships()
active_computer_ships = free_radicals_instance.active_computer_ships()


# %%
# create a class for the player

class PlayerInput:

    def __init__(self, human=True):
        if human:
            self.player = human_player  # Human
            self.board = clean_board_human
            self.size_of_the_board = self.board.size
            self.computer_ship_coordinates = active_computer_ships  # list of ship objects

        else:
            self.player = human_player  # Computer
            self.board = clean_board_computer
            self.size_of_the_board = self.board.size
            self.human_ship_coordinates = active_human_ships  # list of ship objects

    def take_input(self):
        while True:
            try:
                self.guess_row = int(input("Guess Row (1-6): ")) - 1
                self.guess_col = int(input("Guess Col (1-6): ")) - 1
                self.guess = (self.guess_row, self.guess_col)

                # Check if the secret code was entered
                if (self.guess_col == 911) and (self.guess_row == 911):
                    print("You have entered the secret code to terminate the game. Shame!")
                    return self.guess, True  # secret code entered

                if (
                        0 <= self.guess_row <= 5
                        and 0 <= self.guess_col <= 5
                        and self.guess not in human_player.previous_guesses
                ):
                    return self.guess, False  # secret code not entered
                else:
                    print("Invalid input or already guessed. Row and column must be between 1 and 6.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def take_computer_guess(self):
        while True:
            self.guess = (random.randint(0, self.size_of_the_board - 1), random.randint(0, self.size_of_the_board - 1))

            if len(computer_player.previous_guesses) <= 36:
                if self.guess not in computer_player.previous_guesses:  # Check if the guess is not in previous guesses
                    return self.guess  # to avoid the endless cycle of the same guess
            else:
                break

    def is_hit(self, guess, human=True):  ## ship_coordinates = human/computer ship coordinates
        if human:
            if guess in active_computer_ships:
                self.length = [len(sublist) for sublist in dots_computer.taken_dots if guess in sublist]
                human_player.previous_guesses.append(guess)
                human_player.hits.append(guess)
                return True, f"You hit a {self.length[0]} mast ship! Arrr!"
            else:
                human_player.previous_guesses.append(guess)
                return False, "You missed! Blimey!"

        else:
            # go through each ship in ship_coordinates (embedded lists) and return the ship that contains the guess
            if guess in active_human_ships:
                self.length = [len(sublist) for sublist in dots_human.taken_dots if guess in sublist]
                computer_player.previous_guesses.append(guess)
                computer_player.hits.append(guess)
                return True, f"Computer hit your {self.length[0]} mast ship! Oh no!"
            else:
                computer_player.previous_guesses.append(guess)
                return False, "Computer missed! Hip Hip!"

    def fleet_sunk(self, human=True):
        if human:
            if sorted(human_player.hits) == sorted(active_computer_ships):
                return True, "You sank all the ships! Aye, Aye, Captain!"
            else:
                return False, "You still have enemy ships to sink. Keep playing!"
        else:
            if sorted(computer_player.hits) == sorted(active_human_ships):
                return True, "Computer sank all your ships! You lost!"
            else:
                return False, "Computer still has enemy ships to sink. Keep playing!"


# initiate the class for human player and computer player

human_input = PlayerInput(human=True)
computer_input = PlayerInput(human=False)


# %%
class UpdatedBoard:
    def __init__(self, human=True):
        self.previous_guesses_human = human_player.previous_guesses
        self.board_human = human_board_next
        self.hits_human = human_player.hits
        self.previous_guesses_computer = computer_player.previous_guesses
        self.board_computer = computer_board_next
        self.hits_computer = computer_player.hits

    def update_board(self, human=True):
        if human:  # updated board computer
            for guess in self.previous_guesses_human:  # previous guesses of computer
                self.board_computer.board[guess[0]][guess[1]] = 'T'  # apply to human board
            for hit in self.hits_human:
                self.board_computer.board[hit[0]][hit[1]] = 'X'
            return self.board_computer
        else:  # update board human
            for guess in self.previous_guesses_computer:  # previous guesses of computer
                self.board_human.board[guess[0]][guess[1]] = 'T'  # apply to human board
            for hit in self.hits_computer:
                self.board_human.board[hit[0]][hit[1]] = 'X'
            return self.board_human


updated_board_1 = UpdatedBoard()


# %%
class GameTester:
    def __init__(self, human_input, human_player, active_computer_ships,
                 active_human_ships, computer_input, computer_player,
                 updated_board_1, dots_human, dots_computer):
        self.human_input = human_input
        self.human_player = human_player
        self.active_computer_ships = active_computer_ships
        self.ships_computer_1 = GameTester.ships_computer()
        self.active_human_ships = active_human_ships
        self.ships_human_1 = GameTester.ships_human()
        self.computer_input = computer_input
        self.computer_player = computer_player
        self.updated_board_1 = updated_board_1
        self.dots_human = dots_human
        self.dots_computer = dots_computer

    @staticmethod
    def ships_human():
        ships = []
        for ship in human_ship_catalogue.ship_objects:
            ships.append(ship.coordinates)
        return ships

    @staticmethod
    def ships_computer():
        ships = []
        for ship in computer_ship_catalogue.ship_objects:
            ships.append(ship.coordinates)
        return ships

    # Assign the result of the static methods to the corresponding instance variables
    ships_human_1 = ships_human()
    ships_computer_1 = ships_computer()

    def test_function_human(self):
        user_input, another_value = self.human_input.take_input()
        print("User input: ", user_input)
        print("Previous guesses: ", self.human_player.previous_guesses)
        user_is_hit = self.human_input.is_hit(user_input, human=True)
        print("Active computer ship coordinates: ", self.active_computer_ships)
        print("Ships computer: ", self.ships_computer_1)
        print("Neighbouring cells computer: ", self.dots_computer.neighboring_dots)
        print("User is hit: ", user_is_hit)
        user_hits = self.human_player.hits
        print("User hits:", user_hits)
        user_fleet_sunk = self.human_input.fleet_sunk(human=True)
        print("Is fleet sunk: ", user_fleet_sunk)
        print("Show Computer Board after User Hit")
        self.updated_board_1.update_board(
            human=True)  # here reverse - it will update the board of computer because the human strikes
        self.updated_board_1.board_computer.print_board()

    def test_function_computer(self):
        computer_guess = self.computer_input.take_computer_guess()
        print("Computer guess: ", computer_guess)
        print("Previous guesses: ", self.computer_player.previous_guesses)
        computer_is_hit = self.computer_input.is_hit(computer_guess, human=False)
        print("Active human ship coordinates: ", self.active_human_ships)
        print("Ships human: ", self.ships_human_1)
        print("Neighbouring cells human: ", self.dots_human.neighboring_dots)
        print("Computer is hit: ", computer_is_hit)
        computer_hits = self.computer_player.hits
        print("Computer hits:", computer_hits)
        computer_fleet_sunk = self.computer_input.fleet_sunk(human=False)
        print("Is fleet sunk: ", computer_fleet_sunk)
        print("Show User Board after Computer Hit")
        self.updated_board_1.update_board(human=False)  # it will update the board of human because computer strikes
        self.updated_board_1.board_human.print_board()


# %%
# Now, instantiate GameTester
game_tester_instance = GameTester(human_input, human_player, active_computer_ships,
                                  active_human_ships, computer_input, computer_player,
                                  updated_board_1, dots_human, dots_computer)


# %%
# Call your test functions
# game_tester_instance.test_function_human()
# game_tester_instance.test_function_computer()
# %%
# create a class for the game
class Game:
    def __init__(self):
        self.human_player = human_player
        self.computer_player = computer_player
        self.human_input = human_input
        self.computer_input = computer_input
        self.active_human_ships = active_human_ships
        self.active_computer_ships = active_computer_ships
        self.human_board_start = ship_allocator_human.human_board_start
        self.updated_board_1 = updated_board_1

    def play(self, print_completed_boards=False):

        print("Welcome to Battleship!")
        print("----------------------")
        print("To exit the game at any moment, enter row 912 and col 912.")

        while True:
            # Human's turn
            while True:
                print(" ")
                print("Human's turn!")

                guess, secret_code_entered = self.human_input.take_input()

                # Check if the secret code was entered
                if secret_code_entered:
                    print("Secret code entered! Game over.")
                    return

                self.human_input.is_hit(guess, human=True)
                self.updated_board_1.update_board(human=True)
                print("Computer's Board (Human sees his strikes):")
                self.updated_board_1.board_computer.print_board()
                print(" ")
                self.human_input.fleet_sunk(human=True)[1]

                if self.human_input.fleet_sunk(human=True)[0]:
                    break
                else:
                    break

            # Check if the human fleet is sunk before the computer's turn
            if self.human_input.fleet_sunk(human=True)[0]:
                print("Computer fleet is sunk! Game over.")
                break  # Exit the game loop

            # Computer's turn
            while True:
                print("Computer's turn!")
                guess = self.computer_input.take_computer_guess()
                self.computer_input.is_hit(guess, human=False)
                self.updated_board_1.update_board(human=False)

                if print_completed_boards == True:
                    print("Human's board (shows Computer's hits):")
                    self.updated_board_1.board_human.print_board()
                    print(" ")
                else:
                    pass

                self.computer_input.fleet_sunk(human=False)[1]

                if self.computer_input.fleet_sunk(human=False)[0]:
                    break
                else:
                    break

            # Check if the computer fleet is sunk before the human's turn
            if self.computer_input.fleet_sunk(human=False)[0]:
                print("Human fleet is sunk! Game over.")
                break  # Exit the game loop


# %%
# run the game

if __name__ == "__main__":
    game = Game()
    game.play(print_completed_boards=True)
=======
'''
# create the board class
Battleship. Game.

designed and written by Oliver Den
Toronto, 2023

To terminate the game at any moment, enter 912, 912 as coordinates.
'''


# create the board class

class Board:
    def __init__(self, board_size=6, human=True):
        if human:
            self.size = board_size
            self.board = [["O"] * self.size for _ in range(self.size)]
        else:
            self.size = board_size
            self.board = [["O"] * self.size for _ in range(self.size)]

    def print_board(self):
        print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i, row in enumerate(self.board):
            print(f"{i + 1} | {' | '.join(map(str, row))} |")


# Create an instance of the Board class

clean_board_human = Board(board_size=6, human=True)
clean_board_computer = Board(board_size=6, human=False)
# %%
# create a ship class

import random


class Ship:
    def __init__(self, size, human=True):
        if human:
            self.board_size = Board().size
            self.size = size
            self.coordinates = []
            self.taken_dots = dots_human.taken_dots
            self.neighbouring_dots = dots_human.neighboring_dots
        else:
            self.board_size = Board().size
            self.size = size
            self.coordinates = []
            self.taken_dots = dots_computer.taken_dots
            self.neighbouring_dots = dots_computer.neighboring_dots

    def generate_random_coordinates(self):
        while True:
            orientation = random.choice(["horizontal", "vertical"])
            start_row = random.randint(0, self.board_size)
            start_col = random.randint(0, self.board_size)

            valid_coordinates = True
            candidate_coordinates = []

            for i in range(self.size):
                row = start_row + i if orientation == "vertical" else start_row
                col = start_col + i if orientation == "horizontal" else start_col

                # Check if the coordinates are within the valid range
                if not (0 <= row < self.board_size and 0 <= col < self.board_size):
                    valid_coordinates = False
                    break

                candidate_coordinates.append((row, col))

            if any(coord in [cell for ship in self.taken_dots for cell in ship] for coord in
                   candidate_coordinates) or any(
                    coord in [cell for neighbor in self.neighbouring_dots for cell in neighbor] for coord in
                    candidate_coordinates):
                valid_coordinates = False
            else:
                self.coordinates.extend(candidate_coordinates)
                break  # Exit the while loop if valid coordinates are found

        if not valid_coordinates:
            # If checks fail, start over with an empty list of candidates
            self.coordinates = []
            self.generate_random_coordinates()

    def return_coordinates(self):
        return self.coordinates


# %%
# create a ship catalogue

class CatalogueOfShips:
    ship_masts = [3, 2, 2, 1, 1, 1, 1]

    def __init__(self, human=True):
        if human:
            self.ship_objects = []
        else:
            self.ship_objects = []

    def return_masts(self):
        return self.ship_masts


# fixed ship lists

human_ship_catalogue = CatalogueOfShips(human=True)
computer_ship_catalogue = CatalogueOfShips(human=False)


# %%
# create the player class - final version

class Player:
    def __init__(self, human=True):
        if human:  # Human
            self.previous_guesses = []
            self.hits = []
        else:  # Computer
            self.previous_guesses = []
            self.hits = []


# Create an instance of the Player class

human_player = Player(human=True)
computer_player = Player(human=False)


# %%
# create class Dots to store the coordinates of the ships and the dots that have been taken
class Dots:
    def __init__(self, human=True):
        if human:
            self.taken_dots = []
            self.neighboring_dots = []
        else:
            self.taken_dots = []
            self.neighboring_dots = []

    def update_dots_taken(self, coordinates):
        self.taken_dots = coordinates

    def update_ships(self, ships):
        self.ships = ships


# Create an instance of the Dots class

dots_human = Dots(human=True)
dots_computer = Dots(human=False)


# %%
# create a class that generates ships

class ShipGenerator:
    def __init__(self, human=True):
        # Initialize with a list of masts from CatalogueOfShips
        self.masts = CatalogueOfShips().return_masts()

        # Use self.human to track whether it's a human ship generator
        self.human = human

    def generate_list_of_ships(self):
        for mast in self.masts:
            # Create a Ship object based on the mast
            self.ship = Ship(mast, human=self.human)

            # Generate random coordinates for the ship
            self.ship.generate_random_coordinates()
            self.ship_coordinates_return = self.ship.return_coordinates()

            # Add the ship to the appropriate ship_catalogue
            if self.human:
                human_ship_catalogue.ship_objects.append(self.ship)
                dots_human.taken_dots.append(self.ship_coordinates_return)
            else:
                computer_ship_catalogue.ship_objects.append(self.ship)
                dots_computer.taken_dots.append(self.ship_coordinates_return)

            # define the list of neighbouring dots
            if self.human:
                neighbors = []
                for x, y in self.ship_coordinates_return:
                    neighbors.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

                # Remove diagonally attached neighbors
                neighbors = [(x, y) for x, y in neighbors if (x, y) not in self.ship_coordinates_return]
                dots_human.neighboring_dots.append(neighbors)
            else:
                neighbors = []
                for x, y in self.ship_coordinates_return:
                    neighbors.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

                # Remove diagonally attached neighbors
                neighbors = [(x, y) for x, y in neighbors if (x, y) not in self.ship_coordinates_return]
                dots_computer.neighboring_dots.append(neighbors)


# initialize the ship generator for human

gen = ShipGenerator(human=True)
gen.generate_list_of_ships()

# and computer

gen = ShipGenerator(human=False)
gen.generate_list_of_ships()


# %%
# create a class that allocates ships to the board

class ShipAllocator:
    def __init__(self, human=True):
        self.human = human
        self.human_board_start = clean_board_human
        self.computer_board_start = clean_board_computer

    def allocate_ships(self):
        if self.human:
            for ship in human_ship_catalogue.ship_objects:
                for row, col in ship.coordinates:
                    self.human_board_start.board[row][col] = '■'
            else:
                for ship in computer_ship_catalogue.ship_objects:
                    for row, col in ship.coordinates:
                        self.computer_board_start.board[row][col] = '■'


# Create an instance of the ShipAllocator class

ship_allocator_human = ShipAllocator(human=True)
ship_allocator_human.allocate_ships()
ship_allocator_computer = ShipAllocator(human=False)
ship_allocator_computer.allocate_ships()

# create variables

human_board_next = ShipAllocator(human=True).human_board_start
computer_board_next = ShipAllocator(human=False).computer_board_start


# %%
# create a class that creates ship lists for the human and computer

class FreeRadicals:
    def active_human_ships(self):
        self.active_human_ships = [coordinate for sublist in dots_human.taken_dots for coordinate in sublist]
        return self.active_human_ships

    def active_computer_ships(self):
        self.active_computer_ships = [coordinate for sublist in dots_computer.taken_dots for coordinate in sublist]
        return self.active_computer_ships


# Creating an instance of the class
free_radicals_instance = FreeRadicals()

# Calling the instance methods to get the lists
active_human_ships = free_radicals_instance.active_human_ships()
active_computer_ships = free_radicals_instance.active_computer_ships()


# %%
# create a class for the player

class PlayerInput:

    def __init__(self, human=True):
        if human:
            self.player = human_player  # Human
            self.board = clean_board_human
            self.size_of_the_board = self.board.size
            self.computer_ship_coordinates = active_computer_ships  # list of ship objects

        else:
            self.player = human_player  # Computer
            self.board = clean_board_computer
            self.size_of_the_board = self.board.size
            self.human_ship_coordinates = active_human_ships  # list of ship objects

    def take_input(self):
        while True:
            try:
                self.guess_row = int(input("Guess Row (1-6): ")) - 1
                self.guess_col = int(input("Guess Col (1-6): ")) - 1
                self.guess = (self.guess_row, self.guess_col)

                # Check if the secret code was entered
                if (self.guess_col == 911) and (self.guess_row == 911):
                    print("You have entered the secret code to terminate the game. Shame!")
                    return self.guess, True  # secret code entered

                if (
                        0 <= self.guess_row <= 5
                        and 0 <= self.guess_col <= 5
                        and self.guess not in human_player.previous_guesses
                ):
                    return self.guess, False  # secret code not entered
                else:
                    print("Invalid input or already guessed. Row and column must be between 1 and 6.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def take_computer_guess(self):
        while True:
            self.guess = (random.randint(0, self.size_of_the_board - 1), random.randint(0, self.size_of_the_board - 1))

            if len(computer_player.previous_guesses) <= 36:
                if self.guess not in computer_player.previous_guesses:  # Check if the guess is not in previous guesses
                    return self.guess  # to avoid the endless cycle of the same guess
            else:
                break

    def is_hit(self, guess, human=True):  ## ship_coordinates = human/computer ship coordinates
        if human:
            if guess in active_computer_ships:
                self.length = [len(sublist) for sublist in dots_computer.taken_dots if guess in sublist]
                human_player.previous_guesses.append(guess)
                human_player.hits.append(guess)
                return True, f"You hit a {self.length[0]} mast ship! Arrr!"
            else:
                human_player.previous_guesses.append(guess)
                return False, "You missed! Blimey!"

        else:
            # go through each ship in ship_coordinates (embedded lists) and return the ship that contains the guess
            if guess in active_human_ships:
                self.length = [len(sublist) for sublist in dots_human.taken_dots if guess in sublist]
                computer_player.previous_guesses.append(guess)
                computer_player.hits.append(guess)
                return True, f"Computer hit your {self.length[0]} mast ship! Oh no!"
            else:
                computer_player.previous_guesses.append(guess)
                return False, "Computer missed! Hip Hip!"

    def fleet_sunk(self, human=True):
        if human:
            if sorted(human_player.hits) == sorted(active_computer_ships):
                return True, "You sank all the ships! Aye, Aye, Captain!"
            else:
                return False, "You still have enemy ships to sink. Keep playing!"
        else:
            if sorted(computer_player.hits) == sorted(active_human_ships):
                return True, "Computer sank all your ships! You lost!"
            else:
                return False, "Computer still has enemy ships to sink. Keep playing!"


# initiate the class for human player and computer player

human_input = PlayerInput(human=True)
computer_input = PlayerInput(human=False)


# %%
class UpdatedBoard:
    def __init__(self, human=True):
        self.previous_guesses_human = human_player.previous_guesses
        self.board_human = human_board_next
        self.hits_human = human_player.hits
        self.previous_guesses_computer = computer_player.previous_guesses
        self.board_computer = computer_board_next
        self.hits_computer = computer_player.hits

    def update_board(self, human=True):
        if human:  # updated board computer
            for guess in self.previous_guesses_human:  # previous guesses of computer
                self.board_computer.board[guess[0]][guess[1]] = 'T'  # apply to human board
            for hit in self.hits_human:
                self.board_computer.board[hit[0]][hit[1]] = 'X'
            return self.board_computer
        else:  # update board human
            for guess in self.previous_guesses_computer:  # previous guesses of computer
                self.board_human.board[guess[0]][guess[1]] = 'T'  # apply to human board
            for hit in self.hits_computer:
                self.board_human.board[hit[0]][hit[1]] = 'X'
            return self.board_human


updated_board_1 = UpdatedBoard()


# %%
class GameTester:
    def __init__(self, human_input, human_player, active_computer_ships,
                 active_human_ships, computer_input, computer_player,
                 updated_board_1, dots_human, dots_computer):
        self.human_input = human_input
        self.human_player = human_player
        self.active_computer_ships = active_computer_ships
        self.ships_computer_1 = GameTester.ships_computer()
        self.active_human_ships = active_human_ships
        self.ships_human_1 = GameTester.ships_human()
        self.computer_input = computer_input
        self.computer_player = computer_player
        self.updated_board_1 = updated_board_1
        self.dots_human = dots_human
        self.dots_computer = dots_computer

    @staticmethod
    def ships_human():
        ships = []
        for ship in human_ship_catalogue.ship_objects:
            ships.append(ship.coordinates)
        return ships

    @staticmethod
    def ships_computer():
        ships = []
        for ship in computer_ship_catalogue.ship_objects:
            ships.append(ship.coordinates)
        return ships

    # Assign the result of the static methods to the corresponding instance variables
    ships_human_1 = ships_human()
    ships_computer_1 = ships_computer()

    def test_function_human(self):
        user_input, another_value = self.human_input.take_input()
        print("User input: ", user_input)
        print("Previous guesses: ", self.human_player.previous_guesses)
        user_is_hit = self.human_input.is_hit(user_input, human=True)
        print("Active computer ship coordinates: ", self.active_computer_ships)
        print("Ships computer: ", self.ships_computer_1)
        print("Neighbouring cells computer: ", self.dots_computer.neighboring_dots)
        print("User is hit: ", user_is_hit)
        user_hits = self.human_player.hits
        print("User hits:", user_hits)
        user_fleet_sunk = self.human_input.fleet_sunk(human=True)
        print("Is fleet sunk: ", user_fleet_sunk)
        print("Show Computer Board after User Hit")
        self.updated_board_1.update_board(
            human=True)  # here reverse - it will update the board of computer because the human strikes
        self.updated_board_1.board_computer.print_board()

    def test_function_computer(self):
        computer_guess = self.computer_input.take_computer_guess()
        print("Computer guess: ", computer_guess)
        print("Previous guesses: ", self.computer_player.previous_guesses)
        computer_is_hit = self.computer_input.is_hit(computer_guess, human=False)
        print("Active human ship coordinates: ", self.active_human_ships)
        print("Ships human: ", self.ships_human_1)
        print("Neighbouring cells human: ", self.dots_human.neighboring_dots)
        print("Computer is hit: ", computer_is_hit)
        computer_hits = self.computer_player.hits
        print("Computer hits:", computer_hits)
        computer_fleet_sunk = self.computer_input.fleet_sunk(human=False)
        print("Is fleet sunk: ", computer_fleet_sunk)
        print("Show User Board after Computer Hit")
        self.updated_board_1.update_board(human=False)  # it will update the board of human because computer strikes
        self.updated_board_1.board_human.print_board()


# %%
# Now, instantiate GameTester
game_tester_instance = GameTester(human_input, human_player, active_computer_ships,
                                  active_human_ships, computer_input, computer_player,
                                  updated_board_1, dots_human, dots_computer)


# %%
# Call your test functions
# game_tester_instance.test_function_human()
# game_tester_instance.test_function_computer()
# %%
# create a class for the game
class Game:
    def __init__(self):
        self.human_player = human_player
        self.computer_player = computer_player
        self.human_input = human_input
        self.computer_input = computer_input
        self.active_human_ships = active_human_ships
        self.active_computer_ships = active_computer_ships
        self.human_board_start = ship_allocator_human.human_board_start
        self.updated_board_1 = updated_board_1

    def play(self, print_completed_boards=False):

        print("Welcome to Battleship!")
        print("----------------------")
        print("To exit the game at any moment, enter row 912 and col 912.")

        while True:
            # Human's turn
            while True:
                print(" ")
                print("Human's turn!")

                guess, secret_code_entered = self.human_input.take_input()

                # Check if the secret code was entered
                if secret_code_entered:
                    print("Secret code entered! Game over.")
                    return

                self.human_input.is_hit(guess, human=True)
                self.updated_board_1.update_board(human=True)
                print("Computer's Board (Human sees his strikes):")
                self.updated_board_1.board_computer.print_board()
                print(" ")
                self.human_input.fleet_sunk(human=True)[1]

                if self.human_input.fleet_sunk(human=True)[0]:
                    break
                else:
                    break

            # Check if the human fleet is sunk before the computer's turn
            if self.human_input.fleet_sunk(human=True)[0]:
                print("Computer fleet is sunk! Game over.")
                break  # Exit the game loop

            # Computer's turn
            while True:
                print("Computer's turn!")
                guess = self.computer_input.take_computer_guess()
                self.computer_input.is_hit(guess, human=False)
                self.updated_board_1.update_board(human=False)

                if print_completed_boards == True:
                    print("Human's board (shows Computer's hits):")
                    self.updated_board_1.board_human.print_board()
                    print(" ")
                else:
                    pass

                self.computer_input.fleet_sunk(human=False)[1]

                if self.computer_input.fleet_sunk(human=False)[0]:
                    break
                else:
                    break

            # Check if the computer fleet is sunk before the human's turn
            if self.computer_input.fleet_sunk(human=False)[0]:
                print("Human fleet is sunk! Game over.")
                break  # Exit the game loop


# %%
# run the game

if __name__ == "__main__":
    game = Game()
    game.play(print_completed_boards=True)
>>>>>>> 06eaf90a13ff556d6b496385328d05142e254d0a
=======
'''
# create the board class
Battleship. Game.

designed and written by Oliver Den
Toronto, 2023

To terminate the game at any moment, enter 912, 912 as coordinates.
'''


# create the board class

class Board:
    def __init__(self, board_size=6, human=True):
        if human:
            self.size = board_size
            self.board = [["O"] * self.size for _ in range(self.size)]
        else:
            self.size = board_size
            self.board = [["O"] * self.size for _ in range(self.size)]

    def print_board(self):
        print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i, row in enumerate(self.board):
            print(f"{i + 1} | {' | '.join(map(str, row))} |")


# Create an instance of the Board class

clean_board_human = Board(board_size=6, human=True)
clean_board_computer = Board(board_size=6, human=False)
# %%
# create a ship class

import random


class Ship:
    def __init__(self, size, human=True):
        if human:
            self.board_size = Board().size
            self.size = size
            self.coordinates = []
            self.taken_dots = dots_human.taken_dots
            self.neighbouring_dots = dots_human.neighboring_dots
        else:
            self.board_size = Board().size
            self.size = size
            self.coordinates = []
            self.taken_dots = dots_computer.taken_dots
            self.neighbouring_dots = dots_computer.neighboring_dots

    def generate_random_coordinates(self):
        while True:
            orientation = random.choice(["horizontal", "vertical"])
            start_row = random.randint(0, self.board_size)
            start_col = random.randint(0, self.board_size)

            valid_coordinates = True
            candidate_coordinates = []

            for i in range(self.size):
                row = start_row + i if orientation == "vertical" else start_row
                col = start_col + i if orientation == "horizontal" else start_col

                # Check if the coordinates are within the valid range
                if not (0 <= row < self.board_size and 0 <= col < self.board_size):
                    valid_coordinates = False
                    break

                candidate_coordinates.append((row, col))

            if any(coord in [cell for ship in self.taken_dots for cell in ship] for coord in
                   candidate_coordinates) or any(
                    coord in [cell for neighbor in self.neighbouring_dots for cell in neighbor] for coord in
                    candidate_coordinates):
                valid_coordinates = False
            else:
                self.coordinates.extend(candidate_coordinates)
                break  # Exit the while loop if valid coordinates are found

        if not valid_coordinates:
            # If checks fail, start over with an empty list of candidates
            self.coordinates = []
            self.generate_random_coordinates()

    def return_coordinates(self):
        return self.coordinates


# %%
# create a ship catalogue

class CatalogueOfShips:
    ship_masts = [3, 2, 2, 1, 1, 1, 1]

    def __init__(self, human=True):
        if human:
            self.ship_objects = []
        else:
            self.ship_objects = []

    def return_masts(self):
        return self.ship_masts


# fixed ship lists

human_ship_catalogue = CatalogueOfShips(human=True)
computer_ship_catalogue = CatalogueOfShips(human=False)


# %%
# create the player class - final version

class Player:
    def __init__(self, human=True):
        if human:  # Human
            self.previous_guesses = []
            self.hits = []
        else:  # Computer
            self.previous_guesses = []
            self.hits = []


# Create an instance of the Player class

human_player = Player(human=True)
computer_player = Player(human=False)


# %%
# create class Dots to store the coordinates of the ships and the dots that have been taken
class Dots:
    def __init__(self, human=True):
        if human:
            self.taken_dots = []
            self.neighboring_dots = []
        else:
            self.taken_dots = []
            self.neighboring_dots = []

    def update_dots_taken(self, coordinates):
        self.taken_dots = coordinates

    def update_ships(self, ships):
        self.ships = ships


# Create an instance of the Dots class

dots_human = Dots(human=True)
dots_computer = Dots(human=False)


# %%
# create a class that generates ships

class ShipGenerator:
    def __init__(self, human=True):
        # Initialize with a list of masts from CatalogueOfShips
        self.masts = CatalogueOfShips().return_masts()

        # Use self.human to track whether it's a human ship generator
        self.human = human

    def generate_list_of_ships(self):
        for mast in self.masts:
            # Create a Ship object based on the mast
            self.ship = Ship(mast, human=self.human)

            # Generate random coordinates for the ship
            self.ship.generate_random_coordinates()
            self.ship_coordinates_return = self.ship.return_coordinates()

            # Add the ship to the appropriate ship_catalogue
            if self.human:
                human_ship_catalogue.ship_objects.append(self.ship)
                dots_human.taken_dots.append(self.ship_coordinates_return)
            else:
                computer_ship_catalogue.ship_objects.append(self.ship)
                dots_computer.taken_dots.append(self.ship_coordinates_return)

            # define the list of neighbouring dots
            if self.human:
                neighbors = []
                for x, y in self.ship_coordinates_return:
                    neighbors.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

                # Remove diagonally attached neighbors
                neighbors = [(x, y) for x, y in neighbors if (x, y) not in self.ship_coordinates_return]
                dots_human.neighboring_dots.append(neighbors)
            else:
                neighbors = []
                for x, y in self.ship_coordinates_return:
                    neighbors.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

                # Remove diagonally attached neighbors
                neighbors = [(x, y) for x, y in neighbors if (x, y) not in self.ship_coordinates_return]
                dots_computer.neighboring_dots.append(neighbors)


# initialize the ship generator for human

gen = ShipGenerator(human=True)
gen.generate_list_of_ships()

# and computer

gen = ShipGenerator(human=False)
gen.generate_list_of_ships()


# %%
# create a class that allocates ships to the board

class ShipAllocator:
    def __init__(self, human=True):
        self.human = human
        self.human_board_start = clean_board_human
        self.computer_board_start = clean_board_computer

    def allocate_ships(self):
        if self.human:
            for ship in human_ship_catalogue.ship_objects:
                for row, col in ship.coordinates:
                    self.human_board_start.board[row][col] = '■'
            else:
                for ship in computer_ship_catalogue.ship_objects:
                    for row, col in ship.coordinates:
                        self.computer_board_start.board[row][col] = '■'


# Create an instance of the ShipAllocator class

ship_allocator_human = ShipAllocator(human=True)
ship_allocator_human.allocate_ships()
ship_allocator_computer = ShipAllocator(human=False)
ship_allocator_computer.allocate_ships()

# create variables

human_board_next = ShipAllocator(human=True).human_board_start
computer_board_next = ShipAllocator(human=False).computer_board_start


# %%
# create a class that creates ship lists for the human and computer

class FreeRadicals:
    def active_human_ships(self):
        self.active_human_ships = [coordinate for sublist in dots_human.taken_dots for coordinate in sublist]
        return self.active_human_ships

    def active_computer_ships(self):
        self.active_computer_ships = [coordinate for sublist in dots_computer.taken_dots for coordinate in sublist]
        return self.active_computer_ships


# Creating an instance of the class
free_radicals_instance = FreeRadicals()

# Calling the instance methods to get the lists
active_human_ships = free_radicals_instance.active_human_ships()
active_computer_ships = free_radicals_instance.active_computer_ships()


# %%
# create a class for the player

class PlayerInput:

    def __init__(self, human=True):
        if human:
            self.player = human_player  # Human
            self.board = clean_board_human
            self.size_of_the_board = self.board.size
            self.computer_ship_coordinates = active_computer_ships  # list of ship objects

        else:
            self.player = human_player  # Computer
            self.board = clean_board_computer
            self.size_of_the_board = self.board.size
            self.human_ship_coordinates = active_human_ships  # list of ship objects

    def take_input(self):
        while True:
            try:
                self.guess_row = int(input("Guess Row (1-6): ")) - 1
                self.guess_col = int(input("Guess Col (1-6): ")) - 1
                self.guess = (self.guess_row, self.guess_col)

                # Check if the secret code was entered
                if (self.guess_col == 911) and (self.guess_row == 911):
                    print("You have entered the secret code to terminate the game. Shame!")
                    return self.guess, True  # secret code entered

                if (
                        0 <= self.guess_row <= 5
                        and 0 <= self.guess_col <= 5
                        and self.guess not in human_player.previous_guesses
                ):
                    return self.guess, False  # secret code not entered
                else:
                    print("Invalid input or already guessed. Row and column must be between 1 and 6.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def take_computer_guess(self):
        while True:
            self.guess = (random.randint(0, self.size_of_the_board - 1), random.randint(0, self.size_of_the_board - 1))

            if len(computer_player.previous_guesses) <= 36:
                if self.guess not in computer_player.previous_guesses:  # Check if the guess is not in previous guesses
                    return self.guess  # to avoid the endless cycle of the same guess
            else:
                break

    def is_hit(self, guess, human=True):  ## ship_coordinates = human/computer ship coordinates
        if human:
            if guess in active_computer_ships:
                self.length = [len(sublist) for sublist in dots_computer.taken_dots if guess in sublist]
                human_player.previous_guesses.append(guess)
                human_player.hits.append(guess)
                return True, f"You hit a {self.length[0]} mast ship! Arrr!"
            else:
                human_player.previous_guesses.append(guess)
                return False, "You missed! Blimey!"

        else:
            # go through each ship in ship_coordinates (embedded lists) and return the ship that contains the guess
            if guess in active_human_ships:
                self.length = [len(sublist) for sublist in dots_human.taken_dots if guess in sublist]
                computer_player.previous_guesses.append(guess)
                computer_player.hits.append(guess)
                return True, f"Computer hit your {self.length[0]} mast ship! Oh no!"
            else:
                computer_player.previous_guesses.append(guess)
                return False, "Computer missed! Hip Hip!"

    def fleet_sunk(self, human=True):
        if human:
            if sorted(human_player.hits) == sorted(active_computer_ships):
                return True, "You sank all the ships! Aye, Aye, Captain!"
            else:
                return False, "You still have enemy ships to sink. Keep playing!"
        else:
            if sorted(computer_player.hits) == sorted(active_human_ships):
                return True, "Computer sank all your ships! You lost!"
            else:
                return False, "Computer still has enemy ships to sink. Keep playing!"


# initiate the class for human player and computer player

human_input = PlayerInput(human=True)
computer_input = PlayerInput(human=False)


# %%
class UpdatedBoard:
    def __init__(self, human=True):
        self.previous_guesses_human = human_player.previous_guesses
        self.board_human = human_board_next
        self.hits_human = human_player.hits
        self.previous_guesses_computer = computer_player.previous_guesses
        self.board_computer = computer_board_next
        self.hits_computer = computer_player.hits

    def update_board(self, human=True):
        if human:  # updated board computer
            for guess in self.previous_guesses_human:  # previous guesses of computer
                self.board_computer.board[guess[0]][guess[1]] = 'T'  # apply to human board
            for hit in self.hits_human:
                self.board_computer.board[hit[0]][hit[1]] = 'X'
            return self.board_computer
        else:  # update board human
            for guess in self.previous_guesses_computer:  # previous guesses of computer
                self.board_human.board[guess[0]][guess[1]] = 'T'  # apply to human board
            for hit in self.hits_computer:
                self.board_human.board[hit[0]][hit[1]] = 'X'
            return self.board_human


updated_board_1 = UpdatedBoard()


# %%
class GameTester:
    def __init__(self, human_input, human_player, active_computer_ships,
                 active_human_ships, computer_input, computer_player,
                 updated_board_1, dots_human, dots_computer):
        self.human_input = human_input
        self.human_player = human_player
        self.active_computer_ships = active_computer_ships
        self.ships_computer_1 = GameTester.ships_computer()
        self.active_human_ships = active_human_ships
        self.ships_human_1 = GameTester.ships_human()
        self.computer_input = computer_input
        self.computer_player = computer_player
        self.updated_board_1 = updated_board_1
        self.dots_human = dots_human
        self.dots_computer = dots_computer

    @staticmethod
    def ships_human():
        ships = []
        for ship in human_ship_catalogue.ship_objects:
            ships.append(ship.coordinates)
        return ships

    @staticmethod
    def ships_computer():
        ships = []
        for ship in computer_ship_catalogue.ship_objects:
            ships.append(ship.coordinates)
        return ships

    # Assign the result of the static methods to the corresponding instance variables
    ships_human_1 = ships_human()
    ships_computer_1 = ships_computer()

    def test_function_human(self):
        user_input, another_value = self.human_input.take_input()
        print("User input: ", user_input)
        print("Previous guesses: ", self.human_player.previous_guesses)
        user_is_hit = self.human_input.is_hit(user_input, human=True)
        print("Active computer ship coordinates: ", self.active_computer_ships)
        print("Ships computer: ", self.ships_computer_1)
        print("Neighbouring cells computer: ", self.dots_computer.neighboring_dots)
        print("User is hit: ", user_is_hit)
        user_hits = self.human_player.hits
        print("User hits:", user_hits)
        user_fleet_sunk = self.human_input.fleet_sunk(human=True)
        print("Is fleet sunk: ", user_fleet_sunk)
        print("Show Computer Board after User Hit")
        self.updated_board_1.update_board(
            human=True)  # here reverse - it will update the board of computer because the human strikes
        self.updated_board_1.board_computer.print_board()

    def test_function_computer(self):
        computer_guess = self.computer_input.take_computer_guess()
        print("Computer guess: ", computer_guess)
        print("Previous guesses: ", self.computer_player.previous_guesses)
        computer_is_hit = self.computer_input.is_hit(computer_guess, human=False)
        print("Active human ship coordinates: ", self.active_human_ships)
        print("Ships human: ", self.ships_human_1)
        print("Neighbouring cells human: ", self.dots_human.neighboring_dots)
        print("Computer is hit: ", computer_is_hit)
        computer_hits = self.computer_player.hits
        print("Computer hits:", computer_hits)
        computer_fleet_sunk = self.computer_input.fleet_sunk(human=False)
        print("Is fleet sunk: ", computer_fleet_sunk)
        print("Show User Board after Computer Hit")
        self.updated_board_1.update_board(human=False)  # it will update the board of human because computer strikes
        self.updated_board_1.board_human.print_board()


# %%
# Now, instantiate GameTester
game_tester_instance = GameTester(human_input, human_player, active_computer_ships,
                                  active_human_ships, computer_input, computer_player,
                                  updated_board_1, dots_human, dots_computer)


# %%
# Call your test functions
# game_tester_instance.test_function_human()
# game_tester_instance.test_function_computer()
# %%
# create a class for the game
class Game:
    def __init__(self):
        self.human_player = human_player
        self.computer_player = computer_player
        self.human_input = human_input
        self.computer_input = computer_input
        self.active_human_ships = active_human_ships
        self.active_computer_ships = active_computer_ships
        self.human_board_start = ship_allocator_human.human_board_start
        self.updated_board_1 = updated_board_1

    def play(self, print_completed_boards=False):

        print("Welcome to Battleship!")
        print("----------------------")
        print("To exit the game at any moment, enter row 912 and col 912.")

        while True:
            # Human's turn
            while True:
                print(" ")
                print("Human's turn!")

                guess, secret_code_entered = self.human_input.take_input()

                # Check if the secret code was entered
                if secret_code_entered:
                    print("Secret code entered! Game over.")
                    return

                self.human_input.is_hit(guess, human=True)
                self.updated_board_1.update_board(human=True)
                print("Computer's Board (Human sees his strikes):")
                self.updated_board_1.board_computer.print_board()
                print(" ")
                self.human_input.fleet_sunk(human=True)[1]

                if self.human_input.fleet_sunk(human=True)[0]:
                    break
                else:
                    break

            # Check if the human fleet is sunk before the computer's turn
            if self.human_input.fleet_sunk(human=True)[0]:
                print("Computer fleet is sunk! Game over.")
                break  # Exit the game loop

            # Computer's turn
            while True:
                print("Computer's turn!")
                guess = self.computer_input.take_computer_guess()
                self.computer_input.is_hit(guess, human=False)
                self.updated_board_1.update_board(human=False)

                if print_completed_boards == True:
                    print("Human's board (shows Computer's hits):")
                    self.updated_board_1.board_human.print_board()
                    print(" ")
                else:
                    pass

                self.computer_input.fleet_sunk(human=False)[1]

                if self.computer_input.fleet_sunk(human=False)[0]:
                    break
                else:
                    break

            # Check if the computer fleet is sunk before the human's turn
            if self.computer_input.fleet_sunk(human=False)[0]:
                print("Human fleet is sunk! Game over.")
                break  # Exit the game loop


# %%
# run the game

if __name__ == "__main__":
    game = Game()
    game.play(print_completed_boards=True)
>>>>>>> 06eaf90a13ff556d6b496385328d05142e254d0a
