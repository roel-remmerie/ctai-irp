That “active ↔ inactive” flickering in the Crazyflie Loco Positioning System (LPS) almost always means the Crazyflie is intermittently losing reliable UWB distance measurements from one or more anchors (nodes), not that the anchors are actually powering on/off.

Here are the most common causes and what to check, in order of likelihood:
1. Poor UWB signal quality (most common)

If packets are noisy or getting dropped, the Crazyflie will temporarily ignore an anchor → it appears inactive.

    Make sure anchors are not too close together (avoid clustering)

    Avoid placing them near:

        metal surfaces

        large electronics / WiFi routers

        reflective walls (glass, metal frames)

    Try to keep anchors at same height or well-calibrated geometry

2. Inconsistent anchor configuration (very common)

If one anchor is misconfigured or unstable, the whole system can appear to “flip”.

Check:

    All anchors have unique IDs

    All are in the same LPS mode (TWR or TDoA) depending on your setup

    Firmware is consistent across anchors

3. Power issues on anchors

Intermittent power causes exactly this symptom.

    USB hubs (especially unpowered ones) often cause this

    Try:

        different USB ports

        powered USB hub

        different cables

4. Radio interference / channel issues

UWB is usually robust, but interference or bad channel settings can cause packet loss.

    Try changing LPS channel (if using TDoA)

    Move away from:

        WiFi routers (2.4 GHz overlap in harmonics sometimes matters)

        Bluetooth-heavy environments

5. Firmware mismatch

If Crazyflie firmware and anchor firmware don’t match:

    Update both:

        Crazyflie firmware

        LPS anchor firmware

6. Anchor visibility geometry problem

If you are near the edge of the setup:

    Crazyflie might only “see” 2–3 anchors intermittently

    That causes unstable filtering → nodes appear to drop in/out

Try flying:

    more centrally inside the anchor layout

    or increase anchor coverage

7. Client interpretation (false “inactive”)

Sometimes the Crazyflie Client UI shows anchors as inactive due to:

    temporary packet loss

    filtering thresholds in the estimator

Check if:

    position still updates smoothly even when UI toggles
    → then it’s mostly a UI/status issue, not real dropout

Quick diagnostic test

Try this:

    Place Crazyflie stationary on the ground

    Watch anchor status in client

    If they still toggle → it’s signal / power / config

    If stable when stationary but unstable in flight → it’s geometry or signal occlusion

If you want, I can pinpoint it faster

Tell me:

    Are you using TWR or TDoA mode?

    How many anchors?

    Are they USB-powered or battery?

    Does position itself also jump, or only the “active/inactive” status?

With that, I can narrow it down to a very specific cause quickly.

[[-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]]
5
4
[[-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1  0 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]
 [-1 -1 -1 -1 -1 -1 -1]]
5
2
Traceback (most recent call last):
  File "/home/roel/CTAI/IRP/ctai-irp/src/main.py", line 61, in <module>
    swarm.update_swarm(button.text)
  File "/home/roel/CTAI/IRP/ctai-irp/src/services/swarm.py", line 34, in update_swarm
    self._scan_drones()
  File "/home/roel/CTAI/IRP/ctai-irp/src/services/swarm.py", line 54, in _scan_drones
    self.navigation.build_routes()
  File "/home/roel/CTAI/IRP/ctai-irp/src/services/navigation.py", line 138, in build_routes
    cmsg = CMSG(SEARCH_SHAPE_XY, origins_xy, D_MANHATTEN)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/roel/CTAI/IRP/ctai-irp/src/utils/algorithm.py", line 74, in __init__
    score = self.get_score(frontier, c_global, c_self)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/roel/CTAI/IRP/ctai-irp/src/utils/algorithm.py", line 174, in get_score
    if not self.occupied[ny, nx]:
           ~~~~~~~~~~~~~^^^^^^^^
IndexError: index 7 is out of bounds for axis 1 with size 7

This one’s much more concrete than the Crazyflie issue — you’ve got a classic grid boundary bug.
🔥 What the error actually says

