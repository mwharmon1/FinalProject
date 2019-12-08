"""
Author: Michael Harmon
Description: This is a GUI game of rock paper scissors.
Player will be able to create a new player or get their current player data and play
the rock paper scissors against the computer. Games won and games loss will be kept track of.
Last Date Modified: 12/8/2019
"""

import sqlite3
import time
from sqlite3 import Error
from tkinter import messagebox
from tkinter import *
import tkinter
from class_definitions.player_class import Player
from class_definitions.rock_paper_scissors_class import RockPaperScissors
from tkinter import ttk

connection = None
new_player = False
win_count = 0
loss_count = 0
total_wins = 0


def create_connection(db):
    """
    Create connection to the database
    :param db:
    :return: connection
    """
    global connection
    """ Connect to a SQLite database """
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as err:
        print(err)
    return None


def create_table(connection, sql_create_table):
    """Creates table with given sql statement
    :param connection: connection
    :param sql_create_table: create player table if not exists
    """
    try:
        c = connection.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)


def create_tables(connection):
    """
    Call hte crate_table function and pass the connection and sql table to it
    :param connection: current database connection
    :return: nothing
    """
    sql_create_player_table = """ CREATE TABLE IF NOT EXISTS player (
                                        id integer PRIMARY KEY,
                                        first_name text NOT NULL,
                                        last_name text NOT NULL,
                                        gamer_name text NOT NULL,
                                        games_won text                                 
                                    ); """
    # create a database connection
    if connection is not None:
        create_table(connection, sql_create_player_table)
    else:
        print("Unable to connect")


def get_player_data(my_player):
    """
    Get the player data from the player table
    :param my_player: current player
    :return: sql results rows
    """
    global new_player
    global total_wins
    cur = connection.cursor()
    cur.execute("SELECT * FROM player WHERE first_name = (?) AND last_name = (?) AND gamer_name = (?)", my_player)
    rows = cur.fetchall()
    if rows.__len__() <= 0:
        messagebox.showinfo("Welcome")
        new_player = True
    else:
        for r in rows:
            gamer_tree.insert('', 0, text=r[0], values=(r[1], r[2], r[3], r[4]))
            if r[4] is not None:
                player.set_games_won(int(r[4]))
                total_wins = player.get_games_won()
        new_player = False
    player_first_name.set("")
    player_last_name.set("")
    player_gamer_name.set("")
    return rows


def create_new_player(player):
    """
    If the current player does not exist, create the new player by inserting them into the player table
    :param player: Current player data
    :return: last row id of current player
    """
    try:
        sql = ''' INSERT INTO player (first_name, last_name, gamer_name)
                  VALUES(?, ?, ?) '''
        cur = connection.cursor()
        cur.execute(sql, player)
    except Error as e:
        print(e)
    else:
        connection.commit()
        messagebox.showinfo("Success")
        return cur.lastrowid


def update_player_info():
    """
    Update the current players games won by updating the player table
    :return: nothing
    """
    updated_wins = player.get_games_won()
    grand_total_wins = total_wins + updated_wins
    g_name = player.get_gamer_name()
    try:
        cur = connection.cursor()
        cur.execute('UPDATE player SET games_won = (?) WHERE gamer_name = (?)', (grand_total_wins, g_name))
    except Error as e:
        print(e)
    else:
        connection.commit()
        return


