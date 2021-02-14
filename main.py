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

bot = commands.Bot(command_prefix=prefix, description=description, case_insensitive=True)

# TODO: Add help information for commands

channels = [
    os.getenv('PLAYER_0_CHANNEL'), os.getenv('PLAYER_1_CHANNEL'), os.getenv('PLAYER_2_CHANNEL'),
    os.getenv('PLAYER_3_CHANNEL'), os.getenv('PLAYER_4_CHANNEL'), os.getenv('PLAYER_5_CHANNEL'),
    os.getenv('PLAYER_6_CHANNEL'), os.getenv('PLAYER_7_CHANNEL'),
    os.getenv('PLAYER_8_CHANNEL'), os.getenv('PLAYER_9_CHANNEL')
]


async def runException(e: Exception):
    """Helper function to send an Error's discord msg if applicable"""
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
        self.shuffleDeck()
        self.playingPile = []

    def constructDeck(self):
        """Constructs a deck from scratch
        Uno decks have two sets of every standard card except for 0s, which have one,
        and the wild types, which have 4 each"""
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

    async def showPlayingPileTop(self):
        lastCard = self.playingPile[-1]
        print("Last card played: " + lastCard)
        await mainChannel.send("Last card played: " + lastCard)

    def showDeck(self):
        for card in self.deckList:
            print(card)

    def shuffleDeck(self):
        random.seed(datetime.now())
        random.shuffle(self.deckList)  # Should work, double-check

    def drawFromDeck(self) -> Card:
        if len(self.deckList) == 0:
            self.constructDeck()
            self.shuffleDeck()
        drawnCard = self.deckList.pop()
        return drawnCard


class Game:
    def __init__(self):
        self.inLobby = False
        self.inGame = False
        self.isReverse = False
        self.players = []
        self.playersLeft = []
        self.deck = Deck()

    def addPlayer(self, player: Player):
        self.players.append(player)
        print("User {0} - {1} added to game players".format(player.getID(), player.getNick()))
        print("Playerlist is now:")
        for player in self.players:
            print(str(player.playerID) + " - " + player.playerName)
            print("")

    def removePlayer(self, player: Player):
        self.players.remove(player)
        if self.inGame:
            self.playersLeft.append(player)
        print("User {0} - {1} removed from game players".format(player.getID(), player.getNick()))
        print("Playerlist is now:")
        for player in self.players:
            print(str(player.playerID) + " - " + player.playerName)
        print("")
        print("playersLeft list is now:")
        for player in self.playersLeft:
            print(str(player.playerID) + " - " + player.playerName)
        print("")

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


# TODO Add join command with option for mid-game join (only if you haven't already left)
@bot.command(pass_context=True)
async def join(ctx):
    """Adds player to playerList"""
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


# TODO fix start command:
#   Deal cards
#   Display cards
#   Put card on top of playedCards
@bot.command(pass_context=True)
async def start(ctx):
    try:
        """Starts game - sets game.inLobby to False, and game.inGame to True."""
        global game
        if not game.inLobby:
            raise onlyInLobbyError(ctx.message.author.id, ctx.message.author.nick)

        print("User {0} - {1} started the game".format(ctx.message.author.id, ctx.message.author.nick))
        await mainChannel.send("Starting game!")

        game.inLobby = False
        game.inGame = True

    except Exception as e:
        await runException(e)


@bot.command(pass_context=True)
async def listPlayers(ctx):
    """Lists players currently in the game."""
    try:
        print("User {0} - {1} has listed all players".format(ctx.message.author.id, ctx.message.author.nick))
        str = "Players:\n"
        for player in game.players:
            str += player.member.mention + "\n"
        await mainChannel.send(str)
    except Exception as e:
        await runException(e)


@bot.command(pass_context=True)
async def leave(ctx):
    """Removes a player from the game."""
    try:
        userID = ctx.message.author.id
        playerToRemove = None
        for player in game.players:
            if player.playerID == userID:
                playerToRemove = player
        if playerToRemove != None:
            game.removePlayer(playerToRemove)
            await mainChannel.send("You have been removed from the game.")
        else:
            await mainChannel.send("You aren't in the game, fool.")

    except Exception as e:
        await runException(e)


# TODO Add play command
@bot.command(pass_context=True)
async def play(ctx):
    """Plays a card"""
    try:
        pass
    except Exception as e:
        await runException(e)


# TODO Add draw command
@bot.command(pass_context=True)
async def draw(ctx):
    """Draws a card for a player"""
    try:
        pass
    except Exception as e:
        await runException(e)


# TODO add cardNum command
@bot.command(pass_context=True)
async def cardNum(ctx):
    """Shows the amount of cards each player has"""
    try:
        pass
    except Exception as e:
        await runException(e)


# TODO add stopGame command
@bot.command(pass_context=True)
async def stopGame(ctx):
    """Stops the game"""
    try:
        pass
    except Exception as e:
        await runException(e)


# TODO add closeLobby command
@bot.command(pass_context=True)
async def closeLobby(ctx):
    """Closes an open lobby"""
    try:
        pass
    except Exception as e:
        await runException(e)


@bot.event
async def on_ready():
    """Runs on bot startup. Creates a Game object and defines the mainChannel"""
    global game, mainChannel
    mainChannel = bot.get_channel(mainChannelID)
    game = Game()
    print("-------------\nLogged in as {0.user}\n-------------\n".format(bot))


bot.run(TOKEN)
