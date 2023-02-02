from operator import itemgetter, attrgetter, methodcaller

class Player:
    def __init__(self, name, player = False):
        self.name = name
        self.player = player
        self.cards = []

    def __str__(self):
        # print(f'Name: {}, Card Amount: {}', self.name, len(self.cards))
        card_amount = len(self.cards)

        return f'Name: {self.name}, Card Amount: {card_amount}'

    def getName(self):
        return self.name

    def isPlayer(self):
        return self.player

    def addCard(self, card):
        self.cards.append(card)

        # takes card away from player deck
    def removeCard(self, card_position):
        self.cards.pop(card_position)

        # So the "A.I." can chose its color
    def preferredColor(self):
            # Five positions, 0 is wild cards
            # 1 - 4 are colors 
        colors_quant = [0, 0, 0, 0, 0]
        for card in self.cards:
            n_color = colors_quant[card.color]
                # Assign color value as index and add to its value of cards found
            colors_quant[card.color] = n_color + 1
            n_color = 0

            # Index with highest value (color with highest number of cards)
        preferred_color = colors_quant.index(max(colors_quant))

        return preferred_color

    def getCard(self, card_position):
        return self.cards[card_position]

    def playCard(self, card_position):
        chosen_card = self.cards[card_position]
        self.removeCard(card_position)

        return chosen_card

    def unoCheck(self):
            # Counting cards
        if len(self.cards) == 1:
            return self.unoMessage()
        else:
            return ''

    def unoMessage(self):
        player_name = self.getName()
        return f"{player_name} calls UNO!"

    def showCards(self):
        str = ''
        if (len(self.cards) > 0):
            for index, card in enumerate(self.cards):
                str += f"{index}: {card} "

        return str

    def qntCards(self, positions = True):
            # returns number of positions in array
        if positions:
                # len starts counting at 
            return len(self.cards) - 1
        else:
                # Returns actual quantity of cards 
            return len(self.cards) 

    def getCards(self):
        return self.cards
