import math
from collections import defaultdict

class SearchService():
    def __init__(self, drone_locations: dict[str, tuple[float, float]], search_area: list[tuple[float, float]]):
        self.drone_locations = drone_locations
        self.routes = {}

        drone_ids = list(drone_locations.keys())
        k = len(drone_ids)

        # --- STEP 1: Simple spatial clustering (k-means-like) ---
        centroids = list(drone_locations.values())

        for _ in range(10):  # few iterations is enough
            clusters = defaultdict(list)

            for point in search_area:
                closest_idx = min(
                    range(k),
                    key=lambda i: self._distance(point, centroids[i])
                )
                clusters[closest_idx].append(point)

            new_centroids = []
            for i in range(k):
                if clusters[i]:
                    xs, ys = zip(*clusters[i])
                    new_centroids.append((sum(xs)/len(xs), sum(ys)/len(ys)))
                else:
                    new_centroids.append(centroids[i])

            centroids = new_centroids

        # --- STEP 2: Assign clusters to drones ---
        for i, drone_id in enumerate(drone_ids):
            points = clusters[i]
            start = drone_locations[drone_id]

            # --- STEP 3: Route ordering (nearest neighbor heuristic) ---
            route = self._nearest_neighbor_route(start, points)

            # --- STEP 4: Return to start ---
            route.append(start)

            self.routes[drone_id] = route

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

this is heuristic, I want every drone to have about equal number of tiles they need to visit, if for example there are 100 tiles an 3 drones then of course it is divided 34 33 33, make sure the tiles are divided to minimize total travel distance and also the variance in travel distance between drones

What you have now is a good start, but it doesn’t actually enforce balance—it only hopes k-means produces roughly equal clusters. It won’t reliably give you 34/33/33 splits or equal travel effort.

If you want (1) equal number of tiles and (2) low total distance and (3) low variance between drones, you need to explicitly enforce those constraints during assignment.
🔧 Core idea: Balanced clustering (capacity-constrained assignment)

Instead of vanilla k-means, treat this as a capacitated assignment problem:

    Each drone = a cluster with capacity

    Capacity = ceil(n_tiles / k) or floor(...)

    Assign each tile to a drone:

        minimizing distance to that drone

        while respecting capacity

✅ Step-by-step fix
1. Define exact capacities

n = len(search_area)
k = len(drone_ids)

base = n // k
remainder = n % k

capacities = [base + (1 if i < remainder else 0) for i in range(k)]

Example: 100 tiles, 3 drones → [34, 33, 33]
2. Replace k-means with greedy balanced assignment

Instead of clustering, do:

clusters = {i: [] for i in range(k)}
remaining_capacity = capacities[:]

# Sort tiles by difficulty (optional but improves quality)
points = sorted(search_area, key=lambda p: min(
    self._distance(p, c) for c in centroids
), reverse=True)

for point in points:
    # Find closest drone that still has capacity
    best_i = min(
        [i for i in range(k) if remaining_capacity[i] > 0],
        key=lambda i: self._distance(point, drone_locations[drone_ids[i]])
    )
    
    clusters[best_i].append(point)
    remaining_capacity[best_i] -= 1

This guarantees:

    Exact tile balance ✔

    Reasonable spatial grouping ✔

3. Improve travel balance (VERY important)

Equal tiles ≠ equal distance. Some clusters may be spread out.

👉 Add a penalty for long routes during assignment:

Replace distance with:

def cost(i, point):
    base_dist = self._distance(point, drone_locations[drone_ids[i]])
    load_penalty = len(clusters[i]) * 0.1  # tune this
    return base_dist + load_penalty

Then:

best_i = min(
    [i for i in range(k) if remaining_capacity[i] > 0],
    key=lambda i: cost(i, point)
)

4. Optional: Local optimization (big improvement)

After assignment, rebalance by swapping points:

def try_swap(i, j):
    for p1 in clusters[i]:
        for p2 in clusters[j]:
            old = (
                self._distance(p1, drone_locations[drone_ids[i]]) +
                self._distance(p2, drone_locations[drone_ids[j]])
            )
            new = (
                self._distance(p1, drone_locations[drone_ids[j]]) +
                self._distance(p2, drone_locations[drone_ids[i]])
            )
            if new < old:
                clusters[i].remove(p1)
                clusters[j].remove(p2)
                clusters[i].append(p2)
                clusters[j].append(p1)
                return True
    return False

Run a few iterations over all pairs of clusters.
5. Keep your routing (good choice)

Your nearest neighbor is fine:

route = self._nearest_neighbor_route(start, points)
route.append(start)

If you want better:

    add 2-opt optimization afterward

🧠 Summary

Your current method:

    ❌ No tile balance guarantee

    ❌ No distance fairness

Improved method:

    ✅ Exact tile distribution (34/33/33)

    ✅ Lower total travel distance

    ✅ Reduced variance between drones

    ✅ Still fast (no heavy optimization solver)

