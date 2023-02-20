import os

import StaticMethods
import numpy as np
from start_module import Variables
from main_program import container_Manager as cm
import matplotlib.pyplot as plt
import pylab
import fileManager as fm
from matplotlib.widgets import Button, Slider, CheckButtons

draw_first_plot = True
draw_second_plot = False
draw_third_plot = False
c = ['black', 'orange', 'red']


class Graph:
    delta_time = Variables.GraphConstant.delta_time
    startTime = 0
    finishTime = startTime + delta_time

    current_xs = []
    current_ys0 = []
    current_ys1 = []
    current_ys2 = []
    lim = 0
    on_changed_sign = Variables.FilesConstant.current_signal
    file_n = ""

    def getCurrentYS(self, s=Variables.FilesConstant.current_signal):
        if s == 0:
            return self.current_ys0
        if s == 1:
            return self.current_ys1
        return self.current_ys2

    def file_init(self):
        self.file_n = Variables.GraphConstant.gen_files_dir
        if not os.path.isdir(self.file_n):
            os.mkdir(self.file_n)
        mas = str.split(Variables.FilesConstant.file_directory, "/")
        n = str(mas[len(mas) - 1])
        n = n[0:len(n) - 4]
        self.file_n = self.file_n + "/" + n
        if not os.path.isdir(self.file_n):
            os.mkdir(self.file_n)

    def start_init(self):

        n = cm.Container(Variables.FilesConstant.file_directory)
        n.writeFileToList(self.current_ys0, 0)
        n.writeFileToList(self.current_ys1, 1)
        n.writeFileToListAndDate(self.current_ys2, self.current_xs, 2)

        limit = (StaticMethods.predictionLimits(self.getCurrentYS(), 8))
        limit[0] = np.abs(limit[0])
        limit[1] = np.abs(limit[1])
        self.lim = np.max(limit)

        self.file_init()

    def init_value(self, x_s, y_s):

        current_position = 0
        while self.current_xs[current_position] < self.startTime:
            current_position = current_position + 1
        while self.current_xs[current_position] <= self.finishTime:
            x_s.append((self.current_xs[current_position]) - self.startTime)
            y_s.append(self.getCurrentYS(self.on_changed_sign)[current_position])
            current_position = current_position + 1

    def init_to_file(self, x_s, y0_s, y1_s, y2_s):
        current_position = 0
        while self.current_xs[current_position] < self.startTime:
            current_position = current_position + 1
        while self.current_xs[current_position] <= self.finishTime:
            x_s.append((self.current_xs[current_position]) - self.startTime)
            y0_s.append(self.getCurrentYS(0)[current_position])
            y1_s.append(self.getCurrentYS(1)[current_position])
            y2_s.append(self.getCurrentYS(2)[current_position])
            current_position = current_position + 1

    def gen_files(self):

        next_path = self.file_n + "/" + str(StaticMethods.sec_to_time_short(self.startTime))
        if not os.path.isdir(next_path):
            os.mkdir(next_path)
        global sign_slider
        s = self.on_changed_sign
        for i in range(3):
            self.on_changed_sign = i
            sign_slider.set_val(i)
            self.redrawFigure()
            fig.savefig(next_path + "/" + "signal" + str(
                self.on_changed_sign) + Variables.FilesConstant.screen_type)
        self.on_changed_sign = s
        sign_slider.set_val(s)
        x_s0 = []
        y_s_0 = []
        y_s_1 = []
        y_s_2 = []
        self.init_to_file(x_s0, y_s_0, y_s_1, y_s_2)
        start_t = StaticMethods.sec_to_time_short(self.startTime)
        finish_t = StaticMethods.sec_to_time_short(self.finishTime)
        fm.save_input_container(next_path, "signal" + str(0) + ".txt", start_t, finish_t, y_s_0)
        fm.save_input_container(next_path, "signal" + str(1) + ".txt", start_t, finish_t, y_s_1)
        fm.save_input_container(next_path, "signal" + str(2) + ".txt", start_t, finish_t, y_s_2)

    def redrawFigure(self):
        x = []
        y = []
        self.init_value(x, y)
        ax1.clear()
        global draw_first_plot, draw_second_plot, draw_third_plot, c
        if draw_first_plot:
            ax1.plot(x, y, linewidth=0.5, color=c[0])
        if draw_second_plot:
            ax1.plot(x, StaticMethods.normalize_zscore(y), linewidth=0.5, color=c[1])
        if draw_third_plot:
            ax1.plot(x, StaticMethods.normalize_mean(y), linewidth=0.5, color=c[2])

        ax1.set_ylim([-self.lim, self.lim])
        add_time(ax1, StaticMethods.convertSecondsToTime(self.startTime))
        pylab.draw()

    def changeSlider(self):
        hour = self.startTime // 3600
        hour_slider.set_val(hour)
        minute_slider.set_val((self.startTime - hour * 3600) // 60)
        self.redrawFigure()

    def next(self, event):
        if self.finishTime + self.delta_time <= self.current_xs[len(self.current_xs) - 1]:
            self.startTime = self.delta_time + self.startTime
            self.finishTime = self.delta_time + self.finishTime
            self.changeSlider()

    def prev(self, event):
        if self.startTime - self.delta_time >= 0:
            self.startTime = self.startTime - self.delta_time
            self.finishTime = self.finishTime - self.delta_time
            self.redrawFigure()
            self.changeSlider()

    def saveToFile(self, event):
        self.gen_files()

    def set_time(self, hour, minute):
        self.startTime = hour * 3600 + minute * 60
        self.finishTime = self.startTime + self.delta_time

    def buttonGoTo(self, event):
        self.set_time(hour_slider.val, minute_slider.val)
        self.redrawFigure()

    def sign_slider(self, event):
        global sign_slider
        self.on_changed_sign = sign_slider.val
        self.redrawFigure()


def add_time(ax, curr_time):
    ax.text(0.5, -0.125, curr_time,
            verticalalignment='bottom', horizontalalignment='center',
            transform=ax1.transAxes,
            color='green', fontsize=15)


def add_plot_menu():
    rax = pylab.axes([0.05, 0.32, 0.2, 0.15])
    global check
    global c
    check = CheckButtons(rax, ('y=x(t)', 'y=(x(t)-x_average)/sqrt(D)', 'y=(x(t)-x_min)/(x_max-x_min)'), (draw_first_plot, draw_second_plot, draw_third_plot))
    [rec.set_color(c[i]) for i, rec in enumerate(check.labels)]


def func(label):
    if label == 'y=x(t)':
        global draw_first_plot
        draw_first_plot = not draw_first_plot
    elif label == 'y=(x(t)-x_average)/sqrt(D)':
        global draw_second_plot
        draw_second_plot = not draw_second_plot
    elif label == 'y=(x(t)-x_min)/(x_max-x_min)':
        global draw_third_plot
        draw_third_plot = not draw_third_plot
    global gr
    gr.redrawFigure()


def start_plot():
    global gr
    gr = Graph()
    gr.start_init()
    global fig
    fig = plt.figure(figsize=(15, 7))
    global ax1
    ax1 = fig.add_subplot()
    gr.redrawFigure()

    add_time(ax1, StaticMethods.convertSecondsToTime(gr.startTime))

    fig.subplots_adjust(left=0.04, right=0.998, top=1.0, bottom=0.3)

    axes_button_add = pylab.axes([0.675, 0.18, 0.3, 0.075])
    axes_button_remove = pylab.axes([0.06, 0.18, 0.3, 0.075])
    axes_button_save_to_file = pylab.axes([0.675, 0.075, 0.3, 0.075])
    axes_slider1 = pylab.axes([0.06, 0.1, 0.3, 0.075])
    axes_slider2 = pylab.axes([0.06, 0.05, 0.3, 0.075])
    axes_button_go_to = pylab.axes([0.4, 0.075, 0.25, 0.08])
    axes_sign_slider = pylab.axes([0.06, 0.0, 0.3, 0.075])

    button_add = Button(axes_button_add, 'Next')
    button_remove = Button(axes_button_remove, 'Previous')
    button_save_to_file = Button(axes_button_save_to_file, 'Save')

    global hour_slider, minute_slider, sign_slider
    hour_slider = Slider(axes_slider1, "HOURS: ", 0, 23, 0, valstep=1)
    minute_slider = Slider(axes_slider2, "MINUTES: ", 0, 59, 0, valstep=1)
    button_go_to = Button(axes_button_go_to, "Go to")
    sign_slider = Slider(axes_sign_slider, "SIGNAL: ", 0, 2, 0, valstep=1)
    sign_slider.set_val(Variables.FilesConstant.current_signal)
    sign_slider.on_changed(gr.sign_slider)

    button_add.on_clicked(gr.next)
    button_remove.on_clicked(gr.prev)
    button_save_to_file.on_clicked(gr.saveToFile)
    button_go_to.on_clicked(gr.buttonGoTo)

    add_plot_menu()
    global check
    check.on_clicked(func)
    pylab.show()

#
# start_plot()