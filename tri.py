#!/usr/bin/env python3
from math import nan
from numpy.lib.function_base import append
from lib import *




units = [
    [0, 1],
    [sqrt(3)*.5, .5],
    [sqrt(3)*.5, -.5],
    [0, -1],
    [-sqrt(3)*.5, -.5],
    [-sqrt(3)*.5, .5],
]




def triangulate(verts, edges, tris, num_shells):
    # Shell 0
    verts.append(Vector(0, 0))

    # Shells 1+
    for i in range(1, num_shells + 1):
        for j in range(6):
            for k in range(i):
                x = (i - k) * units[j][0] + k * units[(j + 1) % 6][0]
                y = (i - k) * units[j][1] + k * units[(j + 1) % 6][1]

                verts.append(Vector(x, y))

                # Get indices to build triangles
                this_idx = get_index(i, j, k)
                next_idx = get_next_index(i, j, k)
                inner_idx = get_inner_index(i, j, k)
                inner_next_idx = get_inner_next_index(i, j, k)


                tri = [inner_idx, this_idx, next_idx]

                for l in range(len(tri)):
                    edge = get_edge(tri[l], tri[(l+1)%len(tri)])

                    if edge not in edges:
                        edges[edge] = [len(tris)]
                    else:
                        edges[edge].append(len(tris))
                
                tris.append(tri)


                if i != 1 and k != i - 1:
                    tri2 = [inner_idx, next_idx, inner_next_idx]
                    for l in range(len(tri2)):
                        edge = get_edge(tri2[l], tri2[(l+1)%len(tri2)])

                        if edge not in edges:
                            edges[edge] = [len(tris)]
                        else:
                            edges[edge].append(len(tris))

                    tris.append(tri2)




def greedy_grouping(edges, tris):
    marked = set()
    polys = []

    # for each avilable triangle
    for i, tri in enumerate(tris):
        if i in marked:
            continue

        # try to find an available adjacent triangle
        vals = [0, 1, 2]
        random.shuffle(vals)
        for j in vals:
            edge = get_edge(tri[j], tri[(j+1)%len(tri)])

            if edge not in edges:
                continue

            if len(edges[edge]) != 2:
                continue

            other = edges[edge][0]
            if i == other:
                other = edges[edge][1]
            
            if other in marked:
                continue
            
            
            # mark triangles as unavailable
            marked.add(i)
            marked.add(other)
            del edges[edge]

            # join triangles
            quad = join_tris(tris[i], tris[other])
            polys.append(quad)

            break

        if i not in marked:
            polys.append(tri)

    return polys




def subdivide(verts, edges, polys):
    orig_vert_count = len(verts)

    # (1) add midpoint for each edge to verts
    for edge in edges:
        edges[edge] = [len(verts)]
        verts.append(0.5 * (verts[edge[0]] + verts[edge[1]]))
    
    # (2) remesh
    new_polys = []
    new_edges = {}

    for poly in polys:
        # subdivide poly and append to quads
        gons = len(poly)
        for i in range(gons):
            next_edge = get_edge(poly[i],poly[(i+1)%gons])
            prev_edge = get_edge(poly[i],poly[(i-1)%gons])

            print(next_edge, next_edge in edges)

            new_poly = [
                poly[i],
                edges[next_edge][0],
                len(verts),
                edges[prev_edge][0]
            ]

            for j in range(4):
                edge = get_edge(new_poly[j], new_poly[(j+1)%4])
                
                if edge not in new_edges:
                    new_edges[edge] = [len(new_polys)]
                else:
                    new_edges[edge].append(len(new_polys))
                
            new_polys.append(new_poly)
        
        # append centroid to verts
        verts.append(sum([verts[j] for j in poly]) / len(poly))
    
    
    return new_edges, new_polys




def relax(verts, edges, polys):
    # For each point, we apply a force to smooth the mesh.
    # These come in two types of forces:

    # (1) 1D elastic force
    #   - we imagine each edge as an elastic string
    # (2) 2D elastic force
    #   - we imagine each poly as an elastic bubble

    outside_verts = set()
    weight1 = 1
    weight2 = 1

    sum_adj = []
    for i in range(len(verts)):
        sum_adj.append(Vector(0, 0))
    num_adj = [0] * len(verts)

    # Add 1D elastic force
    for edge in edges:
        v1 = edge[0]
        v2 = edge[1]
        # if not an outside edge
        if len(edges[edge]) == 2:
            sum_adj[v1] += verts[v2] * weight1
            sum_adj[v2] += verts[v1] * weight1
            num_adj[v1] += weight1
            num_adj[v2] += weight1
        else:
            outside_verts.add(v1)
            outside_verts.add(v2)
    
    # Add 2D elastic force
    for j, poly in enumerate(polys):
        centroid = sum([verts[j] for j in poly]) / len(poly)
        for vert in poly:
            sum_adj[vert] += centroid * weight2
            num_adj[vert] += weight2

    
    for i in range(len(verts)):
        if num_adj[i] != 0 and i not in outside_verts:
            verts[i] = sum_adj[i] / num_adj[i]
