import time
import logging

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

# Change this if your URI is different
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

logging.basicConfig(level=logging.ERROR)


def run_sequence(scf):
    with MotionCommander(scf, default_height=1) as mc:
        time.sleep(1.0)
        mc.turn_right(360)
        time.sleep(0.5)


if __name__ == "__main__":
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    # Connect to the Crazyflie
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        run_sequence(scf)