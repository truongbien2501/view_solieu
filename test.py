from kivy_garden.graph import Graph, LinePlot

class MyGraph(Graph):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.xlabel = 'Thời gian'
        self.ylabel = 'Mực nước'  
        
        self.x_ticks_major = 10
        self.y_ticks_major = 0.1
        self.x_grid = True
        self.y_grid = True
        
        self.x_grid_label = True
        self.y_grid_label = True
        self.padding = 5
        self.xlog = False
        self.ylog = False
        self.draw_border = True

    def update_plot(self, data):
        if self.plots is None:
            self.plots = LinePlot(color=[1, 0, 0, 1])
            self.add_plot(self.plot)
            
        self.plots.points = [(x, y) for x, y in enumerate(data)]
        
        self.xmin = 0
        self.xmax = len(data) 
        self.ymin = min(data)
        self.ymax = max(data) + 0.1
        
        # self.ask_draw()
        
if __name__ == '__main__':
    graph = MyGraph()
    data = [1.2, 2.5, 1.7, 2.2, 1.9] 
    graph.update_plot(data)