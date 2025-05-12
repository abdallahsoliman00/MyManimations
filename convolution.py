from manimlib import *
import numpy as np


def step(lower, upper, x):
    return np.array([1 if lower <= i <= upper else 0 for i in x])


class VisualiseConvolution(InteractiveScene):
    def construct(self):

        # def create_axes():
        #     ax_grp = VGroup()
        #     for _ in range(3):
        #         ax_grp.add(Axes(
        #             x_range=(-3,3,1),
        #             y_range=(0,1.5,0.5)
        #         ))
        #     return ax_grp
        
        # def add_curves(funcs, ax_grp, colors):
        #     curves = VGroup()
        #     for func,ax,color in zip(funcs,ax_grp,colors):
        #         c = VMobject()
        #         c.set_points_smoothly(ax.c2p(x,func))
        #         c.set_stroke(color=color, width=2)
        #         curves.add(c)
        #     return curves

        # x = np.linspace(-3,3,3001)
        # f1 = np.array([i + 1 if -1 <= i <= 0 else -i + 1 if 0 <= i <= 1 else 0 for i in x])
        # f2 = np.array([1 if -0.5 <= i <= 0.5 else 0 for i in x])
        # f3 = f1*f2
        # group_axes = create_axes().arrange(DOWN*4).scale(0.85).to_edge(LEFT)
        # functions = [f1,f2,f3]
        # colors = [YELLOW_B, BLUE_C, TEAL_C]
        # curves = add_curves(functions, group_axes, colors)
        # self.add(group_axes, curves)


        ax1 = Axes(
            x_range=(-3,3,1),
            y_range=(0,1.5,0.5)
            )
        
        ax2 = Axes(
            x_range=(-3,3,1),
            y_range=(0,1.5,0.5)
            )
        
        ax3 = Axes(
            x_range=(-3,3,1),
            y_range=(0,1.5,0.5)
            )
        
        ax4 = Axes(
            x_range=(-3,3,1),
            y_range=(0,1,0.5)
            ).scale(1.1)
        
        ax_grp = VGroup(ax1,ax2,ax3).arrange(DOWN*4).scale(0.85).to_edge(LEFT)
        ax4.to_edge(RIGHT)

        yshiftarr = np.array([0,0.5,0])
        l1 = VGroup(
            ax1.get_x_axis_label("x").shift(RIGHT * 0.5).scale(0.65),
            ax1.get_y_axis_label("f(x)").shift(yshiftarr).scale(0.65)
        )
        l2 = VGroup(
            ax2.get_x_axis_label("x").shift(RIGHT * 0.5).scale(0.65),
            ax2.get_y_axis_label("g(s-x)").shift(yshiftarr).scale(0.65)
        )
        l3 = VGroup(
            ax3.get_x_axis_label("x").shift(RIGHT * 0.5).scale(0.65),
            ax3.get_y_axis_label("f(x).g(s-x)").shift(yshiftarr).scale(0.65)
        ) 
        l4 = VGroup(
            ax4.get_x_axis_label("s").shift(RIGHT * 0.5).scale(0.65),
            ax4.get_y_axis_label("[f*g](s)").shift(yshiftarr).scale(0.65)
        )

        self.add(ax_grp, ax4, l1, l2, l3, l4)

        x = np.linspace(-3,3,3001)

        f1 = np.array([i + 1 if -1 <= i <= 0 else -i + 1 if 0 <= i <= 1 else 0 for i in x])
        c1 = VMobject()
        c1.set_points_as_corners(ax1.c2p(x,f1))
        c1.set_stroke(color=YELLOW_B, width=2)
        self.add(c1)

        f2 = step(0, 0.5, x)
        c2 = VMobject()
        c2.set_points_as_corners(ax2.c2p(x,f2))
        c2.set_stroke(color=BLUE_C, width=2)
        self.add(c2)

        f3 = f1 * f2
        c3 = VMobject()
        c3.set_points_as_corners(ax3.c2p(x,f3))
        c3.set_stroke(color=TEAL_C, width=2)
        c3.set_fill(color=TEAL_C, opacity=0.3)
        self.add(c3)

        conv = np.convolve(f1,f2,'same') * (x[1]-x[0])
        c4 = VMobject()
        c4.set_points_as_corners(ax4.c2p(x,conv))
        c4.set_stroke(color=TEAL_C, width=2)
        self.add(c4)       

        conv_formula = Tex(
            R"\big[f * g \big](s) = \int_{-\infty}^\infty f(x) g(s - x) \, dx",
            font_size=36,
        ).to_corner(UR)

        self.add(conv_formula)

        init_a = np.trapz(f3, x)

        a_text = TexText(f"Area = {init_a:.6f}", font_size=36).set_color(TEAL_C).next_to(conv_formula, direction=DOWN, buff=0.5)

        a_val = a_text.make_number_changeable(f"{init_a:.6f}")
        
        def get_area():
            return a_val.get_value()

        self.add(a_text)

        s_tracker = ValueTracker(0)
        get_s = s_tracker.get_value

        s_pointer = ArrowTip(
                    angle=PI/2, 
                    color=BLUE_C,
                    stroke_width=5,
                    fill_color = BLUE_C,
                    fill_opacity=1
                    ).scale(0.3)
        
        
        s_text = Tex(f"s = {get_s()}", font_size=22)
        s_val = s_text.make_number_changeable(f"{get_s()}")

        def s_val_updater(a):
            global f2, f3
            f2 = step(0,0.5,get_s()-x)
            f3 = f1*f2
            a.set_value(get_s())

        s_val.add_updater(s_val_updater)

        s_group = VGroup(s_text, s_pointer).arrange(UP).move_to(ax2.c2p(get_s(),0), UP)
        s_group.add_updater(lambda p: p.move_to(ax2.c2p(get_s(),0), UP).shift(DOWN*0))

        self.add(s_group)

        # self.toggle_selection_mode()

        def area_updater(tracker):
            global f3
            tracker.set_value(np.trapz(f3, x))

        a_val.add_updater(area_updater)

        s_dot = GlowDot(ax4.c2p(get_s(), get_area()), color=WHITE)
        s_line = Line(ax4.c2p(get_s(),0), ax4.c2p(get_s(), get_area()), stroke_width=1, color=WHITE)
        self.add(s_dot, s_line)

        s_dot.add_updater(lambda d: d.move_to(ax4.c2p(get_s(), get_area())))
        s_line.add_updater(lambda l: l.put_start_and_end_on(ax4.c2p(get_s(),0), ax4.c2p(get_s(), get_area())))

        def c2_updater(curve):
            global f2
            f2 = step(0,0.5,get_s()-x)
            curve.set_points_as_corners(ax2.c2p(x,f2))
        c2.add_updater(c2_updater)

        def c3_updater(curve):
            global f3
            curve.set_points_smoothly(ax3.c2p(x,f3))
        c3.add_updater(c3_updater)


        # for _ in range(10):
        while True:    
            self.wait(2)
            self.play(s_tracker.animate.set_value(-2.5), run_time=1)
            self.wait()
            self.play(s_tracker.animate.set_value(2.5), run_time=5, rate_func=smooth)
            self.play(s_tracker.animate.set_value(0), run_time=1.5)
