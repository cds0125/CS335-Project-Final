# By: Kevin Kelmonas 11/4/2023
# Project for CS335
# 'Simon Says' Game

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QDialog # 4 different layouts, ...
from PyQt6.QtCore import Qt, QTimer, QEventLoop, QSize, QThread, pyqtSignal
from PyQt6.QtGui import QPalette, QBrush, QImage, QIcon, QFont, QPixmap
import sys # For access to command line arguments
import random # for random color selector
import numpy as np # Alternative: import Array as arr
from IceCreamOrder import *

#---------------------------------------------------------------------------------------------------------
# Code For Main Menu
#---------------------------------------------------------------------------------------------------------

class StartMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Game Menu") # set title of widget
        self.setFixedSize(1000,800) # set size of widget

        # Set Image as background for menu
        palette = QPalette()
        image = QImage("MenuBackground.png")  # Use image as background
        image = image.scaled(1000, 800)  # Scale image to fit the window
        palette.setBrush(QPalette.ColorRole.Window, QBrush(image)) 
        self.setPalette(palette)

        # creates button
        self.button_Simon = QPushButton("Simon Says")
        self.button_Matcher = QPushButton("Color Matcher")
        self.button_IceCream = QPushButton("Ice Cream Shop")
    
        # sets size of button
        self.button_Simon.setFixedSize(250, 100)
        self.button_Matcher.setFixedSize(250, 100)
        self.button_IceCream.setFixedSize(250, 100)

        # assigns function to button click action (use of lambda because ...)
        self.button_Simon.clicked.connect(lambda: self.start_Simon())
        self.button_Matcher.clicked.connect(lambda: self.start_Matcher())
        self.button_IceCream.clicked.connect(lambda: self.start_IceCream())

        # sets background, border look, and font specifics of button and text within it
        self.button_Simon.setStyleSheet("border-image: url(MainMenuButton.png); font-family: Cooper Black; font-size: 30px; font-weight: bold; border-radius: 15px;")
        self.button_Matcher.setStyleSheet("border-image: url(MainMenuButton.png); font-family: Cooper Black; font-size: 30px; font-weight: bold; border-radius: 15px;")
        self.button_IceCream.setStyleSheet("border-image: url(MainMenuButton.png); font-family: Cooper Black; font-size: 30px; font-weight: bold; border-radius: 15px;")

        # Create a QLabel and set the image as its display
        self.title = QLabel(self) 
        self.titlePixmap = QPixmap('GameMenuTitle.png')
        self.title.setFixedSize(900, 125)

        self.title.setPixmap(self.titlePixmap)
        self.title.setScaledContents(True)

        # Create a QHBoxLayout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_Simon)
        button_layout.addWidget(self.button_Matcher)
        button_layout.addWidget(self.button_IceCream)

        # Create a Grid layout in the center of the screen with title (0,1) and buttons (1,1)
        self.layout = QGridLayout()
        self.layout.setSpacing(25)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter) # center layout
        self.layout.addWidget(self.title, 0, 1)  # add title to the grid layout
        self.layout.addLayout(button_layout, 1, 1)  # add button layout to the grid layout

        self.widget = QWidget() 
        self.widget.setLayout(self.layout) # apply button layout to widget
        self.setCentralWidget(self.widget) # center of screen


    def start_Simon(self):

        # Create window for matching game.
        self.game_window = Simon_Says()
        # Sets dimensions of widget
        self.game_window.setFixedSize(1000,800) 
        # Show the new window
        self.game_window.show()
        # Close the current window.
        self.close()

    def start_Matcher(self):

        # Create window for matching game.
        self.game_window = DifficultySelection()
        # Sets dimensions of widget
        self.game_window.setFixedSize(250,200)
        # Show the new window
        self.game_window.show()
        # Close the current window.
        self.close()

    def start_IceCream(self):

        # Create IceCreamGUI instance
        self.game_window = IceCreamGUI() 
        # Show the new window
        self.game_window.show()
        # Close the current window
        self.close()

#---------------------------------------------------------------------------------------------------------
# Code For Simon Says Game
#---------------------------------------------------------------------------------------------------------

# Game Over pop up window (displays message, score, and close option)
class GameOver(QDialog):
        
        def __init__(self, score = None): # score paramater is passed in from Simon_Says() and is players score at the point the game ended
            super().__init__()

            # play mario song
            data, fs = sf.read('marioSimon.mp3')
            sd.play(data,fs, loop = False)

            self.setWindowTitle("Result") # Set title
            self.resize(400, 200)  # Set the size of the window
            self.setStyleSheet("background-color: #1a1a1a;")  # Set the background color

            self.label1 = QLabel("Game Over") # display message
            self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the label
            self.label1.setStyleSheet("font-size: 40px; color: red") # set size and color

            self.label2 = QLabel(f"You Scored: {score}") # display message with players score
            self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the label
            self.label2.setStyleSheet("font-size: 20px; color: white;") # set size and color

            self.button = QPushButton("Close") # create close window button
            self.button.clicked.connect(self.close) # assigns function to close window when clicked
            self.button.setStyleSheet("background-color: grey; color: white") # sets colors

            # displays every element vertically
            layout = QVBoxLayout(self)
            layout.addWidget(self.label1)
            layout.addWidget(self.label2)
            layout.addWidget(self.button)

