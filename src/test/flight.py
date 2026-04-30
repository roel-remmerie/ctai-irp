import cflib.crtp

from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm

RADIO_ADDRESS = "E7E7E7E7E7"
USB_DEFAULT_ADDRESS = "usb://0"

import time

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

FLIGHT_HEIGHT = 0.5
GROUND_LEVEL = 0.0

TAKEOFF_SECONDS = 2.0
LANDING_SECONDS = 2.0

DURATION = 5.0

SAFE_DISTANCE = 0.5

MIN_X = SAFE_DISTANCE
MIN_Y = SAFE_DISTANCE
MIN_Z = SAFE_DISTANCE

MAX_X = 4.95 - SAFE_DISTANCE
MAX_Y = 3.15 - SAFE_DISTANCE
MAX_Z = 2.50 - SAFE_DISTANCE

class DroneCommand:
    @staticmethod
    def activate_led_bit_mask(scf: SyncCrazyflie):
        scf.cf.param.set_value('led.bitmask', 255)

    @staticmethod
    def deactivate_led_bit_mask(scf: SyncCrazyflie):
        scf.cf.param.set_value('led.bitmask', 0)

    @staticmethod
    def light_check(scf: SyncCrazyflie):
        DroneCommand.activate_led_bit_mask(scf)
        time.sleep(2)
        DroneCommand.deactivate_led_bit_mask(scf)

    @staticmethod
    def take_off(scf: SyncCrazyflie):
        commander = scf.cf.high_level_commander
        commander.takeoff(FLIGHT_HEIGHT, TAKEOFF_SECONDS)
        time.sleep(TAKEOFF_SECONDS)

    @staticmethod
    def land(scf: SyncCrazyflie):
        commander = scf.cf.high_level_commander
        commander.land(GROUND_LEVEL, LANDING_SECONDS)
        time.sleep(LANDING_SECONDS)
        commander.stop()

    @staticmethod
    def run_sequence(scf: SyncCrazyflie, sequence):
        for move in sequence:
            DroneCommand.run_step(scf, move)

    @staticmethod
    def run_step(scf: SyncCrazyflie, arguments):
        x, y, z = arguments
        commander = scf.cf.high_level_commander
        commander.go_to(x,y,z,0,DURATION)
        time.sleep(DURATION)

moves = [[
    (MIN_X, MIN_Y, MIN_Z),
    (MIN_X, MAX_Y, MIN_Z),
    (MIN_X, MAX_Y, MAX_Z),
    (MIN_X, MIN_Y, MAX_Z),
    (MAX_X, MIN_Y, MAX_Z),
    (MAX_X, MAX_Y, MAX_Z),
    (MAX_X, MAX_Y, MIN_Z),
    (MAX_X, MIN_Y, MIN_Z),
]]

cflib.crtp.init_drivers()
available = cflib.crtp.scan_interfaces()
uris = [f"{aa[0]}/{RADIO_ADDRESS}" for aa in available if aa[0] != USB_DEFAULT_ADDRESS]
uris = list(dict.fromkeys(uris))

sequence_args = {uri: moves for uri in uris}

factory = CachedCfFactory(rw_cache='./cache')
with Swarm(uris, factory=factory) as swarm:

    try:
        swarm.parallel_safe(DroneCommand.light_check)
        swarm.parallel_safe(DroneCommand.take_off)
        swarm.parallel_safe(DroneCommand.run_sequence, args_dict=sequence_args)
    finally:

        swarm.parallel_safe(DroneCommand.land)