import cflib.crtp

from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm

import queue, threading, time

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
        print(new_state)
        if new_state == SCAN:
            self.swarm_thread = threading.Thread(target=self._run_swarm)
            self.swarm_thread.start()
        elif new_state in SWARM_COMMANDS:
            self.command_queue.put(new_state)

    def _run_swarm(self):
        cflib.crtp.init_drivers()
        available = cflib.crtp.scan_interfaces()
        self.uris = [f"{aa[0]}/{RADIO_ADDRESS}" for aa in available if aa[0] != USB_DEFAULT_ADDRESS]
        self.uris = list(dict.fromkeys(self.uris))

        if self.uris:
            self._run_swarm_process()

        self.state = DISCONNECT
    
    def _run_swarm_process(self):
        self.state = SCAN

        factory = CachedCfFactory(rw_cache='./cache')
        with Swarm(self.uris, factory=factory) as swarm:
            self.state = CONNECTED
            print("connected")
            while True:
                try:
                    command = self.command_queue.get(timeout=0.1)
                    if command == BUILD:
                        positions = swarm.get_estimated_positions()
                        print("estimators reset")
                        self.navigation.set_drone_positions(positions)
                        self.navigation.build_routes()
                    elif command == SEARCH:
                        swarm.parallel_safe(DroneCommand.light_check)
                        swarm.parallel_safe(DroneCommand.take_off)
                        self.state = SEARCH
                    elif command == RECALL:
                        swarm.parallel_safe(DroneCommand.land)
                        self.state = CONNECTED
                    elif command == EMERGENCY:
                        swarm.parallel_safe(DroneCommand.emergency)
                        break
                    elif command == DISCONNECT:
                        if self.state != SEARCH:
                            self.state = DISCONNECT
                            break
                except queue.Empty:
                    pass

                if self.state == SEARCH:
                    try:
                        args_dict = self.navigation.get_step()
                        swarm.parallel_safe(DroneCommand.run_step, args_dict)
                    except Exception as e:
                        print(e)

                time.sleep(0.001)
        
        self.state = DISCONNECT