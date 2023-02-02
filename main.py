from assets.player import Player
from assets.card import Card
from assets.game import Game

def main():
    main_player = input('Insert your desired name: ')

    p1 = Player(main_player.capitalize(), True)
    p2 = Player("Nelson")
    p3 = Player("Martha")
    p4 = Player("Alice")
    players = [p1, p2, p3, p4]

    game = Game(players)
    game.init()

if __name__ == '__main__':
    main()
