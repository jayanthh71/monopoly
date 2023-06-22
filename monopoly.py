import tkinter as tk  # To create Graphical User Interface
import tkextrafont  # To use custom fonts
import random  # For dice rolling
import csv  # To read csv files
import itertools  # To create player loop
import ctypes  # To get HD Graphical User Interface
from PIL import Image, ImageTk  # To import and create images


class Player:
    def __init__(self):
        # Assigning basic requirements for each player
        self.name: str
        self.token: int
        self.token_image: ImageTk.PhotoImage
        self.token_display_image: ImageTk.PhotoImage
        self.location = 1
        self.money = 1500
        self.properties = list()


class Property:
    def __init__(self):
        # Defining types for each attribute  of property
        self.name: str
        self.price: int
        self.colour: str
        self.owned_by = str()
        self.rent = int()
        self.location = tuple()


class Card:
    def __init__(self):
        # Defining types for each attribute  of cards
        self.type: str
        self.function: str
        self.value: str
        self.name: str


class Monopoly:
    def __init__(self):
        # Creating the Graphical User Interface
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("Monopoly")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        # Loading fonts
        self.big_font = tkextrafont.Font(
            file=r"fonts\big_font.ttf", family="Kabel Book", size=20
        )
        self.font = tkextrafont.Font(
            file=r"fonts\small_font.ttf", family="Kabel Book", size=18
        )
        self.small_font = tkextrafont.Font(
            file=r"fonts\tiny_font.ttf", family="Kabel Book", size=12
        )

        # Creating token list
        self.tokens = [
            r"textures\hat_token.png",
            r"textures\car_token.png",
            r"textures\ship_token.png",
            r"textures\dog_token.png",
        ]
        self.display_tokens = [
            r"textures\hat.png",
            r"textures\car.png",
            r"textures\ship.png",
            r"textures\dog.png",
        ]

        # Defining player instances
        self.player_1 = Player()
        self.player_2 = Player()
        self.player_3 = Player()
        self.player_4 = Player()

        # Show title screen
        self.title_screen = tk.Frame(self.root, background="#AAAAAA")
        self.title_screen.pack(fill="both", expand=True)

        # Creating elements on title screen
        title_image = ImageTk.PhotoImage(file=r"textures\title.png")
        title = tk.Label(
            self.title_screen, image=title_image, borderwidth=0, bg="#AAAAAA"
        )
        title.place(relx=0.5, y=50, anchor="n")
        player_select = tk.Label(
            self.title_screen,
            borderwidth=0,
            font=self.big_font,
            text="Player Select",
            bg="#AAAAAA",
        )
        player_select.place(x=532, y=162.5, width=216, height=53, anchor="nw")
        start_button = tk.Button(
            self.title_screen,
            borderwidth=0,
            text="Start Game",
            font=self.font,
            bg="#C70000",
            activebackground="#770000",
            command=self.start_game,
        )
        start_button.place(relx=0.5, y=670, width=166, height=60, anchor="s")

        # Creating arrow images
        right_image = ImageTk.PhotoImage(file=r"textures\right-arrow.png")
        left_image = ImageTk.PhotoImage(file=r"textures\left-arrow.png")

        # Getting player choices
        self.player_1_index = 0
        self.player_1_image = ImageTk.PhotoImage(file=self.display_tokens[0])
        self.player_1_image_label = tk.Label(
            self.title_screen,
            borderwidth=0,
            image=self.player_1_image,
            bg="#AAAAAA",
        )
        self.player_1_image_label.place(x=188, y=393.5, anchor="nw")
        self.player_1_entry = tk.Entry(
            self.title_screen,
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
            self.title_screen,
            borderwidth=0,
            image=left_image,
            bg="#AAAAAA",
            activebackground="#AAAAAA",
            command=lambda: self.prev_token(1),
        )
        player_1_left.place(x=140, y=441.5, anchor="nw")
        player_1_right = tk.Button(
            self.title_screen,
            borderwidth=0,
            image=right_image,
            bg="#AAAAAA",
            activebackground="#AAAAAA",
            command=lambda: self.next_token(1),
        )
        player_1_right.place(x=332, y=441.5, anchor="nw")

        self.player_2_index = 1
        self.player_2_image = ImageTk.PhotoImage(file=self.display_tokens[1])
        self.player_2_image_label = tk.Label(
            self.title_screen,
            borderwidth=0,
            image=self.player_2_image,
            bg="#AAAAAA",
        )
        self.player_2_image_label.place(x=444, y=393.5, anchor="nw")
        self.player_2_entry = tk.Entry(
            self.title_screen,
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
            self.title_screen,
            borderwidth=0,
            image=left_image,
            bg="#AAAAAA",
            activebackground="#AAAAAA",
            command=lambda: self.prev_token(2),
        )
        player_2_left.place(x=396, y=441.5, anchor="nw")
        player_2_right = tk.Button(
            self.title_screen,
            borderwidth=0,
            image=right_image,
            bg="#AAAAAA",
            activebackground="#AAAAAA",
            command=lambda: self.next_token(2),
        )
        player_2_right.place(x=588, y=441.5, anchor="nw")

        self.player_3_index = 2
        self.player_3_image = ImageTk.PhotoImage(file=self.display_tokens[2])
        self.player_3_image_label = tk.Label(
            self.title_screen,
            borderwidth=0,
            image=self.player_3_image,
            bg="#AAAAAA",
        )
        self.player_3_image_label.place(x=708, y=393.5, anchor="nw")
        self.player_3_entry = tk.Entry(
            self.title_screen,
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
            self.title_screen,
            borderwidth=0,
            image=left_image,
            bg="#AAAAAA",
            activebackground="#AAAAAA",
            command=lambda: self.prev_token(3),
        )
        player_3_left.place(x=660, y=441.5, anchor="nw")
        player_3_right = tk.Button(
            self.title_screen,
            borderwidth=0,
            image=right_image,
            bg="#AAAAAA",
            activebackground="#AAAAAA",
            command=lambda: self.next_token(3),
        )
        player_3_right.place(x=852, y=441.5, anchor="nw")

        self.player_4_index = 3
        self.player_4_image = ImageTk.PhotoImage(file=self.display_tokens[3])
        self.player_4_image_label = tk.Label(
            self.title_screen,
            borderwidth=0,
            image=self.player_4_image,
            bg="#AAAAAA",
        )
        self.player_4_image_label.place(x=964, y=393.5, anchor="nw")
        self.player_4_entry = tk.Entry(
            self.title_screen,
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
                self.player_4_entry.insert(0, "Player 1"),
                self.player_4_entry.configure(fg="grey"),
            )
            if self.player_4_entry.get() == ""
            else None,
        )
        player_4_left = tk.Button(
            self.title_screen,
            borderwidth=0,
            image=left_image,
            bg="#AAAAAA",
            activebackground="#AAAAAA",
            command=lambda: self.prev_token(4),
        )
        player_4_left.place(x=916, y=441.5, anchor="nw")
        player_4_right = tk.Button(
            self.title_screen,
            borderwidth=0,
            image=right_image,
            bg="#AAAAAA",
            activebackground="#AAAAAA",
            command=lambda: self.next_token(4),
        )
        player_4_right.place(x=1108, y=441.5, anchor="nw")

        ctypes.windll.shcore.SetProcessDpiAwareness(1)
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
        self.player_1.name = self.player_1_entry.get()
        self.player_2.name = self.player_2_entry.get()
        self.player_3.name = self.player_3_entry.get()
        self.player_4.name = self.player_4_entry.get()

        self.title_screen.destroy()

        # Creating game screen
        self.screen = tk.Frame(self.root, background="#D7BAAA")
        self.screen.pack(fill="both", expand=True)

        # Importing and placing the board
        board_image = ImageTk.PhotoImage(file=r"textures\board.png")
        self.board = tk.Canvas(self.screen, borderwidth=0)
        self.board.place(width=720, height=720, rely=0.5, anchor="w")
        self.board.create_image(0, 0, image=board_image, anchor="nw")
        button_background_image = ImageTk.PhotoImage(
            Image.new("RGB", (560, 720), "#D7BAAA")
        )
        button_background = tk.Label(
            self.screen, image=button_background_image, borderwidth=0
        )
        button_background.place(relx=1, rely=0, anchor="ne")

        # Loading close button and dice roll image
        self.close_player_button_image = ImageTk.PhotoImage(file=r"textures\close.png")
        self.dice_image = ImageTk.PhotoImage(file=r"textures\dice.png")

        # Loading dice images
        self.dice_1_image = ImageTk.PhotoImage(file=r"textures\dice_1.png")
        self.dice_2_image = ImageTk.PhotoImage(file=r"textures\dice_2.png")
        self.dice_3_image = ImageTk.PhotoImage(file=r"textures\dice_3.png")
        self.dice_4_image = ImageTk.PhotoImage(file=r"textures\dice_4.png")
        self.dice_5_image = ImageTk.PhotoImage(file=r"textures\dice_5.png")
        self.dice_6_image = ImageTk.PhotoImage(file=r"textures\dice_6.png")

        # Creating card instances and assigning unique values
        self.chance_list = list()
        self.chest_list = list()
        with open(r"cards.csv", newline="") as file:
            for card_info in csv.reader(file, delimiter="|"):
                card_instance = Card()
                card_instance.type = card_info[0]
                card_instance.function = card_info[1]
                card_instance.value = card_info[2]
                card_instance.name = card_info[3]
                match card_instance.type:
                    case "c":
                        self.chance_list.append(card_instance)
                    case "cc":
                        self.chest_list.append(card_instance)
        random.shuffle(self.chance_list)
        random.shuffle(self.chest_list)

        # Creating property instances and assigning unique values
        self.property_locations = dict()
        property_locations_list = itertools.cycle(range(1, 41))
        with open(r"properties.csv", newline="") as file:
            for property_info in csv.reader(file, delimiter="|"):
                property_instance = Property()
                self.property_locations[
                    next(property_locations_list)
                ] = property_instance
                property_instance.name = property_info[0]
                property_instance.price = int(property_info[1])
                property_instance.colour = property_info[2]
                property_instance.location = eval(property_info[3])

        # Assigning tokens to players
        self.player_1.token_display_image = self.player_1_image
        self.player_1.token_image = ImageTk.PhotoImage(
            file=self.tokens[self.player_1_index]
        )
        self.player_2.token_display_image = self.player_2_image
        self.player_2.token_image = ImageTk.PhotoImage(
            file=self.tokens[self.player_2_index]
        )
        self.player_3.token_display_image = self.player_3_image
        self.player_3.token_image = ImageTk.PhotoImage(
            file=self.tokens[self.player_3_index]
        )
        self.player_4.token_display_image = self.player_4_image
        self.player_4.token_image = ImageTk.PhotoImage(
            file=self.tokens[self.player_4_index]
        )

        # Creating info buttons for each player and displaying token
        p1_token_display = tk.Label(
            self.screen,
            image=self.player_1.token_display_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        p1_token_display.place(x=804, y=20, anchor="nw")
        p1_button = tk.Button(
            self.screen,
            text=self.player_1.name,
            font=self.font,
            bg="#C70000",
            activebackground="#770000",
            borderwidth=0,
            command=lambda: self.display_player_info(self.player_1),
        )
        p1_button.place(width=166, height=60, x=786, y=140, anchor="nw")
        player_1_money_token = tk.Label(
            self.screen,
            image=self.player_1.token_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        player_1_money_token.place(x=775, y=500, anchor="nw")
        self.player_1_money = tk.Label(
            self.screen,
            text=": $1500",
            borderwidth=0,
            font=self.font,
            bg="#D7BAAA",
        )
        self.player_1_money.place(x=830, y=508, anchor="nw")

        p2_token_display = tk.Label(
            self.screen,
            image=self.player_2.token_display_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        p2_token_display.place(x=1080, y=17, anchor="nw")
        p2_button = tk.Button(
            self.screen,
            text=self.player_2.name,
            font=self.font,
            bg="#C70000",
            activebackground="#770000",
            borderwidth=0,
            command=lambda: self.display_player_info(self.player_2),
        )
        p2_button.place(width=166, height=60, x=1224, y=140, anchor="ne")
        player_2_money_token = tk.Label(
            self.screen,
            image=self.player_2.token_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        player_2_money_token.place(x=775, y=548, anchor="nw")
        self.player_2_money = tk.Label(
            self.screen,
            text=": $1500",
            borderwidth=0,
            font=self.font,
            bg="#D7BAAA",
        )
        self.player_2_money.place(x=830, y=556, anchor="nw")

        p3_token_display = tk.Label(
            self.screen,
            image=self.player_3.token_display_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        p3_token_display.place(x=804, y=222, anchor="nw")
        p3_button = tk.Button(
            self.screen,
            text=self.player_3.name,
            font=self.font,
            bg="#C70000",
            activebackground="#770000",
            borderwidth=0,
            command=lambda: self.display_player_info(self.player_3),
        )
        p3_button.place(width=166, height=60, x=786, y=350, anchor="nw")
        player_3_money_token = tk.Label(
            self.screen,
            image=self.player_3.token_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        player_3_money_token.place(x=775, y=596, anchor="nw")
        self.player_3_money = tk.Label(
            self.screen,
            text=": $1500",
            borderwidth=0,
            font=self.font,
            bg="#D7BAAA",
        )
        self.player_3_money.place(x=830, y=604, anchor="nw")

        p4_token_display = tk.Label(
            self.screen,
            image=self.player_4.token_display_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        p4_token_display.place(x=1076, y=230, anchor="nw")
        p4_button = tk.Button(
            self.screen,
            text=self.player_4.name,
            font=self.font,
            bg="#C70000",
            activebackground="#770000",
            borderwidth=0,
            command=lambda: self.display_player_info(self.player_4),
        )
        p4_button.place(width=166, height=60, x=1224, y=350, anchor="ne")
        player_4_money_token = tk.Label(
            self.screen,
            image=self.player_4.token_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        player_4_money_token.place(x=775, y=644, anchor="nw")
        self.player_4_money = tk.Label(
            self.screen,
            text=": $1500",
            borderwidth=0,
            font=self.font,
            bg="#D7BAAA",
        )
        self.player_4_money.place(x=830, y=652, anchor="nw")

        # Placing players on board
        self.player_1.token = self.board.create_image(
            651, 650, image=self.player_1.token_image, anchor="center"
        )
        self.player_2.token = self.board.create_image(
            651, 695, image=self.player_2.token_image, anchor="center"
        )
        self.player_3.token = self.board.create_image(
            696, 650, image=self.player_3.token_image, anchor="center"
        )
        self.player_4.token = self.board.create_image(
            696, 695, image=self.player_4.token_image, anchor="center"
        )

        # Creating player turn loop
        self.player_loop = itertools.cycle(
            [self.player_1, self.player_2, self.player_3, self.player_4]
        )
        self.player_turn_init(next(self.player_loop))
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.root.mainloop()

    def display_player_info(self, player):
        # Shows player info after player button is clicked
        player_info_text = f"{player.name}\n${player.money}\n\n"
        for title in player.properties:
            player_info_text += str(title.name)
            player_info_text += "\n"
        player_info = tk.Label(
            self.screen,
            text=player_info_text,
            borderwidth=0,
            font=self.small_font,
            bg="#9FB5A2",
        )
        player_info.place(height=280, width=250, x=360, y=360, anchor="center")

        # Shows player info close button
        close_player_button = tk.Button(
            self.screen,
            borderwidth=0,
            image=self.close_player_button_image,
            bg="#9FB5A2",
            activebackground="#9FB5A2",
            command=lambda: (
                player_info.destroy(),
                close_player_button.destroy(),
            ),
        )
        close_player_button.place(width=24, height=24, x=460, y=245, anchor="center")

    def player_turn_init(self, player):
        self.current_player = player

        # Showing current player's turn
        current_player_display = tk.Label(
            self.screen,
            text=f"{self.current_player.name}'s Turn",
            font=self.big_font,
            borderwidth=0,
            bg="#D7BAAA",
        )
        current_player_display.place(
            width=300, height=60, x=1000, y=450, anchor="center"
        )

        # Setting up dice and end turn button for current player
        dice_button = tk.Button(
            self.screen,
            image=self.dice_image,
            borderwidth=0,
            activebackground="#C70000",
            bg="#C70000",
            command=lambda: (
                self.end_turn_display(),
                self.player_turn(),
                dice_button.destroy(),
            ),
        )
        dice_button.place(x=1152, y=602, anchor="nw")

    def end_turn_display(self):
        self.end_turn_button = tk.Button(
            self.screen,
            text="END TURN",
            font=self.font,
            borderwidth=0,
            activebackground="#770000",
            bg="#C70000",
            command=lambda: (self.end_turn_func(), self.end_turn_button.destroy()),
        )
        self.end_turn_button.place(width=156, height=66, x=980, y=622, anchor="nw")

    def dice_display(self, dice_1, dice_2):
        # Displayng dice images based on result
        match dice_1:
            case 1:
                self.dice_1_display = tk.Label(
                    self.screen, image=self.dice_1_image, borderwidth=0, bg="#CCE3C7"
                )
            case 2:
                self.dice_1_display = tk.Label(
                    self.screen, image=self.dice_2_image, borderwidth=0, bg="#CCE3C7"
                )
            case 3:
                self.dice_1_display = tk.Label(
                    self.screen, image=self.dice_3_image, borderwidth=0, bg="#CCE3C7"
                )
            case 4:
                self.dice_1_display = tk.Label(
                    self.screen, image=self.dice_4_image, borderwidth=0, bg="#CCE3C7"
                )
            case 5:
                self.dice_1_display = tk.Label(
                    self.screen, image=self.dice_5_image, borderwidth=0, bg="#CCE3C7"
                )
            case 6:
                self.dice_1_display = tk.Label(
                    self.screen, image=self.dice_6_image, borderwidth=0, bg="#CCE3C7"
                )
        match dice_2:
            case 1:
                self.dice_2_display = tk.Label(
                    self.screen, image=self.dice_1_image, borderwidth=0, bg="#CCE3C7"
                )
            case 2:
                self.dice_2_display = tk.Label(
                    self.screen, image=self.dice_2_image, borderwidth=0, bg="#CCE3C7"
                )
            case 3:
                self.dice_2_display = tk.Label(
                    self.screen, image=self.dice_3_image, borderwidth=0, bg="#CCE3C7"
                )
            case 4:
                self.dice_2_display = tk.Label(
                    self.screen, image=self.dice_4_image, borderwidth=0, bg="#CCE3C7"
                )
            case 5:
                self.dice_2_display = tk.Label(
                    self.screen, image=self.dice_5_image, borderwidth=0, bg="#CCE3C7"
                )
            case 6:
                self.dice_2_display = tk.Label(
                    self.screen, image=self.dice_6_image, borderwidth=0, bg="#CCE3C7"
                )
        self.dice_1_display.place(x=360, y=560, anchor="e")
        self.dice_2_display.place(x=372, y=560, anchor="w")

    def player_turn(self):
        # Rolling the dice
        dice_1 = random.randint(1, 6)
        dice_2 = random.randint(1, 6)
        self.roll_no = dice_1 + dice_2
        self.dice_display(dice_1, dice_2)

        # Setting player locations and displaying player landing
        if self.current_player.location + self.roll_no > 40:
            roll_difference = 40 - (self.current_player.location + self.roll_no)
            self.current_player.location = -roll_difference
            self.salary_display = tk.Label(
                self.screen,
                text=f"{self.current_player.name} Got $200 in salary",
                borderwidth=0,
                bg="#CCE3C7",
                font=self.small_font,
            )
            self.salary_display.place(x=360, y=300, anchor="n")
            self.current_player.money += 200
            self.update_money()
        else:
            self.current_player.location += self.roll_no
        self.current_player_location_property = self.property_locations[
            self.current_player.location
        ]

        # Moving players on board
        x, y = self.current_player_location_property.location
        self.board.coords(self.current_player.token, x, y)
        current_player_landing_text = f"{self.current_player.name} Rolled a {self.roll_no}\n&\nLanded on {self.current_player_location_property.name}"
        self.current_player_landing = tk.Label(
            self.screen,
            text=current_player_landing_text,
            bg="#CCE3C7",
            borderwidth=0,
            font=self.small_font,
        )
        self.current_player_landing.place(x=360, y=145, anchor="n")

        # Actions for each space on the board
        if self.current_player_location_property.colour not in [
            "Go",
            "Community Chest",
            "Chance",
            "Tax",
            "Jail",
            "Go to Jail",
            "Free Parking",
        ]:
            if self.current_player_location_property.owned_by not in [
                self.player_1,
                self.player_2,
                self.player_3,
                self.player_4,
            ]:
                # Displays property buying choice if player lands on property
                self.property_choice_display = tk.Button(
                    self.screen,
                    text=f"BUY? (${self.current_player_location_property.price})",
                    bg="#C70000",
                    borderwidth=0,
                    activebackground="#770000",
                    font=self.font,
                    command=lambda: (
                        self.buy_property(),
                        self.property_choice_display.destroy(),
                    ),
                )
                self.property_choice_display.place(
                    width=180, height=66, x=980, y=522, anchor="nw"
                )
            elif self.current_player_location_property.colour == "Utility":
                if (
                    self.current_player
                    != self.current_player_location_property.owned_by
                ):
                    self.pay_utility()
            else:
                if (
                    self.current_player
                    != self.current_player_location_property.owned_by
                ):
                    self.pay_rent()
        elif self.current_player_location_property.colour == "Tax":
            self.pay_tax()
        elif (
            self.current_player_location_property.colour == "Chance"
            or self.current_player_location_property.colour == "Community Chest"
        ):
            self.show_card()
        elif self.current_player_location_property.colour == "Go to Jail":
            self.current_player.location = 11
            fine_display = tk.Button(
                self.screen,
                text=f"FINE ($50)",
                bg="#C70000",
                borderwidth=0,
                activebackground="#770000",
                font=self.font,
                command=lambda: (
                    self.pay_fine(),
                    fine_display.destroy(),
                ),
            )
            fine_display.place(width=180, height=66, x=980, y=522, anchor="nw")
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player.name} has gone to Jail",
                borderwidth=0,
                bg="#CCE3C7",
                font=self.small_font,
            )
            self.action_display.place(x=360, y=260, anchor="n")
            self.board.coords(self.current_player.token, 63, 660)
            self.end_turn_button.destroy()

    def end_turn_func(self):
        # Going to next player in the player turn loop
        self.player_turn_init(next(self.player_loop))

        # Closing all menus
        try:
            self.current_player_landing.destroy()
            self.dice_1_display.destroy()
            self.dice_2_display.destroy()
        except AttributeError:
            pass
        try:
            self.property_choice_display.destroy()
        except AttributeError:
            pass
        try:
            self.action_display.destroy()
        except AttributeError:
            pass
        try:
            self.card_display.destroy()
        except AttributeError:
            pass
        try:
            self.salary_display.destroy()
        except AttributeError:
            pass

    def buy_property(self):
        # Charging money from player
        self.current_player.money -= self.current_player_location_property.price
        if not self.end_check():
            self.current_player.properties.append(self.current_player_location_property)
            self.current_player_location_property.owned_by = self.current_player
            # Displaying purchace
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player.name} Purchased {self.current_player_location_property.name} for ${self.current_player_location_property.price}",
                borderwidth=0,
                bg="#CCE3C7",
                font=self.small_font,
            )
            self.action_display.place(x=360, y=260, anchor="n")

            # Increasing rent of color sets (if any)
            set_colour = self.current_player_location_property.colour
            set_number = 0
            rent = 0
            for title in self.current_player_location_property.owned_by.properties:
                if title.colour == set_colour:
                    set_number += 1
            if set_colour in [
                "Light Blue",
                "Pink",
                "Orange",
                "Red",
                "Yellow",
                "Green",
            ]:
                match set_number:
                    case 1:
                        rent = self.current_player_location_property.price // 10
                    case 2:
                        rent = 2 * (self.current_player_location_property.price // 10)
                    case 3:
                        rent = 4 * (self.current_player_location_property.price // 10)
            elif set_colour in ["Brown", "Dark Blue"]:
                match set_number:
                    case 1:
                        rent = self.current_player_location_property.price // 10
                    case 2:
                        rent = 3 * (self.current_player_location_property.price // 10)
            elif set_colour == "Station":
                match set_number:
                    case 1:
                        rent = 25
                    case 2:
                        rent = 50
                    case 3:
                        rent = 75
                    case 4:
                        rent = 100
            for title in self.current_player_location_property.owned_by.properties:
                if title.colour == set_colour:
                    title.rent = rent

    def pay_rent(self):
        # Rent taken from payer and added to reciever
        self.current_player.money -= self.current_player_location_property.rent
        if not self.end_check():
            self.current_player_location_property.owned_by.money += (
                self.current_player_location_property.rent
            )
            self.update_money()
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player.name} Paid ${self.current_player_location_property.rent} to {self.current_player_location_property.owned_by.name}",
                borderwidth=0,
                bg="#CCE3C7",
                font=self.small_font,
            )
            self.action_display.place(x=360, y=260, anchor="n")

    def pay_tax(self):
        # Tax taken from user
        self.current_player.money -= self.current_player_location_property.price
        if not self.end_check():
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player.name} Paid ${self.current_player_location_property.price} in tax",
                borderwidth=0,
                bg="#CCE3C7",
                font=self.small_font,
            )
            self.action_display.place(x=360, y=260, anchor="n")

    def pay_utility(self):
        # Checks dice roll number and charges accordingly
        utility_count = 0
        for title in self.current_player_location_property.owned_by.properties:
            if title.colour == "Utility":
                utility_count += 1
        if utility_count == 1:
            self.current_player.money -= self.roll_no * 4
            if not self.end_check():
                self.current_player_location_property.owned_by.money += self.roll_no * 4
                self.update_money()
                self.action_display = tk.Label(
                    self.screen,
                    text=f"{self.current_player.name} Paid ${self.roll_no*4} to {self.current_player_location_property.owned_by.name}",
                    borderwidth=0,
                    bg="#CCE3C7",
                    font=self.small_font,
                )
                self.action_display.place(x=360, y=260, anchor="n")
        elif utility_count == 2:
            self.current_player.money -= self.roll_no * 10
            if not self.end_check():
                self.current_player_location_property.owned_by.money += (
                    self.roll_no * 10
                )
                self.update_money()
                self.action_display = tk.Label(
                    self.screen,
                    text=f"{self.current_player.name} Paid ${self.roll_no*10} to {self.current_player_location_property.owned_by.name}",
                    borderwidth=0,
                    bg="#CCE3C7",
                    font=self.small_font,
                )
                self.action_display.place(x=360, y=260, anchor="n")

    def pay_fine(self):
        # Pays fine for jailed players
        self.current_player.money -= 50
        if not self.end_check():
            self.action_display.destroy()
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player.name} Paid $50 in fine",
                borderwidth=0,
                bg="#CCE3C7",
                font=self.small_font,
            )
            self.action_display.place(x=360, y=260, anchor="n")
            self.end_turn_display()

    def show_card(self):
        # Displays Chance and Community Chest cards accordingly
        card_text = str()
        if self.current_player_location_property.colour == "Chance":
            draw_card = self.chance_list.pop(0)
            self.chance_list.append(draw_card)
            match draw_card.function:
                case "get":
                    self.current_player.money += int(draw_card.value)
                    card_text += f"Chance\n\n{draw_card.name}\n\n{self.current_player.name} got ${draw_card.value}"
                case "give":
                    self.current_player.money -= int(draw_card.value)
                    card_text += f"Chance\n\n{draw_card.name}\n\n{self.current_player.name} paid ${draw_card.value}"
                case "giveall":
                    self.current_player.money -= 150
                    for player in [
                        self.player_1,
                        self.player_2,
                        self.player_3,
                        self.player_4,
                    ]:
                        if player != self.current_player:
                            player.money += 50
                    card_text += f"Chance\n\n{draw_card.name}\n\n{self.current_player.name} paid $150\nOther players got $50"
                case "move":
                    self.current_player.location = 1
                    self.current_player.money += 200
                    card_text += f"Chance\n\n{draw_card.name}\n\n{self.current_player.name} got $200"
                    self.board.coords(self.current_player.token, 675, 675)
        else:
            draw_card = self.chest_list.pop(0)
            self.chest_list.append(draw_card)
            match draw_card.function:
                case "get":
                    self.current_player.money += int(draw_card.value)
                    card_text += f"Community Chest\n\n{draw_card.name}\n\n{self.current_player.name} got ${draw_card.value}"
                case "give":
                    self.current_player.money -= int(draw_card.value)
                    card_text += f"Community Chest\n\n{draw_card.name}\n\n{self.current_player.name} paid ${draw_card.value}"
                case "move":
                    self.current_player.location = 1
                    self.current_player.money += 200
                    card_text += f"Community Chest\n\n{draw_card.name}\n\n{self.current_player.name} got $200"
                    self.board.coords(self.current_player.token, 675, 675)
        if not self.end_check():
            self.card_display = tk.Label(
                self.screen,
                text=card_text,
                font=self.small_font,
                borderwidth=0,
                bg="#9FB5A2",
            )
            self.card_display.place(height=160, width=250, x=360, y=500, anchor="s")

    def update_money(self):
        self.player_1_money.config(text=f": ${self.player_1.money}")
        self.player_2_money.config(text=f": ${self.player_2.money}")
        self.player_3_money.config(text=f": ${self.player_3.money}")
        self.player_4_money.config(text=f": ${self.player_4.money}")

    def end_check(self):
        # Checks if players have negative money and ends game accordingly
        if self.current_player.money < 0:
            self.current_player.money = 0
            self.update_money()
            self.end_turn_button.destroy()
            final_player_list = [
                self.player_1,
                self.player_2,
                self.player_3,
                self.player_4,
            ]
            final_player_list.remove(self.current_player)
            final_player_money_list = list()
            for player in final_player_list:
                money = player.money
                for title in player.properties:
                    money += title.rent
                player.money = money
                final_player_money_list.append(player.money)
            winner = final_player_list[
                final_player_money_list.index(max(final_player_money_list))
            ]

            # Displays winner
            end_text = f"{self.current_player.name} is bankrupt\n\n{winner.name} won the game\n\nNet worth:\n\n"
            for player in [self.player_1, self.player_2, self.player_3, self.player_4]:
                end_text += f"{player.name}: ${player.money}\n"
            end_screen = tk.Label(
                self.screen,
                text=end_text,
                borderwidth=0,
                font=self.small_font,
                bg="#9FB5A2",
            )
            end_screen.place(height=280, width=250, x=360, y=360, anchor="center")
            return True
        else:
            self.update_money()
            return False


# This statement only initiates the following when the program is run from main file, i.e.not imported as a module
if __name__ == "__main__":
    Monopoly()
