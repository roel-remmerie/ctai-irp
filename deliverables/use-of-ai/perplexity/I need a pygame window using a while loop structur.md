<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# I need a pygame window using a while loop structure, it needs a grid of green tiles and a button that can be clicked, the text should switch when the button is clicked between on and off

Here’s a simple `pygame` example with a `while` loop, a grid of green tiles, and a clickable button that toggles the label between **On** and **Off**. The basic pattern is to draw the grid every frame, check for mouse clicks on the button, and flip a state variable when clicked.[^1_1][^1_2]

```python
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid and Toggle Button")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_COLOR = (220, 220, 220)
BUTTON_HOVER = (180, 180, 180)
BUTTON_TEXT = (20, 20, 20)

# Grid settings
TILE_SIZE = 50
GRID_COLS = 10
GRID_ROWS = 8
GRID_OFFSET_X = 50
GRID_OFFSET_Y = 50

# Button
button_rect = pygame.Rect(550, 500, 180, 50)
is_on = False

def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(
                GRID_OFFSET_X + col * TILE_SIZE,
                GRID_OFFSET_Y + row * TILE_SIZE,
                TILE_SIZE - 2,
                TILE_SIZE - 2
            )
            pygame.draw.rect(SCREEN, GREEN, rect)
            pygame.draw.rect(SCREEN, DARK_GREEN, rect, 1)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                is_on = not is_on

    SCREEN.fill(BLACK)

    draw_grid()

    # Button drawing
    button_color = BUTTON_HOVER if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(SCREEN, button_color, button_rect, border_radius=8)
    pygame.draw.rect(SCREEN, BLACK, button_rect, 2, border_radius=8)

    button_label = "Off" if is_on else "On"
    text_surface = font.render(button_label, True, BUTTON_TEXT)
    text_rect = text_surface.get_rect(center=button_rect.center)
    SCREEN.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```


## How it works

- The grid is drawn with nested `for` loops using `pygame.draw.rect`, which is the standard way to make tile grids.[^1_3][^1_4]
- The button uses a `pygame.Rect`, and `collidepoint()` checks whether the mouse click happened inside it.[^1_5][^1_1]
- The label changes by flipping `is_on` with `is_on = not is_on`, then rendering `"On"` or `"Off"` based on that state.[^1_6][^1_1]


## Easy tweaks

- Change `GRID_COLS`, `GRID_ROWS`, or `TILE_SIZE` to resize the grid.
- Move the grid by adjusting `GRID_OFFSET_X` and `GRID_OFFSET_Y`.
- Change the button text or colors to match your game style.

