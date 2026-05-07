import time

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

FLIGHT_HEIGHT = 0.75 # Height at which a drone will fly
Z_MIN = 0.0 # The lowest height a drone can go (ground level)

V_DRONE = 0.20 # the speed of a drone (in meters/second)

T_TAKEOFF = FLIGHT_HEIGHT / V_DRONE # time it takes a drone to go from Z_MIN to FLIGHT_HEIGHT
T_LANDING = FLIGHT_HEIGHT / V_DRONE # time it takes a drone to go from FLIGHT_HEIGHT to Z_MIN

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
    def stop_rotors(scf: SyncCrazyflie):
        commander = scf.cf.high_level_commander
        commander.stop()

    @staticmethod
    def run_step(scf: SyncCrazyflie, move: tuple[tuple[float, float], float, float]):
        (x_pn, y_pn), delta_p, max_swarm_delta = move
        duration = delta_p / V_DRONE
        wait_time = max_swarm_delta / V_DRONE

        commander = scf.cf.high_level_commander
        commander.go_to(x_pn,y_pn,FLIGHT_HEIGHT,0,duration)
        time.sleep(wait_time)