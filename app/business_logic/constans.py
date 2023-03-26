import datetime

SELL_OPERATION = "SELL"
BUY_OPERATION = "BUY"
VALID_OPERATION_TYPES = [SELL_OPERATION, BUY_OPERATION]

INSUFFICIENT_BALANCE = "INSUFFICIENT_BALANCE"
INSUFFICIENT_STOCKS = "INSUFFICIENT_STOCKS"
DUPLICATED_OPERATION = "DUPLICATED_OPERATION"
INVALID_OPERATION = "INVALID_OPERATION"
CLOSED_MARKET = "CLOSED_MARKET"

OPEN_MARKET_TIME = datetime.time(6)
CLOSE_MARKET_TIME = datetime.time(15)
OPEN_MARKET_DAYS_OF_WEEK = [0, 1, 2, 3, 4]

TIMEZONE = "America/Mexico_City"
