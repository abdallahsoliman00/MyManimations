import numpy as np
from manimlib import *


x = np.linspace(0, 5, 20)
true_m_nonlin = np.array([2.0, 0.5])
y_obs_nonlin = np.sin(true_m_nonlin[0] * x + true_m_nonlin[1])

def cost_nonlinear(m1, m2):
    y_pred = np.sin(m1 * x + m2)
    residual = y_obs_nonlin - y_pred
    return 0.5 * np.sum(residual**2)

# Gradient via finite difference
def grad_nonlinear(coords, epsilon=1e-3):
    grad = np.zeros(2)
    for i in range(2):
        offset = np.zeros(2)
        offset[i] = epsilon
        f_plus = cost_nonlinear(*(coords + offset))
        f_minus = cost_nonlinear(*(coords - offset))
        grad[i] = (f_plus - f_minus) / (2 * epsilon)
    return grad

def grad_descent(init_coords, alpha=0.01, tol=1e-6, max_iter=5000):
    coords = np.array(init_coords, dtype=float)
    path = [coords.copy()]
    for _ in range(max_iter):
        g = grad_nonlinear(coords)
        coords -= alpha * g
        path.append(coords.copy())
        if np.linalg.norm(g) < tol:
            break
    return np.array(path)

# Run gradient descent from two initial guesses
path1 = grad_descent((3.5,1.5))
path2 = grad_descent((1.1,2.2))



class NonlinearGradientDescent(InteractiveScene):
    def construct(self):
        # Axes for parameter space
        axes = ThreeDAxes(
            x_range=[0, 4, 1],    # m1 range
            y_range=[-1, 3, 1],   # m2 range
            z_range=[0, 20, 5],   # cost range
            height=7,
            width=7,
            depth=7
        )
        axes.add_coordinate_labels(font_size=20, num_decimal_places=1)
        axes.add_axis_labels("m_1", "m_2", "J(m_1,m_2)", font_size=24)
        self.add(axes)
        self.frame.reorient(27, 61, 0, (-0.81, 0.75, 2.27), 11.40)

        # Cost surface
        surface = ParametricSurface(
            lambda u, v: axes.c2p(u, v, cost_nonlinear(u, v)),
            u_range=[0, 4],
            v_range=[-1, 3],
            resolution=(40, 40),
            color=PURPLE,
            opacity=0.25
        )
        surface_mesh = SurfaceMesh(surface, stroke_color=BLUE_E, stroke_width=0.5)

        # Convert path to points in 3D
        def path_to_points(path):
            return [axes.c2p(m1, m2, cost_nonlinear(m1, m2)) for m1, m2 in path]

        points1 = path_to_points(path1)
        points2 = path_to_points(path2)

        path_curve1 = VMobject().set_points_smoothly(points1).set_stroke(RED, 3)
        path_curve2 = VMobject().set_points_smoothly(points2).set_stroke(YELLOW, 3)

        # Moving spheres
        dot1 = Sphere(radius=0.06, color=RED).move_to(points1[0])
        dot2 = Sphere(radius=0.06, color=YELLOW).move_to(points2[0])

        # Add objects
        self.play(ShowCreation(surface), ShowCreation(surface_mesh))
        self.wait(1)
        self.add(dot1, dot2)

        # Animate descent
        self.play(
            ShowCreation(path_curve1),
            ShowCreation(path_curve2),
            MoveAlongPath(dot1, path_curve1),
            MoveAlongPath(dot2, path_curve2),
            run_time=6,
            rate_func=smooth
        )
