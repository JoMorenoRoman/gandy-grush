import config

def next():
    num = config.ceventsBase
    config.ceventsBase += 1
    return num

SWITCH_TOKENS = next()