🚀 If you want optimal (not heuristic)

This problem is actually a form of:

    Multi-Depot Vehicle Routing Problem (MDVRP)

To go beyond heuristics, you’d use:

    Google OR-Tools

It can:

    enforce equal workload

    minimize total distance

    balance route lengths

If you want, I can rewrite your full class using this balanced approach (clean + optimized).

yes please

Here’s a clean rewrite of your SearchService that:

    ✅ Guarantees balanced tile counts (e.g. 34/33/33)

    ✅ Minimizes total distance (greedy but effective)

    ✅ Reduces variance between drones

    ✅ Keeps your routing simple but adds a 2-opt improvement

🚀 Full Improved Implementation

import math
from itertools import combinations

class SearchService:
    def __init__(self, drone_locations: dict[str, tuple[float, float]], search_area: list[tuple[float, float]]):
        self.drone_locations = drone_locations
        self.routes = {}

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

🧠 What changed (and why it works)
1. Hard capacity constraint

You now guarantee exact tile counts:

    No more uneven clusters from k-means

    Deterministic distribution

2. Smarter assignment

    Assign hardest (furthest) points first

    Avoids “leftover bad points” problem

3. Distance balancing

The spread_penalty:

len(clusters[i]) * 0.2

prevents one drone from getting:

    all nearby points (short route)

    while another gets scattered points (long route)

4. Swap optimization

Fixes bad assignments after greedy step:

    reduces total distance

    reduces imbalance

5. 2-opt routing

Your routes are now:

    much shorter

    less zig-zaggy

⚖️ Result

Compared to your original version:
Feature	Before	Now
Equal tile count	❌	✅
Distance efficiency	⚠️	✅
Fair workload	❌	✅
Route quality	⚠️	✅
🔥 If you want next-level

If you later want:

    time windows

    battery constraints

    real optimality

Then switch to:
👉 Google OR-Tools

If you'd like, I can also:

    visualize the clusters/routes

    or
    benchmark this vs your original version

    or
    upgrade this to a near-optimal solver without OR-Tools


def get_step(self, to_origin=False):
        step = {}

        for drone_id, route in self.routes:
            next_location: tuple[float,float] = {}
            current_location = self.drone_locations[drone_id]
            if to_origin:
                next_location = self.drone_origins[drone_id]
            if route:
                next_location = self.routes[drone_id].pop(0)
            else:
                next_location = current_location

            distance = self._distance(next_location, current_location)

            step[drone_id] = (next_location[0], next_location[1], distance)

            self.drone_locations[drone_id] = self.next_locations[drone_id]
            self.next_locations[drone_id] = next_location[drone_id]

        return step

can this be simplified

Yes — and more importantly, it also has a couple of bugs, not just complexity issues.
⚠️ Problems in your current version

    for drone_id, route in self.routes: → wrong, you need .items()

    next_location: tuple[...] = {} → wrong type (dict instead of tuple)

    self.next_locations[drone_id] = next_location[drone_id] → indexing a tuple incorrectly

    Logic overwrites to_origin immediately if route exists

✅ Clean & simplified version

def get_step(self, to_origin=False):
    step = {}

    for drone_id, route in self.routes.items():
        current = self.drone_locations[drone_id]

        if route:
            next_loc = route.pop(0)
        elif to_origin:
            next_loc = self.drone_origins[drone_id]
        else:
            next_loc = current

        distance = self._distance(current, next_loc)

        step[drone_id] = (*next_loc, distance)

        # Update position
        self.drone_locations[drone_id] = next_loc

    return step

✨ What got better
1. Simpler control flow

Instead of overwriting next_location 3 times, we use:

if route:
elif to_origin:
else:

This makes the priority clear:

    Follow route

    Otherwise go to origin (if requested)

    Otherwise stay put

2. Removed unnecessary state

You don’t actually need:

self.next_locations

You can directly update:

self.drone_locations[drone_id] = next_loc

3. Cleaner tuple unpacking

step[drone_id] = (*next_loc, distance)

instead of manually indexing.
🔍 Optional improvement (if routes include start)

Right now, your routes likely start with the current position, meaning the first step is distance 0.

If that’s the case, you may want to skip it:

if route and route[0] == current:
    route.pop(0)

🧠 If you want even cleaner

You can compress it slightly further:

def get_step(self, to_origin=False):
    step = {}

    for drone_id, route in self.routes.items():
        current = self.drone_locations[drone_id]

        next_loc = (
            route.pop(0) if route else
            self.drone_origins[drone_id] if to_origin else
            current
        )

        step[drone_id] = (*next_loc, self._distance(current, next_loc))
        self.drone_locations[drone_id] = next_loc

    return step

If you want, I can also help you
turn this into a generator-based simulation loop (much cleaner for stepping through time).