# Code for Simon Says Game
class Simon_Says(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Simon Says")
        self.Array = np.array([]) # stores sequence of colors, appends new color every turn
        self.click_count = 0 # tracks number of moves left during turn and iterates through color sequence
        self.score = -1 # tracks players current score

        # creates button
        self.button_red = QPushButton()
        self.button_blue = QPushButton()
        self.button_green = QPushButton()
        self.button_yellow = QPushButton()
        self.button_start = QPushButton("Start Game")
        self.button_exit = QPushButton("Main Menu")

        # sets size of button
        self.button_red.setFixedSize(200, 200)
        self.button_blue.setFixedSize(200, 200)
        self.button_green.setFixedSize(200, 200)
        self.button_yellow.setFixedSize(200, 200) 
        self.button_start.setFixedSize(200, 75) 
        self.button_exit.setFixedSize(200, 75)

        # sets color of button
        self.button_red.setStyleSheet('background-color: red; border-color: black; border-style: outset; border-width: 3px; border-top-left-radius: 200px;')
        self.button_blue.setStyleSheet('background-color: blue; border-color: black; border-style: outset; border-width: 3px; border-top-right-radius: 200px;')
        self.button_green.setStyleSheet('background-color: green; border-color: black; border-style: outset; border-width: 3px; border-bottom-left-radius: 200px;')
        self.button_yellow.setStyleSheet('background-color: yellow; border-color: black; border-style: outset; border-width: 3px; border-bottom-right-radius: 200px;')
        self.button_start.setStyleSheet('background-color: grey; color: white; font-family: Broadway; font-size: 25px; border-radius: 15px;')
        self.button_exit.setStyleSheet('background-color: grey; color: white; font-family: Broadway; font-size: 25px; border-radius: 15px;')

        # assigns function to button click action (use of lambda because ...)
        self.button_red.clicked.connect(lambda: self.makeGuess('Red'))
        self.button_blue.clicked.connect(lambda: self.makeGuess('Blue'))
        self.button_green.clicked.connect(lambda: self.makeGuess('Green'))
        self.button_yellow.clicked.connect(lambda: self.makeGuess('Yellow'))
        self.button_start.clicked.connect(self.StartGame) # when clicked, creates loop until true becomes false
        self.button_exit.clicked.connect(lambda: self.exitGame())

        # First row, Title at top of simon says
        self.simon_label = QLabel("Simon Says")
        self.simon_label.setStyleSheet('font-size: 65px; font-family: Broadway; color: white;')
        # Second row, Red and Blue buttons
        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.button_red)
        self.top_layout.addWidget(self.button_blue)
        # Third row, Green and Yellow buttons
        self.bot_layout = QHBoxLayout()
        self.bot_layout.addWidget(self.button_green)
        self.bot_layout.addWidget(self.button_yellow)
        # Fourth row, Start and Exit buttons
        self.opt_layout = QHBoxLayout()
        self.opt_layout.addWidget(self.button_start)
        self.opt_layout.addWidget(self.button_exit)
        # Fith row, Current score
        self.score_label = QLabel(f"Score: {self.click_count}")
        self.score_label.setStyleSheet('font-size: 20px; font-family: Broadway; color: white;')
        # Center and align each row vertically
        self.all_layout = QGridLayout()
        self.all_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) # center layout
        self.all_layout.addWidget(self.simon_label, 0, 1)
        self.all_layout.addLayout(self.top_layout, 1, 1)
        self.all_layout.addLayout(self.bot_layout, 2, 1)
        self.all_layout.addWidget(self.score_label, 3, 1)
        self.all_layout.addLayout(self.opt_layout, 4, 1)
        # Add to Widget
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: #1a1a1a;") # Set background color of widget
        self.widget.setLayout(self.all_layout) # apply button layout to widget
        self.setCentralWidget(self.widget) # center of screen

        self.game_active = False # When 'Start' clicked, game loops while true, necessary to have turns (each turn adds color)

    def makeGuess(self, color): # assgigned to button clicks, avaliable only after starting game, registers a singular color clicked

        # if: game loop is true, and: the button color clicked is equal to the current button in the sequence, and: the color sequence for the user's current turn is not completed (clicks by user remain)
        if self.game_active and color == self.Array[self.click_count] and self.click_count < self.Array.size: 
            self.click_count += 1 # Iterate to the next spot in the array, update clicks remaining, ready for next click by user
            print(f'colors left to guess: {self.Array.size - self.click_count}') # prints in terminal
            if self.click_count == self.Array.size: # if after updating clicks remaining, 0 remain, then reloop start game and 
                print(f'adding color') # prints in terminal
                self.StartGame() # proceeds to next turn (adds a color to the sequence)
        else:
            dialog = GameOver(self.score) # Calls game over popup
            dialog.exec() # runs popup
            print(f'Game Over') # prints in terminal
            self.click_count = 0 # resets colors to be guessed
            self.score = -1 # resets players score
            self.Array = np.array([]) # resets array containing sequence of colors needed to be guessed
            self.game_active = False # ends game loop

    def AddColor(self): # add random color to sequence
       random_number = random.choices(["Red", "Blue", "Green", "Yellow"], k=1) # randomly selects 1 of 4 colors
       self.Array = np.append(self.Array, random_number) # adds color to sequence 
       # print(self.Array)

    # Task: in GUI make it highlight the button repeated for a second then revert it back to normal color and go on to the next index
    def Repeat(self): # prints color sequence

        self.i = 0 # increments until arrays entire sequence has been displayed (dependent on players current score)
        while self.i < len(self.Array):

            data, fs = sf.read('buttonSimon2.wav') # calls audio file 
            print(f'Simon Says: {self.Array[self.i]}') # make it highlight button repeated for 1 second then revert back to normal color

            if self.Array[self.i] == 'Red': # if this color is current index in sequence
                sd.play(data,fs, loop = False) # plays audio file
                self.button_red.setStyleSheet('background-color: red; border-color: white; border-style: outset; border-width: 3px; border-top-left-radius: 200px;') # highlights current color in sequence
                QTimer.singleShot(1500, lambda: self.button_red.setStyleSheet('background-color: red; border-color: black; border-style: outset; border-width: 3px; border-top-left-radius: 200px;')) # revert to original look

            elif self.Array[self.i] == 'Blue': # if this color is current index in sequence
                sd.play(data,fs, loop = False) # plays audio file
                self.button_blue.setStyleSheet('background-color: blue; border-color: white; border-style: outset; border-width: 3px; border-top-right-radius: 200px;') # highlights current color in sequence
                QTimer.singleShot(1500, lambda: self.button_blue.setStyleSheet('background-color: blue; border-color: black; border-style: outset; border-width: 3px; border-top-right-radius: 200px;')) # revert to original look

            elif self.Array[self.i] == 'Green': # if this color is current index in sequence
                sd.play(data,fs, loop = False) # plays audio file
                self.button_green.setStyleSheet('background-color: green; border-color: white; border-style: outset; border-width: 3px; border-bottom-left-radius: 200px;') # highlights current color in sequence
                QTimer.singleShot(1500, lambda: self.button_green.setStyleSheet('background-color: green; border-color: black; border-style: outset; border-width: 3px; border-bottom-left-radius: 200px;')) # revert to original look

            if self.Array[self.i] == 'Yellow': # if this color is current index in sequence
                sd.play(data,fs, loop = False) # plays audio file
                self.button_yellow.setStyleSheet('background-color: yellow; border-color: white; border-style: outset; border-width: 3px; border-bottom-right-radius: 200px;') # highlights current color in sequence
                QTimer.singleShot(1500, lambda: self.button_yellow.setStyleSheet('background-color: yellow; border-color: black; border-style: outset; border-width: 3px; border-bottom-right-radius: 200px;')) # revert to original look

            self.i += 1 # iterates to next color in sequence

            loop = QEventLoop()
            QTimer.singleShot(2000, loop.quit) 
            loop.exec()


    def StartGame(self): # starts turn, each turn a new color is added to sequence making game more challenging
       print("-------------------------") # games turn (output)
       print("~Game~")
       self.score += 1 # Adds to users score
       self.score_label.setText(f"Score: {self.score}") # Updates score label based on current score
       self.AddColor() # Adds new color to sequence
       self.Repeat() # Repeats the colors back to user
       self.game_active = True # starts game loop until you lose, essentially allows user to guess until wrong guess is made
       self.click_count = 0 # resets click count, tracks number of clicks made by user as they are guessing until max required guesses reached
       print("-------------------------") # your turn (input + output)

    def exitGame(self):

        # Create window for matching game.
        self.game_window = StartMenu()
        self.game_window.show()

        # Close the current window.
        self.close()

