import matplotlib.pyplot as plt

from assets.components import *
from services.navigation import NavigationService

class Plot():
    @classmethod
    def _drone_routes(_, image_uri: str, pixels: tuple[int,int], navigation: NavigationService):
        DPI = 100
        fig = plt.figure(figsize=(pixels[0]/DPI, pixels[1]/DPI), dpi=DPI)

        for drone_id, route in navigation.full_routes.items():
            if not route:
                continue

            xs = [p[0] for p in route]
            ys = [p[1] for p in route]

            current = navigation.drone_locations[drone_id]
            start = route[0]
            color = navigation.color_dict[drone_id]

            plt.plot(xs, ys, marker='o', label=f"Drone {drone_id}", color=color)
            plt.scatter(current[0], current[1], color=color, s=100, edgecolors='black', zorder=3)
            plt.scatter(start[0], start[1], color=color, s=100, edgecolors='red', zorder=3)

        plt.title("Drone Search Routes")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)
        plt.axis('equal')
        plt.savefig(image_uri, dpi=DPI)
        plt.close()