IndexError: index 7 is out of bounds for axis 1 with size 7

That means:

    Your grid has size 7 columns → valid indices: 0–6

    Your code tried to access index 7 → 💥 crash

From the line:

if not self.occupied[ny, nx]:

👉 The problem is nx == 7 (or possibly ny == 7)
🧠 Why it’s happening

Somewhere before this, you're likely doing neighbor expansion like:

neighbors = [
    (x+1, y),
    (x-1, y),
    (x, y+1),
    (x, y-1)
]

But you're not checking boundaries before indexing.

So when:

    x == 6 → x+1 == 7 → out of bounds

    OR same for y

✅ The fix (you need this check)

Before accessing the grid, ALWAYS validate indices:

height, width = self.occupied.shape

if 0 <= nx < width and 0 <= ny < height:
    if not self.occupied[ny, nx]:
        ...

⚠️ Subtle but important detail

Notice:

self.occupied[ny, nx]

That means:

    ny → row (height)

    nx → column (width)

So:

0 <= nx < width
0 <= ny < height

NOT the other way around.
🧪 Why your printed grid hints at this

You showed:

[[-1 -1 -1 -1 -1 -1 -1]
 ...
]

That’s:

    8 rows

    7 columns

So:

shape = (8, 7)

Meaning:

    ny ∈ [0,7] ✅

    nx ∈ [0,6] ✅

But your code hit:

axis 1 (columns) size 7 → index 7 invalid

So it’s definitely nx = 7.
💡 Bonus: safer pattern

Instead of checking everywhere manually, you can centralize it:

def in_bounds(x, y, grid):
    h, w = grid.shape
    return 0 <= x < w and 0 <= y < h

Then:

if in_bounds(nx, ny, self.occupied):
    if not self.occupied[ny, nx]:
        ...

🚀 Likely root cause in your algorithm

Given this is inside:

get_score → frontier exploration

You’re probably:

    Expanding frontiers

    Not clipping edges

    Letting search “spill outside” the map

If you want a sharper fix

Paste your get_score function and I’ll:

    pinpoint exactly where it leaks

    suggest a clean, robust rewrite (especially useful for swarm/grid search)


def build_routes(self) -> None:
        if not self.drones_p0:
            raise ValueError("Drone starting positions (p0) not initialized")

        origins_xy = []
        drone_index_map = {}

        for i, drone_id in enumerate(self.drone_ids):
            pos = np.array(self.drones_p0[drone_id])

            # find nearest node index
            idx = np.argmin(np.linalg.norm(self.search_area - pos, axis=1))
            origin_y, origin_x = divmod(idx, NX_SEARCH_NODES)

            origins_xy.append((origin_x, origin_y))
            drone_index_map[i] = drone_id

        # --- Step 3: run CMSG directly on grid ---
        cmsg = CMSG(SEARCH_SHAPE_XY, origins_xy, D_MANHATTEN)
        labels = cmsg.labels

        print(labels)

        # --- Step 4: assign nodes using flat index ---
        assigned = {drone_id: [] for drone_id in self.drone_ids}

        print(self.search_area)

        for idx, node in enumerate(self.search_area):
            node_x, node_y = node

            print(node)

            xi = int(round(node_x * X_PRECISION))
            yi = int(round(node_y * Y_PRECISION))

            print(xi)
            print(yi)

            label = labels[yi, xi]

            if label != -1:
                d = drone_index_map[label]
                assigned[d].append(node)

        # --- Step 5: route inside territory (unchanged logic) ---
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

            route.append(start)
            routes[d] = route

        self.routes = routes

can you explain the code

You’ve got a nice pipeline here—this function is basically:
“take drone start positions → map them onto a grid → partition the grid → assign nodes → build simple routes.”
Let’s walk through it clearly so you see what each part is doing and where things can go wrong.
🧭 1. Validate input

