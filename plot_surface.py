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

        axes = ThreeDAxes((-3, 3),(-3, 3))

        x_label = Tex("x").scale(1.5).move_to(axes.c2p(np.max(axes.x_range) + 0.5, 0, 0))
        y_label = Tex("y").scale(1.5).move_to(axes.c2p(0, np.max(axes.y_range) + 0.5, 0))
        z_label = Tex("z").scale(1.5).move_to(axes.c2p(0, 0, np.max(axes.z_range) + 0.5)).rotate(PI/2, axis=RIGHT)

        self.add(axes, x_label, y_label, z_label)

        self.add(axes)

        def surface_func(u, v):
            r2 = (u**2 + v**2)**0.1
            z = 5 * np.sin(r2 * self.time) / (r2 + 1)
            return u,v,z

        surface = ParametricSurface(
            surface_func,
            u_range=(-3, 3),
            v_range=(-3, 3),
            resolution=(120, 120),
            color=PURPLE,
            opacity=0.8
        )

        def color_by_z(points: np.ndarray) -> np.ndarray:
            z = points[:, 2]  # take z column
            # Normalize x into range [0, 1]
            z_norm = (z - z.min()) / (z.max() - z.min() + 1e-8)
            
            # Build RGB: red increases with x, blue decreases
            r = z_norm
            g = np.zeros_like(z_norm)
            b = 1 - z_norm
            return np.stack((r, g, b), axis=1)

        
        # Apply the RGB function to the surface
        surface.set_color_by_rgb_func(color_by_z)

        surface.add_updater(lambda mob: mob.become(
            ParametricSurface(
                surface_func,
                u_range=(-3, 3),
                v_range=(-3, 3),
                resolution=(120, 120),
                opacity=0.8
            ).set_color_by_rgb_func(color_by_z)
        ))


        self.add(surface)
        self.wait(20)
