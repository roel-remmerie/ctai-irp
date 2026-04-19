import time
import logging

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

logging.basicConfig(level=logging.ERROR)

def run(scf):
    with MotionCommander(scf) as mc:
        print('Take off!')
        mc.take_off(0.5)
        time.sleep(2)

        print('Go forward!')
        mc.forward(0.5)
        time.sleep(2)

        print('Go back!')
        mc.back(0.5)
        time.sleep(2)

        print('Land!')
        mc.land()

if __name__ == '__main__':
    cflib.crtp.init_drivers()
    
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        run(scf)