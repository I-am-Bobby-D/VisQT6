import numpy as np
from quaternion import Quaternion
# Example: Rotate Camera Using Quaternions
class Camera:
    def __init__(self):
        self.eye = np.array([3.0, 3.0, 3.0], dtype=np.float32)
        self.center = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.orientation = Quaternion(1, 0, 0, 0)  # Identity quaternion



    # Moved from scene.py, used in paintGL setup
    def lookAt(self):
        f = self.center - self.eye
        f = f / np.linalg.norm(f)
        s = np.cross(f, self.up)
        s = s / np.linalg.norm(s)
        u = np.cross(s, f)

        return np.array([
            [s[0], u[0], -f[0], 0.0],
            [s[1], u[1], -f[1], 0.0],
            [s[2], u[2], -f[2], 0.0],
            [-np.dot(s, self.eye), -np.dot(u, self.eye), np.dot(f, self.eye), 1.0]
        ], dtype=np.float32)

    #Used in paintGL setup
    def perspective(self, fovy, aspect, znear, zfar):
        f = 1.0 / np.tan(fovy / 2)
        return np.array([
            [f / aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (zfar + znear) / (znear - zfar), -1],
            [0, 0, (2 * zfar * znear) / (znear - zfar), 0]
        ], dtype=np.float32)


    #Not used,
    def rotate(self, axis, angle):
       #"""Rotate the camera by `angle` (in radians) around `axis`."""
        axis = axis / np.linalg.norm(axis)
        half_angle = angle / 2
        sin_half_angle = np.sin(half_angle)
        rotation = Quaternion(
            np.cos(half_angle),
            axis[0] * sin_half_angle,
            axis[1] * sin_half_angle,
            axis[2] * sin_half_angle
        )
        self.orientation = self.orientation * rotation
