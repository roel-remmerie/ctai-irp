<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# python lib crazyflie stop rotors

In the Bitcraze Python library, the usual way to stop the **rotors** is to stop sending setpoints and let the timeout cut motor power, or to use an explicit emergency-stop style command if your control stack provides one.[^1_1][^1_2]

## Practical options

- If you are using the low-level setpoint API, keep sending commands during flight; after about 2 seconds without new setpoints, the Crazyflie cuts power to the motors.[^1_1]
- If you are using `MotionCommander`, calling `mc.stop()` lands/stops the motion command sequence, but it is not the same as an instant motor cut-off.[^1_3]
- For an immediate motor shutdown, Crazyswarm documents `cmdStop()` / emergency stop behavior that cuts power and ignores future commands.[^1_2]


## Minimal example idea

If you are using the standard `cflib` setpoint flow, the simplest safe stop is usually to stop streaming commands and let the timeout disengage the motors. If you need a hard stop, use the emergency-stop mechanism available in your control layer instead of relying on normal landing behavior.[^1_4][^1_2][^1_1]

## Important note

Because these methods differ in how abruptly they stop the drone, pick the one that matches your goal: landing, stopping motion, or cutting power immediately.[^1_4][^1_2][^1_1]
<span style="display:none">[^1_10][^1_5][^1_6][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://github.com/bitcraze/crazyflie-lib-python/blob/master/docs/user-guides/python_api.md

[^1_2]: https://crazyswarm.readthedocs.io/en/latest/api.html

[^1_3]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_motion_commander/

[^1_4]: https://tsrt10.gitlab-pages.liu.se/2024/visionen/User_manual.pdf

[^1_5]: http://ee.bradley.edu/projects/proj2018/crazy/resources/bu_crazyflie_final_report.pdf

[^1_6]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_connect_log_param/

[^1_7]: https://github.com/bitcraze/crazyflie-lib-python

[^1_8]: https://www.diva-portal.org/smash/get/diva2:1440184/FULLTEXT01.pdf

[^1_9]: https://coogan.ece.gatech.edu/papers/pdf/llanes2024crazysim.pdf

[^1_10]: https://crazyflie1.rssing.com/chan-15864016/all_p14.html

