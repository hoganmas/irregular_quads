#!/usr/bin/env python3
from lib import *
from tri import *

figure, axes = plt.subplots()
axes.set_aspect(1)


verts = []
tris = []
edges = {}  # (vert_min, vert_max) -> [adj_poly1, adj_poly2]
num_shells = 3
colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'pink']


start_time = time.time()

triangulate(verts, edges, tris, num_shells)
print('Triangulating grid took', time.time() - start_time, 'seconds')
start_time = time.time()

polys = greedy_grouping(edges, tris)
print('Greedy grouping took', time.time() - start_time, 'seconds')
start_time = time.time()

edges, polys = subdivide(verts, edges, polys)
print('Subdivision took', time.time() - start_time, 'seconds')
start_time = time.time()

num_iters = 2
for i in range(num_iters):
    relax(verts, edges, polys)
print('Relaxation took', time.time() - start_time, 'seconds')
start_time = time.time()

# Emulate rendering

for i, quad in enumerate(polys):
    poly = plt.Polygon(
        [verts[j].list() for j in quad],
        color=colors[i % len(colors)]
    )
    poly.set_edgecolor('black')
    plt.gca().add_patch(poly)

plt.plot([vert.x for vert in verts], [vert.y for vert in verts], 'ko', markersize=5)
print('Rendering took', time.time() - start_time, 'seconds')

plt.show()