if __name__ == '__main__':

    my_db = 'pythonsqlite.db'
    connection = create_connection(my_db)
    create_tables(connection)
    player = None


    def get_player_input():
        """
        Get the current players input from the GUI fields
        :return: nothing
        """
        global player
        player_f_name = player_first_name.get()
        person_l_name = player_last_name.get()
        player_g_name = player_gamer_name.get()
        # create a new player
        try:
            player = Player(str(player_f_name), str(person_l_name), str(player_g_name))
        except ValueError:
            messagebox.showinfo("Error")

        # put the player in a tuple for db
        player_tup = (player.get_first_name(), player.get_last_name(), player.get_gamer_name())
        get_player_data(player_tup)
        if new_player:
            create_new_player(player_tup)
            get_player_data(player_tup)
        return


    def current_time():
        """
        Set up the time on the GUI
        :return: nothing
        """
        global time1
        time2 = time.strftime('%H:%M:%S')
        if time2 != time1:
            time1 = time2
            clock.config(text=time2)
        clock.after(200, current_time)


    def check_for_win(choice):
        """
        This is triggered on the choice selections of rock, paper or scissors.
        It will create a new RockPaperScissors instance
        It will also check to see who won the match and update the win or loss count for player
        then call the update_player_info function and pass the wins or losses to be updated in the player table.
        :param choice: players selection from button click
        :return: nothing
        """
        global win_count
        global loss_count
        new_game = RockPaperScissors()
        computers_choice = new_game.get_random_choice()
        your_choice.set(choice.upper())
        their_choice.set(computers_choice.upper())
        if choice == computers_choice:
            messagebox.showinfo("Tie Game")
        elif choice == 'rock' and computers_choice == 'scissors':
            messagebox.showinfo("You Win")
            win_count += 1
            wins_count_label_string.set(win_count)
            player.set_games_won(win_count)
            update_player_info()
        elif choice == 'paper' and computers_choice == 'rock':
            messagebox.showinfo("You Win")
            win_count += 1
            wins_count_label_string.set(win_count)
            player.set_games_won(win_count)
            update_player_info()
        elif choice == 'scissors' and computers_choice == 'paper':
            messagebox.showinfo("You Win")
            win_count += 1
            wins_count_label_string.set(win_count)
            player.set_games_won(win_count)
            update_player_info()
        else:
            messagebox.showinfo("You lose")
            loss_count += 1
            loss_count_label_string.set(loss_count)


    game = tkinter.Tk()
    game.geometry("700x725")
    game.title('Rock Paper Scissors')
    game.configure(bg='DarkOrange')

    player_first_name = StringVar()
    player_last_name = StringVar()
    player_gamer_name = StringVar()
    time1 = ''

    wins_count_label_string = StringVar()
    loss_count_label_string = StringVar()
    win_loss_ratio_count_label_string = StringVar()
    your_choice = StringVar()
    their_choice = StringVar()
    total_games = StringVar()

    # /////////////////Get Player Info////////////////////////////////////

    player_info_label = Label(game, font=('times', 14, 'bold'), fg='Teal', bg='DarkOrange', text="Player Info") \
        .grid(row=0, column=2)

    clock = Label(game, font=('times', 10, 'bold'), fg='Teal', bg='DarkOrange')
    clock.grid(row=0, column=4)

    player_first_name_label = Label(game, font=('times', 14, 'bold'), fg='Teal', bg='DarkOrange',
                                    text="First Name: ").grid(row=1, column=1)
    Entry(game, textvariable=player_first_name).grid(row=1, column=2)

    player_last_name_label = Label(game, font=('times', 14, 'bold'), fg='Teal', bg='DarkOrange',
                                   text="Last Name: ").grid(row=2, column=1)
    Entry(game, textvariable=player_last_name).grid(row=2, column=2)

    player_gamer_name_label = Label(game, font=('times', 14, 'bold'), fg='Teal', bg='DarkOrange',
                                    text="Gamer Name: ").grid(row=3, column=1)
    Entry(game, textvariable=player_gamer_name).grid(row=3, column=2)

    submit = Button(game, text="Submit", bg='white', command=get_player_input).grid(row=4, column=2)

    # ////////////////Display the current time///////////////////////////
    blank_label_1 = Label(game, text="", bg='DarkOrange').grid(row=5, column=1)

    gamer_tree = ttk.Treeview(height=1)
    gamer_tree.grid(row=6, column=2, columnspan=2)

    gamer_tree["columns"] = ("one", "two", "three", "four")
    gamer_tree.column("#0", width=40, minwidth=20, stretch=NO)
    gamer_tree.column("one", width=100, minwidth=80, stretch=NO)
    gamer_tree.column("two", width=100, minwidth=80, stretch=NO)
    gamer_tree.column("three", width=100, minwidth=80, stretch=NO)
    gamer_tree.column("four", width=80, minwidth=60, stretch=NO)

    gamer_tree.heading("#0", text="ID", anchor=W)
    gamer_tree.heading("one", text="First Name", anchor=W)
    gamer_tree.heading("two", text="Last Name", anchor=W)
    gamer_tree.heading("three", text="Gamer Name", anchor=W)
    gamer_tree.heading("four", text="Games Won", anchor=W)

    blank_label_2 = Label(game, text="", bg='DarkOrange').grid(row=7, column=0)

    # /////////////////Game Set Up////////////////////////////////////

    game_header_label = Label(game, font=('times', 20, 'bold'), fg='white', bg='DarkOrange',
                              text="Rock Paper Scissors!").grid(row=8, column=2)

    blank_label_3 = Label(game, text="", bg='DarkOrange').grid(row=9, column=0)

    rock_button = Button(game, text="Rock", fg='Teal', bg='DarkOrange', command=lambda: check_for_win('rock'))
    rock_button.grid(row=10, column=2)

    blank_label_4 = Label(game, text="", bg='DarkOrange').grid(row=11, column=0)

    paper_button = Button(game, text="Paper", fg='Teal', bg='DarkOrange', command=lambda: check_for_win('paper'))
    paper_button.grid(row=12, column=2)

    blank_label_5 = Label(game, text="", bg='DarkOrange').grid(row=13, column=0)

    scissors_button = Button(game, text="Scissors", fg='Teal', bg='DarkOrange',
                             command=lambda: check_for_win('scissors'))
    scissors_button.grid(row=14, column=2)

    blank_label_6 = Label(game, text="", bg='DarkOrange').grid(row=15, column=0)

    game_stats_label = Label(game, text="Game Stats", font=('times', 20, 'bold'), fg='white', bg='DarkOrange') \
        .grid(row=16, column=2)

    your_move_label = Label(game, text="Your move: ", font=('times', 12, 'bold'), fg='Teal', bg='DarkOrange')
    your_move_label.grid(row=17, column=2)

    your_move_choice = Label(game, textvariable=your_choice, font=('times', 12, 'bold'), fg='white', text="",
                             bg='DarkOrange')
    your_move_choice.grid(row=18, column=2)

    comp_move_label = Label(game, text="Their move: ", font=('times', 12, 'bold'), fg='Teal', bg='DarkOrange')
    comp_move_label.grid(row=19, column=2)

    their_move_choice = tkinter.Label(game, textvariable=their_choice, font=('times', 12, 'bold'), fg='white',
                                      bg='DarkOrange')
    their_move_choice.grid(row=20, column=2)

    wins_label = Label(game, text="Wins: ", font=('times', 12, 'bold'), fg='Teal', bg='DarkOrange')
    wins_label.grid(row=21, column=2)

    wins_count_label = Label(game, textvariable=wins_count_label_string, font=('times', 12, 'bold'), fg='white',
                             text=" ", bg='DarkOrange')
    wins_count_label.grid(row=22, column=2)

    loss_label = Label(game, text="Losses: ", font=('times', 12, 'bold'), fg='Teal', bg='DarkOrange')
    loss_label.grid(row=23, column=2)

    loss_count_label = Label(game, textvariable=loss_count_label_string, font=('times', 12, 'bold'), fg='white',
                             text=" ", bg='DarkOrange')
    loss_count_label.grid(row=24, column=2)

    info = Label(game, text="Michael Harmon - 2019", font=('times', 12, 'bold'), fg='Teal',
                 bg='DarkOrange')
    info.grid(row=25, column=2)

    current_time()
    game.mainloop()
    connection.close()
    del player
