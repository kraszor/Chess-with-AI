from game import Game
import sys


def main():
    Chess = Game()
    Chess.menu()
    left, right, replay = Chess.pick_menu_option()
    if left:
        Chess.play()
    if right:
        Chess.play(True)
    while True:
        Chess.ending_screen()
        left, right, replay = Chess.pick_menu_option(True)
        if left:
            main()
        if right:
            sys.exit(0)
        if replay:
            Chess.replay(Chess.history)


if __name__ == "__main__":
    main()
