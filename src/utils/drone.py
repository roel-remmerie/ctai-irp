import time

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

FLIGHT_HEIGHT = 0.5 # Height at which a drone will fly
Z_MIN = 0.0 # The lowest height a drone can go (ground level)

T_TAKEOFF = 2.0 # time it takes a drone to go from Z_MIN to FLIGHT_HEIGHT
T_LANDING = 2.0 # time it takes a drone to go from FLIGHT_HEIGHT to Z_MIN

V_DRONE = 0.25 # the speed of a drone (in meters/second)

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
        commander.takeoff(FLIGHT_HEIGHT, T_TAKEOFF)
        time.sleep(T_TAKEOFF)

    @staticmethod
    def land(scf: SyncCrazyflie):
        commander = scf.cf.high_level_commander
        commander.land(Z_MIN, T_LANDING)
        time.sleep(T_LANDING)
        commander.stop()

    @staticmethod
    def run_step(scf: SyncCrazyflie, move: tuple[float, float, float, float]):
        x_p1, y_p1, delta_p1_p0, max_swarm_delta = move
        duration = delta_p1_p0 / V_DRONE
        wait_time = max_swarm_delta / V_DRONE

        commander = scf.cf.high_level_commander
        commander.go_to(x_p1,y_p1,FLIGHT_HEIGHT,0,duration)
        time.sleep(wait_time)