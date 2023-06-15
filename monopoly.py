import tkinter as tk  # To Create Graphical User Interface
import tkextrafont  # To use custom fonts
import random  # For dice rolling
import itertools  # To create player loop
from PIL import Image, ImageTk  # To import and create images
from ctypes import windll  # To get HD Graphical User Interface

# Chance and Community Chests
# Title deeds (optional)


class Player:
    def __init__(self, name="Player", token="Hat"):
        # Assigning basic requirements for each player
        self.name = name
        self.token: int
        self.token_name = token
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
        self.owned_by = ""
        self.rent: int
        self.location = tuple()


class Monopoly:
    def __init__(self, player_1, player_2, player_3, player_4):
        # Creating the Graphical User Interface
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("Monopoly")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.screen = tk.Frame(self.root, background="#D7BAAA")
        self.screen.pack(fill="both", expand=True)

        # Loading fonts
        self.big_font = tkextrafont.Font(
            file=r"fonts\big_font.ttf", family="Kabel Bd", size=20
        )
        self.font = tkextrafont.Font(
            file=r"fonts\small_font.ttf", family="Kabel Bd", size=18
        )
        self.small_font = tkextrafont.Font(
            file=r"fonts\tiny_font.ttf", family="Kabel Bd", size=12
        )

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
        exit_button_image = ImageTk.PhotoImage(file=r"textures\exit.png")
        exit_button = tk.Button(
            self.screen,
            borderwidth=0,
            image=exit_button_image,
            bg="#D7BAAA",
            activebackground="#D7BAAA",
            command=self.root.destroy,
        )
        exit_button.place(relx=1, rely=0, anchor="ne")

        # Defining player instances
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_3 = player_3
        self.player_4 = player_4

        # Assigning images to player tokens depending on player choice
        for player in [self.player_1, self.player_2, self.player_3, self.player_4]:
            match player.token_name:
                case "Hat":
                    player.token_image = ImageTk.PhotoImage(
                        file=r"textures\hat_token.png"
                    )
                    player.token_display_image = ImageTk.PhotoImage(
                        file=r"textures\hat.png"
                    )
                case "Car":
                    player.token_image = ImageTk.PhotoImage(
                        file=r"textures\car_token.png"
                    )
                    player.token_display_image = ImageTk.PhotoImage(
                        file=r"textures\car.png"
                    )
                case "Ship":
                    player.token_image = ImageTk.PhotoImage(
                        file=r"textures\ship_token.png"
                    )
                    player.token_display_image = ImageTk.PhotoImage(
                        file=r"textures\ship.png"
                    )
                case "Dog":
                    player.token_image = ImageTk.PhotoImage(
                        file=r"textures\dog_token.png"
                    )
                    player.token_display_image = ImageTk.PhotoImage(
                        file=r"textures\dog.png"
                    )

        # Loading dice images
        self.dice_1_image = ImageTk.PhotoImage(file=r"textures\dice_1.png")
        self.dice_2_image = ImageTk.PhotoImage(file=r"textures\dice_2.png")
        self.dice_3_image = ImageTk.PhotoImage(file=r"textures\dice_3.png")
        self.dice_4_image = ImageTk.PhotoImage(file=r"textures\dice_4.png")
        self.dice_5_image = ImageTk.PhotoImage(file=r"textures\dice_5.png")
        self.dice_6_image = ImageTk.PhotoImage(file=r"textures\dice_6.png")

        # Creating property instances and assigning unique values
        self.property_locations = {}
        property_list = []
        property_locations_list = itertools.cycle(range(1, 41))
        with open(r"properties.txt") as file:
            for line in file.readlines():
                property_info = line.strip().split("|")
                property_instance = Property()
                self.property_locations[
                    next(property_locations_list)
                ] = property_instance
                property_instance.name = property_info[0]
                property_instance.price = int(property_info[1])
                property_instance.colour = property_info[2]
                property_instance.location = eval(property_info[3])
                property_list.append(property_instance)

        # Creating info buttons for each player and displaying token
        p1_token_display = tk.Label(
            self.screen,
            image=player_1.token_display_image,
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
            command=lambda: [self.display_player_info(self.player_1)],
        )
        p1_button.place(width=166, height=60, x=786, y=140, anchor="nw")
        p2_token_display = tk.Label(
            self.screen,
            image=player_2.token_display_image,
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
            command=lambda: [self.display_player_info(self.player_2)],
        )
        p2_button.place(width=166, height=60, x=1224, y=140, anchor="ne")
        p3_token_display = tk.Label(
            self.screen,
            image=player_3.token_display_image,
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
            command=lambda: [self.display_player_info(self.player_3)],
        )
        p3_button.place(width=166, height=60, x=786, y=350, anchor="nw")
        p4_token_display = tk.Label(
            self.screen,
            image=player_4.token_display_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        p4_token_display.place(x=1076, y=230, anchor="nw")
        p4_button = tk.Button(
            self.screen,
            text=player_4.name,
            font=self.font,
            bg="#C70000",
            activebackground="#770000",
            borderwidth=0,
            command=lambda: [self.display_player_info(self.player_4)],
        )
        p4_button.place(width=166, height=60, x=1224, y=350, anchor="ne")

        # Loading close button and dice image
        self.close_player_button_image = ImageTk.PhotoImage(file=r"textures\close.png")
        self.dice_image = ImageTk.PhotoImage(file=r"textures\dice.png")

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
        windll.shcore.SetProcessDpiAwareness(1)
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
            command=lambda: [
                player_info.destroy(),
                close_player_button.destroy(),
            ],
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
        current_player_display.place(width=220, height=60, x=910, y=422, anchor="nw")

        # Setting up dice and end turn button for current player
        dice_button = tk.Button(
            self.screen,
            image=self.dice_image,
            borderwidth=0,
            activebackground="#C70000",
            bg="#C70000",
            command=lambda: [
                self.end_turn_display(),
                self.player_turn(),
                dice_button.destroy(),
            ],
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
            command=lambda: [self.end_turn_func(), self.end_turn_button.destroy()],
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
        else:
            self.current_player.location += self.roll_no
        self.current_player_location_property = self.property_locations[
            self.current_player.location
        ]
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
                    command=lambda: [
                        self.buy_property(),
                        self.property_choice_display.destroy(),
                    ],
                )
                self.property_choice_display.place(
                    width=180, height=66, x=980, y=522, anchor="nw"
                )
            else:
                self.pay_rent()
        elif self.current_player_location_property.colour == "Tax":
            self.pay_tax()
        elif self.current_player_location_property.colour == "Utility":
            self.pay_utility()
        elif self.current_player_location_property.colour == "Go to Jail":
            self.current_player.location = 11
            fine_display = tk.Button(
                self.screen,
                text=f"FINE ($50)",
                bg="#C70000",
                borderwidth=0,
                activebackground="#770000",
                font=self.font,
                command=lambda: [
                    self.pay_fine(),
                    fine_display.destroy(),
                ],
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
            self.salary_display.destroy()
        except AttributeError:
            pass

    def buy_property(self):
        # Charging money from player
        self.current_player.money -= self.current_player_location_property.price
        self.current_player.properties.append(self.current_player_location_property)
        self.current_player_location_property.owned_by = self.current_player
        if not self.end_check():
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
        self.current_player_location_property.owned_by.money += (
            self.current_player_location_property.rent
        )
        if not self.end_check():
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
                self.action_display = tk.Label(
                    self.screen,
                    text=f"{self.current_player.name} Paid ${self.roll_no*10} to {self.current_player_location_property.owned_by.name}",
                    borderwidth=0,
                    bg="#CCE3C7",
                    font=self.small_font,
                )
                self.action_display.place(x=360, y=260, anchor="n")

    def pay_fine(self):
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

    def end_check(self):
        if self.current_player.money < 0:
            self.end_turn_button.destroy()
            for player in [self.player_1, self.player_2, self.player_3, self.player_4]:
                money = player.money
                for title in player.properties:
                    money += title.rent
                player.money = money
            winner = [self.player_1, self.player_2, self.player_3, self.player_4][
                [
                    self.player_1.money,
                    self.player_2.money,
                    self.player_3.money,
                    self.player_4.money,
                ].index(
                    max(
                        [
                            self.player_1.money,
                            self.player_2.money,
                            self.player_3.money,
                            self.player_4.money,
                        ]
                    )
                )
            ]
            self.current_player.money = 0
            end_text = f"{self.current_player.name} is bankrupt\n{winner.name} won the game\n\n"
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
            return False


# This statement only initiates the following when the program is run from main file, i.e.not imported as a module
if __name__ == "__main__":
    Monopoly(
        Player("Player 1", "Hat"),
        Player("Player 2", "Car"),
        Player("Player 3", "Ship"),
        Player("Player 4", "Dog"),
    )
#     print(
#         """
# ███╗░░░███╗░█████╗░███╗░░██╗░█████╗░██████╗░░█████╗░██╗░░░██╗░░░██╗
# ████╗░████║██╔══██╗████╗░██║██╔══██╗██╔══██╗██╔══██╗██║░░░╚██╗░██╔╝
# ██╔████╔██║██║░░██║██╔██╗██║██║░░██║██████╔╝██║░░██║██║░░░░╚████╔╝░
# ██║╚██╔╝██║██║░░██║██║╚████║██║░░██║██╔═══╝░██║░░██║██║░░░░░╚██╔╝░░
# ██║░╚═╝░██║╚█████╔╝██║░╚███║╚█████╔╝██║░░░░░╚█████╔╝███████╗░██║░░░
# ╚═╝░░░░░╚═╝░╚════╝░╚═╝░░╚══╝░╚════╝░╚═╝░░░░░░╚════╝░╚══════╝░╚═╝░░░"""
#     )

#     def main_menu():
#         # Gives options for player to select
#         print("\n*----Main Menu----*")
#         print("\n (1) - Start Game")
#         print(" (2) - About")
#         print(" (3) - Exit")
#         choice = input("\n~ ")
#         return choice

#     def start_game():
#         # Asks for player details
#         while True:
#             try:
#                 player_1_name = input("\nEnter Player 1 name: ")
#                 token_1 = input("1) Hat\n2) Car\n3) Ship\n4) Dog\n~ ")
#                 if token_1.title() not in ["Hat", "Car", "Ship", "Dog"]:
#                     raise TypeError
#                 player_2_name = input("\nEnter Player 2 name: ")
#                 token_2 = input("1) Hat\n2) Car\n3) Ship\n4) Dog\n~ ")
#                 if token_2.title() not in ["Hat", "Car", "Ship", "Dog"]:
#                     raise TypeError
#                 player_3_name = input("\nEnter Player 3 name: ")
#                 token_3 = input("1) Hat\n2) Car\n3) Ship\n4) Dog\n~ ")
#                 if token_3.title() not in ["Hat", "Car", "Ship", "Dog"]:
#                     raise TypeError
#                 player_4_name = input("\nEnter Player 4 name: ")
#                 token_4 = input("1) Hat\n2) Car\n3) Ship\n4) Dog\n~ ")
#                 if token_4.title() not in ["Hat", "Car", "Ship", "Dog"]:
#                     raise TypeError
#                 break
#             except:
#                 continue
#         player_1 = Player(player_1_name, token_1)
#         player_2 = Player(player_2_name, token_2)
#         player_3 = Player(player_3_name, token_3)
#         player_4 = Player(player_4_name, token_4)

#         # Starts game
#         Monopoly(player_1, player_2, player_3, player_4)

#     def about_page():
#         # Shows about page
#         print("\nCreated by Jayanth, Pranav and Nazih.")
#         input("\nPress enter to continue")

#     # Checks user input and takes action accordingly
#     while True:
#         match main_menu():
#             case "1":
#                 start_game()
#             case "2":
#                 about_page()
#             case "3":
#                 break
#             case _:
#                 print("Invalid Choice. Try Again")
