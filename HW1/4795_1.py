import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Set up the parameters
light_position = np.array([10, 10, 10])
camera_position = np.array([0, 0, 10])
camera_target = np.array([0, 0, 0])
object_position = np.array([0, 0, 0])
object_rotation = np.radians([0, 0, 0])  # Rotations around x, y, and z axes in degrees
fov = np.radians(90)
near = 1.0
far = 100.0
aspect_ratio = 1.0
M_diff = np.array([0, 1, 1])  # Cyan color

# Load the 3D model (assumed to be in a file called 'model.raw')
def load_raw_model(file_path):
    vertices = []
    with open(file_path) as f:
        for line in f:
            vertices.append(list(map(float, line.strip().split())))
    vertices = np.array(vertices).reshape(-1, 3, 3)  # Each row contains three vertices of a triangle
    return vertices

vertices = load_raw_model('model.raw')

def create_rotation_matrix(rx, ry, rz):
    cx, cy, cz = np.cos([rx, ry, rz])
    sx, sy, sz = np.sin([rx, ry, rz])

    Rx = np.array([
        [1, 0, 0],
        [0, cx, -sx],
        [0, sx, cx]
    ])

    Ry = np.array([
        [cy, 0, sy],
        [0, 1, 0],
        [-sy, 0, cy]
    ])

    Rz = np.array([
        [cz, -sz, 0],
        [sz, cz, 0],
        [0, 0, 1]
    ])

    return Rz @ Ry @ Rx

def create_translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def create_view_matrix(camera_pos, camera_target):
    forward = camera_target - camera_pos
    forward = forward.astype(np.float64)  # Ensure forward is of float type
    forward /= np.linalg.norm(forward)
    right = np.cross([0, 1, 0], forward)
    right /= np.linalg.norm(right)
    up = np.cross(forward, right)

    view_matrix = np.array([
        [right[0], right[1], right[2], -np.dot(right, camera_pos)],
        [up[0], up[1], up[2], -np.dot(up, camera_pos)],
        [forward[0], forward[1], forward[2], -np.dot(forward, camera_pos)],
        [0, 0, 0, 1]
    ])

    return view_matrix

def create_perspective_matrix(fov, aspect, near, far):
    f = 1 / np.tan(fov / 2)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ])

# Create rotation matrix for 45 degrees around x-axis
rotation_matrix = create_rotation_matrix(*object_rotation)
translation_matrix = np.identity(4)

world_matrix = np.identity(4)
world_matrix[:3, :3] = rotation_matrix

view_matrix = create_view_matrix(camera_position, camera_target)
projection_matrix = create_perspective_matrix(fov, aspect_ratio, near, far)

# Transformation: World -> View -> Projection
def transform_vertices(vertices, world_matrix, view_matrix, projection_matrix):
    transformed_vertices = []
    for triangle in vertices:
        transformed_triangle = []
        for vertex in triangle:
            # Convert to homogeneous coordinates
            vertex = np.append(vertex, 1)
            # Apply transformations
            vertex = vertex @ world_matrix
            vertex = vertex @ view_matrix
            vertex = vertex @ projection_matrix
            # Perspective divide
            vertex /= vertex[3]
            transformed_triangle.append(vertex[:3])
        transformed_vertices.append(transformed_triangle)
    return np.array(transformed_vertices)

def compute_normal(triangle):
    v1, v2, v3 = triangle
    normal = np.cross(v2 - v1, v3 - v1)
    normal /= np.linalg.norm(normal)
    return normal

def compute_lighting(triangle, normal, light_position, M_diff):
    center = np.mean(triangle, axis=0)
    light_dir = light_position - center
    light_dir /= np.linalg.norm(light_dir)
    intensity = np.dot(normal, light_dir)
    intensity = max(0, intensity)  # Clamp to [0, 1]
    color = intensity * M_diff
    return color

transformed_vertices = transform_vertices(vertices, world_matrix, view_matrix, projection_matrix)

# Z-sorting
triangles = [(triangle, np.mean(triangle, axis=0)[2]) for triangle in transformed_vertices]
triangles.sort(key=lambda x: x[1], reverse=True)

# Rendering
fig, ax = plt.subplots()
ax.set_aspect('equal')

for triangle, _ in triangles:
    normal = compute_normal(triangle)
    color = compute_lighting(triangle, normal, light_position, M_diff)
    polygon = Polygon(triangle[:, :2], facecolor=color, edgecolor='k', alpha=0.5)
    ax.add_patch(polygon)

# Setting the limits for the axes
max_range = np.array([vertices[:, :, i].max() - vertices[:, :, i].min() for i in range(3)]).max() / 2.0

mid_x = (vertices[:, :, 0].max() + vertices[:, :, 0].min()) * 0.5
mid_y = (vertices[:, :, 1].max() + vertices[:, :, 1].min()) * 0.5

ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)

ax.set_title('DIY 3-D Rendering')

plt.show()
