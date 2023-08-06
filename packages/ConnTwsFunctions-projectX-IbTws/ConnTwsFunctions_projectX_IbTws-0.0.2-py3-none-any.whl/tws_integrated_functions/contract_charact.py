"""
Class to be used when we want to access details for a contract
"""
from src.tws_integrated_functions.appConnectionTws import ConnectionTwsApi
from ibapi.utils import iswrapper


class ContractCharacteristics(ConnectionTwsApi):

    def __init__(self, addr, port, client_id):
        super().__init__(addr=addr, port=port, client_id=client_id)

    @iswrapper
    def symbolSamples(self, reqId, descs):
        # Print the symbols in the returned results
        print('Number of descriptions: {}'.format(len(descs)))
        for desc in descs:
            print('Symbol: {}'.format(desc.contract.symbol))

        # Choose the first symbol
        self.symbol = descs[0].contract.symbol

    @iswrapper
    def contractDetails(self, reqId, details):
        print('Long name: {}'.format(details.longName))
        print('Category: {}'.format(details.category))
        print('Subcategory: {}'.format(details.subcategory))
        print('Contract ID: {}\n'.format(details.contract.conId))

    @iswrapper
    def contractDetailsEnd(self, reqId):
        print('The End')

    @iswrapper
    def error(self, reqId, code, msg):
        print('Error {}: {}'.format(code, msg))