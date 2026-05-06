import numpy as np
import numpy.typing as npt

from collections import deque

class CMSG: # Constrained multi source growth
    def __init__(self, shape_xy: tuple[int, int], origins_xy: list[tuple[int, int]], directions_yx: npt.NDArray):
        self.x_shape, self.y_shape = shape_xy
        shape = (self.y_shape, self.x_shape)
        n = len(origins_xy)
        self.directions = directions_yx

        # --- Capacity ---
        total = self.y_shape * self.x_shape
        base = total // n
        remainder = total % n

        capacities = np.full(n, base)
        capacities[:remainder] += 1

        # --- State ---
        labels = -np.ones(shape, dtype=int)
        self.occupied = np.zeros(shape, dtype=bool)

        drone_areas = [[] for _ in range(n)]
        frontiers = [set() for _ in range(n)]
        counts = np.zeros(n, dtype=int)
        previous_count = np.zeros(n, dtype=int)
        
        # add starting nodes
        for i, (x_origin, y_origin) in enumerate(origins_xy):
            i_origin = y_origin, x_origin

            labels[y_origin, x_origin] = i
            self.occupied[y_origin, x_origin] = True
            drone_areas[i].append(i_origin)
            counts[i] = 1

            for ny, nx in self.iter_neighbors(i_origin):
                if not self.occupied[ny, nx]:
                    frontiers[i].add((ny, nx))
        
        # --- Main loop ---
        while True:
            if np.array_equal(counts, previous_count):
                break

            previous_count = counts.copy()

            active = [i for i in range(n) if counts[i] < capacities[i]]
            if not active:
                break

            c_global = self.global_centroid() # compute global centroid once per iteration

            # iterate all drones (round robin) in order of ascending #frontiers
            for i in sorted(active, key=lambda d: len(frontiers[d])):

                if not frontiers[i]:
                    continue

                c_self = CMSG.centroid(drone_areas[i]) # drone area centroid

                best_score = -np.inf
                best_cell = None

                for frontier in frontiers[i]:
                    frontier_y, frontier_x = frontier
                    if self.occupied[frontier_y, frontier_x]:
                        continue

                    score = self.get_score(frontier, c_global, c_self)

                    if score > best_score:
                        best_score = score
                        best_cell = frontier

                if best_cell is None:
                    continue

                best_y, best_x = best_cell

                # remove from frontier
                frontiers[i].discard(best_cell)

                if self.occupied[best_y, best_x]:
                    continue

                # assign
                labels[best_y, best_x] = i
                self.occupied[best_y, best_x] = True
                drone_areas[i].append(best_cell)
                counts[i] += 1

                # expand frontier
                for ny, nx in self.iter_neighbors(best_cell):
                    if not self.occupied[ny, nx]:
                        frontiers[i].add((ny, nx))

        # if any unassigned cells remain assign greedy

        # --- Fill remaining unassigned cells by neighborhood majority ---
        unassigned = np.argwhere(labels == -1)

        while len(unassigned) > 0:
            progress = False

            for y, x in unassigned:
                neighbor_scores = np.zeros(n, dtype=float)

                for ny, nx in self.iter_neighbors((y, x)):
                    label = labels[ny, nx]
                    if label != -1:
                        # weighted contribution (favor smaller regions)
                        neighbor_scores[label] += 1.0 / (1 + counts[label])

                if np.any(neighbor_scores > 0):
                    # pick best score
                    max_score = np.max(neighbor_scores)
                    candidates = np.where(neighbor_scores == max_score)[0]

                    # tie-break: prefer smaller regions
                    i = min(candidates, key=lambda d: counts[d])

                    labels[y, x] = i
                    self.occupied[y, x] = True
                    counts[i] += 1

                    progress = True

            if not progress:
                # fallback: assign remaining cells to nearest centroid
                for y, x in unassigned:
                    i = np.argmin([
                        np.linalg.norm(np.array([y, x]) - CMSG.centroid(drone_areas[d]))
                        for d in range(n)
                    ])
                    labels[y, x] = i
                    counts[i] += 1
                break

            unassigned = np.argwhere(labels == -1)

        print(labels)
        print(counts)

        self.labels = labels
        self.counts = counts
    
    def iter_neighbors(self, coord: tuple[int,int]):
        y, x = coord
        for y_directions, x_directions in self.directions:
            ny, nx = y + y_directions, x + x_directions
            if 0 <= ny < self.y_shape and 0 <= nx < self.x_shape:
                yield ny, nx

    @staticmethod
    def centroid(area):
        pts = np.array(area)
        return np.mean(pts, axis=0)
    
    def global_centroid(self):
        coords = np.argwhere(self.occupied)
        return np.mean(coords, axis=0)
    
    def get_score(self, frontier: tuple[int,int], c_global: tuple[float,float], c_self: tuple[float,float]):
        p = np.array(frontier)

        # distances
        d_global = np.linalg.norm(p - c_global)
        d_self = np.linalg.norm(p - c_self)

        openness = 0
        for ny, nx in self.iter_neighbors(frontier):
            if not self.occupied[ny, nx]:
                openness += 1

        score = (
            2.0 * openness # main driver: go where space is
            - 0.5 * d_self # keep region coherent
            - 0.2 * d_global # mild global spreading pressure
        )

        occupied_neighbors = 0
        for ny, nx in self.iter_neighbors(frontier):
            if self.occupied[ny, nx]:
                occupied_neighbors += 1

        score -= 0.8 * occupied_neighbors

        return score
    
class RoutePlanner:
    @staticmethod
    def shortest_bound_path(start_xy, target_xy, mask, shape_xy):
        start = tuple(start_xy)
        target = tuple(target_xy)
        shape_x, shape_y = shape_xy

        queue = deque([start])
        visited = {start: None}

        while queue:
            current = queue.popleft()

            if current == target:
                break

            x, y = current
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy

                if (
                    0 <= nx < shape_x and
                    0 <= ny < shape_y and
                    mask[ny, nx] and
                    (nx, ny) not in visited
                ):
                    visited[(nx, ny)] = current
                    queue.append((nx, ny))

        # reconstruct path
        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = visited.get(cur)

        return path[::-1]