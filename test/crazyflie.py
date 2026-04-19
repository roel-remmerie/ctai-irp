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
    # default_height is the takeoff height; we will go up further to reach 1.5 m
    target_height = 1.5

    with MotionCommander(scf, default_height=1) as mc:
        # Take off to default height
        time.sleep(1.0)

        # Go up to 1.5 m (distance relative to current height)
        # mc.up(target_height - mc.default_height)  # 1.0 m if default_height is 0.5 m
        # time.sleep(0.5)

        # Turn 360 degrees clockwise (negative angle for right/clockwise)
        mc.turn_right(360)  # or mc.turn_left(-360)
        time.sleep(0.5)

        # When the with-block exits, MotionCommander will land automatically
        # Alternatively, you can call mc.land() explicitly:
        # mc.land()
        # time.sleep(2.0)


if __name__ == "__main__":
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    # Connect to the Crazyflie
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        run_sequence(scf)