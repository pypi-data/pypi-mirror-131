from src.tws_integrated_functions.appConnectionTws import ConnectionTwsApi
from ibapi.utils import iswrapper


class AccountSummaryWrapper(ConnectionTwsApi):

    def __init__(self, addr, port, client_id):
        super().__init__(addr=addr, port=port, client_id=client_id)

    @iswrapper
    def accountSummary(self, req_id, acct, tag, val, currency):
        """ Called in response to reqAccountSummary """
        if tag == 'AvailableFunds':
            print('Account {}: available funds = {}: Currency = {}'.format(acct, val, currency))
            self.funds = float(val)

    @iswrapper
    def error(self, reqId, code, msg):
        print('Error {}: {}'.format(code, msg))

