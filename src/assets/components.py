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

scan_button = CustomButton(1100, 40, 150, 50, SCAN)
disconnect_button = CustomButton(1100, 100, 150, 50, DISCONNECT)
build_button = CustomButton(1100, 160, 150, 50, BUILD)
search_button = CustomButton(1100, 220, 150, 50, SEARCH)
recall_button = CustomButton(1100, 280, 150, 50, RECALL)
emergency_button = CustomButton(1100, 340, 150, 50, EMERGENCY)


buttons = [
    scan_button,
    disconnect_button,
    build_button,
    search_button,
    recall_button,
    emergency_button
]

button_state_mapping: dict[str,list[str]] = {
    DISCONNECT: [SCAN],
    SCAN: [],
    CONNECTED: [DISCONNECT, SEARCH, BUILD],
    SEARCH: [RECALL, EMERGENCY],
    RECALL: [],
    EMERGENCY: [],
}
