import numpy as np
from PyQt6.QtCore import Qt
from quaternion import Quaternion

class IO:
# Left click for panning
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = event.position()

# Capture mouse movement
    def mouseMoveEvent(self, event):
        if self.last_mouse_pos is None:
            return

        delta = event.position() - self.last_mouse_pos
        self.last_mouse_pos = event.position()

        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            offset = self.camera.eye - self.camera.center

            # Horizontal orbit
            angle = -delta.x() * 0.01
            q = Quaternion(
                np.cos(angle / 2),
                0,
                np.sin(angle / 2),
                0
            )
            offset = q.to_rotation_matrix() @ offset

            # Vertical orbit
            right = np.cross(
                self.camera.center - self.camera.eye,
                self.camera.up
            )
            right /= np.linalg.norm(right)

            angle = -delta.y() * 0.01
            q = Quaternion(
                np.cos(angle / 2),
                *(right * np.sin(angle / 2))
            )
            offset = q.to_rotation_matrix() @ offset

            self.camera.eye = self.camera.center + offset

        else:
            # Pan
            pan_speed = 0.01
            right = np.cross(self.camera.center - self.camera.eye, self.camera.up)
            right /= np.linalg.norm(right)
            up = np.cross(right, self.camera.center - self.camera.eye)
            up /= np.linalg.norm(up)

            self.camera.eye += -delta.x() * pan_speed * right + delta.y() * pan_speed * up
            self.camera.center += -delta.x() * pan_speed * right + delta.y() * pan_speed * up

        self.update()

# Capture mouse release event
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = None
