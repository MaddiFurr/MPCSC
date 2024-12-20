import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import random

# Define vertices, edges, and surfaces for a cube
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

def draw_cube(position, rotation, color):
    glPushMatrix()
    glTranslatef(*position)
    glRotatef(rotation[0], 1, 0, 0)
    glRotatef(rotation[1], 0, 1, 0)
    glRotatef(rotation[2], 0, 0, 1)
    
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glColor3fv(color)
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    
    glPopMatrix()

def draw_sphere(position, radius, color):
    glPushMatrix()
    glTranslatef(*position)
    glColor3fv(color)
    quad = gluNewQuadric()
    gluSphere(quad, radius, 32, 32)
    gluDeleteQuadric(quad)
    glPopMatrix()

def draw_particle(position):
    glPushMatrix()
    glTranslatef(*position)
    glBegin(GL_POINTS)
    glColor3fv((1, 1, 1))
    glVertex3fv((0, 0, 0))
    glEnd()
    glPopMatrix()

def gpu_stress_test(duration=60):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    clock = pygame.time.Clock()
    start_time = time.time()
    end_time = start_time + duration
    frame_count = 0

    num_shapes = 10  # Reduced number of shapes to avoid overwhelming the GPU
    positions = [(random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5)) for _ in range(num_shapes)]
    velocities = [(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)) for _ in range(num_shapes)]
    rotations = [(random.uniform(0, 360), random.uniform(0, 360), random.uniform(0, 360)) for _ in range(num_shapes)]
    colors = [(random.random(), random.random(), random.random()) for _ in range(num_shapes)]
    shapes = [random.choice(['cube', 'sphere']) for _ in range(num_shapes)]

    particles = [(random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5)) for _ in range(100)]
    particle_velocities = [(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)) for _ in range(100)]

    while time.time() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return frame_count

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(num_shapes):
            # Update positions
            positions[i] = (
                positions[i][0] + velocities[i][0],
                positions[i][1] + velocities[i][1],
                positions[i][2] + velocities[i][2]
            )
            # Bounce off walls
            for j in range(3):
                if positions[i][j] > 5 or positions[i][j] < -5:
                    velocities[i] = (
                        velocities[i][0] * (-1 if j == 0 else 1),
                        velocities[i][1] * (-1 if j == 1 else 1),
                        velocities[i][2] * (-1 if j == 2 else 1)
                    )
            # Update rotations
            rotations[i] = (rotations[i][0] + 1, rotations[i][1] + 1, rotations[i][2] + 1)
            if shapes[i] == 'cube':
                draw_cube(positions[i], rotations[i], colors[i])
            elif shapes[i] == 'sphere':
                draw_sphere(positions[i], 1, colors[i])

        for i in range(len(particles)):
            # Update particle positions
            particles[i] = (
                particles[i][0] + particle_velocities[i][0],
                particles[i][1] + particle_velocities[i][1],
                particles[i][2] + particle_velocities[i][2]
            )
            # Bounce off walls
            for j in range(3):
                if particles[i][j] > 5 or particles[i][j] < -5:
                    particle_velocities[i] = (
                        particle_velocities[i][0] * (-1 if j == 0 else 1),
                        particle_velocities[i][1] * (-1 if j == 1 else 1),
                        particle_velocities[i][2] * (-1 if j == 2 else 1)
                    )
            draw_particle(particles[i])

        pygame.display.flip()
        frame_count += 1

        elapsed_time = int(time.time() - start_time)
        percentage_complete = (elapsed_time / duration) * 100

        # Update window title with FPS, total frames rendered, and percentage complete
        fps = clock.get_fps()
        pygame.display.set_caption(f"GPU Benchmark - FPS: {fps:.2f} | Frames: {frame_count} | {percentage_complete:.2f}% Complete")

        # Remove the frame rate limit
        clock.tick(0)

    pygame.quit()
    return frame_count

# Example usage
if __name__ == "__main__":
    duration = 60  # Run the benchmark for 60 seconds
    print(f"Starting GPU stress test for {duration} seconds...")
    score = gpu_stress_test(duration)
    print(f"\nGPU Benchmark Score: {score} frames")