from src.tws_integrated_functions.appConnectionTws import ConnectionTwsApi
from ibapi.utils import iswrapper


class MarketReader(ConnectionTwsApi):

    def __init__(self, addr, port, client_id):
        super().__init__(addr=addr, port=port, client_id=client_id)

    @iswrapper
    def tickByTickMidPoint(self, reqId, tick_time, midpoint):
        """ Called in response to reqTickByTickData """

        print('tickByTickMidPoint - Midpoint tick: {}'.format(midpoint))

    @iswrapper
    def tickPrice(self, reqId, field, price, attribs):
        """ Called in response to reqMktData """

        print('tickPrice - field: {}, price: {}'.format(field, price))

    @iswrapper
    def tickSize(self, reqId, field, size):
        """ Called in response to reqMktData """

        print('tickSize - field: {}, size: {}'.format(field, size))

    @iswrapper
    def realtimeBar(self, reqId, time, open, high, low, close, volume, WAP, count):
        """ Called in response to reqRealTimeBars """

        print('realtimeBar - Opening price: {}'.format(open))

    @iswrapper
    def historicalData(self, reqId, bar):
        """ Called in response to reqHistoricalData """

        print('historicalData - Close price: {}'.format(bar.close))

    @iswrapper
    def fundamentalData(self, reqId, data):
        """ Called in response to reqFundamentalData """

        print('Fundamental data: ' + data)

    def error(self, reqId, code, msg):
        """ Called if an error occurs """

        print('Error {}: {}'.format(code, msg))

