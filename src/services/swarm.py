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
        self.navigation: NavigationService = None

    def drones_safe(self):
        return self.state != SEARCH or self.state != RECALL

    def update_swarm(self, new_state):
        self.state = new_state

        if new_state == SCAN:
            self.swarm_thread = threading.Thread(target=self._scan_drones)
            self.swarm_thread.start()
        elif new_state == SEARCH:
            self.swarm_thread = threading.Thread(target=self._run_swarm)
            self.swarm_thread.start()
        elif new_state == RECALL or new_state == EMERGENCY:
            self.command_queue.put(new_state)
        

    def _scan_drones(self):
        cflib.crtp.init_drivers()
        available = cflib.crtp.scan_interfaces()
        self.uris = [f"{aa[0]}/{RADIO_ADDRESS}" for aa in available if aa[0] != USB_DEFAULT_ADDRESS]
        self.uris = list(dict.fromkeys(self.uris))
        
        print(self.uris)
        
        if self.uris:
            drones = {uri: (i, 0) for i, uri in enumerate(self.uris)}
            self.navigation = NavigationService(drones)

        self.state = CONNECTED if self.uris else UNAVAILABLE

    def _run_swarm(self):
        try:
            factory = CachedCfFactory(rw_cache='./cache')
            with Swarm(self.uris, factory=factory) as swarm:
                swarm.parallel_safe(DroneCommand.light_check)
                swarm.parallel_safe(DroneCommand.take_off)

                end_cmd = None

                while True:
                    try:
                        cmd = self.command_queue.get(timeout=0.1)
                        if cmd == RECALL or cmd == EMERGENCY:
                            print(cmd)
                            end_cmd = cmd
                            break

                    except queue.Empty:
                        pass

                    args_dict, max_distance = self.navigation.get_step()
                    print(args_dict)
                    # if max_distance == 0:
                    #     print("no distance")
                    #     end_cmd = RECALL
                    #     break

                    try:
                        swarm.parallel_safe(DroneCommand.run_step, args_dict)
                    except Exception as e:
                        swarm.parallel_safe(DroneCommand.land)
                        print("error")
                        print(e)
                        break

                if end_cmd == RECALL:
                    args_dict, _ = self.navigation.get_step(to_origin=True)
                    swarm.parallel_safe(DroneCommand.run_step, args_dict)
                    swarm.parallel_safe(DroneCommand.land)
                elif end_cmd == EMERGENCY:
                    swarm.parallel_safe(DroneCommand.land)
        finally:
            self.state = CONNECTED

    def render_drones(self):
        pass