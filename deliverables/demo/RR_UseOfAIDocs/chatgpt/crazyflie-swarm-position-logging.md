Yeah this function needs a proper cleanup—right now it mixes old state (drone_locations, next_locations) with your new structure (drones_pc, drones_pn, routes) and even has a syntax error (elif without if).

Let’s rebuild it cleanly based on your current architecture.
🧠 What your state means now

From your class:

    drones_pc → current position (list, last element is current)

    drones_pn → next position

    routes → remaining waypoints per drone

👉 So get_step() should:

    Read current position

    Get next waypoint (if any)

    Compute movement

    Update state

    Return structured step info

✅ Clean, correct get_step

def get_step(self):
    step = {}
    max_distance = 0.0

    for drone_id in self.routes.keys():
        route = self.routes[drone_id]

        # Current position (last known)
        current = self.drones_pc[drone_id][-1]

        # Determine next position
        if route:
            next_location = route.pop(0)
        else:
            next_location = current  # stay in place

        # Compute distance
        distance = self._distance(current, next_location)

        # Track max step distance
        if distance > max_distance:
            max_distance = distance

        # Update state
        self.drones_pc[drone_id].append(next_location)
        self.drones_pn[drone_id] = [next_location]

        # Relative movement (useful for control)
        relative_next = (
            next_location[0] - current[0],
            next_location[1] - current[1]
        )

        # Store step info
        step[drone_id] = {
            "current": current,
            "next": next_location,
            "relative": relative_next,
            "distance": distance
        }

    return step, max_distance

🔥 What changed (and why)
1. Removed broken / old variables

self.drone_locations
self.next_locations

👉 These no longer exist in your design.
2. Fixed control flow bug

You had:

elif route:

👉 invalid syntax — now properly handled with if route
3. Proper state update

self.drones_pc[drone_id].append(next_location)
self.drones_pn[drone_id] = [next_location]

👉 Now:

    history is preserved (pc)

    next state is explicit (pn)

4. Structured output (much more usable)

Instead of:

(next_location, next_location, distance, max_distance)

You now get:

{
    "current": (x, y),
    "next": (x, y),
    "relative": (dx, dy),
    "distance": d
}

👉 This is way easier to plug into:

    controllers

    simulators

    Crazyflie commands

⚠️ Important design note

Right now:

route.pop(0)

👉 This is O(n) (slow for long routes)
🚀 Easy optimization

Convert routes to deque:

from collections import deque

self.routes[drone_id] = deque(route)

Then:

next_location = route.popleft()

👉 O(1), much better for real-time stepping
🧠 Optional improvement (smoother swarm motion)

Right now drones may have very different step sizes.

You already compute:

max_distance

👉 You can normalize movement:

scale = 1.0
if max_distance > 0:
    scale = desired_step_size / max_distance

Then scale all relative_next.
🚀 Where this puts you now

You have:

    ✅ optimal initial assignment

    ✅ balanced clustering

    ✅ route optimization

    ✅ step execution engine

👉 This is basically a full multi-drone coverage system

If you want next step, I can help you:

    convert relative_next into Crazyflie velocity commands

    or
    enforce collision avoidance between drones during stepping (this is the next real challenge)


how about a particle swarm optimization algorithm

PSO is tempting here, but it’s not a free upgrade—and in your current setup it’s probably the wrong first tool.

Let me explain why, then show you how to use it correctly if you still want it.
🧠 Reality check: PSO vs your current approach

You already have:

    Hungarian assignment → optimal start positions

    Balanced clustering → good workload distribution

    Nearest neighbor + 2-opt → solid routing heuristic

👉 That’s already a strong classical pipeline.
❌ Where PSO is not a good fit

PSO struggles with:

    combinatorial problems (like TSP / routing order)

    discrete assignments (which node belongs to which drone)

Your problem is:

    “assign + order points”

👉 That’s discrete, while PSO is fundamentally continuous.
✅ Where PSO can help (usefully)

PSO is useful if you reformulate parts of your problem:
1. Optimize cluster centers

Instead of assigning nodes directly, PSO finds:

    ideal “centroids” for each drone

Then:

    assign nodes → nearest centroid

👉 This replaces your greedy clustering + swap step
2. Optimize drone waypoints (continuous paths)

Instead of:

    discrete grid traversal

You optimize:

    smooth trajectories minimizing:

        path length

        overlap

        collisions

3. Global refinement

Use your current solution as a starting point, then:

👉 PSO tries to improve total cost
🚀 Practical PSO integration (recommended approach)

Don’t replace everything. Add PSO as a refinement layer.
🔧 Example: PSO for cluster optimization
Representation

Each particle = cluster centers:

particle = np.array([
    [x1, y1],  # drone 1 center
    [x2, y2],  # drone 2 center
    ...
])

Cost function (this is key)

