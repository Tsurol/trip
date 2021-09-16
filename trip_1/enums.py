from aenum import Enum, IntEnum


class RespCode(IntEnum):
    Succeed = 0
    CacheSucceed = 1
    NotLogin = 100
    BusinessError = 101
    InvalidParams = 102
    NoBalance = 103
    MaxSending = 104
    NoProfit = 105
    NoPermission = 106
    NoBotOnline = 111
    AmountNotMatched = 112
    NoInventory = 201
    NoLotteryCount = 202
    WheelBlocked = 203
    NotOwnedGame = 204

    GameFull = 301
    InvalidGame = 302
    BadRequest = 400
    Maintenance = 401
    NotFound = 404

    Exception = 500
