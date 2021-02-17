import os
import random
import logging

from datetime import datetime

import discord
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
mainChannelID = int(os.getenv('TEST_CHANNEL_ID'))

description = "This bot has become my living hell"
prefix = '!'

bot = commands.Bot(command_prefix=prefix, description=description, case_insensitive=True)

# TODO: Add help information for commands
# TODO: Send go.png if a minute passes between commands of the current player
# TODO: Only send draw.png once per turn

# TODO change this to automatically get channels that are named properly
channels = [
    os.getenv('PLAYER_0_CHANNEL'), os.getenv('PLAYER_1_CHANNEL'), os.getenv('PLAYER_2_CHANNEL'),
    os.getenv('PLAYER_3_CHANNEL'), os.getenv('PLAYER_4_CHANNEL'), os.getenv('PLAYER_5_CHANNEL'),
    os.getenv('PLAYER_6_CHANNEL'), os.getenv('PLAYER_7_CHANNEL'),
    os.getenv('PLAYER_8_CHANNEL'), os.getenv('PLAYER_9_CHANNEL')
]


async def runException(e: Exception):
    """Helper function to send an Error's discord msg if applicable"""
    print(logger.exception(e))
    if callable(getattr(e, 'send_msg', False)):
        await e.send_msg()


class Error(Exception):
    """Base Error Class"""
    pass


class onlyInGameError(Error):
    """Raised when a player tries to do something only available in an inGame state"""

    def __init__(self, playerID: int, playerUsername: str):
        self.message = "User {0} - {1} tried running a command only available in a game.".format(playerID, playerUsername)

    @staticmethod
    async def send_msg():
        await mainChannel.send("This is only available in a game.")

    def __str__(self):
        return self.message


class onlyInLobbyError(Error):
    """Raised when a player tries to do something only available in a lobby state"""

    def __init__(self, playerID: int, playerUsername: str):
        self.message = "User {0} - {1} tried running a command only available in a lobby.".format(playerID,
                                                                                                  playerUsername)

    @staticmethod
    async def send_msg():
        await mainChannel.send("This is only available in a lobby.")

    def __str__(self):
        return self.message


class alreadyInLobbyError(Error):
    """Raised when a player tries to start a second lobby"""

    def __init__(self, playerID: int, playerUsername: str):
        self.message = "User {0} - {1} tried creating an extra lobby.".format(playerID, playerUsername)

    @staticmethod
    async def send_msg():
        await mainChannel.send("Lobby already exists!")

    def __str__(self):
        return self.message


class alreadyJoinedError(Error):
    """Raised when a player tries to join a second time"""

    def __init__(self, playerID: int, playerUsername: str):
        self.message = "User {0} - {1} tried joining a second time.".format(playerID, playerUsername)

    @staticmethod
    async def send_msg():
        await mainChannel.send("Already in game!")

    def __str__(self):
        return self.message


class Card:
    """Creates the card class, defines as value + colour. also a little thing for printing cards
       (as in print the deck: for every card in deck card.print)"""

    value = None
    colour = None

    def __init__(self, value: str, colour: str):
        self.value = value
        self.colour = colour

    def __str__(self) -> str:
        if self.colour != 'Void':
            return str(self.colour + " " + str(self.value))  # prints as "blue 2"
        else:
            return str(self.value)

    if colour == 'Void':
        def setColour(self, newColour: str):
            self.colour = newColour

    def getColour(self):
        return self.colour

    def getValue(self):
        return self.value


class Deck:
    """the deck. defines and constructs the deck with everything uwu."""
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

    def playingPileTop(self):
        lastCard = self.playingPile[-1]
        print("Last card played: " + str(lastCard))
        return lastCard

    def showDeck(self):
        for card in self.deckList:
            print(card)

    def shuffleDeck(self):
        random.seed(datetime.now())
        random.shuffle(self.deckList)  # Should work, double-check

    # TODO empty most of playing pile when deck is empty
    def drawFromDeck(self) -> Card:
        if len(self.deckList) == 0:
            self.constructDeck()
            self.shuffleDeck()
        drawnCard = self.deckList.pop()
        return drawnCard

    def addToPile(self, cardToAdd: Card):
        self.playingPile.append(cardToAdd)


