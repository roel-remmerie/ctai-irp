<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# fly crazyflie swarm without the use of: with cflib.crazyflie.swarm.Swarm() as swarm:

Yes — you can fly a Crazyflie swarm **without** using `with cflib.crazyflie.swarm.Swarm() as swarm:` by managing each `SyncCrazyflie` connection yourself and running commands across them in threads. Bitcraze’s docs show that `Swarm` is just a convenience wrapper around multiple `SyncCrazyflie` links, while `SyncCrazyflie` is the blocking connection primitive you can use directly.[^1_1]

## Direct approach

Instead of `Swarm`, connect to each URI separately with `SyncCrazyflie`, then call the same takeoff, move, and land functions for each drone. The `SyncCrazyflie` API supports a normal context manager, and once connected you can access `scf.cf.high_level_commander` to issue flight commands.[^1_2][^1_3]

```python
import time
import threading

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

URIS = [
    "radio://0/20/2M/E7E7E7E701",
    "radio://0/20/2M/E7E7E7E702",
]

def takeoff_and_land(scf):
    commander = scf.cf.high_level_commander
    commander.takeoff(0.5, 2.0)
    time.sleep(3)
    commander.land(0.0, 2.0)
    time.sleep(2)
    commander.stop()

def fly_one(uri):
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache="./cache")) as scf:
        scf.cf.param.set_value("stabilizer.estimator", 2)
        time.sleep(1)
        takeoff_and_land(scf)

def main():
    cflib.crtp.init_drivers()
    threads = []
    for uri in URIS:
        t = threading.Thread(target=fly_one, args=(uri,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
```


## What changes

- You lose the convenience methods like `swarm.parallel_safe(...)` and `swarm.sequential(...)`, so you implement parallelism yourself with `threading` or `concurrent.futures`.[^1_1]
- You still get the same underlying connection model, because each drone is controlled through its own `SyncCrazyflie` instance.[^1_3][^1_2]
- If you need per-drone motion differences, pass each URI its own sequence of commands, similar to the `args_dict` style shown in the swarm guide.[^1_1]


## When this is useful

This approach is good if you want full control over timing, custom synchronization, or a simpler code path without the swarm helper. The Bitcraze swarm tutorial also confirms that the swarm interface is mainly a wrapper that automates these same operations.[^1_1]

