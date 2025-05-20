from manimlib import *


class Arrow3D(Group):
    def __init__(
        self,
        direction,
        start = ORIGIN,
        color = WHITE,
        shaft_radius : float = 0.03,
        tip_length : float = 0.3,
        tip_radius : float = 0.1,
        buff : float = 0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.direction = np.array(direction)
        self.length = np.linalg.norm(direction)
        self.start = start
        self.tip = direction + self.start

        # Normalize direction
        norm_dir = direction / np.linalg.norm(direction)
        arrow_start = start + buff * norm_dir
        shaft_length = self.length - tip_length

        # Create the shaft: along Z-axis
        shaft = Cylinder(radius=shaft_radius, height=shaft_length, resolution=(24, 16))
        shaft.set_color(color=color)
        shaft.shift(OUT * (shaft_length / 2))  # Position at the center of the shaft

        # Create the tip: aligned on top of the shaft (keeping original positioning)
        tip = Cone(radius=tip_radius, height=tip_length, resolution=(24, 16))
        tip.set_color(color=color)
        tip.shift(OUT * (shaft_length - 1.2*tip_length))  # Original positioning

        # Combine the shaft and tip into a single group
        full_arrow = Group(shaft, tip)

        # Rotate the entire arrow to align with the given direction
        rot_axis = np.cross(OUT, norm_dir)
        angle = angle_between_vectors(OUT, norm_dir)
        if np.linalg.norm(rot_axis) > 1e-6:
            full_arrow.rotate(angle, axis=rot_axis, about_point=arrow_start)

        # We need to shift it to make sure it starts at the origin and points toward the direction
        full_arrow.shift(arrow_start)  # First shift to the starting point
        
        self.add(full_arrow)



class NearestVectorClassification3D(InteractiveScene):
    def construct(self):
        self.frame.reorient(-52, 63, 0, (0.02, 0.34, 0.96), 5.54)
        theta, phi = self.frame.get_euler_angles()[:2]
        # self.add(Text(str(l[0:2]*D)))
        # Axes
        axes = ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-4, 4])
        self.add(axes)

        # Class vectors
        class_vectors = {
            "A": {"vec": np.array([1.5, -0.5, 1.5]), "color": PURPLE},
            "B": {"vec": np.array([-0.5, 1.5, -1]), "color": BLUE},
            "C": {"vec": np.array([0, -2, 1.5]), "color": GREEN},
        }

        arrows = Group()
        labels = VGroup()

        for name, data in class_vectors.items():
            vec = data["vec"]
            color = data["color"]
            arrow = Arrow3D(direction=vec, color=color, start=ORIGIN)
            
            # Create label as a TextMobject with billboarding effect
            label = Text(name, font_size=24, fill_color=GREY)
            label.move_to(1.1*vec)
            
            # Setup updating function to make label face camera
            label.rotate(phi, axis=RIGHT)
            label.rotate(theta, axis=OUT) 
            
            # def update_label(m: Mobject):
            #     m.become( Text(name, font_size=24, fill_color=GREY).move_to(1.1*vec).rotate(phi, axis=RIGHT).rotate(theta, axis=OUT) )

            # label.add_updater(update_label)
            
            arrows.add(arrow)
            labels.add(label)

        self.play(*[FadeIn(arrow) for arrow in arrows])
        self.play(*[FadeIn(label) for label in labels])
        self.wait()

        # Test vector
        test_vec = np.array([0.25, 1, -1.8])
        test_arrow = Arrow3D(test_vec, color=RED)
        test_label = Text("Test", font_size=24, fill_color=GREY)
        test_label.move_to(1.1*test_vec)
        test_label.rotate(phi, axis=RIGHT)
        test_label.rotate(theta, axis=OUT) 
        
        def label_updater(m : Mobject):
            theta, phi = self.frame.get_euler_angles()[:2]
            m.become(Text("Test", font_size=24, fill_color=GREY)).rotate(phi, axis=RIGHT).rotate(theta, axis=OUT).move_to(1.1*test_vec)

        # Add updater to test label
        test_label.add_updater(label_updater)
        
        self.play(FadeIn(test_arrow), FadeIn(test_label))
        self.wait()

        # Draw dashed lines to each class vector and calculate distances
        lines = []
        distances = []
        for name, data in class_vectors.items():
            end = data["vec"]
            line = DashedLine(test_vec, end, color=GREY)
            lines.append(line)
            distances.append(np.linalg.norm(test_vec - end))

        self.play(*[ShowCreation(line) for line in lines])
        self.wait()

        # Highlight nearest class
        nearest_idx = np.argmin(distances)
        nearest_color = list(class_vectors.values())[nearest_idx]["color"]
        nearest_name = list(class_vectors.keys())[nearest_idx]
        self.play(self.frame.animate.reorient(-73, 93, 0, (0.25, 0.75, -0.77), 4.09), run_time=2)

        highlight_line = lines[nearest_idx].copy().set_color(YELLOW).set_stroke(width=6)
        self.play(Transform(lines[nearest_idx], highlight_line))

        # For 2D UI elements, add them to the fixed position in corner
        result = Text(f"Classified as: {nearest_name}", font_size=28, color=nearest_color).to_corner(UL)
        # Make the result label a fixed position overlay
        result.fix_in_frame()
        self.play(FadeIn(result))
        self.wait(3)

