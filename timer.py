import config

"""
    Convierte segundos en una cantidad de frames según los fotogramas configurados.

    Args:
        amount (float): Cantidad de tiempo en segundos.

    Returns:
        int: Número entero de frames correspondientes a la duración indicada.
"""

def seconds(amount:float) -> int:
    frames = config.framerate * amount
    if frames > int(frames):
        frames = int(frames) + 1
    return int(frames)