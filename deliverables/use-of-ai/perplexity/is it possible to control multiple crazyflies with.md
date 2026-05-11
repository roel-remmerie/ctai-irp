<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# is it possible to control multiple crazyflies with the swarm code but send them in different directions

Yes, it is absolutely possible to control multiple Crazyflies with the swarm code and send them in different directions at the same time.[^1_3][^1_8]

### How the swarm code supports different directions

The Bitcraze Python library’s `Swarm` class lets you send commands in parallel or sequentially to each drone, and you can pass drone‑specific arguments (like target positions or trajectories) for each Crazyflie.  This means you can define a different flight sequence (e.g., different `x, y, z` commands or velocity vectors) for each URI in the swarm so they move in independent directions.[^1_8][^1_3]

### Basic idea in practice

- In the `run_sequence`‑style examples, each Crazyflie is given its own sequence of relative movements, so you can assign, for example, one to fly “forward,” one to fly “left,” and one to hover, all simultaneously.[^1_3]
- You structure this by using an `args_dict` where the key is the radio address (URI) and the value is the list of commands or trajectory points for that specific drone.[^1_3]

If you tell me which framework you’re using (`crazyflie-lib-python`, Crazyswarm ROS, or something else), I can sketch a short code snippet that sends each Crazyflie in a different direction.
<span style="display:none">[^1_1][^1_10][^1_2][^1_4][^1_5][^1_6][^1_7][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://forum.bitcraze.io/viewtopic.php?t=3486

[^1_2]: https://github.com/orgs/bitcraze/discussions/1217

[^1_3]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_swarm_interface/

[^1_4]: https://crazyswarm.readthedocs.io/en/latest/configuration.html

[^1_5]: https://crazyswarm.readthedocs.io/en/latest/howto/howto.html

[^1_6]: https://forum.bitcraze.io/viewtopic.php?t=4185

[^1_7]: https://github.com/USC-ACTLab/crazyswarm/issues/175

[^1_8]: https://www.bitcraze.io/2025/06/exploring-the-swarming-potential-of-the-crazyflie/

[^1_9]: http://ee.bradley.edu/projects/proj2018/crazy/resources/bu_crazyflie_final_report.pdf

[^1_10]: https://github.com/orgs/bitcraze/discussions/1749

