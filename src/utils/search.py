import math

X_TILE_DIMS = 0.5 # meters
Y_TILE_DIMS = 0.5

X_MIN = -2.0
Y_MIN = -2.0
X_MAX = 2.0
Y_MAX = 2.0

X_TILES = math.floor((X_MAX - X_MIN) / X_TILE_DIMS)
Y_TILES = math.floor((Y_MAX - Y_MIN) / Y_TILE_DIMS)

X_VALUES = [(x * X_TILE_DIMS) + X_MIN for x in range(X_TILES)]
Y_VALUES = [(y * Y_TILE_DIMS) + Y_MIN for y in range(Y_TILES)]

coordinates = [(x, y) for x in X_VALUES for y in Y_VALUES]