if not self.drones_p0:
    raise ValueError("Drone starting positions (p0) not initialized")

    self.drones_p0 = dict like {drone_id: (x, y)}

    If it’s empty → stop immediately

📍 2. Map drones to grid indices

origins_xy = []
drone_index_map = {}

Loop:

for i, drone_id in enumerate(self.drone_ids):
    pos = np.array(self.drones_p0[drone_id])

    pos = real-world (x, y) position of drone

Find closest grid node

idx = np.argmin(np.linalg.norm(self.search_area - pos, axis=1))

    self.search_area = list of all grid points (flattened)

    Computes distance from drone → all nodes

    Picks closest one

Convert flat index → grid coords

origin_y, origin_x = divmod(idx, NX_SEARCH_NODES)

    Converts 1D index → 2D grid

    Important:

        NX_SEARCH_NODES = number of columns

        So:

            origin_y = row

            origin_x = column

Store results

origins_xy.append((origin_x, origin_y))
drone_index_map[i] = drone_id

    origins_xy → passed into your CMSG algorithm

    drone_index_map → translates CMSG labels back to drone IDs

🧠 3. Run CMSG (territory partitioning)

cmsg = CMSG(SEARCH_SHAPE_XY, origins_xy, D_MANHATTEN)
labels = cmsg.labels

This likely:

    Expands regions from each drone origin

    Assigns each grid cell to a drone

    Produces:

labels[y, x] = drone_index OR -1

🧾 4. Assign nodes to drones

assigned = {drone_id: [] for drone_id in self.drone_ids}

Loop over all nodes

for idx, node in enumerate(self.search_area):
    node_x, node_y = node

⚠️ Important:
Here node is real-world coordinates, not grid indices.
Convert to grid indices

xi = int(round(node_x * X_PRECISION))
yi = int(round(node_y * Y_PRECISION))

    You scale float → integer grid index

    This is where your bug likely comes from

Lookup label

label = labels[yi, xi]

    Find which drone owns this cell

⚠️ CRITICAL PROBLEM AREA

    No bounds check → crash if:

        xi == width

        yi == height

Assign node to drone

if label != -1:
    d = drone_index_map[label]
    assigned[d].append(node)

🚁 5. Build routes (greedy TSP-style)

routes = {}

For each drone:

start = self.drones_p0[d]
nodes = assigned[d]

Greedy nearest-neighbor path

while remaining:
    next_node = min(
        remaining,
        key=lambda n: math.dist(current, n)
    )

    Always go to closest next node

    Simple but not optimal (good enough usually)

Build route

route.append(next_node)
remaining.remove(next_node)
current = next_node

Return to start

route.append(start)

Save result

routes[d] = route
self.routes = routes

⚠️ Your actual bug (confirmed)

This line:

label = labels[yi, xi]

Combined with:

xi = int(round(node_x * X_PRECISION))
yi = int(round(node_y * Y_PRECISION))

👉 You can easily get:

    xi == width

    yi == height

Because rounding pushes edge values out of bounds
✅ Fix (do this)

Add bounds checking:

h, w = labels.shape

if 0 <= xi < w and 0 <= yi < h:
    label = labels[yi, xi]
else:
    continue  # skip invalid node

💡 Even better fix (recommended)

Instead of recomputing indices from floats:

👉 You already have idx from earlier
👉 Use consistent indexing

Replace:

xi = int(round(node_x * X_PRECISION))
yi = int(round(node_y * Y_PRECISION))

With:

yi, xi = divmod(idx, NX_SEARCH_NODES)

✔️ This guarantees:

    No rounding errors

    Perfect alignment with labels

🧠 Big picture

Your pipeline is:

    Map drones → grid

    Partition grid (CMSG)

    Map real nodes → grid indices ⚠️ (bug here)

    Assign nodes

    Build greedy routes

🚀 If you want next step improvements

I can help you:

    Fix the indexing cleanly across the whole pipeline

    Improve routing (your current one is O(n²) greedy)

    Visualize partitions (super useful for debugging swarm behavior)

Just say 👍


