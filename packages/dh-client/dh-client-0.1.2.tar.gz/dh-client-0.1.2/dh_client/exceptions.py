class NotSupportedYet(Exception):
    pass


def raise_not_supported(msg: str = None):
    raise NotSupportedYet(msg)
