from manimlib import *
import numpy as np

class FourierDecomposition(InteractiveScene):

    def construct(self):
        runtime1 = 3
        runtime2 = 9
        direction_multiplier = 1        # Usually 1

        def get_wave(t, amplitudes, freqs):
            wave = np.zeros_like(t)
            for i,j in zip(amplitudes, freqs):
                wave = wave + i*np.sin(2*PI*j*t)
            return wave

        amplitudes = 0.25*np.array([1.920498251805278, 1.2562922502148286, 1.4494118404434762, 1.8975978980716324,
                                   1.0720430624138126, 1.9637169038603992, 0.32250155194042684])
        
        freqs = np.array([0.21716411536928937, 1.5852759935954135, 1.0967514722095275, 0.5855287399691351,
                               1.3943149556553887, 0.7541467263681951, 1.8843579963354955])
        
        colours = ["#C44227", "#C76E15", "#997A00", "#A3C47C", "#269940", "#1476B3", "#6A1FB3"]

        time = np.linspace(0,10,100)


        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value
        
        t_label = Tex("t = 0.00").scale(1.2)
        t_label.to_corner(UR)
        t_label.fix_in_frame()
        t_val = t_label.make_number_changeable("0.00")
        t_val.fix_in_frame()
        t_val.add_updater(lambda n: n.set_value(get_t()))

        self.add(t_label)


        ax = ThreeDAxes(
            x_range=(-3,3,1),
            y_range=(0,10,1),
            z_range=(-3,3,1)
        )
        
        self.frame.reorient(21, 75, 0, (0.14, -1.74, 0.4), 7.07)

        self.add(ax)

        wave_vals = get_wave(time, amplitudes, freqs)

        wave = VMobject()
        wave.set_points_smoothly(ax.c2p(np.zeros_like(time)-2, time, wave_vals))

        self.add(wave)

        self.wait()
        # self.play(ShowCreation(wave), run_time=2)

        def wave_updater(curve):
            wave_vals = get_wave(time + direction_multiplier*get_t(), amplitudes, freqs)
            curve.set_points_smoothly(ax.c2p(np.zeros_like(time)-2, time, wave_vals))

        wave.add_updater(wave_updater)

        self.play(t_tracker.animate.set_value(runtime1), run_time=runtime1, rate_func=linear)
        self.wait()

        wave_vals = get_wave(time, amplitudes, freqs)

        wave.clear_updaters()


        components = VGroup()
        for a,f,c in zip(amplitudes, freqs, colours):
            comp = VMobject()
            comp.set_points_smoothly(ax.c2p(np.zeros_like(time), time, a*np.sin(2*PI*f*(time+direction_multiplier*get_t())))).set_color(c)
            components.add(comp)
        components.arrange(RIGHT).shift([1.5,0,0])


        def component_updater(components : VGroup):
            for amp,freq,comp,col in zip(amplitudes, freqs, components, colours):
                comp_val = amp*np.sin(2*PI*freq*(time+direction_multiplier*get_t()))
                comp\
                .set_points_smoothly(ax.c2p(np.zeros_like(time), time, comp_val))\
                .set_color(col)
            components.arrange(RIGHT).shift([1.5,0,0])
        
        self.play(
                TransformFromCopy(wave, components[0]),
                TransformFromCopy(wave, components[1]),
                TransformFromCopy(wave, components[2]),
                TransformFromCopy(wave, components[3]),
                TransformFromCopy(wave, components[4]),
                TransformFromCopy(wave, components[5]),
                TransformFromCopy(wave, components[6]),
                )
        self.wait()

        self.add(components)

        components.add_updater(component_updater)
        wave.add_updater(wave_updater)

        self.play(
                self.frame.animate.reorient(53, 71, 0, (0.18, -1.77, 0.3), 7.07), 
                t_tracker.animate.set_value(runtime1+3),
                run_time=3,
                rate_func=linear
                )
        self.play(t_tracker.animate.set_value(runtime1+runtime2+3), run_time=runtime2, rate_func=linear)
