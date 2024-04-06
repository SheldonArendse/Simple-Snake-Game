from tkinter import *
import random
import pygame

# Constants
GAME_WIDTH = 800
GAME_HEIGHT = 600
INITIAL_SPEED = 100
SPEED_INCREASE = 5
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Adding game sounds
pygame.init()
eat_sound = pygame.mixer.Sound(r"C:\Users\sheld\PycharmProjects\Snake_Game\sounds\beep.mp3")
death_sound = pygame.mixer.Sound(r"C:\Users\sheld\PycharmProjects\Snake_Game\sounds\Mario_death_sound.mp3")
background_sound = pygame.mixer.Sound(r"C:\Users\sheld\PycharmProjects\Snake_Game\sounds\PacMan_waka_waka_sound.mp3")


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Snake starting point (top left)
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Creating the body of the snake
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)


class Food:
    # Creating food look and style
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")


def game_over():
    death_sound.play()
    canvas.delete(ALL)

    # Game over text on screen
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 80),
                       text="GAME OVER!", fill="red", tags="game over")
    window.update()


def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Checking for collision on left or right
    if x < 0 or x >= GAME_WIDTH:
        print("GAME OVER!")
        return True
    # Checking for collision on top or bottom
    elif y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER!")
        return True
    # Checking for snake body collision
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER!")
            return True

    return False


def next_turn(snake, food):
    global score, SPEED
    x, y = snake.coordinates[0]

    # Direction settings
    if direction == "up":
        y -= SPACE_SIZE

    elif direction == "down":
        y += SPACE_SIZE

    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    # Insert new square at the head of the snake
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        # Increment score
        score += 1
        label.config(text=f"Score: {score} | Speed: {SPEED}ms")
        # Deleting the food object and spawning it in a different location
        canvas.delete("food")
        eat_sound.play()
        food = Food()

        # Increase the speed for every 2 foods eaten
        if score % 2 == 0 and SPEED > 60:
            SPEED -= SPEED_INCREASE
            label.config(text=f"Score: {score} | Speed: {SPEED}ms")

    else:
        # Delete the tail of the snake after it moves
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        # Update the game frame
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


# Window formatting
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Scoreboard formatting
score = 0
direction = 'down'

label = Label(window, text=f"Score: {score} | Speed: 100ms", font=('consolas', 40))
label.pack()

# Game frame formatting
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()


window.update()

# Centering the game frame
window_width = window.winfo_width()
window_height = window.winfo_height()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Binding keys for direction
window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))

snake = Snake()
food = Food()
SPEED = INITIAL_SPEED


next_turn(snake, food)

window.mainloop()

