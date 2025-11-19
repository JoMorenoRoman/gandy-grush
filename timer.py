import config

def seconds(amount:float):
    frames = config.framerate * amount
    if frames > int(frames):
        frames = int(frames) + 1
    return frames