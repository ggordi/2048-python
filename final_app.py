# A tkinter replication of the popular 2048 game
# A portfolio project
# Gili Gordiyenko, Jan 2024 (finished 01/09/24)

import copy
import tkinter as tk
import random
from styles import colors_dict, custom_font, win_font

score_to_add = 0  # this keeps track of the score to add after each successful move

# this function will update the text and color of each cell label according to the current value
#   of each cell. it will also update the player_score_label. this should be called on startup
#   and after any successful move is made.
def update_style():
    for i in range(4):
        for j in range(4):
            current = cell_labels[i][j]
            text = ''
            value = cell_values[i][j]
            if value != 0:
                text = str(value)
            current.configure(text=text, bg=colors_dict.get(cell_values[i][j]))
    player_score_label.configure(text=str(player_score))


# this function will insert a 2 by default into a random position of the matrix. If 'True'
#   is passed into the function, there is a 20% chance a 4 will be inserted.
def insert_value(four=False):
    value = 2
    rand_r = random.randint(0, 3)
    rand_c = random.randint(0, 3)
    while cell_values[rand_r][rand_c] != 0:
        rand_r = random.randint(0, 3)
        rand_c = random.randint(0, 3)
    if four:
        rand_num = random.randint(1, 10)  # 20% chance of generating a 4
        if rand_num <= 2:
            value = 4
    cell_values[rand_r][rand_c] = value


# this function will compress all the values of the matrix passed in to the left.
#   this function returns the value to add to the player's score
def compress_left(matrix):
    global score_to_add
    score_to_add = 0
    # first, move all nonzero elements in the matrix to the left, repeat 4x
    for j in range(4):
        for row in matrix:
            for i in range(len(row) - 1, 0, -1):
                if row[i - 1] == 0:
                    row[i - 1] = row[i]
                    row[i] = 0
    # combine any neighboring like values, and update the score as needed
    for row in matrix:
        for i in range(len(row) - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
                score_to_add += row[i]
    # move all nonzero values left again
    for j in range(4):
        for row in matrix:
            for i in range(len(row) - 1, 0, -1):
                if row[i - 1] == 0:
                    row[i - 1] = row[i]
                    row[i] = 0

# this function returns the matrix compressed to the right
def compress_right(matrix):
    matrix = reverse(matrix)
    compress_left(matrix)
    return reverse(matrix)

# this function returns the matrix compressed up
def compress_up(matrix):
    matrix = transpose(matrix)
    compress_left(matrix)
    return transpose(matrix)

# this function returns the matrix compressed down
def compress_down(matrix):  # there's a bug here with the first row not going down
    matrix = transpose(matrix)
    matrix = reverse(matrix)
    compress_left(matrix)
    matrix = reverse(matrix)
    return transpose(matrix)


# this function will return a transposed version of the matrix passed in
def transpose(matrix):
    transposed = [[0]*4 for i in range(4)]
    for row in range(4):
        for column in range(4):
            transposed[row][column] = matrix[column][row]
    return transposed


# this function will return a reversed version of the matrix passed in
def reverse(matrix):
    reversed = []
    for row in matrix:
        reversed_row = []
        for i in range(3, -1, -1):
            reversed_row.append(row[i])
        reversed.append(reversed_row)
    return reversed


# this function will be called after a move is made to see if it was successful or not.
#   if the move was unsuccessful, do not update the style or add a new value to the matrix.
def after_move(before_matrix):
    # first, check if the user won
    for row in cell_values:
        for entry in row:
            if entry == 2048:
                game_won()
    # if the cell_values matrix is not the same after the move, the move was successful
    if before_matrix != cell_values:
        insert_value(True)
        global player_score
        global score_to_add
        player_score += score_to_add
        score_to_add = 0  # reset this after every successful move
        update_style()
    # otherwise, do nothing. proceed to checking if the user lost the game
    copy_1 = copy.deepcopy(cell_values)
    copy_2 = copy.deepcopy(cell_values)
    copy_2 = compress_down(copy_2)
    if copy_1 == copy_2:
        copy_2 = compress_up(copy_2)
        if copy_1 == copy_2:
            copy_2 = compress_right(copy_2)
            if copy_1 == copy_2:
                compress_left(copy_2)
                if copy_1 == copy_2:
                    game_over()


# this function will be called when the user wins the game, and will show a game won screen
def game_won():
    won_frame = tk.Frame(window, width=200, height=150, bg='#b1ffad')
    won_frame.pack_propagate(False)
    won_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    won_label = tk.Label(won_frame, text='You Won!', font=win_font, bg='white')
    won_label.pack(pady=(50, 0))


# this function will be called when the user loses the game, and will show a game lost screen
def game_over():
    lost_frame = tk.Frame(window, width=200, height=150, bg='#b0d2ff')
    lost_frame.pack_propagate(False)
    lost_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    lost_label = tk.Label(lost_frame, text='You lost!', font=win_font, bg='white')
    lost_label.pack(pady=(50, 0))

# the functions below will be called when the user presses the according arrow key
def on_left_press(event):
    copy_mat = copy.deepcopy(cell_values)
    compress_left(cell_values)
    after_move(copy_mat)

def on_right_press(event):
    global cell_values
    copy_mat = copy.deepcopy(cell_values)
    cell_values = compress_right(cell_values)
    after_move(copy_mat)

def on_up_press(event):
    global cell_values
    copy_mat = copy.deepcopy(cell_values)
    cell_values = compress_up(cell_values)
    after_move(copy_mat)

def on_down_press(event):
    global cell_values
    copy_mat = copy.deepcopy(cell_values)
    cell_values = compress_down(cell_values)
    after_move(copy_mat)


# set up the main window
window = tk.Tk()
window.title('2048')

# set up the main frame, the holder for all the game contents
main_frame = tk.Frame(window, width=450, height=600, bg='white')
main_frame.pack_propagate(False)
main_frame.pack()
# set up the labels
your_score = tk.Label(main_frame, text='Your Score: ', font=custom_font)
your_score.pack(pady=20)
player_score = 0  # this keeps track of the player's score
player_score_label = tk.Label(main_frame, text='0', font=custom_font)
player_score_label.pack(pady=5)

# set up the game frame, the container for the actual game board
game_frame = tk.Frame(main_frame, width=350, height=350, bg='#a39989')
game_frame.grid_rowconfigure(0)
game_frame.grid_columnconfigure(0)
game_frame.pack_propagate(False)
game_frame.pack(pady=(40, 0))
# set up the cells, the matrix of values and the matrix of labels
cell_values = [[0]*4 for i in range(4)]
cell_labels = []
for i in range(4):
    row = []
    for j in range(4):
        label = tk.Label(
            game_frame, text=str(cell_values[i][j]),
            width=8, height=4, bg='#cfc5b4', font=custom_font
        )
        label.grid(row=i, column=j, padx=5, pady=5)
        row.append(label)
    cell_labels.append(row)
# insert two 2s for the start of the game
insert_value()
insert_value()
# now, update the appearance
update_style()

# run the game
window.focus_set()
window.bind('<Left>', on_left_press)
window.bind('<Right>', on_right_press)
window.bind('<Up>', on_up_press)
window.bind('<Down>', on_down_press)

window.mainloop()
