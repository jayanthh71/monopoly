import tkinter as tk  # To Create Graphical User Interface
import tkextrafont  # To use custom fonts
import random  # For dice rolling
import itertools  # To create player loop
from PIL import Image, ImageTk  # To import and create images
from ctypes import windll  # To get HD Graphical User Interface


class Player:
    def __init__(self, name="Player", token="Hat"):
        # Assigning basic requirements for each player
        self.name = name
        self.token = token
        self.token_image: ImageTk.PhotoImage
        self.token_display_image: ImageTk.PhotoImage
        self.location = 1
        self.money = 1500
        self.properties = []


class Property:
    def __init__(self):
        # Assigning placeholder values for each property
        self.name = ""
        self.price = 0
        self.colour = ""
        self.owned_by = ""
        self.rent = 0


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
            file=r"monopoly\fonts\big_font.ttf", family="Kabel Bd", size=20
        )
        self.font = tkextrafont.Font(
            file=r"monopoly\fonts\small_font.ttf", family="Kabel Bd", size=18
        )
        self.small_font = tkextrafont.Font(
            file=r"monopoly\fonts\tiny_font.ttf", family="Kabel Bd", size=12
        )

        # Importing and placing the board
        self.board_image = ImageTk.PhotoImage(file=r"monopoly\textures\board.png")
        self.board = tk.Canvas(self.screen, borderwidth=0)
        self.board.place(width=720, height=720, rely=0.5, anchor="w")
        self.board.create_image(0, 0, image=self.board_image, anchor="nw")
        self.button_background_image = ImageTk.PhotoImage(
            Image.new("RGB", (560, 720), "#D7BAAA")
        )
        self.button_background = tk.Label(
            self.screen, image=self.button_background_image, borderwidth=0
        )
        self.button_background.place(relx=1, rely=0, anchor="ne")
        self.exit_button_image = ImageTk.PhotoImage(file=r"monopoly\textures\exit.png")
        self.exit_button = tk.Button(
            self.screen,
            borderwidth=0,
            image=self.exit_button_image,
            bg="#D7BAAA",
            activebackground="#D7BAAA",
            command=self.root.destroy,
        )
        self.exit_button.place(relx=1, rely=0, anchor="ne")

        # Defining player instances
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_3 = player_3
        self.player_4 = player_4

        # Assigning images to player tokens depending on player choice
        for player in [self.player_1, self.player_2, self.player_3, self.player_4]:
            match player.token:
                case "Hat":
                    player.token_image = ImageTk.PhotoImage(
                        file=r"monopoly\textures\hat_token.png"
                    )
                    player.token_display_image = ImageTk.PhotoImage(
                        file=r"monopoly\textures\hat.png"
                    )
                case "Car":
                    player.token_image = ImageTk.PhotoImage(
                        file=r"monopoly\textures\car_token.png"
                    )
                    player.token_display_image = ImageTk.PhotoImage(
                        file=r"monopoly\textures\car.png"
                    )
                case "Ship":
                    player.token_image = ImageTk.PhotoImage(
                        file=r"monopoly\textures\ship_token.png"
                    )
                    player.token_display_image = ImageTk.PhotoImage(
                        file=r"monopoly\textures\ship.png"
                    )
                case "Dog":
                    player.token_image = ImageTk.PhotoImage(
                        file=r"monopoly\textures\dog_token.png"
                    )
                    player.token_display_image = ImageTk.PhotoImage(
                        file=r"monopoly\textures\dog.png"
                    )

        # Loading dice images
        self.dice_1_image = ImageTk.PhotoImage(file=r"monopoly\textures\dice_1.png")
        self.dice_2_image = ImageTk.PhotoImage(file=r"monopoly\textures\dice_2.png")
        self.dice_3_image = ImageTk.PhotoImage(file=r"monopoly\textures\dice_3.png")
        self.dice_4_image = ImageTk.PhotoImage(file=r"monopoly\textures\dice_4.png")
        self.dice_5_image = ImageTk.PhotoImage(file=r"monopoly\textures\dice_5.png")
        self.dice_6_image = ImageTk.PhotoImage(file=r"monopoly\textures\dice_6.png")

        # Creating property instances and assigning unique values
        self.property_list = []
        self.property_locations = {}
        self.property_locations_list = itertools.cycle(range(1, 41))
        with open(r"monopoly\properties.txt") as file:
            for line in file.readlines():
                self.property_info = line.strip().split("|")
                self.property_instance = Property()
                self.property_locations[
                    next(self.property_locations_list)
                ] = self.property_instance
                self.property_instance.name = self.property_info[0]
                self.property_instance.price = int(self.property_info[1])
                self.property_instance.colour = self.property_info[2]
                self.property_list.append(self.property_instance)

        # Creating info buttons for each player and displaying token
        self.p1_token_display = tk.Label(
            self.screen,
            image=self.player_1.token_display_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        self.p1_token_display.place(x=804, y=20, anchor="nw")
        self.p1_button = tk.Button(
            self.screen,
            text=self.player_1.name,
            font=self.font,
            bg="#C70000",
            activebackground="#770000",
            borderwidth=0,
            command=lambda: [self.display_player_info(self.player_1)],
        )
        self.p1_button.place(width=166, height=60, x=786, y=140, anchor="nw")
        self.p2_token_display = tk.Label(
            self.screen,
            image=self.player_2.token_display_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        self.p2_token_display.place(x=1080, y=17, anchor="nw")
        self.p2_button = tk.Button(
            self.screen,
            text=self.player_2.name,
            font=self.font,
            bg="#C70000",
            activebackground="#770000",
            borderwidth=0,
            command=lambda: [self.display_player_info(self.player_2)],
        )
        self.p2_button.place(width=166, height=60, x=1224, y=140, anchor="ne")
        self.p3_token_display = tk.Label(
            self.screen,
            image=self.player_3.token_display_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        self.p3_token_display.place(x=804, y=222, anchor="nw")
        self.p3_button = tk.Button(
            self.screen,
            text=self.player_3.name,
            font=self.font,
            bg="#C70000",
            activebackground="#770000",
            borderwidth=0,
            command=lambda: [self.display_player_info(self.player_3)],
        )
        self.p3_button.place(width=166, height=60, x=786, y=350, anchor="nw")
        self.p4_token_display = tk.Label(
            self.screen,
            image=self.player_4.token_display_image,
            borderwidth=0,
            bg="#D7BAAA",
        )
        self.p4_token_display.place(x=1076, y=230, anchor="nw")
        self.p4_button = tk.Button(
            self.screen,
            text=self.player_4.name,
            font=self.font,
            bg="#C70000",
            activebackground="#770000",
            borderwidth=0,
            command=lambda: [self.display_player_info(self.player_4)],
        )
        self.p4_button.place(width=166, height=60, x=1224, y=350, anchor="ne")

        # Loading close button and dice image
        self.close_player_info_button_image = ImageTk.PhotoImage(
            file=r"monopoly\textures\close.png"
        )
        self.dice_image = ImageTk.PhotoImage(file=r"monopoly\textures\dice.png")

        # Creating player turn loop
        self.player_loop = itertools.cycle(
            [self.player_1, self.player_2, self.player_3, self.player_4]
        )
        self.player_turn_init(next(self.player_loop))
        windll.shcore.SetProcessDpiAwareness(1)
        self.root.mainloop()

    def display_player_info(self, player):
        # Shows player info after player button is clicked
        self.player_info_text = f"{player.name}\n${player.money}\n\n"
        for title in player.properties:
            self.player_info_text += str(title.name)
            self.player_info_text += "\n"
        self.player_info = tk.Label(
            self.screen,
            text=self.player_info_text,
            borderwidth=0,
            font=self.small_font,
            bg="#8FBC72",
        )
        self.player_info.place(height=280, width=250, x=360, y=360, anchor="center")
        # Shows player info close button
        self.close_player_info_button = tk.Button(
            self.screen,
            borderwidth=0,
            image=self.close_player_info_button_image,
            bg="#8FBC72",
            activebackground="#8FBC72",
            command=lambda: [
                self.player_info.destroy(),
                self.close_player_info_button.destroy(),
            ],
        )
        self.close_player_info_button.place(
            width=24, height=24, x=460, y=245, anchor="center"
        )

    def player_turn_init(self, player):
        self.current_player = player

        # Showing current player's turn
        self.current_player_display = tk.Label(
            self.screen,
            text=f"{self.current_player.name}'s Turn",
            font=self.big_font,
            borderwidth=0,
            bg="#D7BAAA",
        )
        self.current_player_display.place(
            width=220, height=60, x=910, y=422, anchor="nw"
        )

        # Setting up dice and end turn button for current player
        self.dice_button = tk.Button(
            self.screen,
            image=self.dice_image,
            borderwidth=0,
            activebackground="#C70000",
            bg="#C70000",
            command=lambda: [self.player_turn(), self.dice_button.destroy()],
        )
        self.dice_button.place(x=1152, y=602, anchor="nw")
        self.end_turn_button = tk.Button(
            self.screen,
            text="END TURN",
            font=self.font,
            borderwidth=0,
            activebackground="#770000",
            bg="#C70000",
            command=self.end_turn_func,
        )
        self.end_turn_button.place(width=156, height=66, x=980, y=622, anchor="nw")

    def dice_display_func(self, dice_1, dice_2):
        # Displayng dice images based on result
        match dice_1:
            case 1:
                self.dice_1_display = tk.Label(
                    self.screen, image=self.dice_1_image, borderwidth=0, bg="#C4E3A0"
                )
            case 2:
                self.dice_1_display = tk.Label(
                    self.screen, image=self.dice_2_image, borderwidth=0, bg="#C4E3A0"
                )
            case 3:
                self.dice_1_display = tk.Label(
                    self.screen, image=self.dice_3_image, borderwidth=0, bg="#C4E3A0"
                )
            case 4:
                self.dice_1_display = tk.Label(
                    self.screen, image=self.dice_4_image, borderwidth=0, bg="#C4E3A0"
                )
            case 5:
                self.dice_1_display = tk.Label(
                    self.screen, image=self.dice_5_image, borderwidth=0, bg="#C4E3A0"
                )
            case 6:
                self.dice_1_display = tk.Label(
                    self.screen, image=self.dice_6_image, borderwidth=0, bg="#C4E3A0"
                )
        match dice_2:
            case 1:
                self.dice_2_display = tk.Label(
                    self.screen, image=self.dice_1_image, borderwidth=0, bg="#C4E3A0"
                )
            case 2:
                self.dice_2_display = tk.Label(
                    self.screen, image=self.dice_2_image, borderwidth=0, bg="#C4E3A0"
                )
            case 3:
                self.dice_2_display = tk.Label(
                    self.screen, image=self.dice_3_image, borderwidth=0, bg="#C4E3A0"
                )
            case 4:
                self.dice_2_display = tk.Label(
                    self.screen, image=self.dice_4_image, borderwidth=0, bg="#C4E3A0"
                )
            case 5:
                self.dice_2_display = tk.Label(
                    self.screen, image=self.dice_5_image, borderwidth=0, bg="#C4E3A0"
                )
            case 6:
                self.dice_2_display = tk.Label(
                    self.screen, image=self.dice_6_image, borderwidth=0, bg="#C4E3A0"
                )
        self.dice_1_display.place(x=360, y=560, anchor="e")
        self.dice_2_display.place(x=372, y=560, anchor="w")

    def player_turn(self):
        # Rolling the dice
        self.dice_1 = random.randint(1, 6)
        self.dice_2 = random.randint(1, 6)
        self.roll_no = self.dice_1 + self.dice_2
        self.dice_display_func(self.dice_1, self.dice_2)

        # Setting player locations and displaying player landing
        if self.current_player.location + self.roll_no > 40:
            self.roll_difference = 40 - (self.current_player.location + self.roll_no)
            self.current_player.location = -self.roll_difference
            self.salary_display = tk.Label(
                self.screen,
                text=f"{self.current_player.name} Got $200 Salary",
                borderwidth=0,
                bg="#C4E3A0",
                font=self.small_font,
            )
            self.salary_display.place(x=360, y=300, anchor="n")
        else:
            self.current_player.location += self.roll_no
        self.current_player_location_property = self.property_locations[
            self.current_player.location
        ]
        self.current_player_landing_text = f"{self.current_player.name} Rolled a {self.roll_no}\n&\nLanded on {self.current_player_location_property.name}"
        self.current_player_landing = tk.Label(
            self.screen,
            text=self.current_player_landing_text,
            bg="#C4E3A0",
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
        if self.current_player.money <= self.current_player_location_property.price:
            self.current_player.money = 0
        else:
            self.current_player.money -= self.current_player_location_property.price
            self.current_player.properties.append(self.current_player_location_property)
            self.current_player_location_property.owned_by = self.current_player

            # Displaying purchace
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player.name} Purchased {self.current_player_location_property.name} for ${self.current_player_location_property.price}",
                borderwidth=0,
                bg="#C4E3A0",
                font=self.small_font,
            )
            self.action_display.place(x=360, y=260, anchor="n")

        # Increasing rent of color sets (if any)
        self.set_colour = self.current_player_location_property.colour
        self.set_number = 0
        for title in self.current_player_location_property.owned_by.properties:
            if title.colour == self.set_colour:
                self.set_number += 1
        if self.set_colour in [
            "Light Blue",
            "Pink",
            "Orange",
            "Red",
            "Yellow",
            "Green",
        ]:
            match self.set_number:
                case 1:
                    self.rent = self.current_player_location_property.price // 10
                case 2:
                    self.rent = 2 * (self.current_player_location_property.price // 10)
                case 3:
                    self.rent = 4 * (self.current_player_location_property.price // 10)
        elif self.set_colour in ["Brown", "Dark Blue"]:
            match self.set_number:
                case 1:
                    self.rent = self.current_player_location_property.price // 10
                case 2:
                    self.rent = 3 * (self.current_player_location_property.price // 10)
        elif self.set_colour == "Station":
            match self.set_number:
                case 1:
                    self.rent = 25
                case 2:
                    self.rent = 50
                case 3:
                    self.rent = 75
                case 4:
                    self.rent = 100
        for title in self.current_player_location_property.owned_by.properties:
            if title.colour == self.set_colour:
                title.rent = self.rent

    def pay_rent(self):
        # Rent taken from payer and added to reciever
        if self.current_player.money <= self.current_player_location_property.rent:
            self.current_player.money = 0
        else:
            self.current_player.money -= self.current_player_location_property.rent
            self.current_player_location_property.owned_by.money += (
                self.current_player_location_property.rent
            )
        self.action_display = tk.Label(
            self.screen,
            text=f"{self.current_player.name} Paid ${self.current_player_location_property.rent} to {self.current_player_location_property.owned_by.name}",
            borderwidth=0,
            bg="#C4E3A0",
            font=self.small_font,
        )
        self.action_display.place(x=360, y=260, anchor="n")

    def pay_tax(self):
        # Tax taken from user
        if self.current_player.money <= self.current_player_location_property.price:
            self.current_player.money = 0
        else:
            self.current_player.money -= self.current_player_location_property.price
        self.action_display = tk.Label(
            self.screen,
            text=f"{self.current_player.name} Paid ${self.current_player_location_property.price} in tax",
            borderwidth=0,
            bg="#C4E3A0",
            font=self.small_font,
        )
        self.action_display.place(x=360, y=260, anchor="n")

    def pay_utility(self):
        # Checks dice roll number and charges accordingly
        self.serive_count = 0
        for title in self.current_player_location_property.owned_by.properties:
            if title.colour == "Utility":
                self.serive_count += 1
        if self.serive_count == 1:
            if self.current_player.money <= self.current_player_location_property.rent:
                self.current_player.money = 0
            else:
                self.current_player.money -= self.roll_no * 4
                self.current_player_location_property.owned_by.money += self.roll_no * 4
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player.name} Paid ${self.roll_no*4} to {self.current_player_location_property.owned_by.name}",
                borderwidth=0,
                bg="#C4E3A0",
                font=self.small_font,
            )
            self.action_display.place(x=360, y=260, anchor="n")
        elif self.serive_count == 2:
            if self.current_player.money <= self.current_player_location_property.rent:
                self.current_player.money = 0
            else:
                self.current_player.money -= self.roll_no * 10
                self.current_player_location_property.owned_by.money += (
                    self.roll_no * 10
                )
            self.action_display = tk.Label(
                self.screen,
                text=f"{self.current_player.name} Paid ${self.roll_no*10} to {self.current_player_location_property.owned_by.name}",
                borderwidth=0,
                bg="#C4E3A0",
                font=self.small_font,
            )
            self.action_display.place(x=360, y=260, anchor="n")


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
#                 if token_1 not in ["Hat", "Car", "Ship", "Dog"]:
#                     raise TypeError
#                 player_2_name = input("\nEnter Player 2 name: ")
#                 token_2 = input("1) Hat\n2) Car\n3) Ship\n4) Dog\n~ ")
#                 if token_2 not in ["Hat", "Car", "Ship", "Dog"]:
#                     raise TypeError
#                 player_3_name = input("\nEnter Player 3 name: ")
#                 token_3 = input("1) Hat\n2) Car\n3) Ship\n4) Dog\n~ ")
#                 if token_3 not in ["Hat", "Car", "Ship", "Dog"]:
#                     raise TypeError
#                 player_4_name = input("\nEnter Player 4 name: ")
#                 token_4 = input("1) Hat\n2) Car\n3) Ship\n4) Dog\n~ ")
#                 if token_4 not in ["Hat", "Car", "Ship", "Dog"]:
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