class Player:
    """Represents each player currently in the game."""

    def __init__(self, playerName: str, playerID: int, member):
        self.playerName = playerName
        self.playerID = playerID
        self.hand = []
        self.member = member
        self.isTurn = False
        self.drawTimes = 0
        self.hasDrawnSent = False

    def drawCard(self):
        self.hand.append(game.deck.drawFromDeck())

    # TODO add condition for if the card isn't playable
    async def playCard(self, cardNo):
        lastCard = self.hand[-1]
        cardToPlay = self.hand[cardNo]
        if lastCard.getColour() == cardToPlay.getColour() or lastCard.getValue() == cardToPlay.getValue():
            game.deck.deckList.append(self.hand.pop(cardNo - 1))  # I think this works but not sure.
        else:
            await mainChannel.send("Card not valid.")

    def showHand(self):
        for card in self.hand:
            print(card)

    def getID(self):
        return self.playerID

    def getNick(self):
        return self.playerName

    def getMember(self):
        return self.member

    def setTurn(self, isTurnNew: bool):
        self.isTurn = isTurnNew

    def getHand(self):
        return self.hand

    def addDrawTime(self):
        self.drawTimes += 1

    def setHasDrawnSent(self, condition: bool):
        self.hasDrawnSent = condition


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
        print("Player list is now:")
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

    def nextTurn(self):
        for player in self.players:
            if player.isTurn:
                currentPlayerTurn = player
        currentTurn = self.players.index(currentPlayerTurn)
        currentPlayerTurn.setTurn(False)
        playerAmt = len(self.players)
        if self.isReverse:
            nextTurn = currentTurn - 1
        else:
            if currentTurn >= playerAmt - 1:
                nextTurn = 0
            else:
                nextTurn = currentTurn + 1
        self.players[nextTurn].setTurn(True)


def identifyPlayer(playerID: int) -> Player:
    for player in game.players:
        if player.getID() == playerID:
            return player
    print("No player with ID {} found.".format(playerID))


async def printCards(player: Player):
    playerRoles = player.getMember().roles
    for role in playerRoles:
        if "Player" in role.name:
            playerRole = role
    channelNum = playerRole.name[-1]
    channel = get(guild.text_channels, name="player-" + channelNum)
    await channel.purge(limit=50)
    stringToPrint = "**Your Cards:**\n"
    i = 1
    for card in player.getHand():
        stringToPrint += str(i) + ": " + str(card) + "\n"
        i += 1
    await channel.send(stringToPrint)


@bot.command(pass_context=True)
async def lobby(ctx):
    try:
        if game.inLobby:
            raise alreadyInLobbyError(ctx.message.author.id, ctx.message.author.nick)
        game.inLobby = True

        member = await commands.MemberConverter().convert(ctx, str(ctx.message.author.id))
        lobbyCreator = Player(ctx.message.author.nick, ctx.message.author.id, member)
        game.addPlayer(lobbyCreator)

        sender = ctx.message.author.mention
        await mainChannel.send(".here, " + sender + " is trying to start a game!")

    except Exception as e:
        await runException(e)


@bot.command(pass_context=True)
async def join(ctx):
    """Adds player to playerList"""
    try:
        alreadyJoined = False
        alreadyLeft = False
        for player in game.players:
            if player.getID() == ctx.message.author.id:
                raise alreadyJoinedError(ctx.message.author.id, ctx.message.author.nick)
        for player in game.playersLeft:
            if player.getID() == ctx.message.author.id:
                alreadyLeft = True
        if alreadyLeft:
            await mainChannel.send("Begone")
        else:
            member = await commands.MemberConverter().convert(ctx, str(ctx.message.author.id))
            newPlayer = Player(ctx.message.author.nick, ctx.message.author.id, member)
            game.addPlayer(newPlayer)
            # TODO give player role if joining midgame
            if game.inGame:
                player = identifyPlayer(ctx.message.author.id)
                for j in range(7):
                    player.drawCard()

            await mainChannel.send(ctx.message.author.mention + " has joined the game!")
    except Exception as e:
        await runException(e)


