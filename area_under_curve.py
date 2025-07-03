from manimlib import *


class AreaUnderCurve(InteractiveScene):
    
    def construct(self):
        self.set_background_color("#000000")
        # Create Axes and curve
        ax = Axes(
            x_range=(0,4,1),
            y_range=(0,4,1),
            width=6,
            height=6
            )
        
        x = np.linspace(0,4,2001)
        dx_actual = x[1] - x[0]
        def func(x): return 0.4 * ((x + 0.3 - 4) * ((x + 0.3 - 1.5)**2) + 6)
        y = func(x)

        curve = VMobject(z_index=100)
        curve.set_points_smoothly(ax.c2p(x,y))
        curve.set_stroke(BLUE, 3)
        
        # Create axes and curve
        self.play(
            ShowCreation(ax),
            ShowCreation(curve)
        )

        # Add estimation bars
        def get_rectangle_corners(func, x, dx, axes):
            y = func(x)
            return [axes.c2p(x, 0, 0), axes.c2p(x+dx, 0, 0), axes.c2p(x+dx, y, 0), axes.c2p(x, y, 0)]

        def get_bars(func, dx, stroke_width=1):
            bars = VGroup()
            step = int(round(dx / dx_actual))
            x_vals = x[:-2:step]
            n = len(x_vals)
            
            for idx, i in enumerate(x_vals):
                color = interpolate_color(ORANGE, TEAL_E, alpha=idx / max(n - 1, 1))
                bar = Polygon(
                    *get_rectangle_corners(func, i, dx=dx, axes=ax)
                ).set_fill(color, 1).set_stroke(width=stroke_width)
                
                bars.add(bar)
            
            return bars

        dx_tracker = ValueTracker(0.3)
        get_dx = dx_tracker.get_value
        bars = get_bars(func, dx=get_dx())

        self.play(
            ShowCreation(bars)
        )

        # Animate smaller dx
        bars.add_updater(lambda b : b.become(get_bars(func=func, dx=get_dx())))
        self.play(
            dx_tracker.animate.set_value(0.05),
            run_time=4
        )
        bars.clear_updaters()

        bars2 = get_bars(func=func, dx=0.01, stroke_width=0)
        self.play(
            ReplacementTransform(bars,bars2),
            run_time=0.5
        )
        self.wait(2)

