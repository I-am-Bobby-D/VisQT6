import numpy as np
import quaternion
# Example: Rotate Camera Using Quaternions
class Camera:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 3.0])
        self.orientation = Quaternion(1, 0, 0, 0)  # Identity quaternion

    def rotate(self, axis, angle):
        """Rotate the camera by `angle` (in radians) around `axis`."""
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

    def get_view_matrix(self):
        """Compute the view matrix from the camera's quaternion orientation."""
        rotation_matrix = self.orientation.to_rotation_matrix()
        translation = -self.position
        view_matrix = np.eye(4, dtype=np.float32)
        view_matrix[:3, :3] = rotation_matrix
        view_matrix[:3, 3] = rotation_matrix @ translation
        return view_matrix
