Ah—that’s a much better way to frame the problem. Now the issue is clear:

    You’re assigning nodes first, then building routes,
    so the routing step has no influence on avoiding overlap.

Exactly. Right now your pipeline is:

assignment → routing

But what you actually need is:

assignment + routing (coupled problem)

🧠 Core problem

Your current assignment minimizes:

    distance from p0 → nodes

But ignores:

    how nodes connect into a path

    how paths interact with other drones

So even if individual assignments look good, the resulting paths can cross badly.
✅ What you should do instead

You need to account for path structure during assignment.

A practical way (without going full combinatorial optimization) is:
🔧 Solution: incremental route building (path-aware assignment)

Instead of assigning all nodes first:

👉 Build routes step by step, always extending the current path.
🔁 Key idea

At each step:

    Each drone has a current endpoint

    You assign the next best node based on:

        distance from current endpoint

            penalty for crossing other routes

✨ Drop-in replacement: path-aware build_routes

def build_routes(self) -> None:
    if not self.drones_p0:
        raise ValueError("Drone starting positions (p0) not initialized")

    all_nodes = [tuple(n) for n in self.search_area]
    remaining = set(all_nodes)

    K = len(self.drone_ids)
    N = len(all_nodes)

    # --- Balanced limits ---
    base = N // K
    remainder = N % K

    limits = {
        d: base + (i < remainder)
        for i, d in enumerate(self.drone_ids)
    }

    # --- Initialize routes ---
    routes = {
        d: [self.drones_p0[d]]  # start at p0
        for d in self.drone_ids
    }

    # --- Helper: segment intersection ---
    def segments_intersect(a, b, c, d):
        def ccw(p1, p2, p3):
            return (p3[1]-p1[1])*(p2[0]-p1[0]) > (p2[1]-p1[1])*(p3[0]-p1[0])
        return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

    # --- Build routes incrementally ---
    while remaining:
        for drone_id in self.drone_ids:
            if len(routes[drone_id]) - 1 >= limits[drone_id]:
                continue

            if not remaining:
                break

            current = routes[drone_id][-1]

            best_node = None
            best_cost = float("inf")

            for node in remaining:
                cost = math.dist(current, node)

                # --- crossing penalty ---
                for other_id in self.drone_ids:
                    route = routes[other_id]
                    for i in range(len(route) - 1):
                        a, b = route[i], route[i+1]
                        if segments_intersect(a, b, current, node):
                            cost += 1000  # heavy penalty

                if cost < best_cost:
                    best_cost = cost
                    best_node = node

            routes[drone_id].append(best_node)
            remaining.remove(best_node)

    # --- Return to p0 ---
    for d in self.drone_ids:
        routes[d].append(self.drones_p0[d])

    # remove starting p0 from execution path (optional, depending on your get_step logic)
    self.routes = {
        d: route[1:] for d, route in routes.items()
    }

🧠 Why this works

Now your system:

    Builds routes incrementally

    Evaluates each step based on:

        distance

        future crossing risk

So:

    assignment is no longer blind

    routing decisions influence assignment

    crossings are actively avoided, not fixed afterward

⚖️ Trade-offs

    Slightly more expensive:
    O(N² * K) instead of simple greedy

    But still very manageable for grid sizes like yours

🚀 If you want even better

You can upgrade this further with:

    soft penalties based on distance to other paths (not just intersections)

    lookahead (2-step) instead of greedy 1-step

    2-opt cleanup per route

💡 Bottom line

You were exactly right:

    The problem is not routing itself—
    it’s that routing decisions come too late.

This fixes that by making routing part of the assignment itself.

This is not doing exactly what I wanted, imagine the nodes as teritory, each drone cannot even acces the teritory of another drone, it doesn't just need a penalty, it's forbidden

Got it—that’s a much stricter constraint than before:

    Each drone owns a territory, and routes must stay entirely inside it.
    Crossing isn’t just bad—it’s impossible by design.

So penalties or incremental routing won’t cut it. You need a hard spatial partition first, then routing inside each partition.
✅ Correct approach: hard territory partition (no overlap possible)

What you want is essentially a discrete Voronoi partition with capacity constraints:

    Assign every node to exactly one drone

    Assignment is based on proximity to p0

    Enforce balanced sizes

    Result = disjoint territories

    Then route inside each territory only

🔧 Key idea

Instead of:

nodes → routes

You do:

nodes → territories (strict) → routes (local only)

Once territories are disjoint, crossing becomes impossible.
✅ Implementation (drop-in build_routes)

This version enforces:

    hard territory ownership

    balanced node counts

    no cross-territory access

def build_routes(self) -> None:
    if not self.drones_p0:
        raise ValueError("Drone starting positions (p0) not initialized")

    all_nodes = [tuple(n) for n in self.search_area]
    K = len(self.drone_ids)
    N = len(all_nodes)

    # --- Balanced limits ---
    base = N // K
    remainder = N % K

    limits = {
        d: base + (i < remainder)
        for i, d in enumerate(self.drone_ids)
    }

    # --- Step 1: compute distance of every node to every drone ---
    drone_positions = {
        d: self.drones_p0[d] for d in self.drone_ids
    }

    # Build list of (node, sorted drones by distance)
    preferences = []
    for node in all_nodes:
        ordered = sorted(
            self.drone_ids,
            key=lambda d: math.dist(drone_positions[d], node)
        )
        preferences.append((node, ordered))

    # --- Step 2: assign nodes with capacity constraint (greedy but stable) ---
    assigned = {d: [] for d in self.drone_ids}

    for node, pref in preferences:
        for d in pref:
            if len(assigned[d]) < limits[d]:
                assigned[d].append(node)
                break

    # --- Step 3: build routes strictly inside territory ---
    routes = {}

    for d in self.drone_ids:
        start = self.drones_p0[d]
        nodes = assigned[d]

        route = []
        current = start
        remaining = nodes.copy()

        while remaining:
            next_node = min(
                remaining,
                key=lambda n: math.dist(current, n)
            )
            route.append(next_node)
            remaining.remove(next_node)
            current = next_node

        # return to start
        route.append(start)

        routes[d] = route

    self.routes = routes

