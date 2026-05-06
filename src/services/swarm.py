import cflib.crtp

from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm

import queue, threading

from services.navigation import NavigationService

from utils.drone import DroneCommand

from utils.state import *

RADIO_ADDRESS = "E7E7E7E7E7"
USB_DEFAULT_ADDRESS = "usb://0"

class SwarmService():
    def __init__(self):
        self.uris: list[str] = []
        self.state = DISCONNECT
        self.swarm_thread = None
        self.command_queue = queue.Queue()
        self.navigation = NavigationService()

    def drones_safe(self):
        return self.state != SEARCH or self.state != RECALL
    
    def update_swarm(self, new_state: str):
        if new_state == SCAN:
            self.swarm_thread = threading.Thread(target=self._run_swarm)
        elif new_state == SEARCH or new_state == RECALL or new_state == EMERGENCY:
            self.command_queue.put(new_state)

    def _run_swarm(self):
        cflib.crtp.init_drivers()
        available = cflib.crtp.scan_interfaces()
        self.uris = [f"{aa[0]}/{RADIO_ADDRESS}" for aa in available if aa[0] != USB_DEFAULT_ADDRESS]
        self.uris = list(dict.fromkeys(self.uris))

        if self.uris:
            self.state = CONNECTED
            self._run_search()
        else:
            self.state = UNAVAILABLE
    
    def _run_search(self):
        self.state = SCAN

        factory = CachedCfFactory(rw_cache='./cache')
        with Swarm(self.uris, factory=factory) as swarm:
            while True:
                try:
                    command = self.command_queue.get(timeout=0.1)
                    self.state = command
                    if command == BUILD:
                        positions = swarm.get_estimated_positions()
                        self.navigation.set_drone_positions(positions)
                        self.navigation.build_routes()
                    elif command == SEARCH:
                        swarm.parallel_safe(DroneCommand.take_off)
                    elif command == RECALL:
                        swarm.parallel_safe(DroneCommand.land)
                    elif command == EMERGENCY:
                        swarm.parallel_safe(DroneCommand.emergency)
                        break
                except queue.Empty:
                    pass

                if self.state == SEARCH:
                    try:
                        args_dict = self.navigation.get_step()
                        swarm.parallel_safe(DroneCommand.run_step, args_dict)
                    except Exception as e:
                        print(e)
        
        self.state = DISCONNECT