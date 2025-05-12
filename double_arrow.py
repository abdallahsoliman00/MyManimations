from manimlib import *


class DoubleArrow(VMobject):
    def __init__(self,
                 start=LEFT,
                 end=RIGHT, 
                 stroke_width=5, 
                 buff=0.1, 
                 tip_length=0.2,
                 tip_thickness=0.2,
                 **kwargs
        ):
        super().__init__(**kwargs)

        direction = end - start
        unit_dir = direction / np.linalg.norm(direction)

        # Adjusted start and end to account for arrowheads
        new_start = start + unit_dir * (tip_length + buff)
        new_end = end - unit_dir * (tip_length + buff)

        # Central line
        line = Line(new_start, new_end, stroke_width=stroke_width, **kwargs)

        # Arrowhead 1
        tip1 = Triangle(fill_opacity=1, **kwargs)
        tip1.stretch(tip_length / tip1.get_height(), dim=1)
        tip1.stretch(tip_thickness / tip1.get_width(), dim=0)
        tip1.rotate(line.get_angle() + PI/2)
        tip1.move_to(new_start - unit_dir * tip_length / 2)

        # Arrowhead 2
        tip2 = Triangle(fill_opacity=1, **kwargs)
        tip2.stretch(tip_length / tip2.get_height(), dim=1)
        tip2.stretch(tip_thickness / tip2.get_width(), dim=0)
        tip2.rotate(line.get_angle() - PI/2)
        tip2.move_to(new_end + unit_dir * tip_length / 2)

        self.add(line, tip1, tip2)