@bot.command(pass_context=True)
async def start(ctx):
    try:
        """Starts game - sets game.inLobby to False, and game.inGame to True."""
        if not game.inLobby:
            raise onlyInLobbyError(ctx.message.author.id, ctx.message.author.nick)

        print("User {0} - {1} started the game".format(ctx.message.author.id, ctx.message.author.nick))
        await mainChannel.send("Starting game!")

        """Dealing cards & giving roles"""
        for player in game.players:
            roleName = "Player " + str(game.players.index(player) + 1)
            role = get(ctx.guild.roles, name=roleName)
            for j in range(7):
                player.drawCard()  # Append 7 cards to each player currently in game
            await player.getMember().add_roles(role)  # Appends role to player
            await printCards(player)

        game.deck.addToPile(game.deck.drawFromDeck())
        await mainChannel.send("Top of Pile: " + str(game.deck.playingPileTop()))
        game.players[0].setTurn(True)
        game.inLobby = False
        game.inGame = True

    except Exception as e:
        await runException(e)


@bot.command(pass_context=True)
async def listPlayers(ctx):
    """Lists players currently in the game."""
    try:
        print("User {0} - {1} has listed all players".format(ctx.message.author.id, ctx.message.author.nick))
        strToPrint = "Players:\n"
        for player in game.players:
            strToPrint += player.member.mention + "\n"
        await mainChannel.send(strToPrint)
    except Exception as e:
        await runException(e)


@bot.command(pass_context=True)
async def leave(ctx):
    """Removes a player from the game."""
    try:
        userID = ctx.message.author.id
        playerToRemove = None
        playerToRemove = identifyPlayer(userID)
        if playerToRemove is not None:
            game.removePlayer(playerToRemove)
            await mainChannel.send("You have been removed from the game.")
        else:
            await mainChannel.send("You aren't in the game, fool.")

    except Exception as e:
        await runException(e)


# TODO Check that this works
@bot.command(pass_context=True)
async def play(ctx, cardNum):
    """Plays a card"""
    try:
        if game.inGame:
            author = identifyPlayer(ctx.message.author.id)
            if author.isTurn:
                player = identifyPlayer(ctx.message.author.id)
                player.setHasDrawnSent(False)
                await player.playCard(cardNum)
                game.nextTurn()
            else:
                await mainChannel.send("Not your turn :v(")
        else:
            await mainChannel.send("Wait until the game starts you fucker")
    except Exception as e:
        await runException(e)


# TODO Complete draw command
# TODO Add functionality for checking if cards are playable in the Player/Deck class
@bot.command(pass_context=True)
async def draw(ctx):
    """Draws a card for a player"""
    try:
        if game.inGame:
            player = identifyPlayer(ctx.message.author.id)
            player.addDrawTime()
            if player.drawTimes >= 3 and not player.hasDrawnSent:
                await mainChannel.send(file=discord.File('draw.png'))
                player.setHasDrawnSent(True)
            player.drawCard()
            await printCards(player)
        else:
            raise onlyInGameError(ctx.message.author.id, ctx.message.author.nick)
    except Exception as e:
        await runException(e)


@bot.command(pass_context=True)
async def numCards(ctx):
    """Shows the amount of cards each player has"""
    try:
        if game.inGame:
            stringToPrint = "Each player has:\n"
            for player in game.players:
                cardNum = len(player.getHand())
                stringToPrint += "{0.member.mention}: {1} cards\n".format(player, cardNum)
            await mainChannel.send(stringToPrint)
        else:
            raise onlyInGameError(ctx.message.author.id, ctx.message.author.nick)
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
    global game, mainChannel, guild
    mainChannel = bot.get_channel(mainChannelID)
    game = Game()
    guild = bot.guilds[0]
    print("-------------\nLogged in as {0.user}\n-------------\n".format(bot))


bot.run(TOKEN)
