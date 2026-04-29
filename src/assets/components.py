import pygame

from utils.state import *

class CustomButton(pygame.Rect):
    def __init__(
            self,
            left: float,
            top: float,
            width: float,
            height: float,
            text: str
        ):
        self.text = text
        self.active = False
        super().__init__(left, top, width, height)

COLORS = pygame.colordict.THECOLORS

BACKGROUND = COLORS["darkgrey"]
BUTTON_COLOR = COLORS["grey"]
ACTIVE_TEXT_COLOR = COLORS["black"]
INACTIVE_TEXT_COLOR = COLORS["darkgrey"]

scan_button = CustomButton(10, 10, 150, 50, SCAN)
disconnect_button = CustomButton(170, 10, 150, 50, DISCONNECT)
search_button = CustomButton(330, 10, 150, 50, SEARCH)
recall_button = CustomButton(490, 10, 150, 50, RECALL)
emergency_button = CustomButton(650, 10, 150, 50, EMERGENCY)


buttons = [
    scan_button,
    search_button,
    recall_button,
    disconnect_button,
    emergency_button
]

button_state_mapping: dict[str,list[str]] = {
    DISCONNECT: [SCAN],
    SCAN: [],
    UNAVAILABLE: [SCAN],
    CONNECTED: [DISCONNECT, SEARCH],
    SEARCH: [RECALL, EMERGENCY],
    RECALL: [],
    EMERGENCY: [],
}

class DroneMap():
    def __init__(self, width, height, colls, rows):
        self

    