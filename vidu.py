import kivy
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.graph import Graph, LinePlot
import numpy as np
from kivy.lang import Builder

class MainApp(App):

    def build(self):
        Builder.load_file('vidu.kv')
        return MainGrid()


class MainGrid(BoxLayout):

    zoom = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        mucnuoc = [1.03, 0.97, 0.92, 0.64, 0.51, 0.25, 0.07, -0.08, -0.17, -0.18, -0.14, -0.08, 0.07, 0.27, 0.33, 0.45, 0.45, 0.55, 0.64, 0.61, 0.77, 0.77, 0.99, 0.91, 1.01, 0.87, 0.78, 0.68, 0.49, 0.35, 0.14, 0.05, -0.09, -0.18, -0.21, -0.08, -0.03, 0.08, 0.23, 0.31, 0.45, 0.46, 0.53, 0.55, 0.75, 0.69, 0.75, 0.72, 0.74, 0.72, 0.65, 0.6, 0.47, 0.28, 0.17, 0.06, -0.02, -0.08, -0.22, -0.17, -0.11, 0.02, 0.12, 0.23, 0.29, 0.43, 0.39, 0.5, 0.47, 0.49, 0.51, 0.57, 0.52, 0.53, 0.5, 0.47, 0.43, 0.28, 0.18, 0.08, -0.05, -0.12, -0.18, -0.16, -0.11, -0.05, 0.06, 0.12, 0.25, 0.34, 0.38, 0.43, 0.39, 0.4]
        mucnuoc = np.array(mucnuoc)
        self.samples = len(mucnuoc)
        self.zoom = 1
        self.graph = Graph(y_ticks_major=0.5,
                           x_ticks_major=10,
                           border_color=[0, 1, 1, 1],
                           tick_color=[0, 1, 1, 0.7],
                           x_grid=True, y_grid=True,
                           xmin=0, xmax=self.samples,
                           ymin=int(min(mucnuoc))-1, ymax=int(max(mucnuoc))+1,
                           draw_border=False,
                           x_grid_label=True, y_grid_label=True,
                           xlabel ='Thoi gian',ylabel ='Mực nước'
                           )
        
        self.ids.modulation.add_widget(self.graph)
        self.plot_x = np.array(mucnuoc)
        self.plot_y = np.arange(0, self.samples)
        self.plot = LinePlot(color=[1, 1, 0, 1], line_width=1.5)
        self.graph.add_plot(self.plot)
        # self.update_plot(1)

    def update_plot(self, freq):
        self.plot_y = np.sin(2*np.pi*freq*self.plot_x)
        self.plot.points = [(x, self.plot_y[x]) for x in range(self.samples)]

    def update_zoom(self, value):
        if value == '+' and self.zoom < 8:
            self.zoom *= 2
            self.graph.x_ticks_major /= 2
        elif value == '-' and self.zoom > 1:
            self.zoom /= 2
            self.graph.x_ticks_major *= 2


MainApp().run()
