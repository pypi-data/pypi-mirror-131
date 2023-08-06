"""
Class to be used in all other classes to inhered the init
"""

from threading import Thread

from ibapi.client import EClient
from ibapi.wrapper import EWrapper


class ConnectionTwsApi(EWrapper, EClient):
    """
    Serves as the client and the wrapper
    """

    def __init__(self, addr, port, client_id):
        EClient.__init__(self=self, wrapper=self)

        # Connect to TWS
        self.connect(host=addr, port=port, clientId=client_id)

        # Launch the client thread
        thread = Thread(target=self.run)
        thread.start()
