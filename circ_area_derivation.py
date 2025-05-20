from manimlib import *


CREAM = "#FFFFC0"
R = 3


class Area(InteractiveScene):
    def construct(self):
        # Function definitions
        t2c={'r' : ORANGE,
             'A' : PURPLE,
             '\\theta': TEAL,
             'A_c' : BLUE_E,
             'N' : RED,
             r'\pi' : WHITE
             }

        def get_xyz(r, phi, theta=PI/2):
            return r*np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])


        def get_new_circle(N, color=CREAM):
            theta = 2*PI / N
            circ_grp = VGroup()
            circle = Circle(stroke_color=CREAM, radius=R, stroke_width=2).set_fill(color, opacity=0.2)
            circ_grp.add(circle)
            centre = circle.get_center

            for i in range(1, N+1):
                line = DashedLine(start=centre(), end=get_xyz(R, i*theta), dash_length=0.1, stroke_width=2)
                circ_grp.add(line)

            return circ_grp
        
        def get_circ_grp(N, color=CREAM):
            angle = 2*PI/N
            circ = get_new_circle(N, color=color)

            arc_circ = Arc(angle=angle, radius=0.6, arc_center=circ.get_center(), stroke_width=2)
            theta_circ = Tex("\\theta", t2c=t2c).next_to(arc_circ.get_center(), RIGHT*0.8).scale(0.85)
            circ_grp = VGroup(circ, arc_circ, theta_circ)

            return circ_grp
        

        def get_sector(N):
            angle = 2*PI/N
            sec = Sector(start_angle=-(PI-angle)/2, angle=-angle, radius=R, stroke_color=CREAM, stroke_width=2).set_fill(CREAM, opacity=0.2)
            return sec
        
        def get_sector_grp(N):
            angle = 2*PI/N
            sector = get_sector(N)

            arc_sec = Arc(start_angle=-PI/2 - PI/N, angle=angle, radius=0.7, arc_center=sector.get_all_points()[0], stroke_width=2)
            theta_sec = Tex("\\theta", t2c=t2c).next_to(arc_sec, DOWN*0.5).scale(0.7)
            sector_grp = VGroup(sector, arc_sec, theta_sec)

            return sector_grp
        

        def get_triangle(N, color=CREAM):
            angle = 2*PI/N
            vertices = [np.array((0,0,0)),
                        np.array((R*np.sin(angle/2), -R*np.cos(angle/2), 0)),
                        np.array((-R*np.sin(angle/2), -R*np.cos(angle/2), 0))]
            
            triangle = Polygon(*vertices, stroke_color=CREAM, stroke_width=2).set_fill(color=color, opacity=0.2)
            return triangle
        
        def get_triangle_grp(N, color=CREAM):
            angle = 2*PI/N
            triangle = get_triangle(N, color=color)

            arc_tri = Arc(start_angle=-PI/2 - PI/N, angle=angle, radius=0.7, arc_center=triangle.get_all_points()[0], stroke_width=2)
            theta_tri = Tex("\\theta", t2c=t2c).next_to(arc_tri, DOWN*0.5).scale(0.7)
            triangle_grp = VGroup(triangle, arc_tri, theta_tri).move_to(ORIGIN)
            
            return triangle_grp
        
        N_tracker = ValueTracker(6)
        def get_N(): return int(N_tracker.get_value())
        N = get_N()
        angle = 2*PI/N
        
        # Animate circle creation
        circ_grp = get_circ_grp(N)
        self.wait(1)
        self.play(ShowCreation(circ_grp[0]), run_time=1)
        self.wait(1)

        sector_dummy = Sector(angle=angle, radius=R, stroke_color=CREAM, stroke_width=2).set_fill(CREAM, opacity=0.2)
        sector_grp = get_sector_grp(N)
        sector_grp.move_to(RIGHT_SIDE+0.1*LEFT, aligned_edge=RIGHT)

        # Animate sector from circle
        self.add(sector_dummy)
        self.play(circ_grp[0].animate.move_to(LEFT_SIDE + 2*RIGHT).scale(0.6),
                  ReplacementTransform(sector_dummy, sector_grp[0]),
                  run_time=2)
        
        # Add labels
        circ_ref = get_circ_grp(N).move_to(circ_grp[0]).scale(0.6)
        circ_grp[1:].scale(0.6).move_to(circ_ref[1:])
        sec_ref = get_sector_grp(N).move_to(sector_grp[0])
        sector_grp[1:].move_to(sec_ref[1:])

        self.play(*[ShowCreation(circ_grp[i]) for i in (1,2)],
                  *[ShowCreation(sector_grp[i]) for i in (1,2)])
        self.wait(2)

        # Show triangle
        triangle_grp = get_triangle_grp(N)
        intermediate_grp = sector_grp.copy()

        self.play(intermediate_grp.animate.move_to(triangle_grp, aligned_edge=TOP))
        self.play(FadeOut(intermediate_grp), FadeIn(triangle_grp), run_time=0.2)

        self.wait()

        self.play(triangle_grp.animate.shift(UP*2))

        # Add radius and area labels
        triangle_top = triangle_grp[0].get_all_points()[0]
        triangle_bottom = triangle_grp[0].get_all_points()[2]
        C = triangle_grp[0].get_center()
        P = (triangle_top + triangle_bottom)/2
        diff = C - P
        Q = P + diff + diff * np.array([1,-1,1])
        r_label1 = Tex('r', t2c=t2c).scale(0.8).next_to(P)
        r_label2 = Tex('r', t2c=t2c).scale(0.8).next_to(Q, direction=LEFT)
        r_grp = VGroup(r_label1, r_label2)

        A_label = Tex('A', t2c=t2c).scale(0.8).move_to(triangle_grp).shift(DOWN*0.5)
        Ac_label = Tex('A_c', t2c=t2c).move_to(circ_grp).shift(DOWN*0.5)
        A_label_grp = VGroup(A_label, Ac_label)
        
        N_text = Tex(r'N = \text{number of sectors in circle}', t2c={'N' : RED}).scale(0.8).to_corner(UL)

        self.play(ShowCreation(r_grp), ShowCreation(A_label),
                  triangle_grp[0].animate.set_fill(t2c['A'], opacity=0.2)          
        )

        # Show area calculations
        A_1 = Tex(r"A = \frac{1}{2} r \cdot r \sin{\theta}", t2c=t2c).shift(DOWN*0.4)
        A_2 = Tex(r"A = \frac{1}{2} r^2 \sin{\theta}", t2c=t2c).move_to(A_1)
        
        Ac_1 = Tex(r"A_c \approx A \times N", t2c=t2c).next_to(A_2, direction=DOWN)
        Ac_2 = Tex(r"A_c \approx \frac{1}{2} N r^2 \sin{\theta}", t2c=t2c).next_to(Ac_1, direction=DOWN)

        self.play(ShowCreation(A_1))
        self.wait()
        self.play(
            ReplacementTransform(A_1[:5], A_2[:5]),
            ReplacementTransform(A_1[5:8], A_2[5:7]),
            ReplacementTransform(A_1[8:], A_2[7:]),
        )
        self.wait()
        self.play(ShowCreation(Ac_1), ShowCreation(N_text), ShowCreation(Ac_label),
                  circ_grp[0][0].animate.set_fill(t2c['A_c'], opacity=0.2),
                  run_time=2
        )
        self.wait()
        self.play(
            TransformFromCopy(Ac_1[:3], Ac_2[:3]),
            TransformFromCopy(A_2[2:5], Ac_2[3:6]),
            TransformFromCopy(Ac_1[5], Ac_2[6]),
            TransformFromCopy(A_2[5:], Ac_2[7:]),
            run_time=2
            )
        self.wait()
        self.play(
            FadeOut(sector_grp),
            FadeOut(A_2),
            FadeOut(Ac_1),
            Ac_2.animate.move_to(A_2).scale(1.1)
            )
        
        # Show 2 pi/N calculations
        theta_eqn = Tex(r"\theta = \frac{2\pi}{N}", t2c=t2c).move_to(sector_grp).shift(LEFT)
        N_eqn = Tex(r'N = \frac{2\pi}{\theta}', t2c=t2c).next_to(theta_eqn, direction=DOWN)

        self.play(ShowCreation(theta_eqn))
        self.wait()
        self.play(
            TransformFromCopy(theta_eqn[-1], N_eqn[0]),
            TransformFromCopy(theta_eqn[1:-1], N_eqn[1:-1]),
            TransformFromCopy(theta_eqn[0], N_eqn[-1]),
        )
        self.wait()

        intermediate_eqn = Tex(r"A_c \approx \frac{1}{2} \frac{2\pi}{\theta} r^2 \sin{\theta}", t2c=t2c).scale(1.1).move_to(Ac_2)

        self.play(
            ReplacementTransform(Ac_2[:6], intermediate_eqn[:6]),
            TransformFromCopy(N_eqn[2:6], intermediate_eqn[6:10]),
            ReplacementTransform(Ac_2[7:], intermediate_eqn[10:]),
            FadeOut(Ac_2[6]),
            run_time=2
        )
        self.wait()

        final_eqn = Tex(r"A_c \approx \pi r^2 \frac{\sin{\theta}}{\theta}", t2c=t2c).scale(1.1).move_to(Ac_2)
        one = Tex('1').move_to(intermediate_eqn[4])

        self.play(ReplacementTransform(intermediate_eqn[3:7], one))
        self.play(
            ReplacementTransform(intermediate_eqn[0:3], final_eqn[0:3]),
            ReplacementTransform(intermediate_eqn[7], final_eqn[3]),
            ReplacementTransform(intermediate_eqn[10:], final_eqn[4:10]),
            ReplacementTransform(intermediate_eqn[8:10], final_eqn[10:]),
            FadeOut(one),
            run_time=1
        )
        self.wait(2)

        # Define updaters
        def r_updater(r_grp):
            triangle_top = triangle_grp[0].get_all_points()[0]
            triangle_bottom = triangle_grp[0].get_all_points()[2]
            C = triangle_grp[0].get_center()
            P = (triangle_top + triangle_bottom)/2
            diff = C - P
            Q = P + diff + diff * np.array([1,-1,1])
            r_grp[0].next_to(P)
            r_grp[1].next_to(Q, direction=LEFT)
        
        def add_updaters():
            # Add updaters
            circ_grp[0].add_updater(lambda c: c.become(get_new_circle(get_N(), color=c[0].get_fill_color()).scale(0.6).move_to(c)))
            circ_grp[1].add_updater(lambda a: a.become(Arc(angle=2*PI/get_N(), radius=0.5*0.6, arc_center=circ_grp[0].get_center(), stroke_width=2)))

            r_grp.add_updater(r_updater)

            # sector_grp.add_updater(lambda s: s.become(get_sector_grp(N).move_to(s)))
            triangle_grp.add_updater(lambda t: t.become(get_triangle_grp(get_N(), color=t.get_fill_color()).move_to(t)))
            # self.play(Indicate(sector_grp), run_time=0.001)

        def remove_updaters():
            circ_grp.clear_updaters()
            sector_grp.clear_updaters()
            triangle_grp.clear_updaters()

        # Show slices getting smaller
        add_updaters()
        self.play(N_tracker.animate.set_value(40), run_time=2.5)    
        remove_updaters()
        self.wait()    

        # Equation with limit
        limit_eqn = Tex(r"\lim_{N \to \infty} A_c = \pi r^2", t2c=t2c).next_to(final_eqn, DOWN).scale(1.1)
        self.play(ShowCreation(limit_eqn[0:6]),
                  TransformFromCopy(final_eqn[0:6], limit_eqn[6:]))
        
        new_circ = Circle(
            radius=R, stroke_color=CREAM
            ).scale(0.6).move_to(circ_grp).set_fill(t2c['A_c'], 0.2)
        
        self.play(
            FadeOut(final_eqn),
            FadeOut(triangle_grp),
            FadeOut(r_grp),
            FadeOut(theta_eqn),
            FadeOut(N_eqn),
            FadeOut(N_text),
            FadeOut(A_label_grp),
            FadeTransform(circ_grp, new_circ)
            )
        self.wait(1)

        # Show final result
        area_eqn = Tex(
            r"A = \pi r^2", t2c={'A' : t2c['A_c'], "r": ORANGE}
            ).scale(1.65).move_to(ORIGIN + 3*RIGHT)

        self.play(
            TransformMatchingStrings(limit_eqn, area_eqn),
            new_circ.animate.scale(1/0.6).move_to(ORIGIN + 3*LEFT).set_stroke(t2c['A_c'])
        )
        self.wait(3)
