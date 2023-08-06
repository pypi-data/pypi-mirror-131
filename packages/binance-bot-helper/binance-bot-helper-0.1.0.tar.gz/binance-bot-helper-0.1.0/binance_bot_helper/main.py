from pandas import DataFrame,to_numeric

def klines_to_ohlvc(klines: dict) -> DataFrame:
    '''
    Receives a dict with the format of get_historical_klines from python-binance and returns a pandas dataframe with  
    'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time' columns
    '''
    ohlcv = DataFrame.from_dict(klines)
    ohlcv.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'Quote_asset_volume','num_trades', 'taker_buy_asset_volume', 'taker_buy_quote_asset_volume', 'Ignore']
    ohlcv = ohlcv.drop(['Quote_asset_volume','num_trades', 'taker_buy_asset_volume', 'taker_buy_quote_asset_volume', 'Ignore'], axis=1)
    ohlcv.loc[:,'open':'close'] = ohlcv.loc[:,'open':'close'].apply(to_numeric)
    return ohlcv