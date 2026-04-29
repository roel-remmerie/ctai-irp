import pygame

from services.swarm import SwarmService


from assets.components import *
from utils.state import *
from utils.plot import Plot

pygame.init()

swarm = SwarmService()

DISPLAY = (1280, 720)
DRONE_DISPLAY = (600,680)
CAPTION = "UAV Swarm AI - Search & Rescue"

FPS = 60

IMAGE_URI = "drone_map.png"


screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

buttons: list[CustomButton] = buttons

running = True

class Render():
    @classmethod
    def _button(_, button: CustomButton):
        pygame.draw.rect(screen, BUTTON_COLOR, button)
        text_color = ACTIVE_TEXT_COLOR if button.active else INACTIVE_TEXT_COLOR
        text_surface = font.render(button.text, True, text_color)
        text_rect = text_surface.get_rect(center=button.center)
        screen.blit(text_surface, text_rect)

    @classmethod
    def _buttons(_):
        for i in range(len(buttons)):
            buttons[i].active = buttons[i].text in button_state_mapping[swarm.state]
            Render._button(buttons[i])

    @classmethod
    def _drones(_):
        if swarm.navigation:
            Plot._drone_routes(IMAGE_URI, (600, 640), swarm.navigation)
            screen.blit(pygame.image.load(IMAGE_URI).convert(), (40, 40))
        
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if swarm.drones_safe():
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.collidepoint(event.pos) and button.active:
                    swarm.update_swarm(button.text)
    
    screen.fill(BACKGROUND)
    Render._buttons()
    Render._drones()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()