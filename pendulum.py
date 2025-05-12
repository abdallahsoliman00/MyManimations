import numpy as np
from manimlib import *

# class Text(Text):
#     def __init__(
#         self,
#         text: str,
#         use_labelled_svg: bool = True,
#         path_string_config: dict = dict(
#             use_simple_quadratic_approx=True,
#         ),
#         **kwargs
#     ):
#         super().__init__(
#             text=text,
#             use_labelled_svg=use_labelled_svg,
#             path_string_config=path_string_config,
#             fill_color='#333333',
#             **kwargs)
        

# class Tex(Tex):
#     def __init__(
#         self,
#         *tex_strings: str,
#         font_size: int = 48,
#         alignment: str = R"\centering",
#         template: str = "",
#         additional_preamble: str = "",
#         tex_to_color_map: dict = dict(),
#         t2c: dict = dict(),
#         use_labelled_svg: bool = True,
#         **kwargs
#     ):
#         super().__init__(
#             *tex_strings,
#             font_size=font_size,
#             alignment=alignment,
#             template=template,
#             additional_preamble=additional_preamble,
#             tex_to_color_map=tex_to_color_map,
#             t2c=t2c,
#             use_labelled_svg=use_labelled_svg,
#             fill_color='#333333',
#             **kwargs)