#---------------------------------------------------------------------------------------------------------
# Code For Matching Game
#---------------------------------------------------------------------------------------------------------

# Inital window for difficulty selection.
class DifficultySelection(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title.
        self.setWindowTitle("Difficulty Selection")

        # Set the grid layout.
        self.layout = QGridLayout()

        # Create difficulty selection box.
        self.difficulty_label = QLabel("Select Difficulty:")
        self.layout.addWidget(self.difficulty_label, 0, 0, 1, 2)

        # Create options for difficulty.
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        self.layout.addWidget(self.difficulty_combo, 1, 0, 1, 2)

        # Create start game button.
        start_game_button = QPushButton("Start Game")
        start_game_button.clicked.connect(self.start_game)
        self.layout.addWidget(start_game_button, 2, 0, 1, 2)

        # Set layout.
        self.setLayout(self.layout)

    # Definition to open game window.
    def start_game(self):
        # Get selected difficulty.
        selected_difficulty = self.difficulty_combo.currentText()

        # Create window for matching game.
        self.game_window = MatchingGame(selected_difficulty)
        self.game_window.setFixedSize(500,400)
        self.game_window.show()

        # Close the current window.
        self.close()

# Class for the matching game.
class MatchingGame(QWidget):
    def __init__(self, difficulty):
        super().__init__()

        # Matching Game title for window.
        self.setWindowTitle("Matching Game")

        # Initialize lists and size of the game.
        self.color_pairs = []
        self.selected_colors = []
        self.button_size = 50
        self.guess_count = 0

        # Default game difficulty.
        self.difficulty = difficulty

        # Set grid size.
        match self.difficulty:
            case "Easy":
                self.grid_size = 2
            case "Hard":
                self.grid_size = 6
            case _:
                self.grid_size = 4

        # Potential colors for the matching game.
        self.potential_colors = ['red', 'blue', 'green', 'yellow', 'lime', 'orange', 'cyan', 'magenta', 'khaki', 'silver', 'pink', 'beige', 'olive', 'chocolate', 'salmon', 'brown', 'indigo', 'black']
        self.colors = []

        # Choose colors for the grid size.
        for i in range(int((self.grid_size * self.grid_size) / 2)):
            self.colors.append(self.potential_colors[i])

        # Lists for buttons.
        self.buttons = []
        self.selected_buttons = []

        # Run setup UI.
        self.setup_ui()

    # Setup UI function.
    def setup_ui(self):
        # Layout for the game.
        layout = QGridLayout()

        # Create buttons and connect them to the slot.
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                button = QPushButton()
                button.setFixedSize(self.button_size, self.button_size)
                layout.addWidget(button, i + 1, j)
                button.clicked.connect(lambda _, row=i, col=j: self.button_clicked(row, col))
                self.buttons.append(button)

        # Create a new game button.
        self.reset_button = QPushButton("Start New Game")
        self.reset_button.clicked.connect(self.new_game)
        layout.addWidget(self.reset_button, self.grid_size + 1, 0, 1, self.grid_size)

        # Create a change difficulty button.
        difficulty_button = QPushButton("Change Difficulty")
        difficulty_button.clicked.connect(self.change_difficulty)
        layout.addWidget(difficulty_button, self.grid_size + 2, 0, 1, self.grid_size)

        # Create a button to go back to Main Menu
        exit_button = QPushButton("Main Menu")
        exit_button.clicked.connect(lambda: self.exitGame()) 
        layout.addWidget(exit_button, self.grid_size + 3, 0, 1, self.grid_size)

        # Create a label for the guess count.
        self.guess_count_label = QLabel()
        layout.addWidget(self.guess_count_label, self.grid_size + 4, 0, 1, self.grid_size)
        self.guess_count_label.setText(f"Guesses: {self.guess_count}")

        # Create a new game.
        self.new_game()

        # Set the layout.
        self.setLayout(layout)

    # For a new game setup.
    def new_game(self):
        # Generate pairs of colors.
        self.color_pairs = self.colors * 2
        random.shuffle(self.color_pairs)

        # Reset the guess count.
        self.guess_count = 0
        self.guess_count_label.setText(f"Guesses: {self.guess_count}")

        # Reset the new game button.
        self.reset_button.setText(f"Start New Game")

        # Assign colors to buttons.
        for button, color in zip(self.buttons, self.color_pairs):
            button.setStyleSheet(f'background-color: {color};')
            # Comment the below line to see colors.
            button.setStyleSheet(f'')
            button.setDisabled(False)

        # Reset the selected buttons and number of pairs matched.
        self.selected_buttons = []
        self.matched_pairs = 0

    def exitGame(self):

        # Create window for matching game.
        self.game_window = StartMenu()
        self.game_window.show()

        # Close the current window.
        self.close()

    # To change the difficulty.
    def change_difficulty(self):

        # Reopen the difficulty selection window.
        self.difficulty_window = DifficultySelection()
        self.difficulty_window.show()

        self.close() # Close the current game window

    # Button click.
    def button_clicked(self, row, col):
        # Reset the colors if two non-matches were selected.
        if len(self.selected_buttons) == 2:
            for button in self.selected_buttons:
                    button.setStyleSheet('')
                    self.selected_buttons = []
                    self.selected_colors = []

        # Get the button at the coordinate.
        button = self.buttons[row * self.grid_size + col]

        # Do not allow a currently selected button to be selected again.
        if button in self.selected_buttons:
            return

        # Reveal the color of the selected button.
        button.setStyleSheet(f'background-color: {self.color_pairs[row * self.grid_size + col]};')

        # Append to the selected colors list for matching.
        self.selected_colors.append(self.color_pairs[row * self.grid_size + col])

        # Show the color of the button.
        button.setStyleSheet(button.styleSheet() + 'border: 2px solid white;')
        self.selected_buttons.append(button)

        # Check for a match when two buttons are selected.
        if len(self.selected_buttons) == 2:
            # Increment the guess counter.
            self.guess_count += 1

            # Update the guess count label.
            self.guess_count_label.setText(f"Guesses: {self.guess_count}")

            # Check for a match.
            self.check_for_match()

    # Check for a match.
    def check_for_match(self):
        # Check if the color of buttons match.
        if self.selected_colors[0] == self.selected_colors[1]:
            # Match found.
            for button in self.selected_buttons:
                button.setDisabled(True)
            # Increase the number of pairs matched.
            self.matched_pairs += 1

            # Reset selected buttons and colors list.
            self.selected_buttons = []
            self.selected_colors = []

            # Check if all pairs are matched.
            if self.matched_pairs == len(self.colors):
                # Display winning text.
                print("Congratulations! You've matched all pairs. Start a new game?")
                self.reset_button.setText(f"Play Again")

#---------------------------------------------------------------------------------------------------------
# Code For Ice Cream Game
# By Cassie Stevens
#---------------------------------------------------------------------------------------------------------

# Class for the Ice Cream Parlor
# Subclass QMainWindow to customize your application's main window
class IceCreamGUI(QMainWindow):
#Method: Display the default UI
    def __init__(self):
        super().__init__()
    #Set the window Title
        self.setWindowTitle("Ice Cream Parlor")
    #Set geometry of the window
        self.setFixedSize(1000,800)
    #Default ice cream order
        self.order = IceCreamOrder()
    #Start Menu widgets
        self.startMenu()
    #Thread for countdown
        self.countdown_thread = CountdownThread()
        self.countdown_thread.update_signal.connect(self.update_countdown)
        self.reset_countdown() #Reset countdown initially to 60 seconds
        
#Method: Before the game starts UI
    def startMenu(self):
#Start menu
    #Play music
        self.order.playMusic('game1')
    #Main Game Background
        #Create label
        self.gameBackground = QLabel(self)
        self.gameBackgroundPixmap = QPixmap('Ice Cream Parlor Color.png')
        self.gameBackground.setPixmap(self.gameBackgroundPixmap)
        self.gameBackground.resize(self.gameBackgroundPixmap.width(), self.gameBackgroundPixmap.height())
    
    #Score Labels
        self.scoreName = QLabel("Score:",self)
        self.scoreName.setFont(QFont('Times', 20)) 
        self.scoreName.setGeometry(20, 20, 80, 35)
        self.scoreNum = QLabel("0",self)
        self.scoreNum.setFont(QFont('Times', 20)) 
        self.scoreNum.setGeometry(106, 20, 135, 35)
    
    #Timer Labels
        self.timerLabel = QLabel("Time:",self)
        self.timerLabel.setFont(QFont('Times', 20)) 
        self.timerLabel.setGeometry(23, 50, 77, 35)
        self.countdownLabel = QLabel("60", self)
        self.countdownLabel.setFont(QFont('Times', 20)) 
        self.countdownLabel.setGeometry(106, 52, 140, 35)
    
    #Order Labels
        self.orderLabel = QLabel("Order #",self)
        self.orderLabel.setFont(QFont('Times', 19)) 
        self.orderLabel.setGeometry(408, 29, 102, 35)
        self.orderNumLabel = QLabel(str(self.order.orderNum),self)
        self.orderNumLabel.setFont(QFont('Times', 19)) 
        self.orderNumLabel.setGeometry(510, 29, 57, 35)
    
    #Order Image Label    
        self.orderImageLabel = QLabel(self)
        self.orderImageLabel.setGeometry(402, 70, 196, 338)
        self.orderImageLabel.hide()
    
    #Instructions
        self.instructionsLabel = QLabel(self)
        self.instructionsLabel.setGeometry(20, 70, 960, 338)
        self.instructionsLabelPixmap = QPixmap('How to Play.png')
        self.instructionsLabel.setPixmap(self.instructionsLabelPixmap)
        self.instructionsLabel.resize(self.instructionsLabelPixmap.width(), self.instructionsLabelPixmap.height())
    
    #Points
        self.pointsLabel = QLabel(self)
        self.pointsLabel.setGeometry(530, 430, 450, 225)
        self.pointsLabelPixmap = QPixmap('Points Ice Cream.png')
        self.pointsLabel.setPixmap(self.pointsLabelPixmap)
        self.pointsLabel.resize(self.pointsLabelPixmap.width(), self.pointsLabelPixmap.height())
    
    #Start Button
        self.startButton = QPushButton("Click Here to Begin!", self)
        self.startButton.setGeometry(530, 667, 450, 125)
        self.startButton.setFont(QFont('Times', 20))
    #Action for startButton      
        self.startButton.clicked.connect(self.startGame)
        
    #Main menu button
        self.mainMenuButton = QPushButton("Main Menu", self)
        self.mainMenuButton.setGeometry(850, 0, 150, 64)
        self.mainMenuButton.setFont(QFont('Times', 20))
    #Action for mainMenuButton
        self.mainMenuButton.clicked.connect(self.exitIceCreamGame)
#Serve and Reset Buttons 
    #Serve Button    
        self.serveButton = QPushButton("SERVE", self)
        self.serveButton.setGeometry(854, 454, 124, 108)
        self.serveButton.setFont(QFont('Times', 20))
    #Action for Serve Button
        self.serveButton.clicked.connect(self.servedIceCream)
        #Disable and hide
        self.serveButton.hide()
        
    #Reset Button    
        self.resetButton = QPushButton("RESET", self)
        self.resetButton.setGeometry(854, 660, 124, 108)
        self.resetButton.setFont(QFont('Times', 20))
    #Action for Reset Button
        self.resetButton.clicked.connect(self.resetIceCream)
        #Disable and hide
        self.resetButton.hide()
        
#User Scoops Images
    #Label for scoops
        self.yourIceCreamLabel = QLabel("Your Ice Cream", self)
        self.yourIceCreamLabel.setGeometry(600, 430, 191, 35)
        self.yourIceCreamLabel.setFont(QFont('Times', 20))
        self.yourIceCreamLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.yourIceCreamLabel.hide()
        
    #Scoop Top Label
        self.scoopTop = QLabel(self)
        self.scoopTop.setGeometry(542, 468, 150, 100)
        self.scoopTop.hide()
        
    #Scoop Middle Label
        self.scoopMiddle = QLabel(self)
        self.scoopMiddle.setGeometry(542, 574, 150, 100)
        self.scoopMiddle.hide()
        
    #Scoop Bottom Label
        self.scoopBottom = QLabel(self)
        self.scoopBottom.setGeometry(542, 680, 150, 100)
        self.scoopBottom.hide()
        
    #Container Label
        self.containerLabel = QLabel(self)
        self.containerLabel.setGeometry(705, 549, 100, 150)
        self.containerLabel.hide()
        
#Buttons for the ice cream CONTAINERS
    #Waffle Cone Button
        self.waffleConeButton = QPushButton(self)
        self.waffleConeButton.setGeometry(20, 430, 150, 100)
    #Setting image on button
        self.waffleConeButton.setIcon(QIcon(QPixmap('Waffle Cone.png')))
        self.waffleConeButton.setIconSize(QSize(150, 100))
    #Waffle Cone Label
        self.waffleConeLabel = QLabel("Waffle Cone", self)
        self.waffleConeLabel.setGeometry(20, 530, 150, 25)
        self.waffleConeLabel.setFont(QFont('Times', 16))
        self.waffleConeLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    #Action for waffle cone button
        self.waffleConeButton.clicked.connect(self.waffleConeClicked)    
    
    #Cake Cone Button
        self.cakeConeButton = QPushButton(self)
        self.cakeConeButton.setGeometry(20, 555, 150, 100)
        #Setting image on button
        self.cakeConeButton.setIcon(QIcon(QPixmap('Cake Cone.png')))
        self.cakeConeButton.setIconSize(QSize(150, 100))
    #Cake Cone Label
        self.cakeConeLabel = QLabel("Cake Cone", self)
        self.cakeConeLabel.setGeometry(20, 655, 150, 25)
        self.cakeConeLabel.setFont(QFont('Times', 16))
        self.cakeConeLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    #Action for cake cone button
        self.cakeConeButton.clicked.connect(self.cakeConeClicked)
    #Cup Button
        self.cupButton = QPushButton(self)
        self.cupButton.setGeometry(20, 680, 150, 100)
        #Set image on button
        self.cupButton.setIcon(QIcon(QPixmap('Cup.png')))
        self.cupButton.setIconSize(QSize(150, 100))
    #Cup Label
        self.cupLabel = QLabel("Cup", self)
        self.cupLabel.setGeometry(20, 778, 150, 25)
        self.cupLabel.setFont(QFont('Times', 16))
        self.cupLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    #Action for cup button
        self.cupButton.clicked.connect(self.cupClicked)
        
#Buttons for the ice cream FLAVORS      
    #Vanilla Button
        self.vanillaButton = QPushButton(self)
        self.vanillaButton.setGeometry(190, 430, 150, 100)
        #Set image on button
        self.vanillaButton.setIcon(QIcon(QPixmap('Vanilla.png')))
        self.vanillaButton.setIconSize(QSize(150, 100))
        #Vanilla Label
        self.vanillaLabel = QLabel("Vanilla", self)
        self.vanillaLabel.setGeometry(190, 530, 150, 25)
        self.vanillaLabel.setFont(QFont('Times', 16))
        self.vanillaLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    #Action for vanilla button
        self.vanillaButton.clicked.connect(self.vanillaClicked)
        
    #Chocolate Button
        self.chocolateButton = QPushButton(self)
        self.chocolateButton.setGeometry(190, 555, 150, 100)
        #Set image on button
        self.chocolateButton.setIcon(QIcon(QPixmap('Chocolate.png')))
        self.chocolateButton.setIconSize(QSize(150, 100))
    #Chocolate Label
        self.chocolateLabel = QLabel("Chocolate", self)
        self.chocolateLabel.setGeometry(190, 655, 150, 25)
        self.chocolateLabel.setFont(QFont('Times', 16))
        self.chocolateLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    #Action for chocolate button
        self.chocolateButton.clicked.connect(self.chocolateClicked)
        
    #Strawberry Button
        self.strawberryButton = QPushButton(self)
        self.strawberryButton.setGeometry(190, 680, 150, 100)
        #Set image on button
        self.strawberryButton.setIcon(QIcon(QPixmap('Strawberry.png')))
        self.strawberryButton.setIconSize(QSize(150, 100))
    #Strawberry Label
        self.strawberryLabel = QLabel("Strawberry", self)
        self.strawberryLabel.setGeometry(190, 778, 150, 25)
        self.strawberryLabel.setFont(QFont('Times', 16))
        self.strawberryLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    #Action for strawberry button
        self.strawberryButton.clicked.connect(self.strawberryClicked)
        
#Buttons for the ice cream TOPPINGS        
    #Cherry Button
        self.cherryButton = QPushButton(self)
        self.cherryButton.setGeometry(360, 430, 150, 100)
        #Set image on button
        self.cherryButton.setIcon(QIcon(QPixmap('Cherry.png')))
        self.cherryButton.setIconSize(QSize(150, 100))
    #Cherry Label
        self.cherryLabel = QLabel("Cherry", self)
        self.cherryLabel.setGeometry(360, 530, 150, 25)
        self.cherryLabel.setFont(QFont('Times', 16))
        self.cherryLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    #Action for cherry button
        self.cherryButton.clicked.connect(self.cherryClicked)
            
    #Sprinkles Button
        self.sprinklesButton = QPushButton(self)
        self.sprinklesButton.setGeometry(360, 555, 150, 100)
        #Set image on button
        self.sprinklesButton.setIcon(QIcon(QPixmap('Sprinkles.png')))
        self.sprinklesButton.setIconSize(QSize(150, 100))    
    #Sprinkles Label
        self.sprinklesLabel = QLabel("Sprinkles", self)
        self.sprinklesLabel.setGeometry(360, 655, 150, 25)
        self.sprinklesLabel.setFont(QFont('Times', 16))
        self.sprinklesLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    #Action for sprinkles button
        self.sprinklesButton.clicked.connect(self.sprinklesClicked)
         
    #Chocolate Chips Button
        self.chocolateChipsButton = QPushButton(self)
        self.chocolateChipsButton.setGeometry(360, 680, 150, 100)
        #Set image on button
        self.chocolateChipsButton.setIcon(QIcon(QPixmap('Chocolate Chips.png')))
        self.chocolateChipsButton.setIconSize(QSize(150, 100))
    #Chocolate Chips Label
        self.chocolateChipsLabel = QLabel("Chocolate Chips", self)
        self.chocolateChipsLabel.setGeometry(350, 778, 169, 30)
        self.chocolateChipsLabel.setFont(QFont('Times', 16))
        self.chocolateChipsLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    #Action for chocolate chips button
        self.chocolateChipsButton.clicked.connect(self.chocolateChipsClicked)
    
    #No Toppings Button
        self.noToppingsButton = QPushButton("No Toppings", self)
        self.noToppingsButton.setGeometry(190, 305, 150, 100)
        self.noToppingsButton.setFont(QFont('Times', 18))
        self.noToppingsButton.hide()
    #Action for no toppings button
        self.noToppingsButton.clicked.connect(self.noToppingsClicked)
    
    #Disable them for now; will be enabled when start button is clicked
        self.waffleConeButton.setEnabled(False)
        self.cakeConeButton.setEnabled(False)
        self.cupButton.setEnabled(False)
        self.vanillaButton.setEnabled(False)
        self.chocolateButton.setEnabled(False)
        self.strawberryButton.setEnabled(False)
        self.cherryButton.setEnabled(False)
        self.sprinklesButton.setEnabled(False)
        self.chocolateChipsButton.setEnabled(False)
        self.noToppingsButton.setEnabled(False)

#End of game
    #Game Over Screen
        self.endScreen = QLabel(self)
        self.endScreen.hide()
        
    #Play again button
        self.playAgainButton = QPushButton("Play again", self)
        self.playAgainButton.setGeometry(110, 555, 340, 209)
        self.playAgainButton.setFont(QFont('Times', 20))
    #Action for play again button      
        self.playAgainButton.clicked.connect(self.playAgain) 
        self.playAgainButton.hide()
        
    #Return to menu button
        self.returnToMenu = QPushButton("Return to Menu", self)
        self.returnToMenu.setGeometry(585, 555, 340, 209)
        self.returnToMenu.setFont(QFont('Times', 20))
    #Action for play again button      
        self.returnToMenu.clicked.connect(self.exitIceCreamGame)
        self.returnToMenu.hide()
        
#Method: Action for startButton
    def startGame(self):
    #Play menu music
        self.order.playMusic('game2')
    #Hide and disable components of the start menu
        self.startButton.setEnabled(False)
        self.startButton.hide()
        self.instructionsLabel.hide()
        self.pointsLabel.hide()
    #Enable the buttons
        self.waffleConeButton.setEnabled(True)
        self.cakeConeButton.setEnabled(True)
        self.cupButton.setEnabled(True)
        self.vanillaButton.setEnabled(True)
        self.chocolateButton.setEnabled(True)
        self.strawberryButton.setEnabled(True)
        self.cherryButton.setEnabled(False)
        self.sprinklesButton.setEnabled(False)
        self.chocolateChipsButton.setEnabled(False)
        self.noToppingsButton.setEnabled(False)
        self.resetButton.setEnabled(True)
        self.serveButton.setEnabled(True)
    #Reset score, order number, and bonus points to be safe
        self.order.score = 0
        self.order.orderNum = 0
        self.order.streak = 0
    #Set order number and score
        self.orderNumLabel.setText(str(self.order.orderNum))
        self.scoreNum.setText(str(self.order.score))
    #Resets the user's side of things
        self.order.resetUserIceCream()
    #Get new ice cream order
        self.order.takeOrder()
        self.order.getFinalOrder()
    #Order Image Label    
        self.orderImageLabelPixmap = QPixmap('order.png')
        self.orderImageLabel.setPixmap(self.orderImageLabelPixmap.scaled(196, 338, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.orderImageLabel.setGeometry(402, 70, 196, 338)
        self.orderNumLabel.setText(str(self.order.orderNum))
    #Show widgets needed
        self.resetButton.show()
        self.serveButton.show()
        self.orderImageLabel.show()
        self.noToppingsButton.show()
        self.yourIceCreamLabel.show()
    #Countdown
        self.reset_countdown()  #Reset for new game
        self.countdown_thread.start()   #Start countdown

#Method: User clicked a container button
    def waffleConeClicked(self):
    #Set the container user picked
        self.order.userContainer = "Waffle Cone"
    #Set image for the container
        self.containerShow()
    #Disable those buttons for container
        self.waffleConeButton.setEnabled(False)
        self.cakeConeButton.setEnabled(False)
        self.cupButton.setEnabled(False)

#Method: User clicked a container button
    def cakeConeClicked(self):
    #Set the container user picked
        self.order.userContainer = "Cake Cone"
    #Set image for the container
        self.containerShow()
    #Disable those buttons for container
        self.waffleConeButton.setEnabled(False)
        self.cakeConeButton.setEnabled(False)
        self.cupButton.setEnabled(False)
        
#Method: User clicked a container button
    def cupClicked(self):
    #Set the container user picked
        self.order.userContainer = "Cup"
    #Set image for the container
        self.containerShow()
    #Disable those buttons for container
        self.waffleConeButton.setEnabled(False)
        self.cakeConeButton.setEnabled(False)
        self.cupButton.setEnabled(False)
        
#Method: User clicked a container button
    def containerShow(self):
        self.containerLabelPixmap = QPixmap(f'{self.order.userContainer}.png')
        self.containerLabel.setPixmap(self.containerLabelPixmap.scaled(100, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.containerLabel.setGeometry(705, 549, 100, 150)
        self.containerLabel.resize(100,150)
        self.containerLabel.show()
        
#Method: User clicked the vanilla button
    def vanillaClicked(self):
    #Set the flavor user picked
        self.order.userFlavors[self.order.userScoopMaking-1] = "Vanilla"
    #Set image of scoop
        self.updateScoops()
    #Enable toppings buttons
        self.enableToppings()
        
#Method: User clicked the chocolate button
    def chocolateClicked(self):
    #Set the flavor user picked
        self.order.userFlavors[self.order.userScoopMaking-1] = "Chocolate"
    #Set image of scoop
        self.updateScoops()
    #Enable toppings buttons
        self.enableToppings()
        
#Method: User clicked the strawberry button
    def strawberryClicked(self):
    #Set the flavor user picked
        self.order.userFlavors[self.order.userScoopMaking-1] = "Strawberry"
    #Set image of scoop
        self.updateScoops()
    #Enable toppings buttons
        self.enableToppings()
        
#Method: Ice cream flavor clicked, enable toppings buttons
    def enableToppings(self):
        self.cherryButton.setEnabled(True)
        self.sprinklesButton.setEnabled(True)
        self.chocolateChipsButton.setEnabled(True)
        self.noToppingsButton.setEnabled(True)
        
#Method: User clicked the cherry button
    def cherryClicked(self):
    #Set the topping user picked
        self.order.userToppings[self.order.userScoopMaking-1] = "Cherry"
    #Set image of scoop
        self.updateScoops()
    #Scoop is made
        self.order.userScoopMaking -= 1
        
#Method: User clicked the sprinkles button
    def sprinklesClicked(self):
    #Set the topping user picked
        self.order.userToppings[self.order.userScoopMaking-1] = "Sprinkles"
    #Set image of scoop
        self.updateScoops()
    #Scoop is made
        self.order.userScoopMaking -= 1
    #Disable toppings buttons
        self.disableToppings()
                
#Method: User clicked the chocolate chips button
    def chocolateChipsClicked(self):
    #Set the topping user picked
        self.order.userToppings[self.order.userScoopMaking-1] = "Chocolate Chips"
    #Set image of scoop
        self.updateScoops()
    #Scoop is made
        self.order.userScoopMaking -= 1
    #Disable toppings buttons
        self.disableToppings()
#Method: User clicked the no toppings button
    def noToppingsClicked(self):
    #Set the topping user picked
        self.order.userToppings[self.order.userScoopMaking-1] = "No Topping"        
    #Set image of scoop
        self.updateScoops()
    #Scoop is made
        self.order.userScoopMaking -= 1
    #Disable toppings buttons
        self.disableToppings()
        
#Method: Ice cream flavor clicked, enable toppings buttons
    def disableToppings(self):
        self.cherryButton.setEnabled(False)
        self.sprinklesButton.setEnabled(False)
        self.chocolateChipsButton.setEnabled(False)
        self.noToppingsButton.setEnabled(False)

#Method: Action for resetButton
    def resetIceCream(self):
        #Reset user's selection
        self.order.resetUserIceCream()
        #Deduct points for using reset button
        self.order.score -= 25
        self.scoreNum.setText(str(self.order.score))
        self.waffleConeButton.setEnabled(True)
        self.cakeConeButton.setEnabled(True)
        self.cupButton.setEnabled(True)
        self.vanillaButton.setEnabled(True)
        self.chocolateButton.setEnabled(True)
        self.strawberryButton.setEnabled(True)
        self.cherryButton.setEnabled(False)
        self.sprinklesButton.setEnabled(False)
        self.chocolateChipsButton.setEnabled(False)
        self.noToppingsButton.setEnabled(False)
        self.scoopTop.hide()
        self.scoopMiddle.hide()
        self.scoopBottom.hide()
        self.containerLabel.hide()
        #Remove 25 extra points
        if self.order.streak - 25 < 0:
            self.order.streak = 0
        else:
            self.order.streak -= 25
        
#Method: Action for serveButton
    def servedIceCream(self):
        orderSuccess = self.order.compareIceCream()
        if orderSuccess == True:
            self.order.score += 100
        #Set extra points to 0
            self.order.streak += 50
            self.order.score += self.order.streak
        else:   #Incorrect order
            self.order.score -=50
        #Set extra points to 0
            if self.order.streak - 50 < 0:
                self.order.streak = 0
            else:
                self.order.streak -= 50
    #Update Score
        self.scoreNum.setText(str(self.order.score))
    #Get new order
        self.order.takeOrder()
        self.orderTaken()

#Method: When a new order is made, the adjustments needed
    def orderTaken(self):
    #This gets the image for the order
        self.order.getFinalOrder()
    #Update order number
        self.orderNumLabel.setText(str(self.order.orderNum))
    #Update the order image
        self.orderImageLabelPixmap = QPixmap('order.png')
        self.orderImageLabel.setPixmap(self.orderImageLabelPixmap.scaled(196, 338, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.orderImageLabel.resize(196, 338)
        self.orderImageLabel.setGeometry(402, 70, 196, 338)
        self.orderImageLabel.show()
    #Reset user's selection
        self.order.resetUserIceCream()
    #Enable buttons
        self.waffleConeButton.setEnabled(True)
        self.cakeConeButton.setEnabled(True)
        self.cupButton.setEnabled(True)
        self.vanillaButton.setEnabled(True)
        self.chocolateButton.setEnabled(True)
        self.strawberryButton.setEnabled(True)
        self.cherryButton.setEnabled(False)
        self.sprinklesButton.setEnabled(False)
        self.chocolateChipsButton.setEnabled(False)
        self.noToppingsButton.setEnabled(False)
    #Hide Scoops and Container
        self.scoopTop.hide()
        self.scoopMiddle.hide()
        self.scoopBottom.hide()
        self.containerLabel.hide()

#Method: uploading images for the scoops
    def updateScoops(self):
        scoopMaking = self.order.userScoopMaking
        #Makes the image for the scoop
        self.order.singleScoop()
        if scoopMaking == 1:
        #Update the order image
            self.scoopTopPixmap = QPixmap('userScoop.png')
            self.scoopTop.setPixmap(self.scoopTopPixmap.scaled(150, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.scoopTop.resize(150, 100)
            self.scoopTop.setGeometry(542, 468, 150, 100)
            self.scoopTop.show()
        elif scoopMaking == 2:
            self.scoopMiddlePixmap = QPixmap('userScoop.png')
            self.scoopMiddle.setPixmap(self.scoopMiddlePixmap.scaled(150, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.scoopMiddle.resize(150, 100)
            self.scoopMiddle.setGeometry(542, 574, 150, 100)
            self.scoopMiddle.show()
        else: #Bottom scoop
            self.scoopBottomPixmap = QPixmap('userScoop.png')
            self.scoopBottom.setPixmap(self.scoopBottomPixmap.scaled(150, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.scoopBottom.resize(150, 100)
            self.scoopBottom.setGeometry(542, 680, 150, 100)
            self.scoopBottom.show()

#Method update countdown
    def update_countdown(self, time_remaining):
        if time_remaining > 0:
            self.countdownLabel.setText(f"{time_remaining} seconds")
        elif time_remaining == 0: #Time ran out
            self.countdownLabel.setText(f"{time_remaining} seconds")
            self.gameEnd()

#Method reset countdown back to 60 seconds         
    def reset_countdown(self):
        self.countdown_thread.time_remaining = 60

#Method: Game over screen
    def gameEnd(self):
        if self.order.score >= 5000:    #Success
            self.endScreenPixmap = QPixmap('Success.png')
            self.endScreen.setPixmap(self.endScreenPixmap)
            self.endScreen.resize(self.endScreenPixmap.width(), self.endScreenPixmap.height())
        else: #Failure
            self.endScreenPixmap = QPixmap('Failure.png')
            self.endScreen.setPixmap(self.endScreenPixmap)
            self.endScreen.resize(self.endScreenPixmap.width(), self.endScreenPixmap.height())
    #Display end screen
        self.endScreen.show()
        self.playAgainButton.show()
        self.returnToMenu.show()
        
#Method: Play the game again
    def playAgain(self):
        sd.stop()
        self.order.playMusic('game1')
    #Reset score, order number, and bonus points
        self.order.score = 0
        self.order.orderNum = 0
        self.order.streak = 0
    #Set order number and score
        self.orderNumLabel.setText(str(self.order.orderNum))
        self.scoreNum.setText(str(self.order.score))
    #Resets the user's side of things
        self.order.resetUserIceCream()
    #Hide Widgets
        #Game over screen
        self.endScreen.hide()
        self.playAgainButton.hide()
        self.returnToMenu.hide()
        #Buttons overlapping
        self.noToppingsButton.hide()
        self.serveButton.hide()
        self.resetButton.hide()
        self.yourIceCreamLabel.hide()
        self.scoopTop.hide()
        self.scoopMiddle.hide()
        self.scoopBottom.hide()
        self.containerLabel.hide()
    #Show Start menu widgets
        self.pointsLabel.show()
        self.instructionsLabel.show()
        self.startButton.show()
        self.startButton.setEnabled(True)

#Method: Exit game and return to menu     
    def exitIceCreamGame(self):
        #Stop music
        sd.stop()
        #Set the window back to the start menu.
        self.game_window = StartMenu()
        self.game_window.show()
        
        #Close the current window.
        self.close()
        
#Countdown for timer
class CountdownThread(QThread):
    update_signal = pyqtSignal(int)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.time_remaining = 60
    
#Method: Run countdown
    def run(self):
        #Run while time left is >= 0
        while self.time_remaining >= 0:
            self.update_signal.emit(self.time_remaining)
            self.msleep(1000)
            self.time_remaining -= 1
#---------------------------------------------------------------------------------------------------------
# Code To Run Main Menu GUI
#---------------------------------------------------------------------------------------------------------

app = QApplication(sys.argv) # Python list containing the command line arguments passed to the application ( for no command line arguments: app = QApplication([]) )
window = StartMenu() # Create a Qt widget, which will be our window.
window.show()
app.exec() # Start the event loop
