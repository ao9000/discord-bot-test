class APIError(Exception):
    pass


class APIMonthlyLimitReachedError(Exception):
    pass


class CharacterLimitExceededError(Exception):
    pass