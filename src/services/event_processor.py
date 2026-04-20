import pygame

class EventParameters():
    def __init__(self):
        self.running = True
        self.button_active = False

class EventProcessorService():
    def process_events(self):
        event_params = EventParameters()

        for event in pygame.event.get():

            # check if window should be closed
            if event.type == pygame.QUIT:
                event_params.running = False

            # check if button is clciked

        return event_params

            
