import pygame

from services.event_processor import EventProcessorService

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

running = True

event_processor_service = EventProcessorService()

while running:
    # poll for events

    event_params = event_processor_service.process_events()
    running = event_params.running

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE

    pygame.display.flip()
    clock.tick(60)

pygame.quit()