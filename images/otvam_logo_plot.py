"""
Plot the otvam diode logo with meshio/matplotlib.
Thomas Guillod - All rights reserved.
"""

import meshio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col


def plot_surface(points, triangles, idx, color):
    cdata = np.ones(len(points))
    cmap = col.ListedColormap(color)
    plt.tripcolor(points[:, 0], points[:, 1], triangles[idx, :], cdata, cmap=cmap, alpha=None)


def plot_edge(points, triangles, idx, color, width):
    plt.triplot(points[:, 0].transpose(), points[:, 1].transpose(), triangles[idx, :], color=color, linewidth=width, solid_capstyle='round')

def plot_bnd(points, lines, idx, color, width):
    # get the segments
    bnd = lines[idx, :]
    pts_1 = points[bnd[:, 0], :]
    pts_2 = points[bnd[:, 1], :]
    x = np.stack((pts_1[:, 0], pts_2[:, 0]))
    y = np.stack((pts_1[:, 1], pts_2[:, 1]))

    # plot the segments
    plt.plot(x, y, color=color, linewidth=width, solid_capstyle='round')


# load the meash
mesh = meshio.read("otvam.msh")
points = mesh.points
lines = mesh.cells_dict["line"]
triangles = mesh.cells_dict["triangle"]
idx_air = mesh.cell_sets_dict["air"]["triangle"]
idx_diode = mesh.cell_sets_dict["diode"]["triangle"]
idx_bnd = mesh.cell_sets_dict["bnd"]["line"]

# get the colors
blue_line = (67 / 255, 116 / 255, 186 / 255, 1.00)
blue_alpha = (67 / 255, 116 / 255, 186 / 255, 0.25)
gray_line = (120 / 255, 120 / 255, 120 / 255, 1.00)
gray_alpha = (200 / 255, 200 / 255, 200 / 255, 0.05)

# plot the mesh
plt.figure()
plot_surface(points, triangles, idx_air, gray_alpha)
plot_surface(points, triangles, idx_diode, blue_alpha)
plot_edge(points, triangles, idx_air, gray_line, 0.75)
plot_edge(points, triangles, idx_diode, blue_line, 1.5)
plot_bnd(points, lines, idx_bnd, blue_line, 3)
plt.axis("equal")
plt.axis("off")

plt.savefig("otvam.svg")
plt.show()
