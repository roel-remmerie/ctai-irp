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
    def arm(scf: SyncCrazyflie):
        scf.cf.supervisor.send_arming_request(True)

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
    def run_square_sequence(scf: SyncCrazyflie):
        box_size = 1.0
        flight_time = 3.0

        commander = scf.cf.high_level_commander

        commander.go_to(box_size, 0, 0, 0, flight_time, relative=True)
        time.sleep(flight_time)

        commander.go_to(0, box_size, 0, 0, flight_time, relative=True)
        time.sleep(flight_time)

        commander.go_to(-box_size, 0, 0, 0, flight_time, relative=True)
        time.sleep(flight_time)

        commander.go_to(0, -box_size, 0, 0, flight_time, relative=True)
        time.sleep(flight_time)

    @staticmethod
    def run_sequence(scf: SyncCrazyflie, sequence):
        cf = scf.cf

        for arguments in sequence:
            commander = scf.cf.high_level_commander

            x, y, z = arguments[0], arguments[1], arguments[2]
            duration = arguments[3]

            print('Setting position {} to cf {}'.format((x, y, z), cf.link_uri))
            commander.go_to(x, y, 0, 0, duration, relative=True)
            time.sleep(duration)

    @staticmethod
    def run_step(scf: SyncCrazyflie, x, y, distance, max_distnce):
        duration = distance * TIME_PER_METER
        wait_time = max_distnce * TIME_PER_METER
        commander = scf.cf.high_level_commander
        commander.go_to(x,y,0,0,duration, relative=True)
        time.sleep(wait_time)