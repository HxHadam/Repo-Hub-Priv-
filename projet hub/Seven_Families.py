#!/usr/bin/env python3
import tkinter as tk
import random
import threading
import pygame

FAMILY_EMOJIS = {
    'Cat': '🐱',
    'Dog': '🐶',
    'Monkey': '🐵',
    'Frog': '🐸',
    'Unicorn': '🦄',
    'Octopus': '🐙',
    'Turtle': '🐢'
}

MEMBER_EMOJIS = {
    'Grandfather': '👴',
    'Grandmother': '👵',
    'Father': '👨',
    'Mother': '👩',
    'Son': '👦',
    'Daughter': '👧'
}

pygame.mixer.init()
pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def play_sound(file, volume=1.0):
    def worker():
        pygame.mixer.Sound(file).set_volume(volume)
        pygame.mixer.Sound(file).play()
    threading.Thread(target=worker, daemon=True).start()

class Card:
    def __init__(self, family, member):
        self.family = family
        self.member = member
        self.emoji = FAMILY_EMOJIS[family] + MEMBER_EMOJIS[member]

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.completed_families = []

    def has_card(self, family, member):
        return any(card.family == family and card.member == member for card in self.hand)

    def give_card(self, family, member):
        for card in self.hand:
            if card.family == family and card.member == member:
                self.hand.remove(card)
                return card
        return None

class JeuDes7FamillesGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu des 7 Familles – Emoji Edition")
        self.players = [Player("Player 1"), Player("Player 2")]
        self.current_player = 0
        self.deck = self.create_deck()
        self.deal_cards()
        self.level = 1
        self.max_level = 5
        self.lives = 3
        self.selected_cell = None
        self.grid_buttons = []
        self.grid_data = []
        self.user_grid = []
        self.display_time = 4000
        self.sound_volume = 0.5

        self.setup_volume_control()
        self.start_screen()

    def create_deck(self):
        deck = []
        for family in FAMILY_EMOJIS.keys():
            for member in MEMBER_EMOJIS.keys():
                deck.append(Card(family, member))
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        for i in range(7):
            self.players[0].hand.append(self.deck.pop())
            self.players[1].hand.append(self.deck.pop())

    def setup_volume_control(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)
        tk.Label(control_frame, text="🔊 Volume:", font=("Arial", 10)).pack(side="left")
        self.volume_slider = tk.Scale(control_frame, from_=0, to=100, orient="horizontal", length=150, command=self.update_volume)
        self.volume_slider.set(50)
        self.volume_slider.pack(side="left")

    def update_volume(self, val):
        vol = int(val) / 100
        self.sound_volume = vol
        pygame.mixer.music.set_volume(vol)

    def start_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="🧠 Jeu des 7 Familles", font=("Arial", 28)).pack(pady=20)
        tk.Button(self.root, text="Start Game", font=("Arial", 16), command=self.start_turn).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Scale):
                widget.destroy()
        self.grid_buttons.clear()

    def start_turn(self):
        self.clear_screen()
        self.selected_cell = None
        self.show_player_hand(self.players[self.current_player])

    def show_player_hand(self, player):
        hand_frame = tk.Frame(self.root)
        hand_frame.pack(pady=10)

        for card in player.hand:
            btn = tk.Button(hand_frame, text=card.emoji, font=("Arial", 22), width=6, height=3,
                            command=lambda c=card: self.select_card(c))
            btn.pack(side="left", padx=5)

        self.ask_for_card(player)

    def ask_for_card(self, player):
        ask_frame = tk.Frame(self.root)
        ask_frame.pack(pady=10)

        tk.Label(ask_frame, text="Ask for a card!", font=("Arial", 16)).pack()

        self.family_choice = tk.StringVar(value="Cat")
        family_menu = tk.OptionMenu(ask_frame, self.family_choice, *FAMILY_EMOJIS.keys())
        family_menu.pack(side="left", padx=5)

        self.member_choice = tk.StringVar(value="Father")
        member_menu = tk.OptionMenu(ask_frame, self.member_choice, *MEMBER_EMOJIS.keys())
        member_menu.pack(side="left", padx=5)

        tk.Button(ask_frame, text="Ask", font=("Arial", 16), command=self.process_request).pack(pady=10)

    def process_request(self):
        family = self.family_choice.get()
        member = self.member_choice.get()
        card = self.players[1 - self.current_player].give_card(family, member)

        if card:
            play_sound("correct.wav", self.sound_volume)
            self.players[self.current_player].hand.append(card)
            self.check_for_completed_families(self.players[self.current_player])
        else:
            play_sound("fail.wav", self.sound_volume)

        self.current_player = 1 - self.current_player
        self.start_turn()

    def check_for_completed_families(self, player):
        for family in FAMILY_EMOJIS.keys():
            family_cards = [card for card in player.hand if card.family == family]
            if len(family_cards) == 6:
                player.completed_families.append(family)
                play_sound("correct.wav", self.sound_volume)
                self.show_completed_family(family)

    def show_completed_family(self, family):
        completed_frame = tk.Frame(self.root)
        completed_frame.pack(pady=10)
        tk.Label(completed_frame, text=f"{family} Family Completed!", font=("Arial", 18)).pack()

    def show_result(self, message):
        self.clear_screen()
        tk.Label(self.root, text=message, font=("Arial", 24)).pack(pady=20)
        tk.Button(self.root, text="Play Again", font=("Arial", 16), command=self.reset_game).pack(pady=10)

    def reset_game(self):
        self.players = [Player("Player 1"), Player("Player 2")]
        self.current_player = 0
        self.deck = self.create_deck()
        self.deal_cards()
        self.start_screen()

if __name__ == "__main__":
    root = tk.Tk()
    game = JeuDes7FamillesGame(root)
    root.mainloop()
