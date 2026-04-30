import time

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

FLIGHT_HEIGHT = 0.5
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

    @staticmethod
    def run_step(scf: SyncCrazyflie, move):
        x_p1, y_p1, delta_p1_p0, max_swarm_delta = move
        duration = delta_p1_p0 * TIME_PER_METER
        wait_time = max_swarm_delta * TIME_PER_METER

        commander = scf.cf.high_level_commander
        commander.go_to(x_p1,y_p1,FLIGHT_HEIGHT,0,duration)
        time.sleep(wait_time)