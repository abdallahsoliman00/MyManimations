import numpy as np
from manimlib import *


x = np.arange(-5, 6, 1)
np.random.seed(42)
noise = np.random.rand(len(x)) * -1.5
y = 0.6*(np.array([-4.3, -4.5, -2, -2.6, -1.5, -0.9, 1.5, 2.1, 3.5, 3.1, 4.2]) + noise)

print(x,y)


def calc_mse(x, y, init_mc):
    m,c = init_mc
    y_act = m*x +c
    err = y-y_act
    mse = np.mean(err**2)
    return mse


# Finds the gradient in n-dimensions of a function at a point
def grad(x , y, coords, epsilon=0.01):
    args = (x,y)
    coords = np.array(coords)
    grad_vector = np.array([])
    for i in range(2):
        # for each dimension calculate the gradient
        offset = np.zeros(2)
        offset[i] += epsilon    # create a vector with an offset to a coordinate e.g. [0, 0.01, 0]

        coordinates_l = coords - offset
        lower = calc_mse(*args, coordinates_l)

        coordinates_u = coords + offset
        upper = calc_mse(*args, coordinates_u)

        grad = ((upper - lower)/(2*epsilon))
        grad_vector = np.append(grad_vector, grad)
    return grad_vector


def grad_descent(x, y, init_mc, alpha=0.001, epsilon=0.01):
    coords = np.array(init_mc)
    count = 0
    path = [coords.copy()]  # Store the path
    while True:
        gradient = grad(x, y, coords, epsilon)
        coords = coords - alpha * gradient
        path.append(coords.copy())  # Store each point
        count += 1
        if np.linalg.norm(gradient) < 1e-5 or count > 10000:
            print("\nIterations:", count)
            return coords, np.array(path)

# Get the result and path
result, descent_path = grad_descent(x, y, (-0.7, 1))
res2, descent_path2 = grad_descent(x, y, (0.5,-2.5))

print("Optimal m, c:", result)


class GradientDescentAnimation(InteractiveScene):
    def construct(self):
        # Create axes with adjusted scales
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],   # Smaller m range
            y_range=[-3, 3, 1],       # Smaller c range
            z_range=[0, 500, 100],         # Same MSE range
            depth=7,
            height=7,
            width=7
        )
        axes.set_width(FRAME_WIDTH * 0.8)  # Make axes slightly smaller
        
        # Add numerical labels and axis labels
        axes.add_coordinate_labels(
            font_size=24,
            num_decimal_places=1
        )
        axes.add_axis_labels(
            x_tex="m",
            y_tex="c",
            z_tex="MSE",
            font_size=24
        )
        
        # Center everything
        axes.move_to(ORIGIN)
        self.add(axes)

        self.frame.reorient(-68, 92, 0, (0.26, -1.15, -3.66), 7.76)
        
        # Function to calculate MSE for any m, c
        def mse_func(m, c):
            y_pred = m * x + c
            err = y - y_pred
            return np.sum(err**2)
        
        # Create MSE surface with higher resolution
        surface = ParametricSurface(
            lambda u, v: axes.c2p(u, v, mse_func(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
            color=PURPLE,
            opacity=0.2            # Very transparent surface
        )

        surface.mesh = SurfaceMesh(surface,
                                   normal_nudge= -1e-2,
                                   stroke_color=BLUE_E,
                                   stroke_width=0.8)

        
        # Create the path from the stored descent path
        # Filter points to stay within our visible range
        visible_path1 = []
        for m, c in descent_path:
            if (-3 <= m <= 3) and (-3 <= c <= 3):
                visible_path1.append([m, c])
        
        points1 = [axes.c2p(m, c, mse_func(m, c)) for m, c in visible_path1]
        path1 = VMobject()
        path1.set_points_smoothly(points1)
        path1.set_stroke(RED, 3)
        
        # Initial and target points
        point = Sphere(radius=0.05, color=RED)
        point.move_to(points1[0])
        
        target_point = Sphere(radius=0.05, color=GREEN)
        target_point.move_to(points1[-1])


        # Create the path from the stored descent path
        # Filter points to stay within our visible range
        visible_path2 = []
        for m, c in descent_path2:
            if (-3 <= m <= 3) and (-3 <= c <= 3):
                visible_path2.append([m, c])
        
        points2 = [axes.c2p(m, c, mse_func(m, c)) for m, c in visible_path2]
        path2 = VMobject()
        path2.set_points_smoothly(points2)
        path2.set_stroke(YELLOW, 3)
        
        # Initial and target points
        point = Sphere(radius=0.05, color=RED)
        point.move_to(points2[0])
        
        target_point = Sphere(radius=0.05, color=GREEN)
        target_point.move_to(points2[-1])
        
        self.wait(2)

        # Add everything to scene
        self.play(
            ShowCreation(surface),
            ShowCreation(surface.mesh)
        )
        self.add(target_point)
        
        # Create the point that will move
        moving_point1 = Sphere(radius=0.05, color=RED)
        moving_point2 = Sphere(radius=0.05, color=YELLOW)
        self.add(moving_point1)
        self.add(moving_point2)
        
        # Loop the animation until window is closed
        while True:
            # Reset point to start
            moving_point1.move_to(points1[0])
            moving_point2.move_to(points2[0])
            
            # Animate along path
            self.play(
                ShowCreation(path1),
                ShowCreation(path2),
                MoveAlongPath(moving_point1, path1),
                MoveAlongPath(moving_point2, path2),
                run_time=5,
                rate_func=smooth
            )
            
            # Clear the path to prepare for next iteration
            path1.clear_points()
            path1.set_points_smoothly(points1)
            path2.clear_points()
            path2.set_points_smoothly(points2)
            
            self.wait(1)  # Brief pause between iterations


