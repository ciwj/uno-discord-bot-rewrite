class Error(Exception):
    """Base Error Class"""
    pass


class alreadyInLobbyError(Error):
    """Raised when a player tries to start a second lobby"""

    def __init__(self, playerID, playerUsername):
        self.message = "User {0} - {1} tried creating an extra lobby.".format(playerID, playerUsername)

    @staticmethod
    async def send_msg():
        await mainChannel.send("Lobby already exists!")

    def __str__(self):
        return self.message