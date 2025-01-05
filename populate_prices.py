from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import config
import alpaca_trade_api as tradeapi

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)

barsets = api.get_bars("AAPL", TimeFrame.Hour, "2021-06-08", "2021-06-08", adjustment='raw').df()
print(barsets)