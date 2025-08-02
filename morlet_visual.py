from manimlib import *
import numpy as np

class Morlet(InteractiveScene):
    def construct(self):

        f0_tracker = ValueTracker(1)  # Create a ValueTracker for f0
        tau = 4

        ax = ThreeDAxes(
            x_range=(-2, 2, 1),
            y_range=(0, 10, 1),
            z_range=(-2, 2, 1)
        )
        self.add(ax)

        t = np.linspace(0, 10, 1000)
        T = t - tau

        curve = VMobject()

        def update_curve(mob):
            f0 = f0_tracker.get_value()  # Get the current value of f0 from the tracker
            omega_0 = 2 * np.pi * f0  # Update omega_0 based on f0
            x = (np.exp(-T**2 / 2)) * np.sin(omega_0 * t)  # Recalculate x
            y = t
            z = (np.exp(-T**2 / 2)) * np.cos(omega_0 * t)  # Recalculate z
            points = ax.c2p(x, y, z)
            mob.set_points_smoothly(points)

        curve.add_updater(update_curve)
        self.add(curve)

        self.frame.reorient(93, 75, 0)
        # Shift + D to copy coordinates


        # Animate f0 changing from 1 to 5 over 10 seconds
        while True:

            self.play(f0_tracker.animate.set_value(4), run_time=8, rate_func=linear)
            self.play(f0_tracker.animate.set_value(1), run_time=8, rate_func=linear)        