def cost(centers, nodes):
    # Assign each node to closest center
    dists = np.linalg.norm(nodes[:, None, :] - centers[None, :, :], axis=2)
    assignment = np.argmin(dists, axis=1)

    total = 0
    for i in range(len(centers)):
        cluster = nodes[assignment == i]
        if len(cluster) == 0:
            continue

        # compactness
        total += np.sum(np.linalg.norm(cluster - centers[i], axis=1))

    return total

Minimal PSO loop

def pso_optimize(nodes, k, iterations=50, swarm_size=30):
    dim = 2 * k

    # Initialize particles
    particles = np.random.rand(swarm_size, k, 2)
    velocities = np.zeros_like(particles)

    personal_best = particles.copy()
    personal_best_scores = np.array([cost(p, nodes) for p in particles])

    global_best = personal_best[np.argmin(personal_best_scores)]

    for _ in range(iterations):
        for i in range(swarm_size):
            r1, r2 = np.random.rand(), np.random.rand()

            velocities[i] = (
                0.5 * velocities[i]
                + 1.5 * r1 * (personal_best[i] - particles[i])
                + 1.5 * r2 * (global_best - particles[i])
            )

            particles[i] += velocities[i]

            score = cost(particles[i], nodes)

            if score < personal_best_scores[i]:
                personal_best[i] = particles[i]
                personal_best_scores[i] = score

        global_best = personal_best[np.argmin(personal_best_scores)]

    return global_best

Then integrate into your pipeline

centers = pso_optimize(self.unsearched_nodes, k)

# Assign nodes to clusters
dists = np.linalg.norm(
    self.unsearched_nodes[:, None, :] - centers[None, :, :],
    axis=2
)

assignment = np.argmin(dists, axis=1)

Then continue with:

    route building

    2-opt

⚠️ Honest tradeoffs
Pros

    Can escape local minima

    More flexible objective (you can add penalties)

    Works well with NumPy

Cons

    Slower than your current method

    No guarantee of optimality

    Needs tuning (weights, iterations)

🧠 My recommendation (based on your code)

👉 Don’t replace your current system with PSO.

Instead:
Best hybrid strategy

    Keep:

        Hungarian assignment ✅

        Your NumPy clustering ✅

    Add PSO ONLY for:

        refining cluster centers

        or balancing uneven workloads

🔥 If you want something even better than PSO

For your exact problem:

    K-means (with constraints) → faster, simpler

    K-medoids → better for discrete nodes

    OR-Tools VRP solver → industry-grade routing

👉 PSO is cool, but not the most efficient tool here.
🚀 Bottom line

    Your current system = already strong

    NumPy = essential (you’re using it right)

    PSO = optional refinement tool, not a replacement

If you want, I can:

    plug PSO directly into your NavigationService cleanly

    or
    show a constraint-aware k-means version that fits your code better (and is faster than PSO)


self.drones_p0 = drones_p0
        self.drones_pc = drones_p0
        self.drones_pn = drones_p0

do I need deepcopy here?

Yes — in your case you very likely need a deep copy, otherwise you’ll run into subtle bugs.
🧠 What’s happening right now

self.drones_p0 = drones_p0
self.drones_pc = drones_p0
self.drones_pn = drones_p0

👉 All three variables point to the exact same object in memory

So this:

self.drones_pc[drone_id].append(new_point)

will also modify:

self.drones_p0
self.drones_pn

⚠️ Why this is a problem in your design

Your variables are meant to represent different states:

    p0 → initial assignment

    pc → current position (changes over time)

    pn → next position

👉 These should not mutate together
🔥 Extra subtle issue (important)

Your structure is:

dict[str, list[tuple]]

So even this:

self.drones_pc = drones_p0.copy()

❌ is NOT enough

Because:

    dict is copied

    but lists inside are still shared

✅ Correct solution

Use deepcopy:

import copy

self.drones_p0 = copy.deepcopy(drones_p0)
self.drones_pc = copy.deepcopy(drones_p0)
self.drones_pn = copy.deepcopy(drones_p0)

🧠 When shallow copy would be enough

If your structure was:

dict[str, tuple]

Then:

.copy()

would be fine (tuples are immutable)
🚀 Better design (recommended)

You don’t actually need lists for pc and pn.

Instead:

self.drones_p0: dict[str, tuple]
self.drones_pc: dict[str, tuple]
self.drones_pn: dict[str, tuple]

Then:

self.drones_p0 = drones_p0
self.drones_pc = drones_p0.copy()
self.drones_pn = drones_p0.copy()

👉 No deepcopy needed
👉 Cleaner
👉 Less memory
👉 Less bug-prone
🎯 My recommendation
Option A (minimal change)

import copy

self.drones_p0 = copy.deepcopy(drones_p0)
self.drones_pc = copy.deepcopy(drones_p0)
self.drones_pn = copy.deepcopy(drones_p0)

Option B (better design)

Switch to:

dict[str, tuple[float, float]]

and avoid lists entirely unless you really need history
🧠 Rule of thumb

    Mutable inside mutable → deepcopy

    Immutable values → shallow copy is fine

If you want, I can help you clean up your whole state model—right now you’re very close to something that’s both simpler and faster.


