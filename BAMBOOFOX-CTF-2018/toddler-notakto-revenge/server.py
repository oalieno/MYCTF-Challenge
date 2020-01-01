#!/usr/bin/env python3
from Notakto import Notakto
from Notakto.utils import empty_board, pretty_board
from Notakto.constants import BOARD_TEMPLATE
from Notakto.exceptions import NotaktoError

normal = '\033[0m'
bold = '\033[1m'
red = '\033[91m'
green = '\033[92m'

print("========== Welcome to the Notakto Game ==========")
print("Notakto is tic-tac-toe with both players playing the same piece ( an 'X' )")
print("The player who end the game will {}LOSE THE GAME{}".format(bold + red, normal))
print("")
print(BOARD_TEMPLATE.format(*range(9)))

for i in range(1, 101):
    print("========== {} Round ==========".format(i))
    notakto = Notakto(1)
    while True:
        try:
            move = int(input("Your move: "))

            notakto.move(0, move // 3, move % 3)
            if notakto.is_finish():
                print("{}YOU LOSE{}".format(bold + red, normal))
                exit(0)
            print(pretty_board(notakto.boards[0]))

            result = notakto.move_optimize()
            if notakto.is_finish():
                print("{}YOU WIN{}".format(bold + green, normal))
                break
            print("My move: {}".format(result.x * 3 + result.y))
            print(pretty_board(notakto.boards[0]))

        except NotaktoError:
            print("Your move is invalid...")
            exit(0)

print("BAMBOOFOX{N0t4ktO_IS_fUn_iS_It}")
