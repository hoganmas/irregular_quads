from config import *



class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if type(other) == Vector:
            return Vector(self.x + other.x, self.y + other.y)
        return Vector(self.x + other, self.y + other)

    def __radd__(self, other):
        if type(other) == Vector:
            return Vector(self.x + other.x, self.y + other.y)
        return Vector(self.x + other, self.y + other)

    def __iadd__(self, other):
        if type(other) == Vector:
            self.x += other.x
            self.y += other.y
            return self
        else:
            self.x += other
            self.y += other
            return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __rsub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        if type(other) == Vector:
            return self.x * other.x + self.y * other.y
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        if type(other) == Vector:
            return self.x * other.x + self.y * other.y
        return Vector(self.x * other, self.y * other)

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __rtruediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __idiv__(self, other):
        self.x /= other
        self.y /= other
        return self

    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def list(self):
        return [self.x, self.y]

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x
    
    def __str__(self):
        return f"({self.x}, {self.y})"


def get_edge(v1: int, v2: int):
    return (min(v1, v2), max(v1, v2))


def get_index(shell: int, side: int, side_index: int):
    if shell == 0:
        return 0

    num_inside = 3 * shell * (shell - 1)
    num_beside = shell * side + side_index

    return num_inside + num_beside + 1


def get_next_index(shell: int, side: int, side_index: int):
    if shell == 0:
        return 0
    
    num_inside = 3 * shell * (shell - 1)
    num_beside = shell * side + side_index

    # increment num_beside
    num_beside = (num_beside + 1) % (6 * shell)
    return num_inside + num_beside + 1


def get_inner_index(shell: int, side: int, side_index: int):
    if shell <= 1:
        return 0
    
    shell = shell - 1
    num_inside = 3 * shell * (shell - 1)
    num_beside = shell * side + side_index
    num_beside = num_beside % (6 * shell)

    return num_inside + num_beside + 1


def get_inner_next_index(shell: int, side: int, side_index: int):
    if shell <= 1:
        return 0

    shell = shell - 1
    num_inside = 3 * shell * (shell - 1)
    num_beside = shell * side + side_index
    num_beside = (num_beside + 1) % (6 * shell)

    return num_inside + num_beside + 1


def join_tris(tri1: list, tri2: list):
    # find v1, v2 (exclusive vertices)
    v1 = -1
    v1_idx = -1
    for i in range(3):
        if tri1[i] not in tri2:
            v1 = tri1[i]
            v1_idx = i
    
    v2 = -1
    v2_idx = -1
    for i in range(3):
        if tri2[i] not in tri1:
            v2 = tri2[i]
            v2_idx = i

    return [
        v1,
        tri1[(v1_idx + 1) % 3],
        v2, 
        tri2[(v2_idx + 1) % 3]
    ]

