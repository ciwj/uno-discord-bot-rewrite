import os

from dotenv import load_dotenv
from discord.ext import commands
from random import randrange, choice, seed
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

description = "This bot has become my living hell"
prefix = '!'

class Error(Exception):
    """Base Error Class"""
    pass


class alreadyInLobbyError(Error):
    """Raised when a player tries to start a second lobby"""

    def __init__(self, playerID):
        self.message = "player {} tried creating an extra lobby.".format(playerID)

    def __str__(self):
        return self.message


class Player:
    """put shit here"""
    def __init__(self, playerName, playerID, roleID, ctx):
        self.playerName = playerName
        self.playerID = playerID
        self.deck = []
        self.roleID = roleID
        self.setMember(ctx)

        async def setMember(self, ctx):
            self.member = await commands.MemberConverter().convert(str(ctx, self.playerID))

    def drawCard(self):
        self.deck.append(randCard())


channels = [
    712763747315220561, 712763764922908794, 712763848133836870, 712763863384457256, 712763878643073065,
    712763898356564048, 712763914747904091, 712763929020858438, 712763945525575700, 712763957852504197
]



class Card():
    """Creates the card class, defines as value + colour. also a little thing for printing cards
       (as in print the deck:for every card in deck card.print)"""
    def __init__(self, value, colour):
        self.value = value
        self.colour = colour

    def print(self):
        print(str(self.colour) + str(self.value))  # prints as "blue 2"


class Deck():
    """the deck. defines and constructs the deck with everything except wildcards cuz those are hard uwu."""
    deckList = []

    def __init__(self):
        self.constructDeck()
        self.playingPile() = []

    def constructDeck(self):
        for i in ['Red', 'Green', 'Yellow', 'Blue']:
            for j in [1, 2, 3, 4, 5, 6, 7, 8, 9, 'Draw 2', 'Reverse', 'Skip']:
                self.deckList.append(card(j, i))

    def showPlayingPile(self):
        for card in self.playingPile:
            card.print()

    def showDeck(self):
        for card in self.deckList:
            card.print()

    def shuffleDeck(self):
        self.shuffledCards = random.shuffle(self.deckList)


