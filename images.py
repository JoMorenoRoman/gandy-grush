
import os
import pygame

def load_png(nombre: str, medidas: tuple[int, int]):
    """
    Carga una imagen PNG desde la carpeta 'data', la convierte para optimizar su uso en Pygame y la escala a las medidas indicadas.

    Args:
        nombre: Nombre del archivo de imagen.
        medidas: Dimensiones para escalar la imagen.

    Returns:
        pygame.Surface: Superficie proecesada y lista para usar.

    Raises:
        SystemExit: Si el archivo no se encuentra, imprime un mensaje y termina el programa.
    """
    try:
        image = pygame.image.load(os.path.join("data", nombre))
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"no se pudo cargar la imagen: {nombre}")
        raise SystemExit
    image = pygame.transform.scale(image, medidas)
    return image


def colorear_png(imagen: pygame.Surface, color: tuple[int, int, int]):
    """
    Aplica un color a una imagen PNG manteniendo su transparencia.

    Args:
        imagen (pygame.Surface): Imagen original.
        color (tuple[int, int, int]): Color en formato RGB.

    Returns:
        pygame.Surface: Nueva superficie con el color aplicado.

    
        - Usa operaciones de mezcla (`BLEND_RGBA_MULT` y `BLEND_RGBA_ADD`) para aplicar el color.
    """
    copia = imagen.copy()
    copia.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
    copia.fill(color + (0,), special_flags=pygame.BLEND_RGBA_ADD)
    return copia
