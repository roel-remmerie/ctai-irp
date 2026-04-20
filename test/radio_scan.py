import cflib.crtp
from cflib.crazyflie import Crazyflie


def list_uris():
    available = cflib.crtp.scan_interfaces()
    for i in available:
        print(i[0])   # URI, e.g., "radio://0/80/2M/E7E7E7E7E7"


if __name__ == "__main__":
    cflib.crtp.init_drivers()
    print("Detected URIs:")
    list_uris()