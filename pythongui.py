import tkinter as tk
from tkinter import messagebox
from deckofcards import DeckOfCards  # Import the DeckOfCards class

class Player:
    # class to represent a player with a hand of cards
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def draw_card(self):
        # method to draw a card from the player's hand
        if len(self.hand) > 0:
            return self.hand.pop()
        else:
            return None

    def play_card(self, card):
        # method to play a card to the player's hand
        self.hand.append(card)

class SnapPlayer(Player):
    # subclass of Player for the Snap game
    def draw_card(self):
        # method to draw a card in the Snap game and print a message
        card = super().draw_card()
        if card:
            print(f"{self.name} places {card} (Cards in hand: {len(self.hand)})")
            return card
        else:
            return None

class SnapGame:
    # class to represent the Snap game
    def __init__(self, players):
        self.players = [SnapPlayer(player_name, player_hand) for player_name, player_hand in players]
        self.middle_deck = []
        self.current_player = 0

    def remove_player(self, player_name):
        # method to remove a player from the game
        self.players = [player for player in self.players if player.name != player_name]
        if self.current_player >= len(self.players):
            self.current_player = 0

    def switch_turn(self):
        # method to switch to the next player's turn
        self.current_player = (self.current_player + 1) % len(self.players)

    def play_round(self):
        # method to play a round of the Snap game
        snap_player = None
        current_player = self.players[self.current_player]

        drawn_card = current_player.draw_card()
        if drawn_card:
            self.middle_deck.append(drawn_card)

            if len(self.middle_deck) > 1 and self.middle_deck[-1].value == self.middle_deck[-2].value:
                snap_player = current_player

        if snap_player:
            print(f"{snap_player.name} calls snap (cards in hand: {len(snap_player.hand)})")
            snap_player.hand.extend(self.middle_deck)
            self.middle_deck = []

        self.switch_turn()

    def check_empty_hands(self):
        # method to check for players with empty hands
        return [player for player in self.players if len(player.hand) > 0]

class SnapGUI:
    def __init__(self, master, num_players, player_info):
        # gui class for the Snap game
        self.master = master
        self.master.title("Snap Card Game")

        self.game = SnapGame(player_info)

        # label to display the current player's turn and instruction
        self.current_player_label = tk.Label(master, text="")
        self.current_player_label.pack()

        # label to display the top card of the middle deck
        self.middle_deck_label = tk.Label(master, text="Middle Deck")
        self.middle_deck_label.pack()

        # canvas to draw the game elements (cards and boxes)
        self.canvas = tk.Canvas(master, width=800, height=400)
        self.canvas.pack()

        # list to store player card boxes
        self.player_boxes = []
        for i in range(num_players):
            player_box = self.create_card_box(50 + i * 150, 300)
            self.player_boxes.append(player_box)

        # player box for displaying the top card of the middle deck
        self.middle_deck_box = self.create_card_box(400, 150)

        # list to store labels displaying the count of cards for each player
        self.player_count_labels = []
        for i in range(num_players):
            count_label = tk.Label(master, text=f"{player_info[i][0]}'s Cards: {len(player_info[i][1])}")
            count_label.pack()
            self.player_count_labels.append(count_label)

        # button to play a card in the game
        self.play_button = tk.Button(master, text="Play Card", command=self.play_round)
        self.play_button.pack()

        # initial display of the game elements
        self.update_display()

    def create_card_box(self, x, y):
        # function to create a card box on the canvas at the specified coordinates
        box_size = 100
        card_box = self.canvas.create_rectangle(x, y, x + box_size, y + box_size, outline='black', width=2)
        card_text = self.canvas.create_text((x + x + box_size) // 2, (y + y + box_size) // 2, text="", font=("Arial", 12))
        return card_box, card_text

    def update_display(self):
        # update the display of the game elements on the gui

        # display the current player's turn and instruction
        current_player = self.game.players[self.game.current_player]
        self.current_player_label.config(text=f"{current_player.name}, press Play Card to place your card.")

        # display the top card of the middle deck
        middle_deck_text = f"{str(self.game.middle_deck[-1])}" if self.game.middle_deck else "Empty"
        self.middle_deck_label.config(text=f"Middle Deck: {middle_deck_text}")

        # display the top card of each player's hand
        for i, (player_box, card_text) in enumerate(self.player_boxes):
            top_card = current_player.hand[-1] if i == self.game.current_player else self.game.players[i].hand[-1]
            card_text_value = f"{top_card.value}\nof\n{top_card.suit}" if top_card else "Empty"
            self.canvas.itemconfig(card_text, text=card_text_value)

        # display the count of cards for each player
        for i, player_count_label in enumerate(self.player_count_labels):
            player_count_label.config(text=f"{self.game.players[i].name}'s Cards: {len(self.game.players[i].hand)}")

        # display the top card of the middle deck on the designated box
        middle_deck_card = self.game.middle_deck[-1] if self.game.middle_deck else None
        middle_deck_card_text = f"{middle_deck_card.value}\nof\n{middle_deck_card.suit}" if middle_deck_card else "Empty"
        self.canvas.itemconfig(self.middle_deck_box[1], text=middle_deck_card_text)

    def play_round(self):
        # method to handle playing a round of the game
        current_player = self.game.players[self.game.current_player]
        drawn_card = current_player.draw_card()

        if drawn_card:
            self.game.middle_deck.append(drawn_card)

            if len(self.game.middle_deck) > 1 and self.game.middle_deck[-1].value == self.game.middle_deck[-2].value:
                snap_player = current_player
                messagebox.showinfo("Snap!", f"{snap_player.name} calls snap (cards in hand: {len(snap_player.hand)})")
                snap_player.hand.extend(self.game.middle_deck)
                self.game.middle_deck = []

        self.game.switch_turn()

        players_with_cards = self.game.check_empty_hands()
        for current_player in self.game.players:
            if current_player not in players_with_cards:
                messagebox.showinfo("Player Out", f"{current_player.name} is out of the game.")

                self.game.remove_player(current_player.name)
                if len(players_with_cards) == 1:
                    messagebox.showinfo("Game Over", f"{players_with_cards[0].name} wins!")
                    self.master.destroy()
                elif len(players_with_cards) == 0:
                    messagebox.showinfo("Game Over", "No players have any cards left. The game is over.")
                    self.master.destroy()
                return

        self.update_display()

def play():
    # function to start and run the Snap game
    num_players = int(input("Number of players: "))
    deck = DeckOfCards()
    deck.shuffle()
    player_hands = [deck.cards[i * (52 // num_players):(i + 1) * (52 // num_players)] for i in range(num_players)]

    player_info = []
    for i in range(num_players):
        name = input(f"Enter player {i + 1} name: ")
        player_info.append((name, player_hands[i]))

    print("\nPlayer Hands:")

    root = tk.Tk()
    gui = SnapGUI(root, num_players, player_info)
    root.mainloop()

play()
