<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Make a python game, black background I need a drone sprite and a tile sprite, there is a button to send out the drone and then recall the drone once pressed, when the button is pressed the drone flies from a random point on the tiles and each move is in a random direction over the tiles, if the drone touches a tile it turns from green to yellow, some tiles turn red this is predetermined from the generation of the game

Here’s a complete, self‑contained Python game using `pygame` that matches your request.
You can run this in any environment where you have `pygame` installed (on your system, VS Code, Replit, etc.).[^1_1][^1_2]

***

### Full code

```python
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drone Tile Game")
clock = pygame.time.Clock()
FPS = 30

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
RED = (220, 40, 40)
GRAY = (80, 80, 80)
BUTTON_BG = (180, 180, 180)

# Tile grid
TILE_SIZE = 40
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = (HEIGHT - 80) // TILE_SIZE

# Tile class for simple sprites
class Tile:
    def __init__(self, x, y, is_red=False):
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.is_red = is_red
        self.touched = False
        self.color = RED if is_red else GREEN

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, GRAY, self.rect, 1)  # border

# Create tile grid (some tiles are red by default)
tiles = []
for y in range(GRID_HEIGHT):
    row = []
    for x in range(GRID_WIDTH):
        is_red = random.random() < 0.15  # about 15% red tiles
        row.append(Tile(x, y, is_red=is_red))
    tiles.append(row)

# Drone “sprite” (circle for simplicity)
DRONE_RADIUS = 8

class Drone:
    def __init__(self):
        self.reset()

    def reset(self):
        self.active = False
        self.x = 0
        self.y = 0
        self.vx = 1
        self.vy = 1
        self.target_tile = None
        self.move_count = 0

    def launch(self):
        # Random starting tile
        start_y = random.randint(0, GRID_HEIGHT - 1)
        start_x = random.randint(0, GRID_WIDTH - 1)
        t = tiles[start_y][start_x]
        self.x = t.rect.centerx
        self.y = t.rect.centery
        self.move_count = 0
        self.active = True
        self.pick_new_target()

    def pick_new_target(self):
        if not self.active:
            return
        # Pick a random direction: left, right, up, down
        dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        new_x = int(self.x // TILE_SIZE) + dx
        new_y = int(self.y // TILE_SIZE) + dy
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            self.target_tile = tiles[new_y][new_x]
        else:
            # Stay in place if out of bounds
            self.target_tile = tiles[int(self.y // TILE_SIZE)][int(self.x // TILE_SIZE)]

    def update(self):
        if not self.active or self.target_tile is None:
            return

        tx = self.target_tile.rect.centerx
        ty = self.target_tile.rect.centery

        # Move toward the target tile
        if abs(self.x - tx) > 1:
            self.x += 1 if tx > self.x else -1
        if abs(self.y - ty) > 1:
            self.y += 1 if ty > self.y else -1

        # Snap to target and pick next move
        if abs(self.x - tx) <= 1 and abs(self.y - ty) <= 1:
            self.x = tx
            self.y = ty
            self.move_count += 1
            # Mark tile as touched (turns yellow, unless it’s red)
            if not self.target_tile.touched:
                self.target_tile.touched = True
                if not self.target_tile.is_red:
                    self.target_tile.color = YELLOW
            # Next move
            self.pick_new_target()

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, (0, 0, 255), (int(self.x), int(self.y)), DRONE_RADIUS)

# Drone sprite instance
drone = Drone()

# Button
button = pygame.Rect(10, HEIGHT - 70, 150, 50)
font = pygame.font.SysFont("Arial", 20)
button_text = font.render("Launch/Recall", True, (0, 0, 0))

# Main loop
running = True
while running:
    screen.fill(BLACK)

    # Draw tiles
    for row in tiles:
        for tile in row:
            tile.draw(screen)

    # Draw running‑text info
    status_text = "Drone: " + ("active" if drone.active else "idle")
    status = font.render(status_text, True, (200, 200, 200))
    screen.blit(status, (WIDTH - 300, HEIGHT - 70))

    # Draw button
    pygame.draw.rect(screen, BUTTON_BG, button)
    screen.blit(button_text, (button.x + 12, button.y + 15))

    # Draw drone
    drone.draw(screen)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                if drone.active:
                    drone.reset()
                else:
                    drone.launch()

    # Update drone
    drone.update()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
```


