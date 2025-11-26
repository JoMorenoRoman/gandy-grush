from pickle import FALSE
import pygame
import display
import eventq
import graphics
import config
import time
import game_objects.tokens as tokens
import game_objects.tablero as tablero
import pantallas.inicio

_tablero:dict = {}
_funcs:list[dict] = []
_pause_layer = []

def iniciar():
    graphics.clear()
    _tablero.clear()
    _funcs.clear()
    _tablero[tablero.MATRIX] = []
    _tablero[tablero.BUSY] = False
    _tablero[tablero.ANIM_SPEED] = 0.5
    tablero.iniciar(_tablero["matrix"], config.ROWS, config.COLUMNS)

    # Crear timer (90s) y callback al terminar
    timer_draw = make_timer_drawer(90, on_timeout=lambda: pantallas.inicio.iniciar())
    _tablero["timer_draw"] = timer_draw
    render()
    graphics.addRenderer(__name__)

def render():
    _funcs.clear()
    outer = display.createRect(0, 2/3)
    outer = display.square(outer)
    outer = display.createGraphic(1, 1, outer)
    outer[0].fill(config.MAINCOLOR)
    display.align(outer[1], 1, 1)
    graphics.addLayer([outer])
    
    inner = display.createRect(1, 1, outer[1].inflate(-10, -10))
    display.make_multiple(inner, config.COLUMNS, config.ROWS)
    inner = display.createGraphic(1, 1, inner)
    inner[0].fill(config.BACKGROUND)
    display.align(inner[1], 1, 1)
    graphics.addLayer([inner])
    
    token_rect = display.createRect(1/config.ROWS, 1/config.COLUMNS, inner[1])
    tokens.render(token_rect.size)
    capa_tablero = tablero.render(_tablero, inner[1], token_rect)
    _funcs.append(eventq.add_frame_func(lambda: tablero.buscar_matches(_tablero)))
    _funcs.append(eventq.add_frame_func(lambda: tablero.fill_empty(_tablero, capa_tablero, inner[1], token_rect)))
    _dibujar_boton_pausa()

    _funcs.append(eventq.add_frame_func(_tablero["timer_draw"]))

def _dibujar_boton_pausa():
    if _pause_layer:
        graphics.removeLayer(_pause_layer)
        _pause_layer.clear()

    btn_w = display.text_height() * 5
    btn_h = display.text_height() * 2
    rect = pygame.Rect(0, 0, btn_w, btn_h)
    display.align(rect, 2, 0)
    rect.x -= 20
    rect.y += 20

    surf = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
    surf.fill(config.MENU_BG)
    pygame.draw.rect(surf, config.MAINCOLOR, surf.get_rect(), width=3, border_radius=8)
    text = config.font.render("Pausa", True, config.TEXT_COLOR)
    surf.blit(text, text.get_rect(center=surf.get_rect().center))

    _pause_layer.append((surf, rect))
    graphics.addLayer(_pause_layer)

    eventq.addCollision(rect, abrir_menu_pausa)

def abrir_menu_pausa():
    panel_w = display.text_height() * 12
    panel_h = display.text_height() * 8
    panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
    display.align(panel_rect, 1, 1) 

    overlay = pygame.Surface(config.screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel.fill(config.MENU_BG)
    pygame.draw.rect(panel, config.MAINCOLOR, panel.get_rect(), width=4, border_radius=10)

    title = config.font.render("Pausa", True, config.TEXT_COLOR)
    trect = title.get_rect(center=(panel_w // 2, display.text_height()))
    panel.blit(title, trect)

    bw = panel_w - display.text_height() * 2
    bh = display.text_height() * 2

    rein_rect = pygame.Rect(display.text_height(), trect.bottom + display.text_height(), bw, bh)
    rein_surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
    rein_surf.fill(config.MAINCOLOR)
    rein_txt = config.font.render("Reiniciar juego", True, config.TEXT_COLOR)
    rein_surf.blit(rein_txt, rein_txt.get_rect(center=rein_surf.get_rect().center))
    panel.blit(rein_surf, rein_rect)

    volver_rect = pygame.Rect(display.text_height(), rein_rect.bottom + display.text_height(), bw, bh)
    volver_surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
    volver_surf.fill(config.MAINCOLOR)
    volver_txt = config.font.render("Volver al menu inicial", True, config.TEXT_COLOR)
    volver_surf.blit(volver_txt, volver_txt.get_rect(center=volver_surf.get_rect().center))
    panel.blit(volver_surf, volver_rect)

    cont_rect = pygame.Rect(display.text_height(), volver_rect.bottom + display.text_height(), bw, bh)
    cont_surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
    cont_surf.fill(config.MAINCOLOR)
    cont_txt = config.font.render("Continuar", True, config.TEXT_COLOR)
    cont_surf.blit(cont_txt, cont_txt.get_rect(center=cont_surf.get_rect().center))
    panel.blit(cont_surf, cont_rect)

    graphics.addLayer([(overlay, overlay.get_rect())])
    graphics.addLayer([(panel, panel_rect)])

    # Registrar colisiones pausadas con coordenadas globales
    eventq.clear_paused_collisions()
    eventq.add_paused_collision(rein_rect.move(panel_rect.topleft), _accion_reiniciar)
    eventq.add_paused_collision(volver_rect.move(panel_rect.topleft), _accion_volver_menu)
    eventq.add_paused_collision(cont_rect.move(panel_rect.topleft), _accion_continuar)

def _accion_reiniciar():
    eventq.clear_paused_collisions()
    eventq.reset()

def _accion_volver_menu():
    eventq.clear_paused_collisions()
    eventq.reset()

def _accion_continuar():
    eventq.clear_paused_collisions()


def make_timer_drawer(duration_sec:int, on_timeout):
    start_time = time.time()
    layer = []  # capa para el timer
    
    def draw_timer():
        # calcular tiempo restante
        elapsed = time.time() - start_time
        remaining = max(0, int(duration_sec - elapsed))

        if layer:
            graphics.removeLayer(layer)
            layer.clear()

        mins = remaining // 60
        secs = remaining % 60
        text = f"{mins:02}:{secs:02}"

        font = config.font
        surf_text = font.render(text, True, (255, 255, 255))  # texto blanco
        rect_text = surf_text.get_rect()
        display.align(rect_text, 0, 0)
        rect_text.x += 20
        rect_text.y += 20

        # fondo detrás del texto
        bg_width = rect_text.width + 20
        bg_height = rect_text.height + 10
        surf_bg = pygame.Surface((bg_width, bg_height))
        surf_bg.fill((50, 50, 50))  # gris oscuro
        rect_bg = surf_bg.get_rect(topleft=(rect_text.x - 10, rect_text.y - 5))

        layer.append((surf_bg, rect_bg))
        layer.append((surf_text, rect_text))
        graphics.addLayer(layer)

        if remaining <= 0:
            graphics.removeLayer(layer)
            layer.clear()
            on_timeout()
    return draw_timer