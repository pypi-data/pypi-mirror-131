from src.tws_integrated_functions.appConnectionTws import ConnectionTwsApi
from ibapi.utils import iswrapper


class SubmitOrder(ConnectionTwsApi):

    def __init__(self, addr, port, client_id):
        super().__init__(addr=addr, port=port, client_id=client_id)

    @iswrapper
    def nextValidId(self, order_id):
        ''' Provides the next order ID '''
        self.order_id = order_id
        print('Order ID: '.format(order_id))

    @iswrapper
    def openOrder(self,order_id, contract, order, state):
        ''' Called in response to the submitted order '''
        print('Order status: '.format(state.status))
        print('Commission charged: '.format(state.commission))

    @iswrapper
    def orderStatus(self,order_id, status, filled, remaining, avgFillPrice, \
        permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        ''' Check the status of the subnitted order '''
        print('Number of filled positions: {}'.format(filled))
        print('Average fill price: {}'.format(avgFillPrice))

    @iswrapper
    def position(self,account, contract, pos, avgCost):
        ''' Read information about the account's open positions '''
        print('Position in {}: {}'.format(contract.symbol, pos))

    @iswrapper
    def accountSummary(self, req_id, account, tag, value, currency):
        ''' Read information about the account '''
        print('Account {}: {} = {}'.format(account, tag, value))

    @iswrapper
    def error(self, req_id, code, msg):
        print('Error {}: {}'.format(code, msg))

