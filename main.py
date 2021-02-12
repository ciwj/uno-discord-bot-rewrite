from discord.utils import get
from discord.ext import commands
from gameclasses import *
from errors import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
mainChannelID = int(os.getenv('TEST_CHANNEL_ID'))


description = "This bot has become my living hell"
prefix = '!'

bot = commands.Bot(command_prefix=prefix, description=description, case_insensitive=True)

channels = [
    os.getenv('PLAYER_0_CHANNEL'), os.getenv('PLAYER_1_CHANNEL'), os.getenv('PLAYER_2_CHANNEL'), os.getenv('PLAYER_3_CHANNEL'), os.getenv('PLAYER_4_CHANNEL'),
               os.getenv('PLAYER_5_CHANNEL'), os.getenv('PLAYER_6_CHANNEL'), os.getenv('PLAYER_7_CHANNEL'), os.getenv('PLAYER_8_CHANNEL'), os.getenv('PLAYER_9_CHANNEL')
]


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
    global game, mainChannel
    mainChannel = bot.get_channel(mainChannelID)
    game = Game()
    print("-------------\nLogged in as {0.user}\n-------------\n".format(bot))


bot.run(TOKEN)