A practical note: all drones on the same radio should use the same channel, and you still need valid position estimation before takeoff to avoid crashes.[^1_1]
<span style="display:none">[^1_10][^1_11][^1_12][^1_13][^1_14][^1_15][^1_16][^1_17][^1_18][^1_19][^1_4][^1_5][^1_6][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/crazyflie/swarm/

[^1_2]: https://sites.duke.edu/memscapstone/drone-swarm-victors-work/

[^1_3]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_connect_log_param/

[^1_4]: https://github.com/bitcraze/crazyflie-lib-python/blob/master/cflib/crazyflie/swarm.py

[^1_5]: https://forum.bitcraze.io/viewtopic.php?t=4375

[^1_6]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_swarm_interface/

[^1_7]: https://github.com/bitcraze/crazyflie-firmware/blob/master/examples/demos/swarm_demo/control_tower/control_tower.py

[^1_8]: https://forum.bitcraze.io/viewtopic.php?t=4559

[^1_9]: https://fdmcs.math.cnrs.fr/crazyflie_ros2/cflib/-/blob/bd8b374fecd59631eb41478da684bdd46a2041b9/examples/swarm/asynchronizedSwarm.py

[^1_10]: https://crazyswarm.readthedocs.io/en/latest/howto/howto.html

[^1_11]: http://ee.bradley.edu/projects/proj2018/crazy/resources/bu_crazyflie_final_report.pdf

[^1_12]: https://ttk.gricad-gitlab.univ-grenoble-alpes.fr/formationcontrol/formation-control-experiments/-/blob/main/Crazyflie/Swarm example.py

[^1_13]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/crazyflie/syncCrazyflie/

[^1_14]: https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/swarm/synchronized_sequence.py

[^1_15]: https://faculty.washington.edu/minster/bio_inspired_robotics/software_examples/crazyflie_oscillate_class.py

[^1_16]: https://github.com/bitcraze/crazyflie-lib-python/blob/master/cflib/crazyflie/syncCrazyflie.py

[^1_17]: https://fdmcs.math.cnrs.fr/crazyflie_ros2/cflib/-/blob/main/examples/step-by-step/sbs_swarm.py

[^1_18]: https://snyk.io/advisor/python/cflib/example

[^1_19]: https://fdmcs.math.cnrs.fr/crazyflie_ros2/cflib/-/blob/main/docs/user-guides/sbs_swarm_interface.md


---

# without any with statements please

Yes — you can do it **without any `with` statements** by using `Crazyflie.open_link()` and `Crazyflie.close_link()` manually for each drone.[^2_1]

## Example

```python
import time
import threading

import cflib.crtp
from cflib.crazyflie import Crazyflie

URIS = [
    "radio://0/20/2M/E7E7E7E701",
    "radio://0/20/2M/E7E7E7E702",
]

def fly(uri):
    cf = Crazyflie(rw_cache="./cache")
    connected = threading.Event()

    def on_connected(link_uri):
        connected.set()

    def on_failed(link_uri, msg):
        print(f"Failed to connect to {link_uri}: {msg}")
        connected.set()

    cf.connected.add_callback(on_connected)
    cf.connection_failed.add_callback(on_failed)

    cf.open_link(uri)
    connected.wait()

    if not cf.is_connected:
        return

    time.sleep(1)
    cf.param.set_value("stabilizer.estimator", 2)
    time.sleep(1)

    commander = cf.high_level_commander
    commander.takeoff(0.5, 2.0)
    time.sleep(3)
    commander.land(0.0, 2.0)
    time.sleep(2)
    commander.stop()

    cf.close_link()

def main():
    cflib.crtp.init_drivers()
    threads = []
    for uri in URIS:
        t = threading.Thread(target=fly, args=(uri,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
```


## Important points

- `cflib` is asynchronous, so `open_link()` returns immediately and you must wait for the `connected` callback before sending commands.[^2_1]
- You should call `close_link()` yourself when finished, since you are not using the context manager.[^2_1]
- For swarm control, the Bitcraze swarm helper normally wraps multiple `SyncCrazyflie` objects, but you can bypass that and control each `Crazyflie` instance directly.[^2_1]


## If you want low-level control

You can also use `cf.commander.send_setpoint(roll, pitch, yawrate, thrust)` instead of the high-level commander. The Crazyflie Python API documents that `send_setpoint()` is the low-level attitude command, and it must be sent repeatedly fast enough to avoid watchdog timeout.[^2_1]
<span style="display:none">[^2_10][^2_2][^2_3][^2_4][^2_5][^2_6][^2_7][^2_8][^2_9]</span>

<div align="center">⁂</div>

[^2_1]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/crazyflie/swarm/

[^2_2]: https://github.com/bitcraze/crazyflie-lib-python/blob/master/cflib/crazyflie/swarm.py

[^2_3]: https://python.hotexamples.com/examples/cflib.crazyflie/Crazyflie/-/python-crazyflie-class-examples.html

[^2_4]: https://github.com/IMRCLab/crazyswarm2/discussions/516

[^2_5]: https://snyk.io/advisor/python/cflib/functions/cflib.crazyflie.Crazyflie

[^2_6]: https://github.com/bitcraze/crazyflie-lib-python/blob/master/docs/user-guides/sbs_swarm_interface.md

[^2_7]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/python_api/

[^2_8]: https://github.com/bitcraze/crazyflie-lib-python

[^2_9]: https://crazyswarm.readthedocs.io/en/latest/api.html

[^2_10]: https://github.com/bitcraze/crazyflie-lib-python/blob/master/docs/user-guides/python_api.md


---

# crazyflies = [SyncCrazyflie(uri) for uri in self.uris]

        try:
            pass
        finally:
            for scf in crazyflies:
                DroneCommand.stop_rotors(scf)
    does this work

No — as written, that snippet will not work, because `SyncCrazyflie(uri)` does not connect by itself; it only creates the object, and you still need to call the connect/disconnect flow explicitly or use a context manager.[^3_1][^3_2]

## What is missing

`SyncCrazyflie` is documented as a synchronous Crazyflie wrapper whose normal usage is `with SyncCrazyflie(uri, cf=Crazyflie(...)) as scf: ...`, and the connection sequence completes only after the object connects.[^3_1]
Also, your list contains unconnected `SyncCrazyflie` objects, so `DroneCommand.stop_rotors(scf)` would be operating on drones that have not been opened yet.[^3_3][^3_1]

## Non-`with` version

Use `open_link()` on a real `Crazyflie` object for each URI, wait for connection, then stop the rotors, then `close_link()`.[^3_4][^3_1]

```python
import threading
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

crazyflies = []
events = []

for uri in self.uris:
    cf = Crazyflie(rw_cache="./cache")
    scf = SyncCrazyflie(uri, cf=cf)
    evt = threading.Event()

    def connected_cb(link_uri, evt=evt):
        evt.set()

    def failed_cb(link_uri, msg, evt=evt):
        evt.set()

    cf.connected.add_callback(connected_cb)
    cf.connection_failed.add_callback(failed_cb)
    cf.connection_lost.add_callback(failed_cb)

    scf.open_link()
    evt.wait()

    if cf.is_connected:
        crazyflies.append(scf)
        events.append(evt)

try:
    for scf in crazyflies:
        DroneCommand.stop_rotors(scf)
finally:
    for scf in crazyflies:
        scf.close_link()
```


## Safer pattern

If `DroneCommand.stop_rotors()` expects a connected `SyncCrazyflie`, then the connection step must happen before the `try/finally` block that stops the rotors.[^3_3][^3_1]
If you want, I can rewrite this into a clean helper method that handles connect, stop, and cleanup for all URIs without any `with` statements.
<span style="display:none">[^3_10][^3_5][^3_6][^3_7][^3_8][^3_9]</span>

<div align="center">⁂</div>

[^3_1]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/crazyflie/syncCrazyflie/

[^3_2]: https://github.com/bitcraze/crazyflie-lib-python/blob/master/cflib/crazyflie/syncCrazyflie.py

[^3_3]: https://forum.bitcraze.io/viewtopic.php?t=5316

[^3_4]: https://github.com/bitcraze/crazyflie-lib-python/blob/master/docs/user-guides/python_api.md

[^3_5]: https://www.bitcraze.io/2025/06/exploring-the-swarming-potential-of-the-crazyflie/

[^3_6]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_swarm_interface/

[^3_7]: https://crazyswarm.readthedocs.io

[^3_8]: https://crazyswarm.readthedocs.io/en/latest/howto/howto.html

[^3_9]: https://python-docs.synapse.org/reference/synapse_utils/

[^3_10]: https://github.com/orgs/bitcraze/discussions/1310

