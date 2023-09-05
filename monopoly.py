import csv  # To read csv files
import itertools  # To create player loop
import json  # To convert dictionary to json for MySQL
import random  # For dice rolling
import tkinter as tk  # To create Graphical User Interface
from ctypes import windll  # To get HD Graphical User Interface

import mysql.connector as mysql  # For MySQL Connectivity
import tkextrafont  # To use custom fonts
from PIL import Image, ImageTk  # To import and create images


class Monopoly:
    def __init__(self):
        # Creating the Graphical User Interface
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("Monopoly")
        self.root.iconbitmap(default=r"textures\logo.ico")
        self.root.resizable(False, False)

        # Loading fonts
        self.big_font = tkextrafont.Font(
            file=r"fonts\big_font.ttf", family="Kabel Book", size=20
        )
        self.font = tkextrafont.Font(
            file=r"fonts\font.ttf", family="Kabel Book", size=18
        )
        self.small_font = tkextrafont.Font(
            file=r"fonts\small_font.ttf", family="Kabel Book", size=12
        )

        # Creating token list
        self.tokens = [
            r"textures\hat-token.png",
            r"textures\car-token.png",
            r"textures\ship-token.png",
            r"textures\dog-token.png",
        ]
        self.display_tokens = [
            r"textures\hat.png",
            r"textures\car.png",
            r"textures\ship.png",
            r"textures\dog.png",
        ]

        # Defining player instances
        self.player_1 = {"location": 1, "money": 1500, "properties": [], "turn": False}
        self.player_2 = {"location": 1, "money": 1500, "properties": [], "turn": False}
        self.player_3 = {"location": 1, "money": 1500, "properties": [], "turn": False}
        self.player_4 = {"location": 1, "money": 1500, "properties": [], "turn": False}

        # Setting default values
        self.importing_sql = False
        self.is_connected_sql = False

        windll.shcore.SetProcessDpiAwareness(1)
        self.menu_screen_display()

    def menu_screen_display(self):
        # Destroying game screen if exists (coming from exiting game)
        try:
            self.screen.destroy()
            self.push_sql()
        except AttributeError:
            pass

        # Loading images
        background_image = ImageTk.PhotoImage(file=r"textures\background.jpg")
        dark_bg = ImageTk.PhotoImage(file=r"textures\dark-bg.jpg")
        exit_bg = ImageTk.PhotoImage(file=r"textures\exit-bg.jpg")
        self.title_image = ImageTk.PhotoImage(file=r"textures\title.png")

        # Creating menu screen
        self.menu_screen = tk.Canvas(self.root, borderwidth=0)
        self.menu_screen.pack(fill="both", expand=True)

        # Placing elements on menu screen
        self.menu_screen.create_image(0, 0, image=background_image, anchor="nw")
        self.menu_screen.create_image(640, 50, image=self.title_image, anchor="n")
        transparent_label = tk.Label(
            self.menu_screen,
            borderwidth=0,
            image=dark_bg,
            text="PRESS ANY BUTTON TO START",
            font=self.big_font,
            fg="white",
            compound="center",
        )
        transparent_label.place(height=50, width=1276, relx=0.5, rely=0.75, anchor="n")
        exit_button = tk.Button(
            self.menu_screen,
            borderwidth=0,
            image=exit_bg,
            command=self.root.destroy,
            activebackground="#4AD9FF",
        )
        exit_button.place(height=48, width=48, x=1278, y=2, anchor="ne")

        # Sets keybinds to run on press
        self.menu_screen.bind("<KeyPress>", lambda _: self.title_screen_display())
        self.menu_screen.focus_set()

        self.root.mainloop()

    def title_screen_display(self):
        # Destroying connection screen if exists (coming from sql connection)
        try:
            self.connect_screen.destroy()
        except AttributeError:
            pass

        # Destroying menu screen if exists (coming from main menu)
        try:
            self.menu_screen.destroy()
        except AttributeError:
            pass

        # Show title screen
        self.title_screen = tk.Frame(self.root, bg="#2A363B")
        self.title_screen.pack(fill="both", expand=True)

        # Importing neccesary images
        self.button_image = ImageTk.PhotoImage(file=r"textures\button.png")
        self.save_button = ImageTk.PhotoImage(file=r"textures\save.png")
        mysql_button_image = ImageTk.PhotoImage(file=r"textures\mysql.png")

        # Creating elements on title screen
        saves_select = tk.Label(
            self.title_screen,
            borderwidth=0,
            font=self.big_font,
            text="Save Select",
            bg="#2A363B",
            fg="white",
        )
        saves_select.place(relx=0.5, y=162.5, height=53, anchor="n")
        title = tk.Label(
            self.title_screen, image=self.title_image, borderwidth=0, bg="#2A363B"
        )
        title.place(relx=0.5, y=50, anchor="n")
        mysql_button = tk.Button(
            self.title_screen,
            borderwidth=0,
            image=mysql_button_image,
            bg="#2A363B",
            activebackground="#2A363B",
            command=self.connect_sql_screen,
        )
        mysql_button.place(x=1255, y=25, anchor="ne")
        offline_button = tk.Button(
            self.title_screen,
            borderwidth=0,
            text="PLAY\nWITHOUT\nMySQL",
            font=self.small_font,
            compound="center",
            image=self.save_button,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: (
                setattr(self, "save", None),
                setattr(self, "importing_sql", False),
                self.player_select_screen(),
            ),
        )
        offline_button.place(x=25, y=25, anchor="nw")

        # Creating save select displays
        self.save_1_label = tk.Label(
            self.title_screen,
            borderwidth=0,
            font=self.font,
            text="Save 1",
            bg="#2A363B",
            fg="white",
        )
        self.save_1_label.place(x=260, y=303.5, anchor="center")
        self.save_1_button = tk.Button(
            self.title_screen,
            borderwidth=0,
            text="1",
            font=self.big_font,
            compound="center",
            image=self.save_button,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: self.select_save(1),
        )
        self.save_1_button.place(x=188, y=353.5, anchor="nw")
        self.save_2_label = tk.Label(
            self.title_screen,
            borderwidth=0,
            font=self.font,
            text="Save 2",
            bg="#2A363B",
            fg="white",
        )
        self.save_2_label.place(x=516, y=303.5, anchor="center")
        self.save_2_button = tk.Button(
            self.title_screen,
            borderwidth=0,
            text="2",
            font=self.big_font,
            compound="center",
            image=self.save_button,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: self.select_save(2),
        )
        self.save_2_button.place(x=444, y=353.5, anchor="nw")
        self.save_3_label = tk.Label(
            self.title_screen,
            borderwidth=0,
            font=self.font,
            text="Save 3",
            bg="#2A363B",
            fg="white",
        )
        self.save_3_label.place(x=780, y=303.5, anchor="center")
        self.save_3_button = tk.Button(
            self.title_screen,
            borderwidth=0,
            text="3",
            font=self.big_font,
            compound="center",
            image=self.save_button,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: self.select_save(3),
        )
        self.save_3_button.place(x=708, y=353.5, anchor="nw")
        self.save_4_label = tk.Label(
            self.title_screen,
            borderwidth=0,
            font=self.font,
            text="Save 4",
            bg="#2A363B",
            fg="white",
        )
        self.save_4_label.place(x=1036, y=303.5, anchor="center")
        self.save_4_button = tk.Button(
            self.title_screen,
            borderwidth=0,
            text="4",
            font=self.big_font,
            compound="center",
            image=self.save_button,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: self.select_save(4),
        )
        self.save_4_button.place(x=964, y=353.5, anchor="nw")

        self.root.mainloop()

    def select_save(self, save):
        # Destorys select, delete and error label button if exists
        try:
            self.select_button.destroy()
            self.delete_button.destroy()
        except AttributeError:
            pass
        try:
            self.not_connected_label.destroy()
        except AttributeError:
            pass

        # Displays error message if mysql not connected
        if not self.is_connected_sql:
            self.not_connected_label = tk.Label(
                self.title_screen,
                borderwidth=0,
                text="MySQL Not Connected",
                font=self.font,
                bg="#2A363B",
                fg="white",
            )
            self.not_connected_label.place(relx=0.5, y=670, anchor="s")
        else:
            # Resets save buttons in case one is already selected
            self.save_1_button.config(text="1", image=self.save_button)
            self.save_2_button.config(text="2", image=self.save_button)
            self.save_3_button.config(text="3", image=self.save_button)
            self.save_4_button.config(text="4", image=self.save_button)

            selected_save_image = ImageTk.PhotoImage(file=r"textures\selected-save.png")
            self.save = save

            # Indicating that current save has been selected
            match self.save:
                case 1:
                    self.save_1_button.config(text="", image=selected_save_image)
                case 2:
                    self.save_2_button.config(text="", image=selected_save_image)
                case 3:
                    self.save_3_button.config(text="", image=selected_save_image)
                case 4:
                    self.save_4_button.config(text="", image=selected_save_image)

            # Displays select and delete button if save file exists
            if self.save_exists():
                self.select_button = tk.Button(
                    self.title_screen,
                    borderwidth=0,
                    text="SELECT",
                    font=self.font,
                    compound="center",
                    image=self.button_image,
                    bg="#2A363B",
                    activebackground="#2A363B",
                    command=self.import_sql,
                )
                self.select_button.place(
                    x=512.5, y=670, width=170, height=62, anchor="s"
                )
                self.delete_button = tk.Button(
                    self.title_screen,
                    borderwidth=0,
                    text="DELETE",
                    font=self.font,
                    compound="center",
                    image=self.button_image,
                    bg="#2A363B",
                    activebackground="#2A363B",
                    command=self.delete_save,
                )
                self.delete_button.place(
                    x=767.5, y=670, width=170, height=62, anchor="s"
                )
            else:
                self.select_button = tk.Button(
                    self.title_screen,
                    borderwidth=0,
                    text="CREATE",
                    font=self.font,
                    compound="center",
                    image=self.button_image,
                    bg="#2A363B",
                    activebackground="#2A363B",
                    command=lambda: (
                        self.player_select_screen(),
                        setattr(self, "importing_sql", False),
                    ),
                )
                self.select_button.place(
                    relx=0.5, y=670, width=170, height=62, anchor="s"
                )

        self.root.mainloop()

    def connect_sql_screen(self):
        # Destroys title screen and creates connection screen
        self.title_screen.destroy()
        self.connect_screen = tk.Frame(self.root, bg="#2A363B")
        self.connect_screen.pack(fill="both", expand=True)
        back_image = ImageTk.PhotoImage(file=r"textures\back.png")

        # Creating elements on connect screen
        self.connect_label = tk.Label(
            self.connect_screen,
            borderwidth=0,
            font=self.big_font,
            text="MySQL Connection",
            bg="#2A363B",
            fg="white",
        )
        self.connect_label.place(relx=0.5, y=150, height=53, anchor="n")
        title = tk.Label(
            self.connect_screen, image=self.title_image, borderwidth=0, bg="#2A363B"
        )
        title.place(relx=0.5, y=50, anchor="n")
        self.save_connection_button = tk.Button(
            self.connect_screen,
            borderwidth=0,
            text="SAVE",
            font=self.font,
            compound="center",
            image=self.button_image,
            bg="#2A363B",
            activebackground="#2A363B",
            command=self.connect_sql,
        )
        self.save_connection_button.place(
            relx=0.5, y=670, width=170, height=62, anchor="s"
        )
        self.exit_button = tk.Button(
            self.connect_screen,
            borderwidth=0,
            bg="#2A363B",
            activebackground="#2A363B",
            image=back_image,
            command=self.title_screen_display,
        )
        self.exit_button.place(x=25, y=25, anchor="nw")

        # Creating input entries and labels
        host_label = tk.Label(
            self.connect_screen,
            borderwidth=0,
            font=self.font,
            text="Host:",
            bg="#2A363B",
            fg="white",
        )
        host_label.place(relx=0.5, y=230, width=144, height=45, anchor="ne")
        self.host_entry = tk.Entry(
            self.connect_screen,
            borderwidth=0,
            font=self.font,
            justify="center",
            fg="black",
        )
        self.host_entry.place(relx=0.5, y=230, width=144, height=45, anchor="nw")
        self.host_entry.insert(0, "localhost")
        port_label = tk.Label(
            self.connect_screen,
            borderwidth=0,
            font=self.font,
            text="Port:",
            bg="#2A363B",
            fg="white",
        )
        port_label.place(relx=0.5, y=305, width=144, height=45, anchor="ne")
        self.port_entry = tk.Entry(
            self.connect_screen,
            borderwidth=0,
            font=self.font,
            justify="center",
            fg="black",
        )
        self.port_entry.place(relx=0.5, y=305, width=144, height=45, anchor="nw")
        self.port_entry.insert(0, "3306")
        db_label = tk.Label(
            self.connect_screen,
            borderwidth=0,
            font=self.font,
            text="Database:",
            bg="#2A363B",
            fg="white",
        )
        db_label.place(relx=0.475, y=380, width=144, height=45, anchor="ne")
        self.db_entry = tk.Entry(
            self.connect_screen,
            borderwidth=0,
            font=self.font,
            justify="center",
            fg="black",
        )
        self.db_entry.place(relx=0.5, y=380, width=144, height=45, anchor="nw")
        user_label = tk.Label(
            self.connect_screen,
            borderwidth=0,
            font=self.font,
            text="Username:",
            bg="#2A363B",
            fg="white",
        )
        user_label.place(relx=0.475, y=455, width=144, height=45, anchor="ne")
        self.user_entry = tk.Entry(
            self.connect_screen,
            borderwidth=0,
            font=self.font,
            justify="center",
            fg="black",
        )
        self.user_entry.place(relx=0.5, y=455, width=144, height=45, anchor="nw")
        self.user_entry.insert(0, "root")
        pass_label = tk.Label(
            self.connect_screen,
            borderwidth=0,
            font=self.font,
            text="Password:",
            bg="#2A363B",
            fg="white",
        )
        pass_label.place(relx=0.475, y=530, width=144, height=45, anchor="ne")
        self.pass_entry = tk.Entry(
            self.connect_screen,
            borderwidth=0,
            font=self.font,
            justify="center",
            show="*",
            fg="black",
        )
        self.pass_entry.place(relx=0.5, y=530, width=144, height=45, anchor="nw")
        self.root.mainloop()

    def connect_sql(self):
        # Creating dicitonary with connection values
        connect_info = {
            "host": self.host_entry.get(),
            "port": self.port_entry.get(),
            "database": self.db_entry.get(),
            "user": self.user_entry.get(),
            "password": self.pass_entry.get(),
        }
        self.db = None

        # Displays error if any field is empty
        if not all(connect_info.values()):
            self.connect_label.configure(text="Please fill in all the required fields")
            return

        # Connects to MySQL
        try:
            self.db = mysql.connect(**connect_info)
            self.cursor = self.db.cursor()

            # Creates monopoly table and inserts valyes
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS monopoly (save INT PRIMARY KEY, players JSON)"
            )
            self.cursor.executemany(
                "INSERT IGNORE INTO monopoly (save, players) VALUES (%s, %s)",
                [(1, "{}"), (2, "{}"), (3, "{}"), (4, "{}")],
            )
            self.db.commit()

            # MySQL is now connected
            self.is_connected_sql = True
            self.title_screen_display()
        except mysql.Error:
            self.is_connected_sql = False
            self.connect_label.configure(text="Error connecting to the database")

    def save_exists(self):
        # Checks if save exists and returns value accordingly
        self.cursor.execute(
            "SELECT COUNT(*) FROM monopoly WHERE save = %s AND JSON_LENGTH(players) != 0",
            (self.save,),
        )
        existing_save = bool(self.cursor.fetchone()[0])
        return existing_save

    def push_sql(self):
        # Makes player dictionary ready for json conversion
        for player in (self.player_1, self.player_2, self.player_3, self.player_4):
            player["token_image"] = None
            player["token_display_image"] = None
            for prop in player["properties"]:
                prop["owned_by"] = None

        try:
            self.player_1["token_index"] = self.player_1_index
            self.player_2["token_index"] = self.player_2_index
            self.player_3["token_index"] = self.player_3_index
            self.player_4["token_index"] = self.player_4_index
        except AttributeError:
            pass

        players_json = json.dumps(
            {1: self.player_1, 2: self.player_2, 3: self.player_3, 4: self.player_4}
        )

        # Updating the player json in MySQL
        self.cursor.execute(
            "UPDATE monopoly SET players = %s WHERE save = %s",
            (players_json, self.save),
        )
        self.db.commit()

    def import_sql(self):
        self.importing_sql = True

        # Retrieving data from MySQL
        self.cursor.execute(
            "SELECT players FROM monopoly where save = %s", (self.save,)
        )
        players_dict = json.loads(self.cursor.fetchall()[0][0])

        # Assigning data to attributes
        self.player_1 = players_dict["1"]
        self.player_2 = players_dict["2"]
        self.player_3 = players_dict["3"]
        self.player_4 = players_dict["4"]

        for player in (self.player_1, self.player_2, self.player_3, self.player_4):
            player["token_image"] = ImageTk.PhotoImage(
                file=self.tokens[player["token_index"]]
            )
            player["token_display_image"] = ImageTk.PhotoImage(
                file=self.display_tokens[player["token_index"]]
            )
            for prop in player["properties"]:
                prop["coords"] = tuple(prop["coords"])
                prop["owned_by"] = player

        self.start_game()

    def delete_save(self):
        # Deleting the player json in MySQL
        self.cursor.execute(
            "UPDATE monopoly SET players = %s WHERE save = %s",
            ("{}", self.save),
        )
        self.db.commit()

        # Changes the orientation of the buttons
        self.delete_button.destroy()
        self.select_button.destroy()
        self.select_button = tk.Button(
            self.title_screen,
            borderwidth=0,
            text="SELECT",
            font=self.font,
            compound="center",
            image=self.button_image,
            bg="#2A363B",
            activebackground="#2A363B",
            command=self.player_select_screen,
        )
        self.select_button.place(relx=0.5, y=670, width=170, height=62, anchor="s")

    def player_select_screen(self):
        # Destroy title screen
        self.title_screen.destroy()

        # Show select screen
        self.select_screen = tk.Frame(self.root, bg="#2A363B")
        self.select_screen.pack(fill="both", expand=True)

        # Importing neccesary images
        right_image = ImageTk.PhotoImage(file=r"textures\right-arrow.png")
        left_image = ImageTk.PhotoImage(file=r"textures\left-arrow.png")

        # Creating elements on select screen
        title = tk.Label(
            self.select_screen, image=self.title_image, borderwidth=0, bg="#2A363B"
        )
        title.place(relx=0.5, y=50, anchor="n")
        player_select = tk.Label(
            self.select_screen,
            borderwidth=0,
            font=self.big_font,
            text="Player Select",
            bg="#2A363B",
            fg="white",
        )
        player_select.place(x=532, y=162.5, width=216, height=53, anchor="nw")
        start_button = tk.Button(
            self.select_screen,
            borderwidth=0,
            text="START",
            font=self.font,
            compound="center",
            image=self.button_image,
            bg="#2A363B",
            activebackground="#2A363B",
            command=self.start_game,
        )
        start_button.place(relx=0.5, y=670, width=170, height=62, anchor="s")

        # Getting player choices
        self.player_1_index = 0
        self.player_1_image = ImageTk.PhotoImage(file=self.display_tokens[0])
        self.player_1_image_label = tk.Label(
            self.select_screen,
            borderwidth=0,
            image=self.player_1_image,
            bg="#2A363B",
        )
        self.player_1_image_label.place(x=188, y=393.5, anchor="nw")
        self.player_1_entry = tk.Entry(
            self.select_screen,
            borderwidth=0,
            font=self.font,
            justify="center",
            fg="grey",
        )
        self.player_1_entry.place(x=260, y=303.5, width=144, height=45, anchor="center")
        self.player_1_entry.insert(0, "Player 1")
        self.player_1_entry.bind(
            "<FocusIn>",
            lambda _: (
                self.player_1_entry.delete(0, tk.END),
                self.player_1_entry.configure(fg="black"),
            )
            if self.player_1_entry.get() == "Player 1"
            else None,
        )
        self.player_1_entry.bind(
            "<FocusOut>",
            lambda _: (
                self.player_1_entry.insert(0, "Player 1"),
                self.player_1_entry.configure(fg="grey"),
            )
            if self.player_1_entry.get() == ""
            else None,
        )
        player_1_left = tk.Button(
            self.select_screen,
            borderwidth=0,
            image=left_image,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: self.prev_token(1),
        )
        player_1_left.place(x=140, y=441.5, anchor="nw")
        player_1_right = tk.Button(
            self.select_screen,
            borderwidth=0,
            image=right_image,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: self.next_token(1),
        )
        player_1_right.place(x=332, y=441.5, anchor="nw")

        self.player_2_index = 1
        self.player_2_image = ImageTk.PhotoImage(file=self.display_tokens[1])
        self.player_2_image_label = tk.Label(
            self.select_screen,
            borderwidth=0,
            image=self.player_2_image,
            bg="#2A363B",
        )
        self.player_2_image_label.place(x=444, y=393.5, anchor="nw")
        self.player_2_entry = tk.Entry(
            self.select_screen,
            borderwidth=0,
            font=self.font,
            justify="center",
            fg="grey",
        )
        self.player_2_entry.place(x=516, y=303.5, width=144, height=45, anchor="center")
        self.player_2_entry.insert(0, "Player 2")
        self.player_2_entry.bind(
            "<FocusIn>",
            lambda _: (
                self.player_2_entry.delete(0, tk.END),
                self.player_2_entry.configure(fg="black"),
            )
            if self.player_2_entry.get() == "Player 2"
            else None,
        )
        self.player_2_entry.bind(
            "<FocusOut>",
            lambda _: (
                self.player_2_entry.insert(0, "Player 2"),
                self.player_2_entry.configure(fg="grey"),
            )
            if self.player_2_entry.get() == ""
            else None,
        )
        player_2_left = tk.Button(
            self.select_screen,
            borderwidth=0,
            image=left_image,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: self.prev_token(2),
        )
        player_2_left.place(x=396, y=441.5, anchor="nw")
        player_2_right = tk.Button(
            self.select_screen,
            borderwidth=0,
            image=right_image,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: self.next_token(2),
        )
        player_2_right.place(x=588, y=441.5, anchor="nw")

        self.player_3_index = 2
        self.player_3_image = ImageTk.PhotoImage(file=self.display_tokens[2])
        self.player_3_image_label = tk.Label(
            self.select_screen,
            borderwidth=0,
            image=self.player_3_image,
            bg="#2A363B",
        )
        self.player_3_image_label.place(x=708, y=393.5, anchor="nw")
        self.player_3_entry = tk.Entry(
            self.select_screen,
            borderwidth=0,
            font=self.font,
            justify="center",
            fg="grey",
        )
        self.player_3_entry.place(x=780, y=303.5, width=144, height=45, anchor="center")
        self.player_3_entry.insert(0, "Player 3")
        self.player_3_entry.bind(
            "<FocusIn>",
            lambda _: (
                self.player_3_entry.delete(0, tk.END),
                self.player_3_entry.configure(fg="black"),
            )
            if self.player_3_entry.get() == "Player 3"
            else None,
        )
        self.player_3_entry.bind(
            "<FocusOut>",
            lambda _: (
                self.player_3_entry.insert(0, "Player 3"),
                self.player_3_entry.configure(fg="grey"),
            )
            if self.player_3_entry.get() == ""
            else None,
        )
        player_3_left = tk.Button(
            self.select_screen,
            borderwidth=0,
            image=left_image,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: self.prev_token(3),
        )
        player_3_left.place(x=660, y=441.5, anchor="nw")
        player_3_right = tk.Button(
            self.select_screen,
            borderwidth=0,
            image=right_image,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: self.next_token(3),
        )
        player_3_right.place(x=852, y=441.5, anchor="nw")

        self.player_4_index = 3
        self.player_4_image = ImageTk.PhotoImage(file=self.display_tokens[3])
        self.player_4_image_label = tk.Label(
            self.select_screen,
            borderwidth=0,
            image=self.player_4_image,
            bg="#2A363B",
        )
        self.player_4_image_label.place(x=964, y=393.5, anchor="nw")
        self.player_4_entry = tk.Entry(
            self.select_screen,
            borderwidth=0,
            font=self.font,
            justify="center",
            fg="grey",
        )
        self.player_4_entry.place(
            x=1036, y=303.5, width=144, height=45, anchor="center"
        )
        self.player_4_entry.insert(0, "Player 4")
        self.player_4_entry.bind(
            "<FocusIn>",
            lambda _: (
                self.player_4_entry.delete(0, tk.END),
                self.player_4_entry.configure(fg="black"),
            )
            if self.player_4_entry.get() == "Player 4"
            else None,
        )
        self.player_4_entry.bind(
            "<FocusOut>",
            lambda _: (
                self.player_4_entry.insert(0, "Player 4"),
                self.player_4_entry.configure(fg="grey"),
            )
            if self.player_4_entry.get() == ""
            else None,
        )
        player_4_left = tk.Button(
            self.select_screen,
            borderwidth=0,
            image=left_image,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: self.prev_token(4),
        )
        player_4_left.place(x=916, y=441.5, anchor="nw")
        player_4_right = tk.Button(
            self.select_screen,
            borderwidth=0,
            image=right_image,
            bg="#2A363B",
            activebackground="#2A363B",
            command=lambda: self.next_token(4),
        )
        player_4_right.place(x=1108, y=441.5, anchor="nw")

        self.root.mainloop()

    def next_token(self, num):
        # Going to next token image
        match num:
            case 1:
                self.player_1_index = (self.player_1_index + 1) % 4
                self.player_1_image = ImageTk.PhotoImage(
                    file=self.display_tokens[self.player_1_index]
                )
                self.player_1_image_label.config(image=self.player_1_image)
            case 2:
                self.player_2_index = (self.player_2_index + 1) % 4
                self.player_2_image = ImageTk.PhotoImage(
                    file=self.display_tokens[self.player_2_index]
                )
                self.player_2_image_label.config(image=self.player_2_image)
            case 3:
                self.player_3_index = (self.player_3_index + 1) % 4
                self.player_3_image = ImageTk.PhotoImage(
                    file=self.display_tokens[self.player_3_index]
                )
                self.player_3_image_label.config(image=self.player_3_image)
            case 4:
                self.player_4_index = (self.player_4_index + 1) % 4
                self.player_4_image = ImageTk.PhotoImage(
                    file=self.display_tokens[self.player_4_index]
                )
                self.player_4_image_label.config(image=self.player_4_image)

    def prev_token(self, num):
        # Going to previous token image
        match num:
            case 1:
                self.player_1_index = (self.player_1_index + 3) % 4
                self.player_1_image = ImageTk.PhotoImage(
                    file=self.display_tokens[self.player_1_index]
                )
                self.player_1_image_label.config(image=self.player_1_image)
            case 2:
                self.player_2_index = (self.player_2_index + 3) % 4
                self.player_2_image = ImageTk.PhotoImage(
                    file=self.display_tokens[self.player_2_index]
                )
                self.player_2_image_label.config(image=self.player_2_image)
            case 3:
                self.player_3_index = (self.player_3_index + 3) % 4
                self.player_3_image = ImageTk.PhotoImage(
                    file=self.display_tokens[self.player_3_index]
                )
                self.player_3_image_label.config(image=self.player_3_image)
            case 4:
                self.player_4_index = (self.player_4_index + 3) % 4
                self.player_4_image = ImageTk.PhotoImage(
                    file=self.display_tokens[self.player_4_index]
                )
                self.player_4_image_label.config(image=self.player_4_image)

    def start_game(self):
        # Assigning names to players
        try:
            self.player_1["name"] = self.player_1_entry.get()
            self.player_2["name"] = self.player_2_entry.get()
            self.player_3["name"] = self.player_3_entry.get()
            self.player_4["name"] = self.player_4_entry.get()
            self.select_screen.destroy()
        except:
            pass
        try:
            self.title_screen.destroy()
        except AttributeError:
            pass

        # Restets player info if creating new game
        try:
            if not self.save_exists():
                for player in (
                    self.player_1,
                    self.player_2,
                    self.player_3,
                    self.player_4,
                ):
                    player["location"] = 1
                    player["money"] = 1500
                    player["properties"] = []
                    player["turn"] = False
                self.importing_sql = False
        except AttributeError:
            pass

        # Creating game screen
        self.screen = tk.Frame(self.root, background="black")
        self.screen.pack(fill="both", expand=True)

        # Importing and placing the board
        board_image = ImageTk.PhotoImage(file=r"textures\board.png")
        self.board = tk.Canvas(self.screen, borderwidth=0, highlightthickness=0)
        self.board.place(width=720, height=717, anchor="nw")
        self.board.create_image(0, 0, image=board_image, anchor="nw")
        button_background_image = ImageTk.PhotoImage(
            Image.new("RGB", (560, 720), "#CA7264")
        )
        button_background = tk.Label(
            self.screen,
            image=button_background_image,
            borderwidth=0,
        )
        button_background.place(relx=1, rely=0, anchor="ne")

        # Loading some images
        self.close_player_button_image = ImageTk.PhotoImage(file=r"textures\close.png")
        self.dice_image = ImageTk.PhotoImage(file=r"textures\dice.png")
        exit_image = ImageTk.PhotoImage(file=r"textures\exit.png")

        # Creating exit button
        exit_button = tk.Button(
            self.screen,
            borderwidth=0,
            bg="#CA7264",
            activebackground="#CA7264",
            image=exit_image,
            command=self.menu_screen_display,
        )
        exit_button.place(relx=1, anchor="ne")

        # Loading dice images
        self.dice_1_image = ImageTk.PhotoImage(file=r"textures\dice-1.png")
        self.dice_2_image = ImageTk.PhotoImage(file=r"textures\dice-2.png")
        self.dice_3_image = ImageTk.PhotoImage(file=r"textures\dice-3.png")
        self.dice_4_image = ImageTk.PhotoImage(file=r"textures\dice-4.png")
        self.dice_5_image = ImageTk.PhotoImage(file=r"textures\dice-5.png")
        self.dice_6_image = ImageTk.PhotoImage(file=r"textures\dice-6.png")

        # Assigning tokens to players
        try:
            self.player_1["token_display_image"] = self.player_1_image
            self.player_1["token_image"] = ImageTk.PhotoImage(
                file=self.tokens[self.player_1_index]
            )
            self.player_2["token_display_image"] = self.player_2_image
            self.player_2["token_image"] = ImageTk.PhotoImage(
                file=self.tokens[self.player_2_index]
            )
            self.player_3["token_display_image"] = self.player_3_image
            self.player_3["token_image"] = ImageTk.PhotoImage(
                file=self.tokens[self.player_3_index]
            )
            self.player_4["token_display_image"] = self.player_4_image
            self.player_4["token_image"] = ImageTk.PhotoImage(
                file=self.tokens[self.player_4_index]
            )
        except AttributeError:
            pass

        # Creating card instances and assigning unique values
        self.chance_list = []
        self.chest_list = []
        with open(r"cards.csv", "r", newline="") as file:
            for card_info in csv.reader(file):
                card_instance = {}
                card_instance["group"] = card_info[0]
                card_instance["function"] = card_info[1]
                card_instance["value"] = card_info[2]
                card_instance["name"] = card_info[3]
                match card_instance["group"]:
                    case "c":
                        self.chance_list.append(card_instance)
                    case "cc":
                        self.chest_list.append(card_instance)
        random.shuffle(self.chance_list)
        random.shuffle(self.chest_list)

        # Creating property instances and assigning unique values
        self.property_locations = {}
        property_locations_list = itertools.cycle(range(1, 41))
        with open(r"properties.csv", "r", newline="") as file:
            for property_info in csv.reader(file):
                property_instance = {"owned_by": None}
                self.property_locations[
                    next(property_locations_list)
                ] = property_instance
                property_instance["name"] = property_info[0]
                property_instance["price"] = int(property_info[1])
                property_instance["colour"] = property_info[2]
                property_instance["coords"] = eval(property_info[3])

        # Creating info buttons for each player and displaying token
        p1_token_display = tk.Label(
            self.screen,
            image=self.player_1["token_display_image"],
            borderwidth=0,
            bg="#CA7264",
        )
        p1_token_display.place(x=804, y=20, anchor="nw")
        p1_button = tk.Button(
            self.screen,
            text=self.player_1["name"],
            font=self.font,
            compound="center",
            image=self.button_image,
            bg="#CA7264",
            activebackground="#CA7264",
            borderwidth=0,
            command=lambda: self.display_player_info(self.player_1),
        )
        p1_button.place(width=170, height=62, x=786, y=140, anchor="nw")
        player_1_money_token = tk.Label(
            self.screen,
            image=self.player_1["token_image"],
            borderwidth=0,
            bg="#CA7264",
        )
        player_1_money_token.place(x=775, y=500, anchor="nw")
        self.player_1_money = tk.Label(
            self.screen,
            text=": $1500",
            borderwidth=0,
            font=self.font,
            bg="#CA7264",
        )
        self.player_1_money.place(x=830, y=508, anchor="nw")

        p2_token_display = tk.Label(
            self.screen,
            image=self.player_2["token_display_image"],
            borderwidth=0,
            bg="#CA7264",
        )
        p2_token_display.place(x=1080, y=17, anchor="nw")
        p2_button = tk.Button(
            self.screen,
            text=self.player_2["name"],
            font=self.font,
            compound="center",
            image=self.button_image,
            bg="#CA7264",
            activebackground="#CA7264",
            borderwidth=0,
            command=lambda: self.display_player_info(self.player_2),
        )
        p2_button.place(width=170, height=62, x=1224, y=140, anchor="ne")
        player_2_money_token = tk.Label(
            self.screen,
            image=self.player_2["token_image"],
            borderwidth=0,
            bg="#CA7264",
        )
        player_2_money_token.place(x=775, y=548, anchor="nw")
        self.player_2_money = tk.Label(
            self.screen,
            text=": $1500",
            borderwidth=0,
            font=self.font,
            bg="#CA7264",
        )
        self.player_2_money.place(x=830, y=556, anchor="nw")

        p3_token_display = tk.Label(
            self.screen,
            image=self.player_3["token_display_image"],
            borderwidth=0,
            bg="#CA7264",
        )
        p3_token_display.place(x=804, y=222, anchor="nw")
        p3_button = tk.Button(
            self.screen,
            text=self.player_3["name"],
            font=self.font,
            compound="center",
            image=self.button_image,
            bg="#CA7264",
            activebackground="#CA7264",
            borderwidth=0,
            command=lambda: self.display_player_info(self.player_3),
        )
        p3_button.place(width=170, height=62, x=786, y=350, anchor="nw")
        player_3_money_token = tk.Label(
            self.screen,
            image=self.player_3["token_image"],
            borderwidth=0,
            bg="#CA7264",
        )
        player_3_money_token.place(x=775, y=596, anchor="nw")
        self.player_3_money = tk.Label(
            self.screen,
            text=": $1500",
            borderwidth=0,
            font=self.font,
            bg="#CA7264",
        )
        self.player_3_money.place(x=830, y=604, anchor="nw")

        p4_token_display = tk.Label(
            self.screen,
            image=self.player_4["token_display_image"],
            borderwidth=0,
            bg="#CA7264",
        )
        p4_token_display.place(x=1076, y=230, anchor="nw")
        p4_button = tk.Button(
            self.screen,
            text=self.player_4["name"],
            font=self.font,
            compound="center",
            image=self.button_image,
            bg="#CA7264",
            activebackground="#CA7264",
            borderwidth=0,
            command=lambda: self.display_player_info(self.player_4),
        )
        p4_button.place(width=170, height=62, x=1224, y=350, anchor="ne")
        player_4_money_token = tk.Label(
            self.screen,
            image=self.player_4["token_image"],
            borderwidth=0,
            bg="#CA7264",
        )
        player_4_money_token.place(x=775, y=644, anchor="nw")
        self.player_4_money = tk.Label(
            self.screen,
            text=": $1500",
            borderwidth=0,
            font=self.font,
            bg="#CA7264",
        )
        self.player_4_money.place(x=830, y=652, anchor="nw")

        if not self.importing_sql:
            # Placing players on board
            self.player_1["token"] = self.board.create_image(
                651, 650, image=self.player_1["token_image"], anchor="center"
            )
            self.player_2["token"] = self.board.create_image(
                651, 695, image=self.player_2["token_image"], anchor="center"
            )
            self.player_3["token"] = self.board.create_image(
                696, 650, image=self.player_3["token_image"], anchor="center"
            )
            self.player_4["token"] = self.board.create_image(
                696, 695, image=self.player_4["token_image"], anchor="center"
            )

            # Creating player turn loop
            self.player_loop = itertools.cycle(
                [self.player_1, self.player_2, self.player_3, self.player_4]
            )
            self.player_turn_init(next(self.player_loop))
        else:
            # Placing players on board
            x1, y1 = self.property_locations[self.player_1["location"]]["coords"]
            self.player_1["token"] = self.board.create_image(
                x1, y1, image=self.player_1["token_image"], anchor="center"
            )
            x2, y2 = self.property_locations[self.player_2["location"]]["coords"]
            self.player_2["token"] = self.board.create_image(
                x2, y2, image=self.player_2["token_image"], anchor="center"
            )
            x3, y3 = self.property_locations[self.player_3["location"]]["coords"]
            self.player_3["token"] = self.board.create_image(
                x3, y3, image=self.player_3["token_image"], anchor="center"
            )
            x4, y4 = self.property_locations[self.player_4["location"]]["coords"]
            self.player_4["token"] = self.board.create_image(
                x4, y4, image=self.player_4["token_image"], anchor="center"
            )

            # Updating money labels
            self.player_1_money.configure(text=f": ${self.player_1['money']}")
            self.player_2_money.configure(text=f": ${self.player_2['money']}")
            self.player_3_money.configure(text=f": ${self.player_3['money']}")
            self.player_4_money.configure(text=f": ${self.player_4['money']}")

            player_order_stack = []
            player_list = [self.player_4, self.player_3, self.player_2, self.player_1]
            for player in (self.player_1, self.player_2, self.player_3, self.player_4):
                player_list.pop()
                if player["turn"]:
                    # Creating player turn loop
                    self.player_loop = itertools.cycle(
                        [player, *player_list[::-1], *player_order_stack]
                    )
                    self.player_turn_init(next(self.player_loop))
                else:
                    player_order_stack.append(player)

        self.root.mainloop()

    def display_player_info(self, player):
        # Try destroying info screen if already exists
        try:
            self.player_info.destroy()
            self.close_player_button.destroy()
        except AttributeError:
            pass

        # Shows player info after player button is clicked
        player_info_text = f"{player['name']}\n${player['money']}\n\n"
        player_info_text += "\n".join([title["name"] for title in player["properties"]])

        self.player_info = tk.Label(
            self.screen,
            text=player_info_text,
            borderwidth=0,
            font=self.small_font,
            bg="#B9CEB5",
        )
        self.player_info.place(height=280, width=250, x=360, y=360, anchor="center")

        # Shows player info close button
        self.close_player_button = tk.Button(
            self.screen,
            borderwidth=0,
            image=self.close_player_button_image,
            bg="#B9CEB5",
            activebackground="#B9CEB5",
            command=lambda: (
                self.player_info.destroy(),
                self.close_player_button.destroy(),
            ),
        )
        self.close_player_button.place(x=460, y=245, anchor="center")

    def player_turn_init(self, player):
        self.current_player = player
        self.current_player["turn"] = True

        # Showing current player's turn
        current_player_display = tk.Label(
            self.screen,
            text=f"{self.current_player['name']}'s Turn",
            font=self.big_font,
            borderwidth=0,
            bg="#CA7264",
        )
        current_player_display.place(
            width=560, height=60, x=1000, y=460, anchor="center"
        )

        # Setting up dice and end turn button for current player
        dice_button = tk.Button(
            self.screen,
            image=self.dice_image,
            borderwidth=0,
            bg="#CA7264",
            activebackground="#CA7264",
            command=lambda: (
                self.end_turn_display(),
                self.player_turn(),
                dice_button.destroy(),
            ),
        )
        dice_button.place(x=1032, y=532, anchor="nw")

    def end_turn_display(self):
        self.end_turn_button = tk.Button(
            self.screen,
            text="END TURN",
            font=self.font,
            borderwidth=0,
            compound="center",
            image=self.button_image,
            bg="#CA7264",
            activebackground="#CA7264",
            command=lambda: (self.end_turn_func(), self.end_turn_button.destroy()),
        )
        self.end_turn_button.place(width=170, height=62, x=1012, y=615, anchor="nw")

    def dice_display(self, dice_1, dice_2):
        # Displayng dice images based on result
        dice_images = {
            1: self.dice_1_image,
            2: self.dice_2_image,
            3: self.dice_3_image,
            4: self.dice_4_image,
            5: self.dice_5_image,
            6: self.dice_6_image,
        }
        self.dice_1_display = tk.Label(
            self.screen, image=dice_images[dice_1], borderwidth=0, bg="#CCE3C7"
        )
        self.dice_1_display.place(x=360, y=560, anchor="e")
        self.dice_2_display = tk.Label(
            self.screen, image=dice_images[dice_2], borderwidth=0, bg="#CCE3C7"
        )
        self.dice_2_display.place(x=372, y=560, anchor="w")

    def player_turn(self):
        # Rolling the dice
        dice_1 = random.randint(1, 6)
        dice_2 = random.randint(1, 6)
        self.roll_no = dice_1 + dice_2
        self.dice_display(dice_1, dice_2)

        # Setting player locations and displaying player landing
        if self.current_player["location"] + self.roll_no > 40:
            roll_difference = 40 - (self.current_player["location"] + self.roll_no)
            self.current_player["location"] = -roll_difference
            self.salary_display = tk.Label(
                self.screen,
                text=f"{self.current_player['name']} Got $200 in salary",
                borderwidth=0,
                bg="#CCE3C7",
                font=self.small_font,
            )
            self.salary_display.place(x=360, y=300, anchor="n")
            self.current_player["money"] += 200
            self.update_money()
        else:
            self.current_player["location"] += self.roll_no
        self.current_player_location_property = self.property_locations[
            self.current_player["location"]
        ]

        # Moving players on board
        x, y = self.current_player_location_property["coords"]
        self.board.coords(self.current_player["token"], x, y)
        current_player_landing_text = f"{self.current_player['name']} Rolled a {self.roll_no}\n&\nLanded on {self.current_player_location_property['name']}"
        self.current_player_landing = tk.Label(
            self.screen,
            text=current_player_landing_text,
            bg="#CCE3C7",
            borderwidth=0,
            font=self.small_font,
        )
        self.current_player_landing.place(x=360, y=145, anchor="n")

        # Actions for each space on the board
        if self.current_player_location_property["colour"] not in [
            "Go",
            "Community Chest",
            "Chance",
            "Tax",
            "Jail",
            "Go to Jail",
            "Free Parking",
        ]:
            if self.current_player_location_property["owned_by"] not in [
                self.player_1,
                self.player_2,
                self.player_3,
                self.player_4,
            ]:
                # Displays property buying choice if player lands on property
                self.property_choice_display = tk.Button(
                    self.screen,
                    text=f"BUY: ${self.current_player_location_property['price']}",
                    compound="center",
                    image=self.button_image,
                    bg="#CA7264",
                    activebackground="#CA7264",
                    borderwidth=0,
                    font=self.font,
                    command=lambda: (
                        self.buy_property(),
                        self.property_choice_display.destroy(),
                    ),
                )
                self.property_choice_display.place(
                    width=170, height=62, x=1012, y=515, anchor="nw"
                )
            elif self.current_player_location_property["colour"] == "Utility":
                if (
                    self.current_player
                    != self.current_player_location_property["owned_by"]
                ):
                    self.pay_utility()
            else:
                if (
                    self.current_player
                    != self.current_player_location_property["owned_by"]
                ):
                    self.pay_rent()
        elif self.current_player_location_property["colour"] == "Tax":
            self.pay_tax()
        elif (
            self.current_player_location_property["colour"] == "Chance"
            or self.current_player_location_property["colour"] == "Community Chest"
        ):
            self.show_card()
        elif self.current_player_location_property["colour"] == "Go to Jail":
            self.current_player["location"] = 11
            fine_display = tk.Button(
                self.screen,
                text=f"FINE: $50",
                compound="center",
                image=self.button_image,
                bg="#CA7264",
                activebackground="#CA7264",
                borderwidth=0,
                font=self.font,
                command=lambda: (
                    self.pay_fine(),
                    fine_display.destroy(),
                ),
            )
            fine_display.place(width=170, height=62, x=1012, y=515, anchor="nw")
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player['name']} has gone to Jail",
                borderwidth=0,
                bg="#CCE3C7",
                font=self.small_font,
            )
            try:
                self.player_info.destroy()
                self.close_player_button.destroy()
            except AttributeError:
                pass
            self.action_display.place(x=360, y=260, anchor="n")
            self.board.coords(self.current_player["token"], 63, 660)
            self.end_turn_button.destroy()

    def end_turn_func(self):
        # Going to next player in the player turn loop
        self.current_player["turn"] = False
        self.player_turn_init(next(self.player_loop))

        # List of attributes to destroy
        attributes_to_destroy = [
            "current_player_landing",
            "dice_1_display",
            "dice_2_display",
            "property_choice_display",
            "action_display",
            "card_display",
            "salary_display",
        ]

        # Loop through the attributes and destroy them
        for attribute in attributes_to_destroy:
            try:
                getattr(self, attribute).destroy()
            except AttributeError:
                pass

    def buy_property(self):
        # Charging money from player
        self.current_player["money"] -= self.current_player_location_property["price"]
        if not self.end_check():
            self.current_player["properties"].append(
                self.current_player_location_property
            )
            self.current_player_location_property["owned_by"] = self.current_player

            # Displaying purchace
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player['name']} Purchased {self.current_player_location_property['name']} for ${self.current_player_location_property['price']}",
                borderwidth=0,
                bg="#CCE3C7",
                font=self.small_font,
            )
            try:
                self.player_info.destroy()
                self.close_player_button.destroy()
            except AttributeError:
                pass
            self.action_display.place(x=360, y=260, anchor="n")

            # Increasing rent of color sets (if any)
            set_colour = self.current_player_location_property["colour"]
            set_number = 0
            rent = 0
            for title in self.current_player_location_property["owned_by"][
                "properties"
            ]:
                if title["colour"] == set_colour:
                    set_number += 1
            if set_colour == "Station":
                match set_number:
                    case 1:
                        rent = 75
                    case 2:
                        rent = 100
                    case 3:
                        rent = 125
                    case 4:
                        rent = 150
            else:
                match set_number:
                    case 1:
                        rent = self.current_player_location_property["price"] // 2
                    case 2:
                        rent = self.current_player_location_property["price"]
                    case 3:
                        rent = self.current_player_location_property["price"] * 2

            for title in self.current_player_location_property["owned_by"][
                "properties"
            ]:
                if title["colour"] == set_colour:
                    title["rent"] = rent

    def pay_rent(self):
        # Rent taken from payer and added to reciever
        self.current_player["money"] -= self.current_player_location_property["rent"]
        if not self.end_check():
            self.current_player_location_property["owned_by"][
                "money"
            ] += self.current_player_location_property["rent"]
            self.update_money()
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player['name']} Paid ${self.current_player_location_property['rent']} to {self.current_player_location_property['owned_by']['name']}",
                borderwidth=0,
                bg="#CCE3C7",
                font=self.small_font,
            )
            try:
                self.player_info.destroy()
                self.close_player_button.destroy()
            except AttributeError:
                pass
            self.action_display.place(x=360, y=260, anchor="n")

    def pay_tax(self):
        # Tax taken from user
        self.current_player["money"] -= self.current_player_location_property["price"]
        if not self.end_check():
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player['name']} Paid ${self.current_player_location_property['price']} in tax",
                borderwidth=0,
                bg="#CCE3C7",
                font=self.small_font,
            )
            try:
                self.player_info.destroy()
                self.close_player_button.destroy()
            except AttributeError:
                pass
            self.action_display.place(x=360, y=260, anchor="n")

    def pay_utility(self):
        # Checks dice roll number and charges accordingly
        utility_count = 0
        for title in self.current_player_location_property["owned_by"]["properties"]:
            if title["colour"] == "Utility":
                utility_count += 1
        if utility_count == 1:
            self.current_player["money"] -= self.roll_no * 4
            if not self.end_check():
                self.current_player_location_property["owned_by"]["money"] += (
                    self.roll_no * 4
                )
                self.update_money()
                self.action_display = tk.Label(
                    self.screen,
                    text=f"{self.current_player['name']} Paid ${self.roll_no*4} to {self.current_player_location_property['owned_by']['name']}",
                    borderwidth=0,
                    bg="#CCE3C7",
                    font=self.small_font,
                )
                try:
                    self.player_info.destroy()
                    self.close_player_button.destroy()
                except AttributeError:
                    pass
                self.action_display.place(x=360, y=260, anchor="n")
        elif utility_count == 2:
            self.current_player["money"] -= self.roll_no * 10
            if not self.end_check():
                self.current_player_location_property["owned_by"]["money"] += (
                    self.roll_no * 10
                )
                self.update_money()
                self.action_display = tk.Label(
                    self.screen,
                    text=f"{self.current_player['name']} Paid ${self.roll_no*10} to {self.current_player_location_property['owned_by']['name']}",
                    borderwidth=0,
                    bg="#CCE3C7",
                    font=self.small_font,
                )
                try:
                    self.player_info.destroy()
                    self.close_player_button.destroy()
                except AttributeError:
                    pass
                self.action_display.place(x=360, y=260, anchor="n")

    def pay_fine(self):
        # Pays fine for jailed players
        self.current_player["money"] -= 50
        if not self.end_check():
            self.action_display.destroy()
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player['name']} Paid $50 in fine",
                borderwidth=0,
                bg="#CCE3C7",
                font=self.small_font,
            )
            try:
                self.player_info.destroy()
                self.close_player_button.destroy()
            except AttributeError:
                pass
            self.action_display.place(x=360, y=260, anchor="n")
            self.end_turn_display()

    def show_card(self):
        # Displays Chance and Community Chest cards accordingly
        card_text = ""
        if self.current_player_location_property["colour"] == "Chance":
            draw_card = self.chance_list.pop(0)
            self.chance_list.append(draw_card)
            match draw_card["function"]:
                case "get":
                    self.current_player["money"] += int(draw_card["value"])
                    card_text += f"Chance\n\n{draw_card['name']}\n\n{self.current_player['name']} got ${draw_card['value']}"
                case "give":
                    self.current_player["money"] -= int(draw_card["value"])
                    card_text += f"Chance\n\n{draw_card['name']}\n\n{self.current_player['name']} paid ${draw_card['value']}"
                case "giveall":
                    self.current_player["money"] -= 150
                    for player in [
                        self.player_1,
                        self.player_2,
                        self.player_3,
                        self.player_4,
                    ]:
                        if player != self.current_player:
                            player["money"] += 50
                    card_text += f"Chance\n\n{draw_card['name']}\n\n{self.current_player['name']} paid $150\nOther players got $50"
                case "move":
                    self.current_player["location"] = 1
                    self.current_player["money"] += 200
                    card_text += f"Chance\n\n{draw_card['name']}\n\n{self.current_player['name']} got $200"
                    self.board.coords(self.current_player["token"], 675, 675)
        else:
            draw_card = self.chest_list.pop(0)
            self.chest_list.append(draw_card)
            match draw_card["function"]:
                case "get":
                    self.current_player["money"] += int(draw_card["value"])
                    card_text += f"Community Chest\n\n{draw_card['name']}\n\n{self.current_player['name']} got ${draw_card['value']}"
                case "give":
                    self.current_player["money"] -= int(draw_card["value"])
                    card_text += f"Community Chest\n\n{draw_card['name']}\n\n{self.current_player['name']} paid ${draw_card['value']}"
                case "move":
                    self.current_player["location"] = 1
                    self.current_player["money"] += 200
                    card_text += f"Community Chest\n\n{draw_card['name']}\n\n{self.current_player['name']} got $200"
                    self.board.coords(self.current_player["token"], 675, 675)
        if not self.end_check():
            self.card_display = tk.Label(
                self.screen,
                text=card_text,
                font=self.small_font,
                borderwidth=0,
                bg="#B9CEB5",
            )
            self.card_display.place(height=160, width=250, x=360, y=500, anchor="s")

    def update_money(self):
        self.player_1_money.config(text=f": ${self.player_1['money']}")
        self.player_2_money.config(text=f": ${self.player_2['money']}")
        self.player_3_money.config(text=f": ${self.player_3['money']}")
        self.player_4_money.config(text=f": ${self.player_4['money']}")

    def end_check(self):
        # Checks if players have negative money and ends game accordingly
        if self.current_player["money"] < 0:
            self.current_player["money"] = 0
            self.update_money()
            self.end_turn_button.destroy()
            final_player_list = [
                self.player_1,
                self.player_2,
                self.player_3,
                self.player_4,
            ]
            final_player_list.remove(self.current_player)
            final_player_money_list = []
            for player in final_player_list:
                money = player["money"]
                for title in player["properties"]:
                    money += title["rent"]
                player["money"] = money
                final_player_money_list.append(player["money"])
            winner = final_player_list[
                final_player_money_list.index(max(final_player_money_list))
            ]

            # Displays winner
            end_text = f"{self.current_player['name']} is bankrupt\n\n{winner['name']} won the game\n\nNet worth:\n\n"
            for player in [self.player_1, self.player_2, self.player_3, self.player_4]:
                end_text += f"{player['name']}: ${player['money']}\n"
            end_screen = tk.Label(
                self.screen,
                text=end_text,
                borderwidth=0,
                font=self.small_font,
                bg="#B9CEB5",
            )
            end_screen.place(height=280, width=250, x=360, y=360, anchor="center")
            return True
        else:
            self.update_money()
            return False


# This statement only initiates the following when the program is run from main file, i.e.not imported as a module
if __name__ == "__main__":
    Monopoly()
