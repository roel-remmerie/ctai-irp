delta_pn_pnminus1 is pretty clunky, yeah. You can make it both shorter and clearer.

If it specifically means pₙ − pₙ₋₁, the cleanest minimal options are:

    dp → very common shorthand (delta position)

    dp_n → if you want to keep the index explicit

    d_p → slightly more readable than dp

    Δp → best mathematically (if your language allows Unicode)

If you want to be just a bit more explicit without blowing up length:

    dp_prev

    dp_back

Honestly, dp is the sweet spot if the context is clear—it’s what most people would expect.

this is my code

import random
import math
from itertools import combinations

# search nodes per meter along <axis>

X_PRECISION = 4 # the x axis
Y_PRECISION = 4 # the y axis

# distance a drone must keep between itself and the <cardinal direction> positioning nodes along <axis> (in meters)

X_MIN = 0.5 # western, x axis
X_MAX = 0.5 # eastern, x axis
Y_MIN = 0.5 # southern, y axis
Y_MAX = 0.5 # northern, y axis

# most <directions> positioning node location along the (x,y,z) axes respectively

NODE_0 = (0,0,0) # most western, southern and lowest
NODE_6 = (4.95, 3.15, 2.5) # most eastern, northern and highest

I want to read node 0 and 6 not hardcoded but from this yaml file

0:
  x: 0.0
  y: 0.0
  z: 0.0
1:
  x: 0.0
  y: 3.15
  z: 2.5
2:
  x: 4.95
  y: 3.15
  z: 0.0
3:
  x: 4.95
  y: 0.0
  z: 2.5
4:
  x: 0.0
  y: 0.0
  z: 2.5
5:
  x: 0.0
  y: 3.15
  z: 0.0
6:
  x: 4.95
  y: 3.15
  z: 2.5
7:
  x: 4.95
  y: 0.0
  z: 0.0

You don’t want those coordinates hardcoded—good call. YAML is perfect for this.

First, install a YAML parser if you don’t have one:

pip install pyyaml

Then you can load your file and extract nodes like this:

import yaml

# load YAML file
with open("nodes.yaml", "r") as f:
    nodes = yaml.safe_load(f)

# access node 0 and node 6
node_0 = nodes[0]
node_6 = nodes[6]

# convert to tuples if needed
NODE_0 = (node_0["x"], node_0["y"], node_0["z"])
NODE_6 = (node_6["x"], node_6["y"], node_6["z"])

print(NODE_0)
print(NODE_6)

One subtle gotcha

YAML keys like 0: are usually parsed as integers, so nodes[0] works.
If you ever quote them ("0":), then you'd need nodes["0"].
If you want it cleaner/shorter

You can avoid repetition:

def get_node(nodes, i):
    n = nodes[i]
    return (n["x"], n["y"], n["z"])

NODE_0 = get_node(nodes, 0)
NODE_6 = get_node(nodes, 6)

If you're going to use many nodes, it's even better to convert everything at once:

nodes = {
    i: (n["x"], n["y"], n["z"])
    for i, n in nodes.items()
}

Then:

NODE_0 = nodes[0]
NODE_6 = nodes[6]

That keeps the rest of your code clean and fast.

what is the difference between math.dist and math.hypot

They’re related, but not interchangeable—each has a slightly different purpose.
🔹 math.hypot

math.hypot computes the length of a vector from the origin:

math.hypot(x, y)        # √(x² + y²)
math.hypot(x, y, z)     # √(x² + y² + z²)

So it assumes you're measuring from (0, 0, …) to a point.

Example:

math.hypot(3, 4)  # 5.0

🔹 math.dist

math.dist computes the distance between two points:

math.dist(p, q)

Example:

math.dist((1, 2), (4, 6))  # 5.0

🔑 Key difference

    math.hypot → distance from the origin

    math.dist → distance between two arbitrary points

🔄 How they relate

You can replicate math.dist using math.hypot:

math.dist(p, q)
# is equivalent to:
math.hypot(*(a - b for a, b in zip(p, q)))

👍 When to use which

    Use math.dist when working with coordinates (like your nodes)

    Use math.hypot when you already have differences or components

💡 In your case (nodes)

Instead of:

dx = x2 - x1
dy = y2 - y1
dz = z2 - z1
d = math.hypot(dx, dy, dz)

You can simply do:

d = math.dist(NODE_0, NODE_6)

Cleaner and harder to mess up.


