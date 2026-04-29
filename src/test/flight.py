import cflib.crtp

from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm

RADIO_ADDRESS = "E7E7E7E7E7"
USB_DEFAULT_ADDRESS = "usb://0"

import time

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

FLIGHT_HEIGHT = 1.0
GROUND_LEVEL = 0.0

TAKEOFF_SECONDS = 2.0
LANDING_SECONDS = 2.0

TIME_PER_METER = 4.0

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

cflib.crtp.init_drivers()
available = cflib.crtp.scan_interfaces()
uris = [f"{aa[0]}/{RADIO_ADDRESS}" for aa in available if aa[0] != USB_DEFAULT_ADDRESS]
uris = list(dict.fromkeys(uris))

factory = CachedCfFactory(rw_cache='./cache')
with Swarm(uris, factory=factory) as swarm:
    swarm.parallel_safe(DroneCommand.light_check)
    swarm.parallel_safe(DroneCommand.take_off)