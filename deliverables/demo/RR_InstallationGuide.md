# Installation Guide

## Materials

- a pc, laptop or raspberry pi, with a usb port

| amount | item | product page |
|---|---|---|
| **N** | Crazyflie 2.1+ | https://store.bitcraze.io/products/crazyflie-2-1-plus |
| **N** | Flow deck v2 | https://store.bitcraze.io/collections/decks/products/flow-deck-v2 |
| **N** | Loco positioning deck | https://store.bitcraze.io/collections/decks/products/loco-positioning-deck |
| 8 | Loco positioning node | https://store.bitcraze.io/products/loco-positioning-node |
| 1 | Crazyradio 2.0 | https://store.bitcraze.io/products/crazyradio-2-0 |

N between 1 and 15, 15+ is possible but requires more setup and some changes in code

## Setup

### Guides

Please read the following guides by bitcraze to complete the setup

- [Crazyflie](https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyflie-2-x/)
    - [Crazyradio](https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyradio-2-0/)
    - [cfclient](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/installation/install/)
- [Expansion decks](https://www.bitcraze.io/documentation/tutorials/getting-started-with-expansion-decks/)
    - [Flow deck](https://www.bitcraze.io/documentation/tutorials/getting-started-with-flow-deck/)
- [Loco positioning system](https://www.bitcraze.io/documentation/system/positioning/loco-positioning-system/)
    - [getting started with LPS](https://www.bitcraze.io/documentation/tutorials/getting-started-with-loco-positioning-system/)
    - [LP configuration tool](https://github.com/bitcraze/lps-tools)

### Personal setup

1. After you have acquired the source code of this project you create a python virtual environment using python 3.12 (anything >= 3.11 should work fine) in the root folder (folder where main.py is located)
```sh
python3.12 -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```
2. Using the virtual environment you just created
    1. ```pip install requirements.txt```
    2. follow the steps to run the **cfclient** (it has already been installed using the ```requirements.txt``` file)
    3. follow the steps to install the **loco positioning configuration tool**
3. Follow the steps to build and flash the **Crazyradio**
4. Follow the steps to build and update each **Crazyflie**
    - each crazyflie has the same base link uri ```radio://0/80/2M/E7E7E7E7E7```
    - give each crazyflie a unique channel number so the link uri looks like this ```radio://0/xx/2M/E7E7E7E7E7``` preferably xx > 80 for simplicity
5. mount the **Flow deck** at the bottom and the **Loco positioning deck** at the top for each crazyflie as specified by the **expansion decks** guide
6. Follow the steps to get started with the **Loco positioning system**
    - each node and crazyflie must be set to **TDoa 2** (**TDoA 3** should also be possible, only use one at a time)
    - after writing the positions to the anchors, save the configuration to a yaml file named ```loco_positioning_nodes.yaml``` in the root folder
7. place all the drones you will be using inside the perimeter of the positioning nodes
8. all the drones you use must be face in the direction of +inf along the x-axis of your perimeter
9. execute ```python main.py```

### EXTRA feel free to change these params in root_folder_name/services/navigation.py and remove the node offset if it is not required for your node setup

```python
# search nodes per meter along <axis>

X_PRECISION = 2 # the x axis
Y_PRECISION = 2 # the y axis

# distance a drone must keep between itself and the <cardinal direction> positioning nodes along <axis> (in meters)

X_MIN = 1.0 # western, x axis
X_MAX = 1.0 # eastern, x axis
Y_MIN = 0.5 # southern, y axis
Y_MAX = 0.5 # northern, y axis

nodes[0]["x"] += 0.2 # remove this node offset
```

or change the speed if you are feeling bold using root_folder_name/utils/drone.py

```python
FLIGHT_HEIGHT = 0.75 # Height at which a drone will fly
Z_MIN = 0.0 # The lowest height a drone can go (ground level)

V_XY_DRONE = 0.20 # the speed of a drone (in meters/second)
V_Z_DRONE = 0.5 # the speed of a drone (in meters/second)
```