Would you like a version where clicking the grid tiles also changes their color?
<span style="display:none">[^1_10][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://stackoverflow.com/questions/65165483/how-to-update-text-appearing-on-button-click-in-pygame-module

[^1_2]: https://stackoverflow.com/questions/7415109/creating-a-rect-grid-in-pygame

[^1_3]: https://www.geeksforgeeks.org/python/slide-puzzle-using-pygame-python/

[^1_4]: https://www.pygame.org/docs/ref/draw.html

[^1_5]: https://www.appsloveworld.com/python/3550/switch-text-on-click-python-pygame-wih-a-functions-button

[^1_6]: https://pythonprogramming.altervista.org/how-to-make-buttons-in-pygame/

[^1_7]: https://www.reddit.com/r/pygame/comments/pwzls2/drawrect_in_tilemap_game/

[^1_8]: https://stackoverflow.com/questions/63547995

[^1_9]: https://gist.github.com/EncodeTheCode/aa512cef8eae806ce5de104266a9a591

[^1_10]: https://pythonprogramming.altervista.org/buttons-in-pygame/


---

# import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
\# poll for events
\# pygame.QUIT event means the user clicked X to close your window
for event in pygame.event.get():
if event.type == pygame.QUIT:
running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    
    
    # RENDER YOUR GAME HERE
    
    
    # flip() the display to put your work on screen
    pygame.display.flip()
    
    
    clock.tick(60)  # limits FPS to 60
    pygame.quit()

can I do event handling in a seperate function?

Yes, you can handle events in a separate function. This is a good practice for cleaner code, especially as your game grows. Here's your template updated with an `handle_events()` function.[^2_1]

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

def handle_events():
    """Process pygame events and return True if the game should continue."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        # Add other events here like KEYDOWN, MOUSEBUTTONDOWN, etc.
    return True

while running:
    # Handle events
    running = handle_events()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
```


## Why this works well

The function returns `False` only when the user wants to quit (X button), so `running` gets updated automatically. You can easily add more event handling inside `handle_events()`:[^2_2]

```python
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse clicked!")
    return True
```


## Advanced version

For even cleaner code, you can pass game state to the function:

```python
def handle_events(game_state):
    """Update game_state based on events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_state['jumping'] = True
    return True

# In main loop:
game_state = {'jumping': False}
running = handle_events(game_state)
```


## Common patterns

- **Simple quit**: Return `running` state (as shown above).
- **Game actions**: Use a dictionary or class for game state.
- **Multiple handlers**: Have separate functions like `handle_input()`, `handle_collisions()`.

This keeps your main loop focused on the game loop structure: **events → update → render → flip**.[^2_3]

<div align="center">⁂</div>

[^2_1]: https://stackoverflow.com/questions/65165483/how-to-update-text-appearing-on-button-click-in-pygame-module

[^2_2]: https://stackoverflow.com/questions/7415109/creating-a-rect-grid-in-pygame

[^2_3]: https://www.appsloveworld.com/python/3550/switch-text-on-click-python-pygame-wih-a-functions-button


---

# is it better to loop crazyflie swarm first or pygame window first

**Run the Crazyflie swarm control loop first (prioritize it), then integrate the Pygame window.** Crazyflie swarms require precise, real-time control loops (typically 100-250Hz) for stability, while Pygame visualization runs at 60FPS and can tolerate minor delays.[^3_1][^3_2]

## Recommended Structure

Use a **single main loop** that prioritizes drone control:

```python
import pygame
import time
from cflib.crazyflie import Crazyflie  # or your swarm lib
# Assume cf is your Crazyflie swarm object

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

drone_state = {}  # Track positions, etc.
control_dt = 1/250  # 250Hz control rate
viz_dt = 1/60       # 60Hz viz rate
last_control = 0
last_viz = 0

def update_swarm():
    """Send setpoints/commands to drones - runs at high rate."""
    # cf.send_setpoint(...) or swarm.parallel(...)
    pass

def render_visualization():
    """Draw drone positions in Pygame."""
    screen.fill("black")
    # Draw swarm positions from drone_state
    pygame.display.flip()

while running:
    current_time = time.time()
    
    # PRIORITY 1: Drone control (non-blocking, high rate)
    if current_time - last_control >= control_dt:
        update_swarm()
        last_control = current_time
    
    # PRIORITY 2: Pygame events (must run every frame)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # PRIORITY 3: Visualization (60Hz)
    if current_time - last_viz >= viz_dt:
        render_visualization()
        last_viz = current_time
    
    clock.tick(250)  # Main loop at control rate

pygame.quit()
```


## Why Swarm First?

| Aspect | Crazyflie Swarm | Pygame Window |
| :-- | :-- | :-- |
| **Timing Critical** | Yes (setpoints every 4-10ms) [^3_1] | No (60FPS fine) |
| **Real-time Needs** | High (PID stability) | Low (rendering) |
| **Blocking Risk** | Commands must be timely | Can lag slightly |
| **Loop Rate** | 100-250Hz | 60Hz |

- **Drones crash** if control lags >50ms.[^3_3]
- **Pygame** just looks choppy if delayed.
- Seen in Crazyflie + Pygame examples: control in threads/main, viz secondary.[^3_4]


## Alternatives

- **Threading**: Drone control in high-priority thread, Pygame main thread.

```python
import threading
drone_thread = threading.Thread(target=drone_control_loop, daemon=True)
drone_thread.start()
# Then run Pygame main loop
```

- **Asyncio**: `asyncio` for non-blocking drone CRTP comms + Pygame event loop.

Start with the single-loop approach above—it's simplest and ensures drone priority. Test with 1 drone first![^3_5]
<span style="display:none">[^3_10][^3_6][^3_7][^3_8][^3_9]</span>

<div align="center">⁂</div>

[^3_1]: http://ee.bradley.edu/projects/proj2018/crazy/resources/bu_crazyflie_final_report.pdf

[^3_2]: https://github.com/bitcraze/crazyflie-lib-python/blob/master/cflib/crazyflie/swarm.py

[^3_3]: https://crazyswarm.readthedocs.io/en/latest/api.html

[^3_4]: https://gist.github.com/thecodemaiden/a1b9e50d53e786950fab

[^3_5]: https://www.bitcraze.io/2024/04/crazysim-a-software-in-the-loop-simulator-for-the-crazyflie/

[^3_6]: https://github.com/bitcraze/crazyflie-vision

[^3_7]: https://dev.to/ingeborg_adolfs_c414578af/multiple-game-loops-in-pygame-ce-305l

[^3_8]: https://stackoverflow.com/questions/50454159/loop-in-pygame-it-never-continues-but-keeps-looping-what-am-i-missing

[^3_9]: https://forum.bitcraze.io/viewtopic.php?t=976

[^3_10]: https://cs10.org/bjc-r/cur/programming/pygame/game-loop.html?topic=berkeley_bjc%2Fpython%2Fpygame.topic

