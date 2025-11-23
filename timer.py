import config

def seconds(amount:float) -> int:
    frames = config.framerate * amount
    if frames > int(frames):
        frames = int(frames) + 1
    return int(frames)