class PendulumToPhasePlane(Scene):
    def calculate_path(self, state_calc, init_state, time=5, dt=0.01):
        multiplier = int(1/dt)
        state_array = np.array([init_state])

        old_state = np.array(init_state)
        for _ in range(time*multiplier):
            new_state = state_calc(old_state)
            state_array = np.append(state_array, [new_state], axis=0)
            old_state = new_state

        state_array = state_array.T
        return state_array

    def calc_pendulum_state(self, prev_state, delta_t=0.01):
        x1, x2 = prev_state
        state_dt = np.array([x2, -(self.g/self.l)*np.sin(x1)])
        new_state = prev_state + delta_t * state_dt
        return new_state

    def construct(self):
        # First part: Pendulum animation
        r = 0.2
        g = 9.81
        l = 1.5
        period = (g/l)**0.5
        theta = 45 * DEGREES  

        pendulum = VGroup(
            Line(start=[0,r], end=UP*l, color=WHITE),
            Circle(radius=r, color=RED_A, fill_color=RED, fill_opacity=1),
        )

        # Create pendulum at vertical position
        bob_pos = l*np.sin(theta)*RIGHT + l*np.cos(theta)*DOWN
        initial_length = -1 * np.sin(theta)
        
        perp_arrow = Arrow(
            start=bob_pos,
            end=bob_pos + RIGHT * initial_length,
            buff=0,
            thickness=3,
            tip_width_ratio=3,
            max_width_to_length_ratio=0.05,
            color=WHITE
        ).rotate(theta + PI/2, about_point=bob_pos).rotate(-PI/2, about_point=l*np.sin(theta)*RIGHT + l*np.cos(theta)*DOWN)

        def update_perp_arrow(group):
            # Get current angle from pendulum's position
            bob_pos = group[1].get_center()
            current_angle = np.arctan2(bob_pos[0], -bob_pos[1])
            
            # Calculate new length based on sin(theta)
            new_length = -1 * np.sin(current_angle)  # Removed abs() to allow negative values
            
            # Update perpendicular arrow
            perp_arrow = group[2]
            perp_arrow.become(Arrow(
                start=bob_pos,
                end=bob_pos + RIGHT * new_length,  # Length can be negative
                buff=0,
                thickness=3,
                tip_width_ratio=3,
                max_width_to_length_ratio=0.05,
                color=WHITE
            ))
            perp_arrow.rotate(current_angle, about_point=bob_pos)  # Rotate to be perpendicular
        
        # Create downward arrow
        arrow_length = 0.7
        down_arrow = Arrow(
            start=ORIGIN,
            end=DOWN * arrow_length,
            buff=0,
            thickness=3,
            tip_width_ratio=3,
            max_width_to_length_ratio=0.05,
            color=WHITE
        )
        
        # Position arrow with start at bob's center
        bob_center = pendulum[1].get_center()
        down_arrow.put_start_and_end_on(
            bob_center,  # Start at bob's center
            bob_center + DOWN * arrow_length  # End below bob
        )
        
        # Move pendulum to starting position
        pendulum.shift(DOWN*l)  # Move down so pivot is at origin
        pendulum.rotate(theta, about_point=ORIGIN)  # Rotate about pivot
        
        # Position arrows
        bob = pendulum[1]  # Get reference to the bob
        
        # Add pivot point
        pivot = Dot(ORIGIN, color=BLUE)
        
        # Add a vertical line indicating theta
        theta_line = DashedLine(start=ORIGIN, end=DOWN*l, color=WHITE)
        
        # Add angle arc
        angle_arc = Arc(
            radius=0.5,
            angle=theta,
            start_angle=-PI/2,  # Start from vertical (pointing down)
            color=WHITE,
            stroke_width=2
        )
        
        # Add angle label
        angle_label = Tex("\\theta").scale(0.5)  # Made text smaller
        angle_label.next_to(angle_arc, DOWN)  # Changed position to UP
        
        def update_arrow(arrow):
            bob_center = bob.get_center()
            arrow.put_start_and_end_on(
                bob_center,  # Start at bob's center
                bob_center + DOWN * arrow_length  # End below bob
            )
            
        def update_arc(arc):
            # Calculate current angle from pendulum's position
            bob_pos = pendulum[1].get_center()
            current_angle = np.arctan2(bob_pos[0], -bob_pos[1])  # Calculate angle from vertical
            new_arc = Arc(
                radius=0.5,
                angle=current_angle,  # Use absolute value for correct arc
                start_angle=-PI/2,
                color=YELLOW
            )
            arc.become(new_arc)
            
        def update_label(label):
            # Calculate current angle same way as arc
            bob_pos = pendulum[1].get_center()
            current_angle = np.arctan2(bob_pos[0], -bob_pos[1])
            label_angle = current_angle/2  # Halfway between vertical and pendulum
            label_radius = 0.7
            new_pos = np.array([
                label_radius * np.sin(label_angle),
                -label_radius * np.cos(label_angle),
                0
            ])
            label.move_to(new_pos)
            
        # Add updaters
        down_arrow.add_updater(update_arrow)
        angle_arc.add_updater(update_arc)
        angle_label.add_updater(update_label)
        
        # Create labels for forces with consistent colors
        ma_label = Tex("ma", t2c={"m": BLUE, "a": PURPLE}).scale(0.4)
        mg_label = Tex("mg", t2c={"m": BLUE, "g": GREEN}).scale(0.4)
        

        def update_ma_label(label):
            # Get perp arrow's end point
            arrow_end = perp_arrow.get_end()
            # Position label slightly to the right of arrow tip
            label.next_to(arrow_end, LEFT, buff=0.1)
            
        def update_mg_label(label):
            # Get down arrow's end point
            arrow_end = down_arrow.get_end()
            # Position label slightly to the right of arrow tip
            label.next_to(arrow_end, RIGHT, buff=0.1)
            
        # Add updaters to labels
        ma_label.add_updater(update_ma_label)
        mg_label.add_updater(update_mg_label)
        
        # Add objects in order (back to front)
        self.add(theta_line)      # Add dashed line first (back layer)
        self.add(angle_arc)       # Add angle arc
        self.add(angle_label)     # Add angle label
        self.add(pendulum)        # Add pendulum
        self.add(pivot)           # Add pivot last (top layer)


        # Create the animation
        self.play(
            Rotate(pendulum, -2*theta, about_point=ORIGIN),
            run_time=period/2,
            rate_func=smooth
        )
        
        self.play(
            Rotate(pendulum, 2*theta, about_point=ORIGIN),
            run_time=period/2,
            rate_func=smooth
        )

        # Show arrows and labels together
        self.play(
            ShowCreation(down_arrow),
            ShowCreation(mg_label)
        )
        
        self.play(
            ShowCreation(perp_arrow),
            ShowCreation(ma_label)
        )
        pendulum.add(perp_arrow)
        pendulum.add_updater(update_perp_arrow)

        # Continue animation
        for _ in range(1):
            self.play(
                Rotate(pendulum, -2*theta, about_point=ORIGIN),
                run_time=period/2,
                rate_func=smooth
            )
            
            self.play(
                Rotate(pendulum, 2*theta, about_point=ORIGIN),
                run_time=period/2,
                rate_func=smooth
            )

        # Remove updaters before transformation
        ma_label.clear_updaters()
        mg_label.clear_updaters()

        # Clear updaters before fade out
        down_arrow.clear_updaters()
        angle_arc.clear_updaters()
        angle_label.clear_updaters()
        pendulum.clear_updaters()

        # Fade out pendulum animation with all elements
        self.play(
            *[FadeOut(mob, run_time=1.5) for mob in [
                pendulum,
                perp_arrow,
                pivot,
                theta_line,
                angle_arc,
                angle_label,
                down_arrow
            ]],
            rate_func=smooth
        )



        # Second part: Equation derivation
        kw = dict(font_size=40, t2c={
            "m": BLUE,
            "g": GREEN,
            "L": RED,
            "\\theta": YELLOW,
            "a": PURPLE,
            "=": WHITE,
            "+": WHITE,
            "-": WHITE,
            "1": WHITE,
            "2": WHITE,
            "(": WHITE,
            ")": WHITE,
        })

        # # Create force equation at top with matching colors
        # force_equation = VGroup(
        #     Tex("ma", t2c={"m": BLUE, "a": PURPLE}),
        #     Tex("=", color=WHITE),
        #     Tex("-", color=WHITE),
        #     Tex("mg", t2c={"m": BLUE, "g": GREEN}),
        #     Tex("\\sin\\theta", t2c={"\\theta": YELLOW})
        # ).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.5)

        force_equation = Tex("ma = -mg \\sin{\\theta}", **kw)

        # Create other equations
        second_equation = Tex("mL\\ddot{\\theta} = -mg\\sin\\theta", **kw)
        third_equation = Tex("\\ddot{\\theta} = -{g \\over L}\\sin\\theta", **kw)

        equations = VGroup(
            force_equation,
            second_equation,
            third_equation
        ).arrange(DOWN, buff=0.5)

        force_equation.move_to(equations[0])

        # Transition the labels to equation
        self.play(
            ReplacementTransform(ma_label, force_equation[0:2]), 
            ReplacementTransform(mg_label, force_equation[4:6]),
            Write(force_equation[2]),  # equals sign
            Write(force_equation[3]),  # minus sign
            Write(force_equation[6:])   # sin theta
        )
        self.wait()

        # Transform to second equation
        self.play(
            TransformFromCopy(force_equation[:2], second_equation[:4]),  # ma -> mL\ddot\theta
            TransformFromCopy(force_equation[2:], second_equation[4:]),  # mg sin theta
            run_time=2
        )
        self.wait()

        # Transform to third equation
        self.play(
            TransformFromCopy(second_equation[1], third_equation[5:7]),       # L
            TransformFromCopy(second_equation[2:6], third_equation[:4]),    # \ddot\theta=-
            TransformFromCopy(second_equation[7], third_equation[4]),       # g
            TransformFromCopy(second_equation[8:], third_equation[7:]),     # sin\theta
            run_time=2
        )
        self.wait()

        # Fade out first two equations
        self.play(
            FadeOut(force_equation),
            FadeOut(second_equation),
            run_time=1
        )

        
        state_equation1 = Tex(
            "\\dot{\\theta} = \\dot{\\theta}", **kw
        )
        state_equation2 = third_equation.copy()

        # Arrange equations
        state_equations = VGroup(state_equation1, state_equation2).arrange(DOWN, buff=0.5)

        # Transform to state space form and show substitution
        self.play(
            ReplacementTransform(third_equation, state_equations[1]),
            Write(state_equations[0]),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)
        

        self.g = 9.81
        self.l = 1.5

        # Create axes with proper labels
        axes = Axes(
            x_range=[-8, 8, 2],
            y_range=[-5, 5, 1],
            axis_config={"color": WHITE}
        ).scale(0.65).shift(RIGHT*1.25)
        

        # Add labels
        x_label = Tex(r"\theta").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Tex(r"\dot{\theta}").next_to(axes.y_axis.get_end(), RIGHT)
        axes_labels = VGroup(x_label, y_label)

        # Function for vector field
        def calc_state_dt(coords_array):
            result = np.zeros_like(coords_array)
            result[:, 0] = coords_array[:, 1]
            result[:, 1] = -(self.g/self.l)*np.sin(coords_array[:, 0])
            return result
        

        # Create vector field
        vector_field = VectorField(
            calc_state_dt,
            axes,
            density=2.5,
            stroke_width=1.5,
            max_vect_len_to_step_size=0.5,
        )

        # Calculate trajectories
        trajectory1 = self.calculate_path(
            self.calc_pendulum_state,
            [np.pi/4, 0],
            time=3,
            dt=0.01
        )
        

        # Create path mobjects
        path1 = VMobject()
        path1.set_points_smoothly([
            axes.c2p(x, y) for x, y in zip(trajectory1[0], trajectory1[1])
        ])
        path1.set_color("#FFFFFF")
        path1.set_stroke(width=3)

        # Move equations first
        self.play(
            state_equations.animate.move_to(LEFT_SIDE + RIGHT*1.5).scale(0.9)
        )
        self.wait()

        # Then show phase plane
        self.play(
            ShowCreation(axes),
            Write(axes_labels)
        )
        self.wait()

        # Show vector field
        self.play(ShowCreation(vector_field))
        self.wait()

        # Show trajectories
        self.play(ShowCreation(path1), run_time=2)
        self.wait(2)