***

### What this does

- **Black background** and a grid of tiles (green by default).[^1_2]
- Some tiles are **predetermined red** when the game starts.
- The **Drone** is a small blue circle that:
    - Starts at a **random tile** when you press the button.
    - Moves in **random directions** over the tiles (one move per step).
    - When it lands on a tile, that tile turns **yellow** (unless it is already red).
- The **same button** toggles between:
    - “Launch” the drone (if it’s idle).
    - “Recall” the drone (if it’s flying → stops and disappears until next launch).

If you tell me whether you want an actual image sprite (PNG) for the drone or stay with the simple circle, I can adapt the code to load a sprite instead.
<span style="display:none">[^1_10][^1_3][^1_4][^1_5][^1_6][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://matlabsimulation.com/drone-simulator-python/

[^1_2]: https://thepythoncode.com/article/platformer-game-with-pygame-in-python?ya_src=serp300

[^1_3]: https://www.geeksforgeeks.org/python/spiral-sprint-game-in-python-using-pygame/

[^1_4]: https://www.youtube.com/watch?v=-Sq_qn_Ea9c

[^1_5]: https://www.reddit.com/r/Python/comments/db95f4/i_made_a_short_game_for_a_game_jam_with_python/

[^1_6]: https://stackoverflow.com/questions/74672476/making-a-sliding-puzzle-game-using-turtle-not-tkinter-or-pygame

[^1_7]: https://github.com/Erikx3/2D_Pygame_Drone_Simulation

[^1_8]: https://www.youtube.com/watch?v=Ongc4EVqRjo

[^1_9]: https://realpython.com/build-python-turtle-game-space-invaders-clone/

[^1_10]: https://www.pygame.org/project-Drones+Fight-1749-.html


---

# all tiles are green at the start it lights up red or yellow, the drone can go a lot faster but always starts at the center bottom

Here’s an updated version of the Python/Pygame game that matches your new requirements:

- All tiles start **green**.
- When the drone passes over a tile, it turns **yellow**;
- Some tiles are **predetermined to turn red** after a random touch (or you can set a fixed pattern).
- The drone now **starts at the center‑bottom tile** and moves **much faster**.

***

### Updated code (copy + run)

```python
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drone Tile Game")
clock = pygame.time.Clock()
FPS = 60  # smoother animation

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
RED = (220, 40, 40)
GRAY = (80, 80, 80)
BUTTON_BG = (180, 180, 180)

# Tile grid
TILE_SIZE = 40
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = (HEIGHT - 100) // TILE_SIZE  # extra space for UI

# Tile class
class Tile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.touched = 0           # 0: green, 1: yellow, 2: red
        self.color = GREEN

    def update_color(self):
        if self.touched == 0:
            self.color = GREEN
        elif self.touched == 1:
            self.color = YELLOW
        elif self.touched == 2:
            self.color = RED

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, GRAY, self.rect, 1)  # border

# Create tile grid (all green at start)
tiles = []
for y in range(GRID_HEIGHT):
    row = []
    for x in range(GRID_WIDTH):
        row.append(Tile(x, y))
    tiles.append(row)

# List of positions that should turn red after being touched
# Format: (x, y) coordinates in the grid
RED_TILES = [
    (GRID_WIDTH // 2 - 3, GRID_HEIGHT // 2),
    (GRID_WIDTH // 2 + 2, GRID_HEIGHT // 2 + 1),
    (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 3),
    (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2 - 2),
]
# Mark these tiles internally (for logic); they start green
for x, y in RED_TILES:
    if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
        tiles[y][x].red_candidate = True
    else:
        tiles[y][x].red_candidate = False

# Center‑bottom tile (start position)
START_X = GRID_WIDTH // 2
START_Y = GRID_HEIGHT - 1

# Drone “sprite” (fast circle)
DRONE_RADIUS = 8
DRONE_SPEED = 4  # pixels per frame

class Drone:
    def __init__(self):
        self.reset()

    def reset(self):
        self.active = False
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.target_tile = None
        self.move_count = 0

    def launch(self):
        # Start at center bottom tile
        start_t = tiles[START_Y][START_X]
        self.x = start_t.rect.centerx
        self.y = start_t.rect.centery
        self.active = True
        self.pick_new_target()

    def pick_new_target(self):
        if not self.active:
            return
        # Random direction: left, right, up, down
        dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        new_x = int(self.x // TILE_SIZE) + dx
        new_y = int(self.y // TILE_SIZE) + dy
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            self.target_tile = tiles[new_y][new_x]
        else:
            # If going out of bounds, stay in the same tile
            self.target_tile = tiles[int(self.y // TILE_SIZE)][int(self.x // TILE_SIZE)]

    def update(self):
        if not self.active or self.target_tile is None:
            return

        tx = self.target_tile.rect.centerx
        ty = self.target_tile.rect.centery

        # Move toward target faster
        if self.x < tx:
            self.x += DRONE_SPEED
        elif self.x > tx:
            self.x -= DRONE_SPEED
        if self.y < ty:
            self.y += DRONE_SPEED
        elif self.y > ty:
            self.y -= DRONE_SPEED

        # Snap to target and handle tile change
        if (abs(self.x - tx) <= DRONE_SPEED and
            abs(self.y - ty) <= DRONE_SPEED):

            self.x = tx
            self.y = ty
            self.move_count += 1

            # Mark tile as touched (yellow)
            if not hasattr(self.target_tile, "red_candidate"):
                self.target_tile.red_candidate = False

            # If tile is touched for the first time → yellow
            if self.target_tile.touched == 0:
                self.target_tile.touched = 1
                self.target_tile.update_color()

            # Check if this tile should ever turn red
            if self.target_tile.red_candidate:
                # After a few passes, turn it red (simple rule)
                if self.move_count % 5 == 0:  # roughly every 5 passes, turn red
                    self.target_tile.touched = 2
                    self.target_tile.update_color()

            # Next move
            self.pick_new_target()

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, (0, 0, 255), (int(self.x), int(self.y)), DRONE_RADIUS)

# Drone sprite
drone = Drone()

# Button
button = pygame.Rect(10, HEIGHT - 70, 150, 50)
font = pygame.font.SysFont("Arial", 20)
button_text = font.render("Launch/Recall", True, (0, 0, 0))

# Main loop
running = True
while running:
    screen.fill(BLACK)

    # Draw tiles
    for row in tiles:
        for tile in row:
            tile.draw(screen)

    # Draw UI text
    status_text = "Drone: " + ("active" if drone.active else "idle")
    status = font.render(status_text, True, (200, 200, 200))
    screen.blit(status, (WIDTH - 300, HEIGHT - 70))

    # Draw button
    pygame.draw.rect(screen, BUTTON_BG, button)
    screen.blit(button_text, (button.x + 12, button.y + 15))

    # Draw drone
    drone.draw(screen)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                if drone.active:
                    drone.reset()
                else:
                    drone.launch()

    # Update drone
    drone.update()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
```


***

### What this version does

- **All tiles green at start**, then turn **yellow when touched**, and some set tiles eventually turn **red** after a few passes.
- Drone **always starts at the center‑bottom tile** of the grid.
- **Much faster** movement (`DRONE_SPEED = 4`) and smoother frame rate (`FPS = 60`).

If you want, I can next show you how to load an actual **PNG sprite for the drone** instead of the blue circle.

---

# can I replace the simulated drone with a real crazyflie drone, the blue dot must mimmic the movements of the crazyflie drone

Yes, you *can* replace the simulated blue‑dot drone with a **real Crazyflie** and have the on‑screen dot mimic its actual movement over the tile grid.[^3_1][^3_2]
Here’s how to think about it and how to adapt your code.

***

### 1. Big‑picture idea

- You keep your **same Pygame tile grid** (black background, green tiles, the button, etc.).
- Instead of your own random “drone logic,” you:
    - Connect to the **real Crazyflie** via the `cflib` Python library.[^3_2][^3_1]
    - Read the drone’s **real‑time position** (x, y, maybe z, optionally from a motion‑capture system or on‑board pose estimation).[^3_3][^3_4]
    - Map that position to your **tile grid** and move the **blue dot** to that tile.
    - When the Crazyflie flies over a tile, you mark that tile as **yellow then possibly red**, just like before.

***

### 2. What you need set up

Before you can run this, you need:

- Crazyflie (e.g., Crazyflie 2.1 or 3) + radio dongle (or UDP/WiFi if using a LiteWing‑style Crazyflie).[^3_5][^3_6]
- Installed **`crazyflie-lib-python`** (often called `cflib`):

```bash
pip install cflib
```


[^3_1][^3_2]

- (Optional but very useful) A way to get the Crazyflie’s **position**:
    - Motion‑capture system (e.g., OptiTrack + QTM) and a bridge to send poses to the drone.[^3_4]
    - Or, for simple demos, you can fake position from logs or use a simple coordinate‑mapper.[^3_3]

***

### 3. How to adapt your current code

You **keep your existing Pygame loop** and:

1. **Add a Crazyflie‑reading thread** that:
    - Connects to the Crazyflie.[^3_2][^3_5]
    - Periodically reads its **(x, y)** position (either from onboard logs or from an external tracker).
2. **Add a mapping function** from Crazyflie coordinates to your tile grid:
```python
# Example: map Crazyflie world position (in meters) to your screen tile
def world_to_tile_pos(x_world, y_world):
    # Example: your grid spans roughly [-1m, +1m] in x and y
    x_min, x_max = -1.2, 1.2
    y_min, y_max = -1.2, 1.2
    w = x_max - x_min
    h = y_max - y_min

    nx = max(0, min(GRID_WIDTH - 1, int((x_world - x_min) / w * GRID_WIDTH)))
    ny = max(0, min(GRID_HEIGHT - 1, int((y_world - y_min) / h * GRID_HEIGHT)))
    t = tiles[ny][nx]
    return t.rect.centerx, t.rect.centery
```

3. **Update the drone “dot”** in your Pygame loop from the real position:
```python
# In your Drone class or as a global variable
drone_dot_x = 0
drone_dot_y = 0
drone_lock = threading.Lock()

# In the Crazyflie‑reading thread:
def crazyflie_position_callback(x, y, z):
    global drone_dot_x, drone_dot_y
    with drone_lock:
        drone_dot_x, drone_dot_y = world_to_tile_pos(x, y)

# In your Pygame loop instead of your old simulated drone:
#   - Do not call drone.update()
#   - Draw the dot at the Crazyflie’s latest position:
def draw_drone_dot(surface):
    with drone_lock:
        x, y = drone_dot_x, drone_dot_y
    pygame.draw.circle(surface, (0, 0, 255), (int(x), int(y)), DRONE_RADIUS)
```

4. **Touching tiles still works the same way**:

- Every frame, convert the Crazyflie position to a tile, and mark that tile as touched (green → yellow → red, using your earlier logic).

***

### 4. Very simple integration sketch

Keeping your **existing code structure**, you would:

1. Start a background thread that:
    - Opens the Crazyflie link.[^3_2]
    - Subscribes to a “position” log (e.g., `kalman.stateX`, `kalman.stateY`).[^3_2]
    - Calls `crazyflie_position_callback(x, y, z)` whenever new data arrives.
2. In your Pygame tick:
    - Use the latest `drone_dot_x, drone_dot_y` from the shared variable.
    - Draw the blue dot there.
    - Use the same tile‑touched logic as before.

If you tell me whether you:

- Are using **radio** or **WiFi** (LiteWing), and
- Already have **position data** (e.g., from a tracker or logs),

I can give you a concrete **minimal integration snippet** that plugs directly into the code you already have.
<span style="display:none">[^3_10][^3_7][^3_8][^3_9]</span>

<div align="center">⁂</div>

[^3_1]: https://github.com/bitcraze/crazyflie-lib-python

[^3_2]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/python_api/

[^3_3]: https://www.bitcraze.io/category/crazyflie/simulation/

[^3_4]: https://www.baytas.net/blog/crazyflie

[^3_5]: https://circuitdigest.com/microcontroller-projects/how-to-program-litewing-drone-using-python-with-crazyflie-cflib-python-sdk

[^3_6]: https://www.youtube.com/watch?v=J1Y-7AttoFY

[^3_7]: https://www.bitcraze.io/2024/04/python-bindings-for-the-crazyflie-firmware/

[^3_8]: https://github.com/mikecentral/Crazyflie-Drone

[^3_9]: https://docs.firialabs.com/codeair/flight_lib/flight_lib.html

[^3_10]: https://github.com/orgs/bitcraze/discussions/1528


---

# I'm using crazyradio

Yes—since you’re using **Crazyradio**, you can absolutely turn your existing tile game into a real‑world display that mirrors the **actual Crazyflie’s position** over the grid.[^4_1][^4_2]
Here’s how you can plug it directly into the code you already have.

***

### 1. What changes in your game

- Keep your **Pygame tile grid exactly as before** (black background, green tiles, button, everything).
- Replace the internal drone‑movement logic with:
    - A **background thread** that:
        - Connects to the Crazyflie via `cflib` over Crazyradio.[^4_2][^4_1]
        - Reads its **estimated position** (e.g., `kalman.stateX`, `kalman.stateY`).[^4_3][^4_4]
    - A **shared variable** (`drone_dot_x/y`) that the Pygame loop reads every frame and draws the blue dot at that position.

***

### 2. Crazyflie + Crazyradio setup (Python side)

Install and initialize:

```bash
pip install cflib
```

Then, in your program, add a Crazyflie‑reading class:

```python
import threading
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig

# Your Pygame global for the dot position
drone_dot_x = 0
drone_dot_y = 0
drone_dot_lock = threading.Lock()

URI = 'radio://0/80/2M/E7E7E7E7E7'  # Replace with your Crazyflie's URI

class CrazyfliePositionReader:
    def __init__(self):
        self.is_connected = False

    def _connected(self, link_uri):
        print(f"Connected to {link_uri}")
        self.is_connected = True

    def _disconnected(self, link_uri):
        print(f"Disconnected from {link_uri}")
        self.is_connected = False

    def _log_pos_callback(self, timestamp, data, logconf):
        global drone_dot_x, drone_dot_y
        x = data['kalman.stateX']   # meters
        y = data['kalman.stateY']   # meters
        # Map Crazyflie world (x,y) to your tile grid
        tx, ty = world_to_tile_pos(x, y)   # see below
        with drone_dot_lock:
            drone_dot_x = tx
            drone_dot_y = ty

    def start(self):
        # Initialize drivers
        cflib.crtp.init_drivers()

        # Create Crazyflie instance
        cf = Crazyflie(rw_cache='./cache')
        cf.connected.add_callback(self._connected)
        cf.disconnected.add_callback(self._disconnected)

        with SyncCrazyflie(URI, cf=cf) as scf:
            # Set up logging
            logconf = LogConfig(name='Position', period_in_ms=100)
            logconf.add_variable('kalman.stateX', 'float')
            logconf.add_variable('kalman.stateY', 'float')

            scf.cf.log.add_config(logconf)
            logconf.data_received_cb.add_callback(self._log_pos_callback)

            logconf.start()

            # Block while the drone is connected
            while self.is_connected:
                time.sleep(0.1)

            logconf.stop()
```


***

### 3. Mapping Crazyflie position to your tile grid

Add this helper function (same as before, tuned for your grid):

```python
# Example: your Crazyflie flies over a ~2m wide area
def world_to_tile_pos(x_world, y_world):
    x_min, x_max = -1.0, 1.0
    y_min, y_max = -1.0, 1.0

    w = x_max - x_min
    h = y_max - y_min

    nx = max(0, min(GRID_WIDTH - 1,
                    int((x_world - x_min) / w * GRID_WIDTH)))
    ny = max(0, min(GRID_HEIGHT - 1,
                    int((y_world - y_min) / h * GRID_HEIGHT)))

    t = tiles[ny][nx]
    return t.rect.centerx, t.rect.centery
```


***

### 4. Plug it into your existing Pygame loop

Somewhere near the start of your program (before the main loop), start the Crazyflie reader in a thread:

```python
reader = CrazyfliePositionReader()
reader_thread = threading.Thread(target=reader.start, daemon=True)
reader_thread.start()
```

Then, in your draw step, **remove your internal drone movement** and just draw the real‑drone dot:

```python
def draw_real_drone_dot(surface):
    global drone_dot_x, drone_dot_y
    with drone_dot_lock:
        x, y = drone_dot_x, drone_dot_y
    pygame.draw.circle(surface, (0, 0, 255), (int(x), int(y)), DRONE_RADIUS)

# In your main loop, instead of drone.update():
#   - Remove that line
#   - Call:
draw_real_drone_dot(screen)
```

Optionally, you can still use the **same tile‑touch logic** whenever you assign a new `(x, y)` to the drone dot, so tiles turn yellow / red in real time as the Crazyflie flies over them.

***

### 5. Notes for your setup

- Make sure:
    - The Crazyflie is powered on.
    - The Crazyradio PA is connected via USB.
    - No other tool (like `cfclient`) is already connected to it.[^4_5][^4_2]
- The **`kalman.stateX/Y`** logs give the on‑board position estimate; if you want super‑accurate tracking, you’d add a motion‑capture system (e.g., OptiTrack) and read tracking data instead.[^4_4][^4_6]

If you paste your current full code (or just the drone‑related part), I can edit it directly and show you **exactly where to plug in the Crazyradio + Crazyflie reader** so it “just works” with your existing tile grid.
<span style="display:none">[^4_10][^4_11][^4_7][^4_8][^4_9]</span>

<div align="center">⁂</div>

[^4_1]: https://python.hotexamples.com/examples/cflib.crazyflie/Crazyflie/-/python-crazyflie-class-examples.html

[^4_2]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_connect_log_param/

[^4_3]: https://forum.bitcraze.io/viewtopic.php?t=4117

[^4_4]: https://forum.bitcraze.io/viewtopic.php?t=2976

[^4_5]: https://github.com/bitcraze/crazyflie-lib-python/blob/master/cflib/crtp/radiodriver.py

[^4_6]: https://www.baytas.net/blog/crazyflie

[^4_7]: https://docs.px4.io/main/en/complete_vehicles_mc/crazyflie21

[^4_8]: https://snyk.io/advisor/python/cflib/functions/cflib.drivers.crazyradio.Crazyradio

[^4_9]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/functional-areas/crazyradio_lib/

[^4_10]: https://www.youtube.com/watch?v=J1Y-7AttoFY

[^4_11]: https://snyk.io/advisor/python/cflib/functions/cflib.crazyflie.log.LogConfig

