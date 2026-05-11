You can control both the file format and exact pixel size in Matplotlib by setting the figure size in inches and the DPI (dots per inch).
Key idea

Pixels = inches × DPI

So for 640 × 600 px, one clean option is:

    width = 6.4 inches

    height = 6.0 inches

    DPI = 100

Example

import matplotlib.pyplot as plt

# Create figure with exact size
fig, ax = plt.subplots(figsize=(6.4, 6.0), dpi=100)

# Example plot
ax.plot([1, 2, 3], [4, 5, 6])

# Save as PNG with exact resolution
plt.savefig("plot.png", dpi=100)

plt.close()

Alternative (more explicit control)

You can compute it directly:

width_px, height_px = 640, 600
dpi = 100

fig = plt.figure(figsize=(width_px / dpi, height_px / dpi), dpi=dpi)

Common gotcha

If your saved image ends up slightly off in size, it’s usually because of:

plt.savefig("plot.png", dpi=100, bbox_inches='tight')

⚠️ bbox_inches='tight' can change the final pixel dimensions by trimming whitespace.

If you need exactly 640×600, don’t use that option.

If you want, I can also show how to:

    remove margins completely without breaking size

    match the plot exactly to a pygame surface

    export with transparent background


use the alternative approach on this plot

class Plot():
    @classmethod
    def plot_drone_routes(_, navigation: NavigationService):
        plt.figure(figsize=(8, 8))

        for drone_id, route in navigation.routes.items():
            print(len(route))

            if not route:
                continue

            xs = [p[0] for p in route]
            ys = [p[1] for p in route]

            color = (random.random(), random.random(), random.random())

            plt.plot(xs, ys, marker='o', label=f"Drone {drone_id}", color=color)

            start = route[0]
            plt.scatter(start[0], start[1], color=color, s=100, edgecolors='black', zorder=3)

            plt.text(start[0], start[1], drone_id, fontsize=9)

        plt.title("Drone Search Routes")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)
        plt.axis('equal')
        plt.show()

You just need to replace the fixed figsize=(8, 8) with the pixel-based calculation, and make sure the same DPI is used when saving.

Here’s your function rewritten using the “alternative approach” (exact 640×600 output):

import matplotlib.pyplot as plt
import random

class Plot():
    @classmethod
    def plot_drone_routes(_, navigation):
        # Target size in pixels
        width_px, height_px = 640, 600
        dpi = 100

        # Convert pixels → inches
        fig = plt.figure(figsize=(width_px / dpi, height_px / dpi), dpi=dpi)

        for drone_id, route in navigation.routes.items():
            print(len(route))

            if not route:
                continue

            xs = [p[0] for p in route]
            ys = [p[1] for p in route]

            color = (random.random(), random.random(), random.random())

            plt.plot(xs, ys, marker='o', label=f"Drone {drone_id}", color=color)

            start = route[0]
            plt.scatter(start[0], start[1], color=color, s=100, edgecolors='black', zorder=3)

            plt.text(start[0], start[1], drone_id, fontsize=9)

        plt.title("Drone Search Routes")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)
        plt.axis('equal')

        # Save with exact size
        plt.savefig("drone_routes.png", dpi=dpi)

        # Optional: still show it
        plt.show()

Important details

    figsize=(width_px / dpi, height_px / dpi) → guarantees pixel size

    dpi in savefig must match the figure DPI

    Do not add bbox_inches='tight' if you need exactly 640×600

If you want a cleaner image (optional)

If you notice padding around the plot but still want exact size, you can control margins manually instead of using tight:

plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.1)

If you’re planning to load this into pygame next, I can help you make the coordinate system line up perfectly with your grid so routes overlay correctly.

now can I use this image in a pygame window

Yes—you can load and display that saved PNG directly in Pygame. It works just like any other image.
Basic workflow

    Save the plot (drone_routes.png) ✔️

    Load it in pygame

    Blit it to the screen

Minimal example

import pygame
import sys

pygame.init()

# Match your matplotlib output size
WIDTH, HEIGHT = 640, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load the image
plot_image = pygame.image.load("drone_routes.png").convert()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw image
    screen.blit(plot_image, (0, 0))

    pygame.display.flip()
    clock.tick(60)

Important things to watch

1. Size must match (or scale it)
If your window is also 640×600, it will fit perfectly.
Otherwise:

plot_image = pygame.transform.scale(plot_image, (WIDTH, HEIGHT))

2. Coordinate alignment (very important for your use case)
Matplotlib and pygame use different coordinate systems:

    Matplotlib → origin bottom-left

    Pygame → origin top-left

So if you later overlay drones or interact with the image, you may need to flip Y:

pygame_y = HEIGHT - matplotlib_y

3. Performance tip
Don’t reload the image every frame—load it once (like above).
Optional: smoother integration

If you plan to:

    update routes frequently

    animate drones

Then saving → loading each frame is too slow. In that case, you’d want to:

    render matplotlib to a buffer, or

    draw directly in pygame (better for real-time)

If you want, I can show you how to:

    overlay moving drones on top of the plot

    or
    completely replace matplotlib with a pygame-native grid renderer (faster and cleaner for simulations)


