import os
import random
from datetime import datetime

from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

description = "This bot has become my living hell"
prefix = '!'

bot = commands.Bot(command_prefix=prefix, description=description, case_insensitive=True)

# mainChannelID = 709900240919986250
mainChannelID = 809555265342537738
mainChannel = bot.get_channel(mainChannelID)


class Error(Exception):
    """Base Error Class"""
    pass


class alreadyInLobbyError(Error):
    """Raised when a player tries to start a second lobby"""

    def __init__(self, playerID, playerUsername):
        self.message = "user {0} - {1} tried creating an extra lobby.".format(playerID, playerUsername)

    @staticmethod
    async def send_msg():
        await mainChannel.send("Lobby already exists!")

    def __str__(self):
        return self.message


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


channels = [
    712763747315220561, 712763764922908794, 712763848133836870, 712763863384457256, 712763878643073065,
    712763898356564048, 712763914747904091, 712763929020858438, 712763945525575700, 712763957852504197
]


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


@bot.command(pass_context=True)
async def lobby(ctx):
    try:
        global game
        if game.inLobby:
            raise alreadyInLobbyError(ctx.message.author.id, ctx.message.author.nick)
        game.inLobby = True

        member = await commands.MemberConverter().convert(ctx, str(ctx.message.author.id))
        lobbyCreator = Player(ctx.message.author.nick, ctx.message.author.id,
                              get(member.guild.roles, name=("Player 1")), member)
        game.addPlayer(lobbyCreator)

        sender = ctx.message.author.mention
        await mainChannel.send(".here, " + sender + " is trying to start a game!")

    except Exception as e:
        print(e)
        if callable(getattr(e, 'send_msg', False)):
            await e.send_msg()


@bot.command(pass_context=True)
async def start(ctx):
    try:
        pass
    except Exception as e:
        print(e)


@bot.event
async def on_ready():
    global game
    game = Game()
    print("-------------\nLogged in as {0.user}\n-------------\n".format(bot))


bot.run(TOKEN)
