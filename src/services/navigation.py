import math
import yaml
import copy
import random
import copy

import numpy as np
from scipy.optimize import linear_sum_assignment

from typing import Dict, List, Tuple

import numpy as np
from numpy.typing import NDArray

Position2D = Tuple[float, float]
Position3D = Tuple[float, float, float]
Route = List[Position2D]

from cflib.crazyflie.swarm import SwarmPosition

from utils.algorithm import CMSG, RoutePlanner

LOCO_POSITIONING_NODES_FILENAME = "loco_positioning_nodes.yaml"

nodes = {}

with open(LOCO_POSITIONING_NODES_FILENAME, "r") as f:
    nodes = yaml.safe_load(f)

# most <directions> positioning node location along the (x,y,z) axes respectively

# node 0: western, southern and lowest
# node 6: eastern, northern and highest

# search nodes per meter along <axis>

X_PRECISION = 2 # the x axis
Y_PRECISION = 2 # the y axis

# distance a drone must keep between itself and the <cardinal direction> positioning nodes along <axis> (in meters)

X_MIN = 0.5 # western, x axis
X_MAX = 0.5 # eastern, x axis
Y_MIN = 0.0 # southern, y axis
Y_MAX = 0.0 # northern, y axis

# numbder of search nodes along the x/y axis

NX_SEARCH_NODES = math.ceil((nodes[6]["x"] - nodes[0]["x"] - X_MIN - X_MAX) * X_PRECISION)
NY_SEARCH_NODES = math.ceil((nodes[6]["y"] - nodes[0]["y"] - Y_MIN - Y_MAX) * Y_PRECISION)

SEARCH_SHAPE_XY = (NX_SEARCH_NODES, NY_SEARCH_NODES)

# Create an np.ndarray 

x_vals = np.arange(NX_SEARCH_NODES) / X_PRECISION + X_MIN
y_vals = np.arange(NY_SEARCH_NODES) / Y_PRECISION + Y_MIN

xx, yy = np.meshgrid(x_vals, y_vals)

searchable_nodes = np.column_stack((xx.ravel(), yy.ravel()))

# D_ANY[0] == [north_y, north_x]
# 4-directional movement (Manhatten distance)
D_MANHATTEN = np.array([
    [1, 0, -1, 0],# y
    [0, 1, 0, -1] # x
]).transpose()

# 8-directional movement (Chebyshev neighborhood)
D_CHEBYSHEV = np.array([
    [1, 1, 0, -1, -1, -1, 0, 1],# y
    [0, 1, 1, 1, 0, -1, -1, -1] # x
]).transpose()

