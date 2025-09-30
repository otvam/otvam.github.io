"""
Generate the otvam diode logo with gmsh.
Thomas Guillod - All rights reserved.
"""

import numpy as np
import gmsh


# size of the domain and the diode
d_max = 4.0
d_min = 0.0
d_diode = 0.65

# get the diode coordinates
d_line = d_diode / (2 * np.sqrt(2))
d_offset = d_diode * np.sqrt(3) / (2 * np.sqrt(2))
d_cat = (d_max - d_min) / 2 + d_offset / 2
xy_cat_mid = np.array([d_cat, d_cat])
xy_cat_dw = np.array([d_cat - d_line, d_cat + d_line])
xy_cat_up = np.array([d_cat + d_line, d_cat - d_line])
xy_ano_mid = np.array([d_cat - d_offset, d_cat - d_offset])
xy_ano_dw = np.array([d_cat - d_line - d_offset, d_cat + d_line - d_offset])
xy_ano_up = np.array([d_cat + d_line - d_offset, d_cat - d_line - d_offset])

# init the mesh
gmsh.initialize()
gmsh.model.add("otvam")

# get the box points
p_box_min_min = gmsh.model.occ.addPoint(d_min, d_min, 0)
p_box_max_min = gmsh.model.occ.addPoint(d_max, d_min, 0)
p_box_max_max = gmsh.model.occ.addPoint(d_max, d_max, 0)
p_box_min_max = gmsh.model.occ.addPoint(d_min, d_max, 0)

# get the box lines
l_1 = gmsh.model.occ.addLine(p_box_min_min, p_box_max_min)
l_2 = gmsh.model.occ.addLine(p_box_max_min, p_box_max_max)
l_3 = gmsh.model.occ.addLine(p_box_max_max, p_box_min_max)
l_4 = gmsh.model.occ.addLine(p_box_min_max, p_box_min_min)

# get the box surface
cbox = gmsh.model.occ.addCurveLoop([l_1, l_2, l_3, l_4])
box = gmsh.model.occ.addPlaneSurface([cbox])

# get the diode points
p_cat_mid = gmsh.model.occ.addPoint(xy_cat_mid[0], xy_cat_mid[1], 0)
p_cat_dw = gmsh.model.occ.addPoint(xy_cat_dw[0], xy_cat_dw[1], 0)
p_cat_up = gmsh.model.occ.addPoint(xy_cat_up[0], xy_cat_up[1], 0)
p_ano_mid = gmsh.model.occ.addPoint(xy_ano_mid[0], xy_ano_mid[1], 0)
p_ano_dw = gmsh.model.occ.addPoint(xy_ano_dw[0], xy_ano_dw[1], 0)
p_ano_up = gmsh.model.occ.addPoint(xy_ano_up[0], xy_ano_up[1], 0)
p_mid_up = gmsh.model.occ.addPoint((xy_cat_mid[0] + xy_ano_up[0]) / 2, (xy_cat_mid[1] + xy_ano_up[1]) / 2, 0)
p_mid_dw = gmsh.model.occ.addPoint((xy_cat_mid[0] + xy_ano_dw[0]) / 2, (xy_cat_mid[1] + xy_ano_dw[1]) / 2, 0)

# get the box lines
l_box_ano = gmsh.model.occ.addLine(p_box_min_min, p_ano_mid)
l_box_cat = gmsh.model.occ.addLine(p_box_max_max, p_cat_mid)
l_cat_up = gmsh.model.occ.addLine(p_cat_mid, p_cat_up)
l_cat_dw = gmsh.model.occ.addLine(p_cat_mid, p_cat_dw)
l_ano_up = gmsh.model.occ.addLine(p_ano_mid, p_ano_up)
l_ano_dw = gmsh.model.occ.addLine(p_ano_mid, p_ano_dw)
l_ano_mid_dw = gmsh.model.occ.addLine(p_ano_dw, p_mid_dw)
l_mid_cat_dw = gmsh.model.occ.addLine(p_mid_dw, p_cat_mid)
l_ano_mid_up = gmsh.model.occ.addLine(p_ano_up, p_mid_up)
l_mid_cat_up = gmsh.model.occ.addLine(p_mid_up, p_cat_mid)

l_mid_ano_up = gmsh.model.occ.addLine(p_mid_up, p_ano_mid)
l_mid_ano_dw = gmsh.model.occ.addLine(p_mid_dw, p_ano_mid)
l_mid_up_dw = gmsh.model.occ.addLine(p_mid_up, p_mid_dw)

# get the diode surface
ctri = gmsh.model.occ.addCurveLoop([l_ano_up, l_ano_dw, l_ano_mid_dw, l_mid_cat_dw, l_ano_mid_up, l_mid_cat_up])
tri = gmsh.model.occ.addPlaneSurface([ctri])

# get the lines for the fragment
l_oth = [(1, l_box_ano), (1, l_box_cat), (1, l_cat_up), (1, l_cat_dw)]
l_ext = [(1, l_ano_up), (1, l_ano_dw), (1, l_ano_mid_dw), (1, l_mid_cat_dw), (1, l_ano_mid_up), (1, l_mid_cat_up)]
l_int = [(1, l_mid_ano_up), (1, l_mid_ano_dw), (1, l_mid_up_dw)]

# fragment the mesh
(out, outmap) = gmsh.model.occ.fragment([(2, box)], [(2, tri)] + l_oth + l_ext + l_int)
gmsh.model.occ.synchronize()

# get the different domains
box = outmap[0]
diode = outmap[1]
bnd = outmap[2:12]

# flatten the bnd indices
bnd = [item for sublist in bnd for item in sublist]
mesh = gmsh.model.getBoundary(diode, oriented = False)

# get the domain / boundary indices
idx_bnd = [idx for (_, idx) in bnd]
idx_box = [idx for (_, idx) in box]
idx_diode = [idx for (_, idx) in diode]
idx_mesh = [idx for (_, idx) in mesh]
idx_air = list(set(idx_box) - set(idx_diode))

# set the groups
gmsh.model.addPhysicalGroup(2, idx_air, name="air")
gmsh.model.addPhysicalGroup(2, idx_diode, name="diode")
gmsh.model.addPhysicalGroup(1, idx_bnd, name="bnd")

# set the field for the mesh
field_bnd = gmsh.model.mesh.field.add("Distance")
gmsh.model.mesh.field.setNumbers(1, "CurvesList", idx_mesh)
gmsh.model.mesh.field.setNumber(1, "Sampling", 5)

# set the field for the threshold mesh
field_mesh = gmsh.model.mesh.field.add("Threshold")
gmsh.model.mesh.field.setNumber(2, "InField", field_bnd)
gmsh.model.mesh.field.setNumber(2, "SizeMin", 0.4)
gmsh.model.mesh.field.setNumber(2, "SizeMax", 1.0)
gmsh.model.mesh.field.setNumber(2, "DistMin", 0.1)
gmsh.model.mesh.field.setNumber(2, "DistMax", 1.5)

# generate the mesh
gmsh.option.setNumber("Mesh.MeshSizeFactor", 1.5)
gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 1.0)
gmsh.model.mesh.field.setAsBackgroundMesh(field_mesh)
gmsh.model.mesh.generate(2)

# save and show the results
gmsh.write("otvam.msh")
gmsh.fltk.run()
gmsh.finalize()
