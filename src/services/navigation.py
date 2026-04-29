import random
import math
from itertools import combinations


ACCURACY = 4 # nodes per meter
X_BOUND = 0.75 # meters
Y_BOUND = 0.75 # meters
X_NODES = int(X_BOUND * ACCURACY)
Y_NODES = int(Y_BOUND * ACCURACY)
SEARCH_AREA = (X_NODES, Y_NODES)
print(SEARCH_AREA)

search_area = [(x,y) for x in range(SEARCH_AREA[0]) for y in range(SEARCH_AREA[1])]

class NavigationService:
    def __init__(self, drone_locations: dict[str, tuple[float, float]]):
        self.drone_origins = drone_locations
        self.drone_locations = drone_locations
        self.next_locations = drone_locations
        self.routes: dict[str, list[tuple[float, float]]] = {}
        self.color_dict = {drone_id: (random.random(), random.random(), random.random()) for drone_id in drone_locations.keys()}

        drone_ids = list(drone_locations.keys())
        k = len(drone_ids)
        n = len(search_area)

        # --- STEP 1: Define exact capacities ---
        base = n // k
        remainder = n % k
        capacities = [base + (1 if i < remainder else 0) for i in range(k)]

        # --- STEP 2: Balanced assignment ---
        clusters = {i: [] for i in range(k)}
        remaining_capacity = capacities[:]

        # Sort points: assign difficult (far) points first
        points = sorted(
            search_area,
            key=lambda p: min(self._distance(p, drone_locations[d]) for d in drone_ids),
            reverse=True
        )

        def cost(i, point):
            start = drone_locations[drone_ids[i]]
            base_dist = self._distance(point, start)
            spread_penalty = len(clusters[i]) * 0.2  # tune this
            return base_dist + spread_penalty

        for point in points:
            candidates = [i for i in range(k) if remaining_capacity[i] > 0]
            best_i = min(candidates, key=lambda i: cost(i, point))

            clusters[best_i].append(point)
            remaining_capacity[best_i] -= 1

        # --- STEP 3: Local swap optimization ---
        self._improve_clusters(clusters, drone_ids)

        # --- STEP 4: Build routes ---
        for i, drone_id in enumerate(drone_ids):
            start = drone_locations[drone_id]
            route = self._nearest_neighbor_route(start, clusters[i])

            # Improve route
            route = self._two_opt(route)

            route.append(start)
            self.routes[drone_id] = route

        self.full_routes = self.routes.copy()

    def get_step(self, to_origin=False):
        step = {}

        max_distance = 0

        for drone_id, route in self.routes.items():
            next_location: tuple[float,float] = {}
            current = self.drone_locations[drone_id]
            if to_origin:
                next_location = self.drone_origins[drone_id]
            elif route:
                next_location = self.routes[drone_id].pop(0)
            else:
                next_location = current

            distance = self._distance(next_location, current)

            self.drone_locations[drone_id] = self.next_locations[drone_id]
            self.next_locations[drone_id] = next_location

            if distance > max_distance:
                max_distance = distance

            relative_next = next_location[0] - current[0], next_location[1] - current[1]

            step[drone_id] = (relative_next[0]/ACCURACY, relative_next[1]/ACCURACY, distance/ACCURACY, max_distance)

        return step, max_distance

    # ------------------ HELPERS ------------------

    def _distance(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def _nearest_neighbor_route(self, start, points):
        points = points[:]
        route = [start]
        current = start

        while points:
            next_point = min(points, key=lambda p: self._distance(current, p))
            route.append(next_point)
            points.remove(next_point)
            current = next_point

        return route

    # --- 2-opt route optimization ---
    def _two_opt(self, route):
        best = route
        improved = True

        while improved:
            improved = False
            for i in range(1, len(best) - 2):
                for j in range(i + 1, len(best)):
                    if j - i == 1:
                        continue
                    new_route = best[:]
                    new_route[i:j] = reversed(best[i:j])

                    if self._route_length(new_route) < self._route_length(best):
                        best = new_route
                        improved = True
            route = best

        return best

    def _route_length(self, route):
        return sum(self._distance(route[i], route[i+1]) for i in range(len(route)-1))

    # --- Cluster improvement via swaps ---
    def _improve_clusters(self, clusters, drone_ids):
        improved = True

        while improved:
            improved = False

            for i, j in combinations(clusters.keys(), 2):
                for p1 in clusters[i]:
                    for p2 in clusters[j]:
                        d_i = self.drone_locations[drone_ids[i]]
                        d_j = self.drone_locations[drone_ids[j]]

                        old = (
                            self._distance(p1, d_i) +
                            self._distance(p2, d_j)
                        )
                        new = (
                            self._distance(p1, d_j) +
                            self._distance(p2, d_i)
                        )

                        if new < old:
                            clusters[i].remove(p1)
                            clusters[j].remove(p2)
                            clusters[i].append(p2)
                            clusters[j].append(p1)
                            improved = True
                            break
                    if improved:
                        break
                if improved:
                    break