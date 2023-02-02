from sys import exit
from time import sleep
from re import match
from random import randint
from json import load

from assets.utils import *
from assets.card import Card

class Game:
    def __init__(self, players):
        self.players = players
        self.table_card = 0
        self.deck = []
            # To reuse used deck
        self.played_cards = []

    def getPlayer(self, position):
        return self.players[position]

    def getPlayers(self):
        return self.players

    def getPlayerQuantity(self):
        return len(self.players)

    def getTableCard(self):
        return self.table_card

    def showTableCard(self):
        card_output = colorize(self.table_card)
        return f'Table Card: {card_output}'

    def setTableCard(self, card):

        self.table_card = card
            # Adds new card to played cards array
        self.played_cards.append(self.table_card)

        # Assemble deck from the json
    def deckAssemble(self):
            # reads json
        with open('assets/deck.json','r') as file:
            cards = load(file)

        for card in cards:
            self.deck.append(
                Card(card['color'],
                    card['number'],
                    card['usage']
                )
            )

    def init(self):
        self.deckAssemble()
        self.drawCards()
        self.start()

    def __str__(self):
        self.output("Players: ")
        for player in self.players:
            self.output(f'Player: {player}')

        self.output("Cards in deck")
        for card in self.deck:
            self.output(f'Card {card}')

        self.output("Table card")
        self.output(self.table_card)

    def drawCard(self):
        deck_size = len(self.deck) - 1
        random_number = randint(1,deck_size)

        return self.deck.pop(random_number)

    def drawCards(self):
        quant_cards = 7
        for player in self.players:
            for i in range(quant_cards):
                player.addCard(self.drawCard())

        # Draws card to the table
        self.setTableCard(self.drawCard())

    def autoPlay(self, player, table_card):
        cards = player.getCards()
        player_name = player.getName()
        next_player_action = False

        # player.showCards()
        for index, card in enumerate(cards):
            played = False
            if self.isPlayable(card, table_card):

                played_card = player.playCard(index)
                self.playCard(player, played_card)
                next_player_action = self.actionCard(played_card, player)

                played = True
                break
            # No playable cards in player deck
            # makes him buy automatically
        if not played:
            bought_card = self.buyCardOption(player)

                # Question if wanted to play the bought card
            if self.isPlayable(bought_card, table_card):
                    # Bring last added card info to test playability
                played_card = player.playCard(-1)
                self.playCard(player, played_card)
                next_player_action = self.actionCard(played_card, player)

        return next_player_action

    def isPlayable(self, play_card, table_card):

        def equalCheck(card1, card2):
            if card1 == card2:
                return True
            else:
                return False

        tc_color = table_card.getColor()
        tc_usage = table_card.getUsage()
        tc_number = table_card.getNumber()

        p_color = play_card.getColor()
        p_usage = play_card.getUsage()
        p_number = play_card.getNumber()

        playable = False

        # Wild card or Color change (Wild cards)
        if tc_color == 0 or p_color == 0:
            playable = True
        elif p_color == 0 and (p_usage == 2 or p_usage == 4):
            # print('flag1')
            playable = True
        # Colored cards
        elif p_usage == 0 or p_usage == 1 or p_usage == 3 or p_usage == 5:
            # Checks for same color
            if equalCheck(tc_color, p_color):
                playable = True
            # Checks for matching number
            elif equalCheck(tc_number, p_number):
                playable = True
        else:
            # Checks for same usage (+2 with +2, etc)
            if equalCheck(tc_usage, p_usage):
                playable = True

        # Return if its playable (True) or not (False)
        return playable

    def buyCard(self, player, amount):
        player_name = player.getName()

        for i in range(amount):
            player.addCard(self.drawCard())

        if amount > 1:
            ext = f' {amount} Cards'
        else:
            ext = '.'

        out_str = f"{player_name} bought{ext}"
        self.output(out_str, True)

        # Card buying function
    def buyCardOption(self, player):
        player_name = player.getName()
        bought_card = self.drawCard()
        player.addCard(bought_card)

        out_str = f"{player_name} bought."
        self.output(out_str, True)

        return bought_card

    def colorChange(self, table_card, pre_chosen = False):
        if not pre_chosen:
            color_options = '     '
            for index, color in enumerate(Color):
                if index != 0:
                    color_options += f'{index}: {getTermColor(index)}{color.name.capitalize()}{getTermColor(5)} '

            while(True):
                chosen_color = int(input(f'{color_options}\n     Choose a color: '))
                table_card.setColor(chosen_color)

                if chosen_color >= 1 and chosen_color <= 4:
                    break
                else:
                    self.output("Invalid option... Try again.", True)
        else:
            chosen_color = pre_chosen
            table_card.setColor(chosen_color)

        chosen_color_name = Color(chosen_color).name.capitalize()
        self.output(f'Chose the color {getTermColor(chosen_color)}{chosen_color_name}{getTermColor(5)}', True)

    def actionCard(self, card, player):
        preferred_color = False
        type = card.getUsage()

        if not player.isPlayer():
            preferred_color = player.preferredColor()
            # +4 and selects color

        if type == 2:
            self.colorChange(card, preferred_color)

            # To select color
        elif type == 4:
            self.colorChange(card, preferred_color)

        return type

    def actionTableCard(self, card, player):
        type = card.getUsage()
        player_name = player.getName()

        r = False
        if type > 0:
                # Buy two [+2]
            if type == 1:
                self.buyCard(player, 2)
                r = True

                # Buy four [+4]
            elif type == 2:
                self.buyCard(player, 4)
                r = True

                # Next player blocked
            elif type == 3:
                out_str = f"{player_name} is blocked for this round"
                self.output(out_str, True)
                r = True

        return r

    def playedCardMessage(self, player_name, card):
        output = f'{player_name} played {card}'
        self.output(output, True)

    def playCard(self, player, card):
        player_name = player.getName()

        self.setTableCard(card)
        self.playedCardMessage(player_name, card)

        # Validate input is integer
    def intInput(self, input_data):
        received_input_str = str(input_data)
        r = False

            # Checks if empty input
        if len(received_input_str) != 0:
                # Only numbers in the string
            if match('[0-9]+', received_input_str) is not None:
                r = True

        return r

    def askInput(self, qnt_cards):
        self.output("Draw card type: 'buy'", True)
        input_data = input("     Choose (Play a card or buy): ")

        return input_data

    def validateInput(self, input_data, qnt_cards):
        if input_data > qnt_cards:
            self.output("No card in inserted index", True)
            return False
        else:
            return True

    def reverseCardPlayed(self, reverse_status):
        new_reverse_status = False
        if reverse_status == True:
            new_reverse_status = False
        else:
            new_reverse_status = True

        return new_reverse_status

        # Checks for empty hand, winning the game
    def checkEndGame(self, player):
        if not player.cards:
            player_name = player.getName()
            self.output(f"\nGame Over.")
            self.output(f"{player_name} Wins!")
            exit()

    def output(self, string, indent = False):
        sleep(0.25)
        indent_str = ''
        if indent:
            indent_str = '     '

        if string:
            print(f"{indent_str}{string}")

    def start(self):
        reversed = False
        next_player_action = False
            # Last player position in the array
        max_player_position = self.getPlayerQuantity() - 1
            # so as it increments, first player (Player 0) goes first
        i = max_player_position

        while(True):
                # Loop through number of players
            last_player_position = i
            if not reversed:
                i += 1
                if i > max_player_position:
                    i = 0
            else:
                    # If card reverse gets played, next player is the player before the one that just played
                i = last_player_position - 1
                    # Negates number going negative
                    # sending position (i) to last player instead
                if i < 0:
                    i = max_player_position

                # returns this turns player
            player = self.getPlayer(i)


            player_name = player.getName()
            card_amount = player.qntCards(False)
            self.output(f"{player_name}'s turn! - {card_amount} Cards")

            table_card = self.getTableCard()
            print(f'Table card: {table_card}')

                # Action card verify
            if next_player_action:
                next_player_action = self.actionTableCard(table_card, player)

                # Checks for action cards for this turn (+2, +4, block)
            if next_player_action:
                next_player_action = False

            elif player.isPlayer():
                self.output("Your turn! Options: ", True)

                    # Display the cards and returns the number of cards in hand
                qnt_cards = player.qntCards()

                while(True):
                    played_card = False
                    player_bought = False

                        # Display cards to choose
                    self.output(player.showCards(), True)
                    input_data = self.askInput(qnt_cards)

                        # It'll always arrive a string because input ...
                    if self.intInput(input_data):
                        input_data = int(input_data)

                    if input_data == 'buy' or input_data == 'b':
                        bought_card = self.buyCardOption(player)
                        self.output(f"You bought: {bought_card}", True)

                            # Question if wanted to play the bought card
                        if self.isPlayable(bought_card, table_card):
                            play_bought_card = input(f"     Wish to play it now? y\\n: ")
                            if play_bought_card.lower() == 'y':
                                    # Bring last added card info to test playability
                                played_card = player.getCard(-1)
                        else:
                            break
                    else:
                        if self.intInput(input_data):
                            validate_input = self.validateInput(input_data, qnt_cards)
                                # If number doesnt exceed number of positions in the array
                            if validate_input:
                                    # Gets the card to test playability
                                played_card = player.getCard(input_data)

                        # Breaks the loop
                    if played_card and self.isPlayable(played_card, table_card):

                            # In case played recently bought card (Used string command)
                        if not self.intInput(input_data):
                            input_data = -1

                            # Removes card from player deck and returns it
                        played_card = player.playCard(input_data)

                            # Inserts card into the table
                        self.playCard(player, played_card)

                            # Checks for UNO call
                        self.output(player.unoCheck(), True)

                        next_player_action = self.actionCard(played_card, player)

                        if next_player_action == 5:
                            reversed = self.reverseCardPlayed(reversed)

                        # print(f"Action: {next_player_action}")                    
                        break
                    elif input_data == 'buy' or input_data == 'b':
                        next_player_action = False
                        break

            else:
                    # "A.I." plays by itself, eg. plays whatever
                next_player_action = self.autoPlay(player, table_card)

                if next_player_action == 5:
                    reversed = self.reverseCardPlayed(reversed)

                # Check if player is out of cards, winning the game
            self.checkEndGame(player)

            self.output('End of turn.\n')
