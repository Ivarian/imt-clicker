# -*- coding: utf-8 -*-

# Imports
import random as rd
import time
import sys
import argparse
from pynput.keyboard import KeyCode
from achievements import earn, milestones, achievement_list
from strings import imt_logo, morse, mit_logo
from pynput import keyboard
import ui


# Intro cutscene
def play_intro():

    # 1% chance to get the easter egg MIT logo instead of the regular IMT logo
    if rd.randint(0, 99) == 0:
        logo = mit_logo
        mit_easter_egg = True
    else:
        logo = imt_logo
        mit_easter_egg = False

    print("Bienvenue à l'expérience immersive de...")
    time.sleep(1)
    for line in logo:
        print(line)
        time.sleep(0.5)
    for c in "      ":
        sys.stdout.write(c)
        sys.stdout.flush()
    for c in "C L I C K E R":
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.25)
    time.sleep(1)

    if mit_easter_egg:
        print()
        earn("♪ Telecom est une école internationale ♪")

    print("\nAppuyez sur Entrée pour cliquer, et sur \"h\" pour une liste des commandes :)")


class Game:

    def __init__(self, gui_mode=False, debug_mode=False):

        # Variables
        self.credits_ects = 0
        self.professor = 0 #note : might need a better structure in the future as more upgrades get addedN
        self.enter_pressed = False
        self.game_over = False

        if not debug_mode:
            play_intro()

        # Game is either text-only or GUI-based
        if gui_mode:
            self.start_game_gui_mode()
        else:
            self.start_game_text_mode()

    def get_n_credits(self, n):
        self.credits_ects += n
        if self.credits_ects in milestones: #note: broken in current state since we are likely to go over milestones
            earn(milestones[self.credits_ects])

    def buy_a_professor(self, professor_price=10): #should probably store professor price somewhere
        assert(self.credits_ects>=10)
        self.credits_ects = self.credits_ects - professor_price
        self.professor += 1

    def earn_upgrade_credits(self): #called every X seconds in main
        self.credits_ects += self.professor
        print("Vos profs ont bien travaillé!")

    def get_a_credit(self):
        self.credits_ects += 1
        print(f"Vous avez {self.credits_ects} crédits ECTS !")

        if rd.randint(0, 999) == 0:
            print(morse)
            print("Vous avez trouvé un morse ! Curieux.")
            earn("Morse")

        if self.credits_ects in milestones:
            earn(milestones[self.credits_ects])

    def on_release(self, key):
        if key == keyboard.Key.enter:  # click
            self.get_a_credit()

        elif key == KeyCode.from_char('a'):
            print("List of achievements:")
            print([key if achievement_list[key] else "???" for key in achievement_list])

        elif key == KeyCode.from_char('h'):
            print('''List of commands:
        h (help): display this message
        a (achievements): view achievements
        Enter: click
        Esc: quit game''')

        elif key == KeyCode.from_char('c'):
            print("Nan, pour cliquer faut juste faire entrée sans rien écrire")

        elif key == keyboard.Key.esc:  # exit game
            self.game_over = True
            return False

        else:
            print("Invalid command. Did you mean \"c\" (click)?")


    def start_game_gui_mode(self):

        game_ui = ui.launch_widget(self)

        # create game ui which takes the game as input when button is clicked, you can handle everything in the ui
        # itself by calling the appropriate game functions over there
        while not self.game_over:
            pass

        print("Game finished!")

    # Game logic
    def start_game_text_mode(self):
        listener = keyboard.Listener(on_release=self.on_release)
        listener.start()
        while not self.game_over:
            pass
        print("Game finished!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", action="store_true",
                        help="launches in GUI mode")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="launches in debug mode (skips intro)")
    args = parser.parse_args()
    Game(args.gui, args.debug)

