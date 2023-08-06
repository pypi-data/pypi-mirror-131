import math
import random
import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
warnings.filterwarnings("ignore")

class plot:
    def __init__(self, data=[], plot_type='', title='', style='tufte', width=8, height=6, labels=[],
                 xlabel='', ylabel='', font_size=12, font_family='monospace', ax=None, fig=None):
        plt.rcParams['font.family'] = font_family
        plt.rcParams['font.size'] = font_size
        self._plot_width = width
        self._plot_height = height
        self._font_size = font_size
        self._style = style
        self._plot_type = plot_type
        self._x, self._y = [], []
        if ax is None or fig is None:
            self.fig, self.ax = plt.subplots()
        else: self.fig, self.ax = fig, ax
        self.set_axis_labels(xlabel, ylabel)
        self.set_title(title)
        self._labels = labels
        self.set_plot_size(width, height)
        if len(data) != 0:
            if isinstance(data[0], (tuple, list, np.ndarray)):
                self.add_data(data[0], data[1])
            else:
                self.add_data(data)
            self.show()
        
    def set_plot_type(self, plot_type):
        """set chart type"""
        self._plot_type = plot_type
        return self
        
    def set_plot_size(self, w=8, h=6):
        """set width and height of the chart"""
        self.fig.set_figwidth(w)
        self.fig.set_figheight(h)
        self._plot_width = w
        self._plot_height = h
        return self
    
    def set_title(self, title=''):
        """set chart title"""
        self.ax.set_title(title, fontsize=self._font_size + 5)
        return self
    
    def set_axis_labels(self, xlabel='', ylabel=''):
        """set chart x-y labels"""
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        return self
    
    def set_labels(self, labels):
        """set legend"""
        if self._plot_type == 'line':
            for i in range(len(self._x)):
                self.ax.text(self._x[i][-1] + 0.3, self._y[i][-1], labels[i], va='center', fontsize=self._font_size)
        if self._plot_type == 'scatter':
            if isinstance(labels, str): labels = (labels,)
            for label, x, y in zip(labels, self._x, self._y):
                pos = x.index(max(x))
                x, y = x[pos], y[pos]
                self.ax.annotate(
                    label,
                    xy=(x, y), xytext=(40, 20),
                    textcoords='offset points', ha='right', va='bottom',
                    arrowprops=dict(arrowstyle = '-', connectionstyle='arc3,rad=0'))
        return self
    
    def save(self, name='', format='png', dpi=300):
        """set chart as a picture"""
        self.fig.savefig(fname=name+'.'+format, format=format, dpi=dpi)
        print('The file saved successfully')
        
    def add_data(self, *args):
        """set chart data"""
        if self._plot_type == '':
            if len(args) == 1 and len(self._labels) == 0:
                self._plot_type = 'hist'
            elif len(args) == 1 and len(self._labels) != 0:
                self._plot_type = 'bar'
            elif len(args) != 1 and sorted(args[0]) == args[0]:
                self._plot_type = 'line'
            else: self._plot_type = 'scatter'
                
        if self._plot_type in ('hist', 'bar'):
            self._x = args[0]
        elif self._plot_type in ('line', 'scatter'):
            if len(args) != 2:
                raise TypeError("2 positional arguments are expected")
            x, y = args
            if any(isinstance(el, (tuple, list, np.ndarray)) for el in y):
                [self._y.append(i) for i in y]
                if any(isinstance(el, (tuple, list, np.ndarray)) for el in x):
                    [self._x.append(i) for i in x]
                else: [self._x.append(x) for i in y]
            else:
                self._x.append(x)
                self._y.append(y)
        return self
    
    def _calc_tick_value(self, value_max, value_min, spine_len, spine=[]):
        """compute optimal ticker step"""
        x_gap = 0
        n_tickers = 0
        max_tickers = spine_len * 1.5
        min_dec = np.array(sorted(spine)[1:]) - np.array(sorted(spine)[:-1])
        mult = 10**(math.floor(math.log(abs(value_max - value_min), 10)) - 1)
        fin_fract = mult * 10
        dec_array = np.array([.025, .05, .1, .25, .5, 1, 2.5, 5, 10, 50, 100])
        if (min_dec == np.round(min_dec, 0)).all():
            dec_array = np.array([1, 5, 10, 50, 100, 500, 1000])
            mult = 1 if mult <=1 else mult
        if self._plot_type == 'hist':
            dec_array = np.array([1, 5, 10, 50, 100, 500, 1000])
        for dec in mult * dec_array:
            fract = dec
            if fract < (value_max - value_min) / max_tickers: 
                fract /= 10
            n_tickers_temp = (value_max - value_min) / fract
            x_gap_temp = (value_min // fract * fract + fract - value_min) / fract
            if (x_gap_temp >= x_gap) & (n_tickers_temp >= n_tickers) & (n_tickers_temp <= max_tickers):
                x_gap = x_gap_temp
                n_tickers = n_tickers_temp
                fin_fract = fract
        return fin_fract

    def _remove_axis_lines(self, sides):
        """remove axis spines"""
        for side in sides:
            self.ax.spines[side].set_visible(False)
    
    def _adjast_spine(self, k_breath=0.05):
        """set spines bounds and gaps"""
        if self._plot_type in ('scatter', 'line'):
            self.ax.spines['bottom'].set_bounds(self._x_left, self._x_right)
            self.ax.spines['left'].set_bounds(self._y_bottom, self._y_top)
            self.ax.set_xlim([self._x_left - (self._x_max - self._x_min) * k_breath, self._x_right + self._x_tick_dec * 0.2])
            self.ax.set_ylim([self._y_bottom - (self._y_max - self._y_min) * k_breath, self._y_top + self._y_tick_dec * 0.2])
        if self._plot_type == 'hist':
            self.ax.spines['bottom'].set_bounds(self._x_left, self._x_right)
            self.ax.spines['left'].set_bounds(self._y_bottom, self._y_top)
            self.ax.spines['bottom'].set_position(('axes', -0.05))
            self.ax.set_xlim([self._x_left - (self._x_max - self._x_min) * k_breath, self._x_right + self._x_tick_dec * 0.2])
            self.ax.set_ylim([self._y_bottom, self._y_top + self._y_tick_dec * 0.2])
            
            bottom_line = np.linspace(self._x_left, self._x_right)
            self.ax.plot(bottom_line, [self._y_bottom for _ in bottom_line], linestyle='-', color='k')
        if self._plot_type == 'bar':
            self.ax.set_xlim([0, self._x_right + self._x_tick_dec * 0.2])
            self.ax.spines['bottom'].set_bounds(self._x_left, self._x_right)
        
    def _adjast_ticks(self, n_ticks=5):
        """set tickers in a right positions"""
        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(base=self._x_tick_dec))
        self.ax.tick_params(length=7)
        if self._plot_type != 'bar':
            self.ax.yaxis.set_major_locator(ticker.MultipleLocator(base=self._y_tick_dec))
            
    def _line_scatter_params(self):
        """compute parameters for line and scatter chart"""
        x_flatten = [item for sublist in self._x for item in sublist]
        y_flatten = [item for sublist in self._y for item in sublist]
        self._x_min, self._x_max = min(x_flatten), max(x_flatten)
        self._y_min, self._y_max = min(y_flatten), max(y_flatten)
        
        self._y_tick_dec = self._calc_tick_value(self._y_max, self._y_min, self._plot_height*1.3, y_flatten)
        self._y_bottom = (self._y_min // self._y_tick_dec) * self._y_tick_dec
        self._y_top = (self._y_max // self._y_tick_dec + 1) * self._y_tick_dec
        
        self._x_tick_dec = self._calc_tick_value(self._x_max, self._x_min, self._plot_width, x_flatten)
        self._x_left = self._x_min // self._x_tick_dec * self._x_tick_dec
        self._x_right = (self._x_max // self._x_tick_dec + 1) * self._x_tick_dec
        
    def _hist_params(self):
        """compute parameters for hist chart"""
        self._x_min, self._x_max = min(self._x), max(self._x)
        self._x_tick_dec = self._calc_tick_value(self._x_max, self._x_min, self._plot_width, self._x)
        self._x_left = self._x_min // self._x_tick_dec * self._x_tick_dec
        self._x_right = (self._x_max // self._x_tick_dec + 1) * self._x_tick_dec
            
        bins = list(np.arange(self._x_left, self._x_right + self._x_tick_dec, self._x_tick_dec / 2))
        y_bins = np.histogram(self._x, bins=bins)[0]
        self._y_min, self._y_max = min(y_bins), max(y_bins)
        self._y_tick_dec = self._calc_tick_value(self._y_max, self._y_min, self._plot_height)
        self._y_bottom = 0
        self._y_top = (self._y_max // self._y_tick_dec + 1) * self._y_tick_dec
        
    def _bar_params(self):
        """compute parameters for bar chart"""
        self._x_min, self._x_max = min(self._x), max(self._x)
        self._x_tick_dec = self._calc_tick_value(self._x_max, self._x_min, self._plot_width, self._x)
        self._x_left = 0
        self._x_right = (self._x_max // self._x_tick_dec + 1) * self._x_tick_dec
        
    def _calc_scatter_marker_size(self):
        """calculate markers size for scatter plot"""
        _markers_number = len([item for sublist in self._y for item in sublist])
        return self._plot_width * self._font_size - _markers_number / 100
    
    def show(self):
        """display the chart"""
        if len(self._x) == 0: raise TypeError("The data is not set")
        if self._plot_type == 'line':
            linestyles = ['solid', 'dashed', 'dotted', 'dashdot']
            for i in range(len(self._x)):
                if len(self._x[i]) < 100:
                    self.ax.plot(self._x[i], self._y[i], linestyle=linestyles[i if i<4 else 0], color='black', linewidth=1, zorder=1)
                    self.ax.scatter(self._x[i], self._y[i], color='white', s=100, zorder=2)
                    self.ax.scatter(self._x[i], self._y[i], color='black', s=20, zorder=3)
                else: self.ax.plot(self._x[i], self._y[i], linestyle='-', color='black', linewidth=1, zorder=1)
            self._line_scatter_params()
            if len(self._labels) > 0: self.set_labels(self._labels)
        elif self._plot_type == 'scatter':
            markers = ['o', 'D', 's', 'v', 'p', 'P', '*']
            marker_size = self._calc_scatter_marker_size()
            for i in range(len(self._x)):
                self.ax.scatter(self._x[i], self._y[i], color='white', marker=markers[i], s=marker_size, linewidths=0.7, edgecolors='black')                    
            self._line_scatter_params()
            if len(self._labels) > 0: self.set_labels(self._labels)
        elif self._plot_type == 'hist':
            self._hist_params()
            bins = list(np.arange(self._x_left, self._x_right + self._x_tick_dec, self._x_tick_dec / 2))
            self.ax.hist(self._x, bins=bins, fc='w', ec='k')
            if len(self._labels) > 0: self.set_labels(self._labels)
        elif self._plot_type == 'bar':
            self._bar_params()
            if len(self._labels) == 0: self._labels = list(range(len(self._x)))
            self.ax.barh(list(reversed(self._labels)), list(reversed(self._x)), color='w', edgecolor='k')
            self._remove_axis_lines(['left'])
            self.ax.tick_params(axis='y', which='both', left=False)

        self._remove_axis_lines(['top', 'right'])
        self._adjast_spine()
        self._adjast_ticks()

def show_examples():
    """Show the plots examples"""
    fig, (ax_1, ax_2) = plt.subplots(2, 2, figsize=(15,20))
    ax1, ax2 = ax_1
    ax3, ax4 = ax_2

    x = list(range(1950, 1959))
    y = [164, 241, 234, 211, 122, 186, 183, 147, 143]
    hist_data = np.random.rand(3000) * 45.34
    bar_data = [10, 20, 30, 10, 50]
    bar_labels = ['Madrid', 'London', 'Tokyo', 'Sidney', 'Paris']

    p1 = plot(plot_type='scatter', fig=fig, ax=ax1, width=20, height=12)
    ax1.set_title("plot_type='scatter'")
    p1.add_data(x, y)
    p1.set_axis_labels('year', 'density')
    p1.show()

    p2 = plot(plot_type='line', fig=fig, ax=ax2, width=20, height=12)
    ax2.set_title("plot_type='line'")
    p2.add_data(x, y)
    p2.set_axis_labels('year', 'volume')
    p2.show()

    p3 = plot(plot_type='hist', fig=fig, ax=ax3, width=20, height=12)
    ax3.set_title("plot_type='hist'")
    p3.add_data(hist_data)
    p3.show()

    p4 = plot(plot_type='bar', fig=fig, ax=ax4, width=20, height=12, labels=bar_labels)
    ax4.set_title("plot_type='bar'")
    p4.add_data(bar_data)
    p4.show()