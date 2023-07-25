import os
from math import pi

import matplotlib.pyplot as plt
import numpy as np

from classy_blocks import Face, Loft, Mesh
from classy_blocks.util import constants

# SPHERE
R_SPHERE                            = 0.05      # [m]
R_SPHERE_OUTER                      = 1.95      # [m] - diameter of the outer sphere, zone with strucutred mesh shaped like a sphere

# CELL SIZE
BALL_CELL_SIZE                      = 0.00015   # [m]
DOMAIN_CELL_SIZE                    = 0.08      # [m]

print("BALL_CELL_SIZE:\t", BALL_CELL_SIZE)
print("DOMAIN_CELL_SIZE:\t", DOMAIN_CELL_SIZE)

# REFINEMENT LAYER
TOTAL_THICKNESS_REFINEMENT_LAYER    = 0.0005    # [m]
COUNT_REFINEMENT_LAYER              = 30        # [º]
C2C_EXPANSION_REFINEMENT_LAYER      = 1.2       # [º]

print("TOTAL_THICKNESS_REFINEMENT_LAYER:\t", TOTAL_THICKNESS_REFINEMENT_LAYER)
print("COUNT_REFINEMENT_LAYER:\t", COUNT_REFINEMENT_LAYER)
print("C2C_EXPANSION_REFINEMENT_LAYER:\t", C2C_EXPANSION_REFINEMENT_LAYER)


# ----------------- AUTOMATIC ----------------- 
r2 = R_SPHERE
r1 = R_SPHERE + TOTAL_THICKNESS_REFINEMENT_LAYER   
r0 = R_SPHERE_OUTER

print("r2:\t", r2)
print("r1:\t", r1)
print("r0:\t", r0)

count = int(0.25*2*pi*R_SPHERE_OUTER / DOMAIN_CELL_SIZE)

print("count:\t", count)

L_UPSTREAM      = R_SPHERE * 60
L_DOWNSTREAM    = R_SPHERE * 140
WIDTH           = R_SPHERE * 60

print("L_UPSTREAM:\t", L_UPSTREAM)
print("L_DOWNSTREAM:\t", L_DOWNSTREAM)
print("WIDTH:\t", WIDTH)


# from outer to inner
geometry = {
    'sphere_0': [
        'type   searchableSphere',
        'origin (0 0 0)',
        'centre (0 0 0)',
        f'radius {r0}',
    ],
    'sphere_1': [
        'type   searchableSphere',
        'origin (0 0 0)',
        'centre (0 0 0)',
        f'radius {r1}',
    ],
    'sphere_2': [
        'type   searchableSphere',
        'origin (0 0 0)',
        'centre (0 0 0)',
        f'radius {r2}',
    ]
}

# create a 4x4 grid of points;
# source point
co = r0 / 3**0.5

xc = [-L_UPSTREAM, -co, co, L_DOWNSTREAM]
yc = [-WIDTH,      -co, co, WIDTH]
zc = [-WIDTH,      -co, co, WIDTH]




# MAIN
def main ():

    mesh = Mesh()
    oplist = []

    projected_faces = {
        4: 'top',
        10: 'back',
        12: 'right',
        14: 'left',
        16: 'front',
        22: 'bottom',
    }

    create_3x3(oplist, projected_faces)

    # --------------------------------------------------
    # ADD 1st RING
    oplist = add_ring(oplist, projected_faces, (DOMAIN_CELL_SIZE, BALL_CELL_SIZE), "sphere_1", r1/r0)

    # --------------------------------------------------
    # ADD 2nd RING
    projected_faces = {
        27: 'top',
        28: 'top',
        29: 'top',
        30: 'top',
        31: 'top',
        32: 'top',
    }

    oplist = add_boundary_layer(oplist, projected_faces, "sphere_2", r2/r1, invert=0)
    for i in range(6):
        oplist[i+33].set_patch('top', 'sphere')

    # --------------------------------------------------
    # ADD ALL LOFTS
    for o in oplist:
        if o is not None:
            mesh.add(o)

    # set counts; since count is propagated automatically, only a handful
    # of blocks need specific counts set

    # x-direction
    oplist[12].chop(0, start_size=DOMAIN_CELL_SIZE*2.5, end_size=DOMAIN_CELL_SIZE)
    oplist[14].chop(0, start_size=DOMAIN_CELL_SIZE, end_size=DOMAIN_CELL_SIZE*4)

    # y-direction
    for i in (10, 16):
        oplist[i].chop(1, start_size=DOMAIN_CELL_SIZE, end_size=DOMAIN_CELL_SIZE)

    # z-direction:
    for i in (3, 21):
        oplist[i].chop(2, start_size=DOMAIN_CELL_SIZE, end_size=DOMAIN_CELL_SIZE)

    # --------------------------------------------------

    # DEBUG PLOT
    plot_points(oplist[27:])

    mesh.set_default_patch('sides', 'wall')
    mesh.add_geometry(geometry)

    mesh.write(os.path.join("system", "blockMeshDict"), debug_path="debug.vtk")