# cards = [
#    ['Red 0', 0, 0], ['Red 1', 0, 1], ['Red 1', 0, 1], ['Red 2', 0, 2], ['Red 2', 0, 2], ['Red 3', 0, 3],
#    ['Red 3', 0, 3], ['Red 4', 0, 4], ['Red 4', 0, 4], ['Red 5', 0, 5], ['Red 5', 0, 5], ['Red 6', 0, 6],
#    ['Red 6', 0, 6], ['Red 7', 0, 7], ['Red 7', 0, 7], ['Red 8', 0, 8], ['Red 8', 0, 8], ['Red 9', 0, 9],
#    ['Red 9', 0, 9], ['Red Draw 2', 0, 10], ['Red Draw 2', 0, 10], ['Red Skip', 0, 11], ['Red Skip', 0, 11],
#    ['Red Reverse', 0, 12], ['Red Reverse', 0, 12], ['Green 0', 1, 0], ['Green 1', 1, 1], ['Green 1', 1, 1],
#    ['Green 2', 1, 2], ['Green 2', 1, 2], ['Green 3', 1, 3], ['Green 3', 1, 3], ['Green 4', 1, 4], ['Green 4', 1, 4],
#    ['Green 5', 1, 5], ['Green 5', 1, 5], ['Green 6', 1, 6], ['Green 6', 1, 6], ['Green 7', 1, 7], ['Green 7', 1, 7],
#    ['Green 8', 1, 8], ['Green 8', 1, 8], ['Green 9', 1, 9], ['Green 9', 1, 9], ['Green Draw 2', 1, 10],
#    ['Green Draw 2', 1, 10], ['Green Skip', 1, 11], ['Green Skip', 1, 11], ['Green Reverse', 1, 12],
#    ['Green Reverse', 1, 12], ['Yellow 0', 2, 0], ['Yellow 1', 2, 1], ['Yellow 1', 2, 1], ['Yellow 2', 2, 2],
#    ['Yellow 2', 2, 2], ['Yellow 3', 2, 3], ['Yellow 3', 2, 3], ['Yellow 4', 2, 4], ['Yellow 4', 2, 4],
#    ['Yellow 5', 2, 5], ['Yellow 5', 2, 5], ['Yellow 6', 2, 6], ['Yellow 6', 2, 6], ['Yellow 7', 2, 7],
#    ['Yellow 7', 2, 7], ['Yellow 8', 2, 8], ['Yellow 8', 2, 8], ['Yellow 9', 2, 9], ['Yellow 9', 2, 9],
#    ['Yellow Draw 2', 2, 10], ['Yellow Draw 2', 2, 10], ['Yellow Skip', 2, 11], ['Yellow Skip', 2, 11],
#    ['Yellow Reverse', 2, 12], ['Yellow Reverse', 2, 12], ['Blue 0', 3, 0], ['Blue 1', 3, 1], ['Blue 1', 3, 1],
#    ['Blue 2', 3, 2], ['Blue 2', 3, 2], ['Blue 3', 3, 3], ['Blue 3', 3, 3], ['Blue 4', 3, 4], ['Blue 4', 3, 4],
#    ['Blue 5', 3, 5], ['Blue 5', 3, 5], ['Blue 6', 3, 6], ['Blue 6', 3, 6], ['Blue 7', 3, 7], ['Blue 7', 3, 7],
#    ['Blue 8', 3, 8], ['Blue 8', 3, 8], ['Blue 9', 3, 9], ['Blue 9', 3, 9], ['Blue Draw 2', 3, 10],
#    ['Blue Draw 2', 3, 10], ['Blue Skip', 3, 11], ['Blue Skip', 3, 11], ['Blue Reverse', 3, 12],
#    ['Blue Reverse', 3, 12], ['Wild Card', 4, 13], ['Wild Card', 4, 13], ['Wild Card', 4, 13], ['Wild Card', 4, 13],
#   ['Wild Draw 4', 4, 14], ['Wild Draw 4', 4, 14], ['Wild Draw 4', 4, 14], ['Wild Draw 4', 4, 14]
# ]
# startCards = [
#    ['Red 0', 0, 0], ['Red 1', 0, 1], ['Red 1', 0, 1], ['Red 2', 0, 2], ['Red 2', 0, 2], ['Red 3', 0, 3],
#    ['Red 3', 0, 3], ['Red 4', 0, 4], ['Red 4', 0, 4], ['Red 5', 0, 5], ['Red 5', 0, 5], ['Red 6', 0, 6],
#    ['Red 6', 0, 6], ['Red 7', 0, 7], ['Red 7', 0, 7], ['Red 8', 0, 8], ['Red 8', 0, 8], ['Red 9', 0, 9],
#    ['Red 9', 0, 9], ['Green 0', 1, 0], ['Green 1', 1, 1], ['Green 1', 1, 1],
#    ['Green 2', 1, 2], ['Green 2', 1, 2], ['Green 3', 1, 3], ['Green 3', 1, 3], ['Green 4', 1, 4], ['Green 4', 1, 4],
#    ['Green 5', 1, 5], ['Green 5', 1, 5], ['Green 6', 1, 6], ['Green 6', 1, 6], ['Green 7', 1, 7], ['Green 7', 1, 7],
#    ['Green 8', 1, 8], ['Green 8', 1, 8], ['Green 9', 1, 9], ['Green 9', 1, 9],
#    ['Yellow 0', 2, 0], ['Yellow 1', 2, 1], ['Yellow 1', 2, 1], ['Yellow 2', 2, 2],
#    ['Yellow 2', 2, 2], ['Yellow 3', 2, 3], ['Yellow 3', 2, 3], ['Yellow 4', 2, 4], ['Yellow 4', 2, 4],
#    ['Yellow 5', 2, 5], ['Yellow 5', 2, 5], ['Yellow 6', 2, 6], ['Yellow 6', 2, 6], ['Yellow 7', 2, 7],
#    ['Yellow 7', 2, 7], ['Yellow 8', 2, 8], ['Yellow 8', 2, 8], ['Yellow 9', 2, 9], ['Yellow 9', 2, 9],
#    ['Blue 0', 3, 0], ['Blue 1', 3, 1], ['Blue 1', 3, 1],
#    ['Blue 2', 3, 2], ['Blue 2', 3, 2], ['Blue 3', 3, 3], ['Blue 3', 3, 3], ['Blue 4', 3, 4], ['Blue 4', 3, 4],
#    ['Blue 5', 3, 5], ['Blue 5', 3, 5], ['Blue 6', 3, 6], ['Blue 6', 3, 6], ['Blue 7', 3, 7], ['Blue 7', 3, 7],
#    ['Blue 8', 3, 8], ['Blue 8', 3, 8], ['Blue 9', 3, 9], ['Blue 9', 3, 9]
# ]

bot = commands.Bot(command_prefix=prefix, description=description, case_insensitive=True)


def randCard():
    seed(datetime.now)
    card = choice(cards)
    return card


@bot.command(pass_context=True)
async def lobby(ctx):
    try:
        pass

    except Exception as e:
        print(e)

