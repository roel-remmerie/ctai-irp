import queue, threading, time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from services.navigation import NavigationService

from utils.drone import *

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
            self.state = SCAN
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
        self.state = CONNECTED
        print("connecting")

        swarm: list[SyncCrazyflie] = []
        events = []

        for uri in self.uris:
            cf = Crazyflie(rw_cache="./cache")
            scf = SyncCrazyflie(uri, cf=cf)
            evt = threading.Event()

            def connected_cb(link_uri, evt=evt):
                print(f"connected {link_uri}")
                evt.set()

            def failed_cb(link_uri, msg, evt=evt):
                print(f"failed {link_uri}")
                print(msg)
                evt.set()

            cf.connected.add_callback(connected_cb)
            cf.connection_failed.add_callback(failed_cb)
            cf.connection_lost.add_callback(failed_cb)

            scf.open_link()
            evt.wait()

            if cf.is_connected:
                swarm.append(scf)
                events.append(evt)

        print("connecting finished")

        try:
            while True:
                    try:
                        command = self.command_queue.get(timeout=0.1)
                        if command == BUILD:
                            positions = MultiDroneCommand.get_positions(swarm)
                            self.navigation.set_drone_positions(positions)
                            self.navigation.build_routes()
                        elif command == SEARCH:
                            print("light check")
                            MultiDroneCommand.light_check(swarm)
                            print("light check done")

                            time.sleep(1)

                            MultiDroneCommand.reset_estimators(swarm)

                            print("takeoff")
                            MultiDroneCommand.take_off(swarm)
                            print("takeoff succeeded")
                            self.state = SEARCH
                        elif command == RECALL:
                            MultiDroneCommand.land(swarm)
                            self.state = CONNECTED
                            break
                        elif command == EMERGENCY:
                            MultiDroneCommand.stop_rotors(swarm)
                            break
                        elif command == DISCONNECT:
                            if self.state != SEARCH:
                                self.state = DISCONNECT
                                break
                    except queue.Empty:
                        pass

                    if self.state == SEARCH:
                        try:
                            args_dict, max_dist = self.navigation.get_step()
                            MultiDroneCommand.run_step(swarm, args_dict, max_dist)
                        except Exception as e:
                            print(e)
        finally:
            for scf in swarm:
                scf.close_link()