# create a 3x3 grid of blocks; leave the middle out
def create_3x3 (oplist, projected_faces):

    for i in range(3):
        for j in range(3):
            for k in range(3):
                if i == j == k == 1:
                    # the middle block is the sphere - hollow
                    oplist.append(None)
                    continue

                n = len(oplist)

                bottom_face = Face([
                    [xc[k],   yc[j],   zc[i]],
                    [xc[k+1], yc[j],   zc[i]],
                    [xc[k+1], yc[j+1], zc[i]],
                    [xc[k],   yc[j+1], zc[i]]
                ])

                top_face = Face([
                    [xc[k],   yc[j],   zc[i+1]],
                    [xc[k+1], yc[j],   zc[i+1]],
                    [xc[k+1], yc[j+1], zc[i+1]],
                    [xc[k],   yc[j+1], zc[i+1]],
                ])

                o = Loft(bottom_face, top_face)

                if n in projected_faces: # blocks around the center
                    o.project_side(projected_faces[n], 'sphere_0', edges=True)

                if k == 0: # first block - inlet
                    o.set_patch('left', 'inlet')

                if k == 2: # last block - outlet
                    o.set_patch('right', 'outlet')

                oplist.append(o)

    return oplist




def add_ring (oplist, projected_faces, sizes, str_sphere, growth, invert=1):

    cell_size1, cell_size2 = sizes

    j = 0
    for i, side in projected_faces.items():
        block = oplist[i]

        bottom_face = block.get_face(side)

        if j > 2 and invert:
            # starting from block's "other side"
            bottom_face = bottom_face.invert()

        top_points = np.array([bottom_face.points[j].position for j in range(4)])*growth
        top_face = Face(top_points)

        o = Loft(bottom_face, top_face)
        o.project_side('top', str_sphere, edges=True)

        o.chop(0, count=count)
        o.chop(1, count=count)
        o.chop(2, start_size=cell_size1, end_size=cell_size2)

        oplist.append(o)
        j+=1

    return oplist


def add_boundary_layer (oplist, projected_faces, str_sphere, growth, invert=1):

    j = 0
    for i, side in projected_faces.items():
        block = oplist[i]

        bottom_face = block.get_face(side)

        if j > 2 and invert:
            # starting from block's "other side"
            bottom_face = bottom_face.invert()

        top_points = np.array([bottom_face.points[j].position for j in range(4)])*growth
        top_face = Face(top_points)

        o = Loft(bottom_face, top_face)
        o.project_side('top', str_sphere, edges=True)

        o.chop(0, count=count)
        o.chop(1, count=count)
        o.chop(2, count=COUNT_REFINEMENT_LAYER, c2c_expansion=1/C2C_EXPANSION_REFINEMENT_LAYER)

        oplist.append(o)
        j+=1

    return oplist


def plot_points (oplist):

    points = []

    print(len(oplist))

    for o in oplist:
        point_plot = []

        if o is None: 
            continue

        point_plot += [o.bottom_face.points[j].position for j in range(4)]
        point_plot += [o.top_face.points[j].position for j in range(4)]

        points.append(np.array(point_plot))

    ax = plt.figure().add_subplot(projection='3d')
    for i in range(len(points)):
        ax.plot(points[i][:4,0], points[i][:4,1], points[i][:4,2], color="b")
        ax.plot(points[i][3:,0], points[i][3:,1], points[i][3:,2], color="r")

    plt.show()




if __name__ == "__main__":
    main()
