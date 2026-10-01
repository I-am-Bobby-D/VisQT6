import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from camera import Camera
from quaternion import Quaternion
from IO import IO

# scene as data class vs current state as renderer
# Vertex and Fragment Shaders
VERTEX_SHADER_SOURCE = """
#version 330 core
layout (location = 0) in vec3 position;
uniform mat4 projection;
uniform mat4 view;
void main()
{
    gl_Position = projection * view * vec4(position, 1.0);
}
"""

FRAGMENT_SHADER_SOURCE = """
#version 330 core
out vec4 FragColor;
uniform vec3 color;
void main()
{
    FragColor = vec4(color, 1.0);
}
"""

class GLWidget(IO, QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.show_axes = True
        self.camera = Camera()

    def initializeGL(self):
        # Compile shaders
        vertex_shader = compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER)
        fragment_shader = compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)
        self.shader_program = compileProgram(vertex_shader, fragment_shader)

        # Define axes lines (X, Y, Z)
        self.vertices = np.array([
            # X axis
            -1.0, 0.0, 0.0,  1.0, 0.0, 0.0,
            # Y axis
             0.0, -1.0, 0.0,  0.0, 1.0, 0.0,
            # Z axis
             0.0, 0.0, -1.0,  0.0, 0.0, 1.0,
        ], dtype=np.float32)

        # Create VAO and VBO
        # Vertex Array Object: contains glVertexAttribPointer
        # Vertex Buffer Object: stores vertex data
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * self.vertices.itemsize, None)
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        glEnable(GL_DEPTH_TEST)


    # Called by default: __init__-> initializeGL - > resizeGL -> paintGL
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.1, 1.0)

        glUseProgram(self.shader_program)

        # Set projection and view matrices using camera instance methods
        projection = self.camera.perspective(np.radians(45), self.width() / self.height(), 0.1, 100.0)
        view = self.camera.lookAt()

        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "projection"), 1, GL_FALSE, projection)
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "view"), 1, GL_FALSE, view)

        if self.show_axes:
            glBindVertexArray(self.VAO)

            # Draw X axis (red)
            glUniform3f(glGetUniformLocation(self.shader_program, "color"), 1.0, 0.0, 0.0)
            glDrawArrays(GL_LINES, 0, 2)

            # Draw Y axis (green)
            glUniform3f(glGetUniformLocation(self.shader_program, "color"), 0.0, 1.0, 0.0)
            glDrawArrays(GL_LINES, 2, 2)

            # Draw Z axis (blue)
            glUniform3f(glGetUniformLocation(self.shader_program, "color"), 0.0, 0.0, 1.0)
            glDrawArrays(GL_LINES, 4, 2)

            glBindVertexArray(0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
