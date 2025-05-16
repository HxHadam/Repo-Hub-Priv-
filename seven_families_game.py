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
pygame.mixer.music.load("sounds/bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def play_sound(file, volume=1.0):
    def worker():
        sound = pygame.mixer.Sound(file)
        sound.set_volume(volume)
        sound.play()
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
        self.discard_pile = []
        self.deal_cards()
        self.sound_volume = 0.5
        self.volume_slider = None
        self.main_menu()

    def create_deck(self):
        deck = [Card(f, m) for f in FAMILY_EMOJIS for m in MEMBER_EMOJIS]
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        for _ in range(7):
            self.players[0].hand.append(self.deck.pop())
            self.players[1].hand.append(self.deck.pop())

    def setup_volume_slider(self, parent):
        if self.volume_slider is not None:
            self.volume_slider.destroy()

        self.volume_slider = tk.Scale(parent, from_=0, to=100, orient="horizontal", command=self.update_volume)
        self.volume_slider.set(self.sound_volume * 100)
        self.volume_slider.pack(pady=10)

    def update_volume(self, val):
        vol = int(val) / 100
        self.sound_volume = vol
        pygame.mixer.music.set_volume(vol)

    def main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="🧠 Jeu des 7 Familles", font=("Arial", 26)).pack(pady=20)
        tk.Button(self.root, text="▶️ Démarrer la partie", font=("Arial", 16), command=self.start_turn).pack(pady=10)
        tk.Button(self.root, text="📘 Règles du jeu", font=("Arial", 14), command=self.show_rules).pack(pady=5)
        tk.Button(self.root, text="⚙️ Paramètres", font=("Arial", 14), command=self.settings_menu).pack(pady=5)

    def settings_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="⚙️ Paramètres", font=("Arial", 26)).pack(pady=20)
        tk.Label(self.root, text="Ajustez le volume sonore", font=("Arial", 18)).pack(pady=10)

        self.setup_volume_slider(self.root)

        tk.Button(self.root, text="⬅️ Retour", font=("Arial", 14), command=self.main_menu).pack(pady=20)

    def show_rules(self):
        self.clear_screen()
        tk.Label(self.root, text="📘 Règles du Jeu des 7 Familles", font=("Arial", 20)).pack(pady=10)
        rules = (
            "- Le but est de réunir les 6 membres de chaque famille.\n"
            "- À chaque tour, un joueur peut demander une carte à l'autre joueur.\n"
            "- Si le joueur adverse possède la carte, il la donne.\n"
            "- Sinon, le joueur pioche une carte.\n"
            "- Le premier à compléter toutes les familles gagne."
        )
        tk.Label(self.root, text=rules, font=("Arial", 14), justify="left").pack(pady=10)
        tk.Button(self.root, text="⬅️ Retour", font=("Arial", 14), command=self.main_menu).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_turn(self):
        self.clear_screen()
        self.show_player_hand(self.players[self.current_player])
        self.display_deck()
        self.display_discard()

    def show_player_hand(self, player):
        tk.Label(self.root, text=f"🎮 {player.name}", font=("Arial", 18)).pack(pady=5)
        hand_frame = tk.Frame(self.root)
        hand_frame.pack(pady=10)
        for card in player.hand:
            btn = tk.Label(hand_frame, text=card.emoji, font=("Arial", 22), width=5)
            btn.pack(side="left", padx=2)
        self.ask_for_card(player)

    def display_deck(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Button(frame, text=f"🂠 Pioche ({len(self.deck)})", font=("Arial", 16), command=self.draw_card).pack(side="left", padx=10)

    def display_discard(self):
        frame = tk.Frame(self.root)
        frame.pack()
        top = self.discard_pile[-1].emoji if self.discard_pile else "🗑️"
        tk.Label(frame, text=f"Défausse : {top}", font=("Arial", 16)).pack()

    def draw_card(self):
        if self.deck:
            drawn = self.deck.pop()
            self.players[self.current_player].hand.append(drawn)
            self.check_completed_families(self.players[self.current_player])
            self.check_end_game()
            self.start_turn()
        else:
            self.show_result("Plus de cartes !")

    def ask_for_card(self, player):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Label(frame, text="Demander une carte :", font=("Arial", 14)).pack()

        self.family_choice = tk.StringVar(value="Cat")
        tk.OptionMenu(frame, self.family_choice, *FAMILY_EMOJIS).pack(side="left", padx=5)

        self.member_choice = tk.StringVar(value="Father")
        tk.OptionMenu(frame, self.member_choice, *MEMBER_EMOJIS).pack(side="left", padx=5)

        tk.Button(frame, text="Demander", command=self.process_request).pack(side="left", padx=10)

    def process_request(self):
        fam = self.family_choice.get()
        mem = self.member_choice.get()
        opponent = self.players[1 - self.current_player]
        card = opponent.give_card(fam, mem)

        if card:
            play_sound("sounds/correct.mp3", self.sound_volume)
            self.players[self.current_player].hand.append(card)
            self.check_completed_families(self.players[self.current_player])
        else:
            play_sound("sounds/fail.mp3", self.sound_volume)
            self.draw_card()

        self.discard_pile.append(Card(fam, mem))
        self.check_end_game()
        self.current_player = 1 - self.current_player
        self.start_turn()

    def check_completed_families(self, player):
        for family in FAMILY_EMOJIS:
            cards = [c for c in player.hand if c.family == family]
            if len(cards) == 6 and family not in player.completed_families:
                player.completed_families.append(family)
                play_sound("sounds/correct.mp3", self.sound_volume)
                self.show_completed_family(family)

    def show_completed_family(self, family):
        tk.Label(self.root, text=f"🎉 Famille {family} complétée !", font=("Arial", 16), fg="green").pack(pady=5)

    def check_end_game(self):
        player = self.players[self.current_player]
        if len(player.completed_families) == len(FAMILY_EMOJIS):
            self.show_result(f"{player.name} a gagné!")
            play_sound("victory.wav", self.sound_volume)

    def show_result(self, message):
        self.clear_screen()
        tk.Label(self.root, text=message, font=("Arial", 22)).pack(pady=20)
        tk.Button(self.root, text="🔁 Rejouer", command=self.reset_game).pack()

    def reset_game(self):
        self.players = [Player("Player 1"), Player("AI")]
        self.deck = self.create_deck()
        self.discard_pile = []
        self.current_player = 0
        self.deal_cards()
        self.start_turn()

if __name__ == "__main__":
    root = tk.Tk()
    game = JeuDes7FamillesGame(root)
    root.mainloop()
