import main

mainChannel = main.mainChannel


class Player:
    """Represents each player currently in the game."""

    def __init__(self, playerName, playerID, roleID, member):
        self.playerName = playerName
        self.playerID = playerID
        self.hand = []
        self.roleID = roleID
        self.member = member

    def drawCard(self, deck):
        self.hand.append(deck.drawFromDeck())

    def getID(self):
        return self.playerID

    def getNick(self):
        return self.playerName


class Card:
    """Creates the card class, defines as value + colour. also a little thing for printing cards
       (as in print the deck: for every card in deck card.print)"""

    value = None
    colour = None

    def __init__(self, value, colour):
        self.value = value
        self.colour = colour

    def __str__(self) -> str:
        if self.colour != 'Void':
            return str(self.colour + str(self.value))  # prints as "blue 2"
        else:
            return str(self.value)

    if colour == 'Void':
        def setColour(self, newColour):
            self.colour = newColour


class Deck:
    """the deck. defines and constructs the deck with everything except wildcards cuz those are hard uwu."""
    deckList = []

    def __init__(self):
        self.constructDeck()
        self.playingPile = []

    def constructDeck(self):
        """Constructs a deck from scratch
        Uno decks have two sets of every standard card except for 0s, which have one"""
        for i in ['Red', 'Green', 'Yellow', 'Blue']:
            for j in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Draw 2', 'Reverse', 'Skip']:
                self.deckList.append(Card(j, i))
                if j != '0':
                    self.deckList.append(Card(j, i))
        for j in ['Wild Card', 'Wild Draw 4']:
            for i in range(4):
                self.deckList.append(Card(j, 'Void'))

    def showPlayingPile(self):
        for card in self.playingPile:
            print(card)

    def showDeck(self):
        for card in self.deckList:
            print(card)

    def shuffleDeck(self):
        random.seed(datetime.now())
        self.shuffledCards = random.shuffle(self.deckList)

    def drawFromDeck(self):
        self.draw = self.deckList.pop()
        return self.draw


class Game:
    def __init__(self):
        self.inLobby = False  # Assuming Game object is created by the lobby command
        self.inGame = False
        self.isReverse = False
        self.players = []

    def addPlayer(self, player: Player):
        self.players.append(player)
        print("User {0} - {1} added to game players".format(player.getID(), player.getNick()))
