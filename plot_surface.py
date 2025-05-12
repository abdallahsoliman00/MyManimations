from manimlib import *
import numpy as np

def func():
    x = np.linspace(-3, 3, 60)
    y = np.linspace(-3, 3, 60)
    X, Y = np.meshgrid(x, y)
    Z = 5*np.sin(X**2 + Y**2) / (X**2 + Y**2 + 1)
    return X, Y, Z

class SurfacePlot3D(InteractiveScene):
    def construct(self):
        self.frame.reorient(-14, 47, 0, (-0.32, -0.26, 1.13), 8.66)

        axes = ThreeDAxes()

        x_label = Tex("x").scale(1.5).move_to(axes.c2p(np.max(axes.x_range) + 0.5, 0, 0))
        y_label = Tex("y").scale(1.5).move_to(axes.c2p(0, np.max(axes.y_range) + 0.5, 0))
        z_label = Tex("z").scale(1.5).move_to(axes.c2p(0, 0, np.max(axes.z_range) + 0.5)).rotate(PI/2, axis=RIGHT)

        self.add(axes, x_label, y_label, z_label)

        self.add(axes)

        x_mesh, y_mesh, z_mesh = func()
        n_rows, n_cols = x_mesh.shape

        z_max = np.max(z_mesh)/2
        z_min = np.min(z_mesh)/2

        def param_surface(u, v):
            i = min(int(u * (n_rows - 1)), n_rows - 1)
            j = min(int(v * (n_cols - 1)), n_cols - 1)

            x = x_mesh[i, j]
            y = y_mesh[i, j]
            z = z_mesh[i, j]

            return axes.c2p(x, y, z)  # lock to axes!

        surface = ParametricSurface(
            param_surface,
            u_range=[0, 1],
            v_range=[0, 1],
            opacity=0.8,
            resolution=(n_rows, n_cols),
            color=PURPLE
        )

        def rgb_func(point):
            # Extract the height (z-value)
            x, y, z = point
            
            # Normalize z to [0, 1] where 0 is lowest and 1 is highest
            normalized_z = np.clip((z - z_min) / (z_max - z_min), 0, 1)
            
            # Yellow RGB: (1, 1, 0)
            # Dark Blue RGB: (0, 0, 0.5)
            # Linear interpolation between the two colors
            r = 1 - normalized_z  # From 1 (yellow) to 0 (dark blue)
            g = 1 - normalized_z  # From 1 (yellow) to 0 (dark blue)
            b = 0.5 * normalized_z  # From 0 (yellow) to 0.5 (dark blue)
            
            return np.array([r, g, b])
        
        # Apply the RGB function to the surface
        surface.set_color_by_rgb_func(rgb_func)

        self.add(surface)
        self.wait(2)