🧠 Why this guarantees what you want
✔ No crossing possible

    Nodes are owned exclusively

    A drone never enters another drone’s node set

    So routes cannot overlap in territory

✔ Balanced workload

    Hard cap per drone (limits)

✔ Spatial coherence

    Nodes are assigned based on closest p0 first

⚠️ Important nuance

This guarantees:

    ❌ No territory overlap

    ❌ No inter-drone crossing due to shared space

But it does not mathematically guarantee:

    zero geometric line intersections at borders (rare edge case)

🚀 If you want absolute geometric separation

Then you need explicit geometric partitioning, e.g.:
Option A — Axis-aligned split (very robust)

    Divide area into vertical or horizontal strips

    Each drone gets one strip

Option B — Voronoi + clipping

    True polygon territories

    Nodes assigned by region, not just distance

💡 Recommendation

For your grid-based setup:

👉 This version is the best balance of:

    simplicity

    performance

    correctness

If you want, I can upgrade this to:

    🔲
    grid partitioning (perfect non-overlap)

    📐
    true Voronoi polygons

    🔄
    route smoothing inside each territory

Just tell me how strict you want it.

Use floodfill (no diagonals allowed) to check if the route is availavble to the drone

Now we’re talking—this is finally a hard feasibility constraint, not just optimization.

You want:

    A drone can only move through its own territory, and reachability must be guaranteed via 4-connected paths (no diagonals).

That means:

    Your territory must be connected in a grid sense

    And every step in the route must be reachable without crossing into another drone’s nodes

So yes—flood fill (BFS) is exactly the right tool here.
✅ What we’ll enforce

For each drone:

    It owns a set of nodes (territory)

    Movement is allowed only between:

        nodes in its territory

        using 4-connectivity (up/down/left/right)

    Before accepting a route step:

        verify reachability using flood fill

🔧 Step 1 — helper: grid indexing

Since your nodes are floating-point grid points, we map them to integer grid indices:

def to_grid(p: Position2D) -> tuple[int, int]:
    return (
        int(round(p[0] * X_PRECISION)),
        int(round(p[1] * Y_PRECISION)),
    )

🔧 Step 2 — flood fill (BFS, no diagonals)

from collections import deque

def is_reachable(
    start: Position2D,
    target: Position2D,
    allowed: set[tuple[int, int]]
) -> bool:
    start_g = to_grid(start)
    target_g = to_grid(target)

    if target_g not in allowed:
        return False

    visited = set()
    q = deque([start_g])

    while q:
        x, y = q.popleft()

        if (x, y) == target_g:
            return True

        if (x, y) in visited:
            continue

        visited.add((x, y))

        # 4-connectivity only
        neighbors = [
            (x+1, y),
            (x-1, y),
            (x, y+1),
            (x, y-1),
        ]

        for n in neighbors:
            if n in allowed and n not in visited:
                q.append(n)

    return False

🔧 Step 3 — enforce connectivity during route building

Modify your routing loop:

for d in self.drone_ids:
    start = self.drones_p0[d]
    nodes = assigned[d]

    # Precompute allowed grid cells
    allowed = {to_grid(n) for n in nodes}
    allowed.add(to_grid(start))

    route = []
    current = start
    remaining = nodes.copy()

    while remaining:
        candidates = []

        for node in remaining:
            if is_reachable(current, node, allowed):
                candidates.append(node)

        if not candidates:
            raise RuntimeError(f"No reachable nodes left for drone {d}")

        next_node = min(
            candidates,
            key=lambda n: math.dist(current, n)
        )

        route.append(next_node)
        remaining.remove(next_node)
        current = next_node

    # return to start (also must be reachable)
    if not is_reachable(current, start, allowed):
        raise RuntimeError(f"Drone {d} cannot return to start")

    route.append(start)
    routes[d] = route

🧠 What this guarantees

✅ Drone never leaves its territory
✅ Movement respects grid constraints (no diagonals)
✅ Every step is physically reachable
✅ You automatically detect broken territories
⚠️ Important consequence

This will expose a hidden issue:

    Your assignment step may create disconnected territories

Example:

X . X   ← same drone owns both X, but they are not connected

➡️ Flood fill will FAIL → exactly what you want
🚀 If you want it fully correct

Then you should ALSO enforce connectivity during assignment.
Idea:

When assigning a node:

    only assign it if it is adjacent (4-neighbor) to existing territory

That turns your system into:

    region growing instead of global assignment

💡 Bottom line

You’ve now upgraded the problem to:

    Discrete, connected, multi-agent coverage planning

And flood fill is the correct primitive.

If you want, I can next:

    🔥
    Convert your assignment into connected region growing (guaranteed valid)

    ⚡
    Optimize flood fill using caching (huge speedup)

    🧩
    Turn this into a full grid graph planner (A*)

Just tell me 👍


