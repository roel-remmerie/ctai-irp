import time

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.positioning.motion_commander import MotionCommander


def activate_led_bit_mask(scf):
    scf.cf.param.set_value('led.bitmask', 255)

def deactivate_led_bit_mask(scf):
    scf.cf.param.set_value('led.bitmask', 0)

def light_check(scf):
    activate_led_bit_mask(scf)
    time.sleep(2)
    deactivate_led_bit_mask(scf)
    time.sleep(2)

def hover_sequence(scf):
    with MotionCommander(scf, default_height=0.75):
        time.sleep(3)

# uris = {
#     'radio://0/79/2M/E7E7E7E7E7',
#     'radio://0/80/2M/E7E7E7E7E7',
#     'radio://0/81/2M/E7E7E7E7E7'
#     # Add more URIs if you want more copters in the swarm
#     # URIs in a swarm using the same radio must also be on the same channel
# }

if __name__ == '__main__':
    cflib.crtp.init_drivers()

    available_adresses = cflib.crtp.scan_interfaces()
    uris = [f"{aa[0]}/E7E7E7E7E7" for aa in available_adresses]

    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        print('Connected to Crazyflies')
        # swarm.parallel_safe(light_check)
        swarm.reset_estimators()

        swarm.sequential(hover_sequence)