class NavigationService:
    def __init__(self):
        self.search_area: NDArray[np.float64] = searchable_nodes
        self.unsearched_nodes: NDArray[np.float64] = copy.deepcopy(searchable_nodes)

        self.drone_ids: List[str] = []
        self.color_dict: Dict[str, Tuple[float, float, float]] = {}

        self.drones_p0: Dict[str, Position2D] = {}
        self.drones_pc: Dict[str, Position2D] = {}
        self.drones_pn: Dict[str, Position2D] = {}

        self.routes: Dict[str, Route] = {}
        self.full_routes: Dict[str, Route] = {}

    def set_drone_positions(self, positions: dict[str, SwarmPosition]):
        drones_p_none: Dict[str, Position2D] = {drone_id: (p.x, p.y) for drone_id, p in positions.items()}
        self.drone_ids = list(drones_p_none.keys())
        self.color_dict = {
            drone_id: (random.random(), random.random(), random.random())
            for drone_id in self.drone_ids
        }

        drone_positions = np.array(list(drones_p_none.values())) # (K, 2)
        nodes = self.unsearched_nodes # (N, 2)

        dist_matrix = np.linalg.norm(drone_positions[:, None, :] - nodes[None, :, :], axis=2) # (K x N)

        row_ind, col_ind = linear_sum_assignment(dist_matrix)

        drones_p0 = {}
        assigned_nodes = []

        for r, c in zip(row_ind, col_ind):
            drone_id: str = self.drone_ids[r]
            node: Position2D = tuple(nodes[c])

            drones_p0[drone_id] = node
            assigned_nodes.append(c)

        self.unsearched_nodes = np.delete(nodes, assigned_nodes, axis=0)

        self.drones_p0 = drones_p0
        self.drones_pc = copy.deepcopy(drones_p0)
        self.drones_pn = copy.deepcopy(drones_p0)

    def build_routes(self) -> None:
        if not self.drones_p0:
            raise ValueError("Drone starting positions (p0) not initialized")

        origins_xy = []
        drone_index_map = {}

        for i, drone_id in enumerate(self.drone_ids):
            pos = np.array(self.drones_p0[drone_id])

            idx = np.argmin(np.linalg.norm(self.search_area - pos, axis=1))
            origin_y, origin_x = divmod(idx, NX_SEARCH_NODES)

            origins_xy.append((origin_x, origin_y))
            drone_index_map[i] = drone_id

        # --- Step 3: run CMSG ---
        cmsg = CMSG(SEARCH_SHAPE_XY, origins_xy, D_MANHATTEN)
        labels = cmsg.labels

        # --- Step 4: assign nodes ---
        assigned = {drone_id: [] for drone_id in self.drone_ids}

        for node in self.search_area:
            node_x, node_y = node

            xi = int(round((node_x - X_MIN) * X_PRECISION))
            yi = int(round((node_y - Y_MIN) * Y_PRECISION))

            xi = min(max(xi, 0), NX_SEARCH_NODES - 1)
            yi = min(max(yi, 0), NY_SEARCH_NODES - 1)

            label = labels[yi, xi]

            if label != -1:
                drone_id = drone_index_map[label]
                assigned[drone_id].append((node_x, node_y))

        # --- Step 5: route inside territory ---
        routes = {}

        for label_id, drone_id in drone_index_map.items():
            start = self.drones_p0[drone_id]
            nodes = assigned[drone_id]

            # ✅ build territory mask (y, x indexing!)
            territory_mask = (labels == label_id)

            route = []
            current = start
            remaining = nodes.copy()

            while remaining:
                next_node = min(
                    remaining,
                    key=lambda n: math.dist(current, n)
                )

                # convert to grid coords
                cx = int(round((current[0] - X_MIN) * X_PRECISION))
                cy = int(round((current[1] - Y_MIN) * Y_PRECISION))

                nx = int(round((next_node[0] - X_MIN) * X_PRECISION))
                ny = int(round((next_node[1] - Y_MIN) * Y_PRECISION))

                path_grid = RoutePlanner.shortest_bound_path(
                    (cx, cy),
                    (nx, ny),
                    territory_mask,
                    SEARCH_SHAPE_XY
                )

                # convert back to world coords
                path_world = [
                    (
                        x / X_PRECISION + X_MIN,
                        y / Y_PRECISION + Y_MIN
                    )
                    for x, y in path_grid
                ]

                route.extend(path_world[1:])
                current = next_node
                remaining.remove(next_node)

            # --- return to start (SAFE) ---
            cx = int(round((current[0] - X_MIN) * X_PRECISION))
            cy = int(round((current[1] - Y_MIN) * Y_PRECISION))

            sx = int(round((start[0] - X_MIN) * X_PRECISION))
            sy = int(round((start[1] - Y_MIN) * Y_PRECISION))

            return_grid = RoutePlanner.shortest_bound_path(
                (cx, cy),
                (sx, sy),
                territory_mask,
                SEARCH_SHAPE_XY
            )

            return_world = [
                (
                    x / X_PRECISION + X_MIN,
                    y / Y_PRECISION + Y_MIN
                )
                for x, y in return_grid
            ]

            route.extend(return_world[1:])

            routes[drone_id] = route

        self.routes = routes
        self.full_routes = copy.deepcopy(routes)

    def get_step(self) -> Dict[str, List[Tuple[Position2D, float, float]]]:
        self.drones_pc = copy.deepcopy(self.drones_pn)

        self.drones_pn = {
            drone_id: (
                self.routes[drone_id].pop(0)
                if self.routes[drone_id]
                else self.drones_pc[drone_id]
            )
            for drone_id in self.drone_ids
        }

        distances: Dict[str, float] = {
            drone_id: math.dist(
                self.drones_pc[drone_id],
                self.drones_pn[drone_id]
            )
            for drone_id in self.drone_ids
        }

        max_distance: float = max(distances.values())

        step: Dict[str, List[Tuple[Position2D, float, float]]] = {
            drone_id: [
                (
                    self.drones_pn[drone_id],
                    distances[drone_id],
                    max_distance
                )
            ]
            for drone_id in self.drone_ids
        }

        return step
        