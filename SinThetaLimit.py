from manimlib import *
import numpy as np

class SinThetaLimit(InteractiveScene):
    def construct(self):
        r = 1  # Fixed radius
        theta_tracker = ValueTracker(PI/2)
        theta = theta_tracker.get_value
        circle_color = BLUE
        vector_color = WHITE

        def get_vector(theta):
            mag = r / theta if theta != 0 else 0
            x = mag * np.cos(theta) if theta != 0 else r
            y = mag * np.sin(theta) if theta != 0 else 0
            return np.array([x, y, 0])

        # Circle for reference
        radius = r / theta()  # start with theta=0.3

        circle = Circle(radius=radius, stroke_color=circle_color)
        vector = Arrow(ORIGIN, get_vector(theta()), buff=0, stroke_color=vector_color)

        self.play(ShowCreation(circle))
        self.play(GrowArrow(vector))

        circle.add_updater(lambda c: c.become(Circle(radius=r/theta(), stroke_color=circle_color)))
        vector.add_updater(lambda a: a.become(Arrow(ORIGIN, get_vector(theta()), buff=0, fill_color=vector_color, stroke_width=min(3, 1/theta()))))

        # Trace path of tip of the vector
        dot = always_redraw(lambda: Dot(get_vector(theta_tracker.get_value()), color=RED))
        self.add(dot)

        self.play(theta_tracker.animate.set_value(0.1),
                  self.frame.animate.reorient(0, 0, 0, (0, 0, 0.0), 21),
                  run_time=3)

        # Label for sin(theta)/theta
        label = Tex(r"\lim_{\theta \to 0} \frac{\sin(\theta)}{\theta} = 1")
        label.to_corner(UP + RIGHT)
        self.play(Write(label))

        self.wait(3)
