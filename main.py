import os
import random
from datetime import datetime

from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
mainChannelID = int(os.getenv('TEST_CHANNEL_ID'))

description = "This bot has become my living hell"
prefix = '!'

# TODO commands to add:
#   Add listPlayers command DONE BUT DOUBLE CHECK ME
#   Add leaveGame command
#   Add join command with option for mid-game join (only if you haven't already left)

# TODO fix start command:
#   Send message on run
#   Construct deck, deal cards
#   Display cards
#   Put card on top of playedCards

bot = commands.Bot(command_prefix=prefix, description=description, case_insensitive=True)

channels = [
    os.getenv('PLAYER_0_CHANNEL'), os.getenv('PLAYER_1_CHANNEL'), os.getenv('PLAYER_2_CHANNEL'),
    os.getenv('PLAYER_3_CHANNEL'), os.getenv('PLAYER_4_CHANNEL'),
    os.getenv('PLAYER_5_CHANNEL'), os.getenv('PLAYER_6_CHANNEL'), os.getenv('PLAYER_7_CHANNEL'),
    os.getenv('PLAYER_8_CHANNEL'), os.getenv('PLAYER_9_CHANNEL')
]


async def runException(e: Exception):
    print(e)
    if callable(getattr(e, 'send_msg', False)):
        await e.send_msg()


class Error(Exception):
    """Base Error Class"""
    pass


class onlyInLobbyError(Error):
    """Raised when a player tries to do something only available in a lobby state"""

    def __init__(self, playerID, playerUsername):
        self.message = "User {0} - {1} tried running a command only available in a lobby.".format(playerID,
                                                                                                  playerUsername)

    @staticmethod
    async def send_msg():
        await mainChannel.send("This is only available in a lobby.")

    def __str__(self):
        return self.message


class alreadyInLobbyError(Error):
    """Raised when a player tries to start a second lobby"""

    def __init__(self, playerID, playerUsername):
        self.message = "User {0} - {1} tried creating an extra lobby.".format(playerID, playerUsername)

    @staticmethod
    async def send_msg():
        await mainChannel.send("Lobby already exists!")

    def __str__(self):
        return self.message


class alreadyJoinedError(Error):
    """Raised when a player tries to join a second time"""

    def __init__(self, playerID, playerUsername):
        self.message = "User {0} - {1} tried joining a second time.".format(playerID, playerUsername)

    @staticmethod
    async def send_msg():
        await mainChannel.send("You're already in the game, bastard. May your soul rot like the grape under my fridge.")

    def __str__(self):
        return self.message


class Player:
    """Represents each player currently in the game."""

    def __init__(self, playerName, playerID, role, member):
        self.playerName = playerName
        self.playerID = playerID
        self.hand = []
        self.role = role
        self.member = member

    def drawCard(self, deck):
        self.hand.append(deck.drawFromDeck())

    def playCard(self, deck):
        deck.deckList.append(self.hand.pop())  # I think this works but not sure.

    def showHand(self):
        for card in self.hand:
            print(card)

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
        self.inLobby = False
        self.inGame = False
        self.isReverse = False
        self.players = []
        self.deck = Deck()

    def addPlayer(self, player: Player):
        self.players.append(player)
        print("User {0} - {1} added to game players".format(player.getID(), player.getNick()))
        print("Playerlist is now:")
        for player in self.players:
            print(str(player.playerID) + " - " + player.playerName)
            print("----------------------------")

    def numPlayers(self):
        return len(self.players)

    def listPlayers(self):
        print("current players:")
        for player in self.players:
            print(str(player.playerID) + " - " + player.playerName)


@bot.command(pass_context=True)
async def lobby(ctx):
    try:
        global game
        if game.inLobby:
            raise alreadyInLobbyError(ctx.message.author.id, ctx.message.author.nick)
        game.inLobby = True

        member = await commands.MemberConverter().convert(ctx, str(ctx.message.author.id))
        lobbyCreator = Player(ctx.message.author.nick, ctx.message.author.id,
                              get(member.guild.roles, name="Player 1"), member)
        game.addPlayer(lobbyCreator)

        sender = ctx.message.author.mention
        await mainChannel.send(".here, " + sender + " is trying to start a game!")

    except Exception as e:
        await runException(e)


@bot.command(pass_context=True)
async def join(ctx):
    try:
        global game
        alreadyJoined = False
        for player in game.players:
            if player.playerID == ctx.message.author.id:
                alreadyJoined = True
        if alreadyJoined:
            raise alreadyJoinedError(ctx.message.author.id, ctx.message.author.nick)
        member = await commands.MemberConverter().convert(ctx, str(ctx.message.author.id))
        roleNum = game.numPlayers() + 1
        role = get(member.guild.roles, name=("Player " + str(roleNum)))
        newPlayer = Player(ctx.message.author.nick, ctx.message.author.id, role, member)
        game.addPlayer(newPlayer)

        await mainChannel.send(ctx.message.author.mention + " has joined the game!")
    except Exception as e:
        await runException(e)


@bot.command(pass_context=True)
async def start(ctx):
    try:
        global game
        if not game.inLobby:
            raise onlyInLobbyError(ctx.message.author.id, ctx.message.author.nick)

        print("User {0} - {1} started the game".format(ctx.message.author.id, ctx.message.author.nick))
        await mainChannel.send("Starting game!")

        game.inLobby = False
        game.inGame = True

    except Exception as e:
        await runException(e)


@bot.event
async def on_ready():
    global game, mainChannel
    mainChannel = bot.get_channel(mainChannelID)
    game = Game()
    print("-------------\nLogged in as {0.user}\n-------------\n".format(bot))


bot.run(TOKEN)
