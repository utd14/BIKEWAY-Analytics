import open3d as o3d
import numpy as np

# Task 1
print("Task 1: Loading and Visualization")
mesh = o3d.io.read_triangle_mesh("D:\Classes\Data Visualization\Assignment4\Assignment5\eyeball\eyeball.ply") 
o3d.visualization.draw_geometries([mesh], window_name="Original Mesh", width=1024, height=768)

print(f"Number of vertices: {len(mesh.vertices)}")
print(f"Number of triangles: {len(mesh.triangles)}")
print(f"Has colors: {mesh.has_vertex_colors()}")
print(f"Has normals: {mesh.has_vertex_normals()}")
print()

# Task 2
print("Task 2: Conversion to Point Cloud")
pcd = o3d.io.read_point_cloud("D:\Classes\Data Visualization\Assignment4\Assignment5\eyeball\eyeball.ply")  
o3d.visualization.draw_geometries([pcd], window_name="Conversion to Point Cloud", width=1024, height=768)

print(f"Number of vertices: {len(pcd.points)}")
print(f"Has colors: {pcd.has_colors()}")
print()

# Task 3
print("Task 3: Surface Reconstruction from Point Cloud")
pcd.estimate_normals()
mesh_poisson, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
bbox = pcd.get_axis_aligned_bounding_box()
mesh_poisson = mesh_poisson.crop(bbox)
o3d.visualization.draw_geometries([mesh_poisson], window_name="Reconstructed Mesh (Poisson)", width=1024, height=768)

print(f"Number of vertices: {len(mesh_poisson.vertices)}")
print(f"Number of triangles: {len(mesh_poisson.triangles)}")
print(f"Has colors: {mesh_poisson.has_vertex_colors()}")
print()

# Task 4
print("Task 4: Voxelization")
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.05)
o3d.visualization.draw_geometries([voxel_grid], window_name="Voxelized Model", width=1024, height=768)

print(f"Number of voxels: {len(voxel_grid.get_voxels())}")
print(f"Has colors: True")
print()

# Task 5
print("Task 5: Adding a Plane")
vertices = np.asarray(mesh_poisson.vertices)
center = vertices.mean(axis=0)
size = 2.0

plane_mesh = o3d.geometry.TriangleMesh.create_box(width=size, height=size, depth=0.01)
plane_mesh.translate([center[0] - size/2, center[1] - size/2, center[2]])
plane_mesh.paint_uniform_color([0.3, 0.3, 0.3])
o3d.visualization.draw_geometries([mesh_poisson, plane_mesh], window_name="Plane + Original Mesh", width=1024, height=768)

print("Plane added next to the object")
print()

# Task 6
print("Task 6: Surface Clipping")
vertices = np.asarray(mesh_poisson.vertices)
plane_z = center[2]
mask = vertices[:, 2] < plane_z
indices = np.where(mask)[0]
mesh_clipped = mesh_poisson.select_by_index(indices)
o3d.visualization.draw_geometries([mesh_clipped], window_name="Clipped Mesh (Right removed)", width=1024, height=768)

print(f"Number of remaining vertices: {len(mesh_clipped.vertices)}")
print(f"Number of triangles: {len(mesh_clipped.triangles)}")
print(f"Has colors: {mesh_clipped.has_vertex_colors()}")
print(f"Has normals: {mesh_clipped.has_vertex_normals()}")
print()

# Task 7
print("Task 7: Working with Color and Extremes")
vertices = np.asarray(mesh_clipped.vertices)
z_coords = vertices[:, 2]
z_min, z_max = z_coords.min(), z_coords.max()
z_normalized = (z_coords - z_min) / (z_max - z_min)

colors = np.zeros((len(vertices), 3))
colors[:, 0] = 1 - z_normalized
colors[:, 2] = z_normalized
colors[:, 1] = 0.5

mesh_clipped.vertex_colors = o3d.utility.Vector3dVector(colors)

min_idx = np.argmin(z_coords)
max_idx = np.argmax(z_coords)
min_point = vertices[min_idx]
max_point = vertices[max_idx]

wireframe_min = o3d.geometry.TriangleMesh.create_box(width=0.1, height=0.1, depth=0.1)
wireframe_min.translate(min_point - 0.05)
wireframe_min.paint_uniform_color([0, 0, 1])

wireframe_max = o3d.geometry.TriangleMesh.create_box(width=0.1, height=0.1, depth=0.1)
wireframe_max.translate(max_point - 0.05)
wireframe_max.paint_uniform_color([1, 0, 0])

o3d.visualization.draw_geometries([mesh_clipped, wireframe_min, wireframe_max], 
                                  window_name="3D Model with Z-Extremes and Axes", width=1024, height=768)

print(f"Minimum Z coordinates: {min_point}")
print(f"Maximum Z coordinates: {max_point}")