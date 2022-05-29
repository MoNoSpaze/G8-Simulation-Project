from PyQt5 import QtCore, QtGui, QtWidgets

import sys
import os

from PyQt5.QtWidgets import QMainWindow, QApplication

import pyqtgraph as pg
from PyQt5.QtCore import QTimer, QDateTime
from datetime import datetime as dt

from pyqtgraph import PlotWidget
import numpy as np
import pandas as pd

from interface_3 import *

err_tag = 0

h_val = 2.5
k_val = 0.6

x_target_1 = []
y_target_1 = []

u1 = 5.21
firing_angle = 45

t_all = 0
u_x = 0.0
u_y = 0.0

x_animation = []
y_animation = []
t_animation = []


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer = QTimer()

        global widgets
        global err_tag

        widgets = self.ui

        widgets.path_btn.setCheckable(True)
        widgets.path_btn.clicked.connect(self.set_tab_panel)

        widgets.option_btn.setCheckable(True)
        widgets.option_btn.clicked.connect(self.set_tab_panel)

        widgets.speed_input.setText("5.21")
        widgets.speed_input.textChanged.connect(Path.set_speed_value)
        widgets.speed_input.textChanged.connect(self.set_error_panel)

        widgets.angle_input.setText("45")
        widgets.angle_input.textChanged.connect(Path.set_angle_value)
        widgets.angle_input.textChanged.connect(self.set_error_panel)

        widgets.pos_x_input.textChanged.connect(Target.set_target_position)
        widgets.pos_x_input.textChanged.connect(self.set_error_panel)
        widgets.pos_x_input.textChanged.connect(Graph.plot_target)

        widgets.pos_y_input.textChanged.connect(Target.set_target_position)
        widgets.pos_y_input.textChanged.connect(self.set_error_panel)
        widgets.pos_y_input.textChanged.connect(Graph.plot_target)

        widgets.pos_x_input.setText("2.5")
        widgets.pos_y_input.setText("0.6")

        widgets.start_btn.clicked.connect(Path.calc_shooting_value)

        widgets.show_cont_checkbox.toggled.connect(Option.time_stamp_onclick)
        widgets.save_calc_btn.clicked.connect(Option.save_calculation)

        Graph.set_graph_widget(Graph)

        self.show()

    def set_tab_panel(self, MainWindow):
        btn = widgets.tab_btn.sender()
        btn_name = btn.objectName()
        # print(btn_name)
        if btn_name == "path_btn":
            widgets.menu_stacked_tab.setCurrentWidget(self.ui.path_page)

            widgets.path_btn.setStyleSheet("color:#000000;\n"
                                           "font: 75 16pt \"Moon\";\n"
                                           "font-weight:bold;\n"
                                           "background-color:#ebc400;\n"
                                           "border-top: 5px solid #ebc400;\n"
                                           "border-left: 5px solid #ebc400;\n"
                                           "border-right: 5px solid #ebc400;\n"
                                           "border-bottom: 5px solid #797270;\n"
                                           "border-radius: 1px;\n")

            widgets.option_btn.setStyleSheet("    color:#000000;\n"
                                             "    font: 75 16pt \"Moon\";\n"
                                             "    font-weight:bold;\n"
                                             "    background-color:#ffd400;\n"
                                             "    border: 5px solid #ffd400;\n"
                                             "    border-radius: 1px;\n")
        if btn_name == "option_btn":
            widgets.menu_stacked_tab.setCurrentWidget(self.ui.option_page)

            widgets.option_btn.setStyleSheet("color:#000000;\n"
                                             "font: 75 16pt \"Moon\";\n"
                                             "font-weight:bold;\n"
                                             "background-color:#ebc400;\n"
                                             "border-top: 5px solid #ebc400;\n"
                                             "border-left: 5px solid #ebc400;\n"
                                             "border-right: 5px solid #ebc400;\n"
                                             "border-bottom: 5px solid #797270;\n"
                                             "border-radius: 1px;\n")

            widgets.path_btn.setStyleSheet("    color:#000000;\n"
                                           "    font: 75 16pt \"Moon\";\n"
                                           "    font-weight:bold;\n"
                                           "    background-color:#ffd400;\n"
                                           "    border: 5px solid #ffd400;\n"
                                           "    border-radius: 1px;\n")

    def set_error_panel(self):
        if err_tag == 0:
            widgets.error_stacked_tab.setCurrentWidget(widgets.err_0)
        if err_tag == 1:
            widgets.error_stacked_tab.setCurrentWidget(widgets.err_1)
        if err_tag == 2:
            widgets.error_stacked_tab.setCurrentWidget(widgets.err_2)
        if err_tag == 3:
            widgets.error_stacked_tab.setCurrentWidget(widgets.err_3)


class Graph(object):
    def __init__(self):
        pass

    def set_graph_widget(self):
        widgets.Graph_widget.setBackground('w')
        widgets.Graph_widget.showGrid(x=True, y=True)

    def plot_target(self):
        global h_val, k_val

        widgets.Graph_widget.setXRange(-0.5, h_val + 1)
        widgets.Graph_widget.setYRange(-0.5, k_val + 1)
        widgets.Graph_widget.setAspectLocked(1)
        target_pen = pg.mkPen(color=(170, 0, 0), width=4)
        widgets.Graph_widget.clear()
        widgets.Graph_widget.plot(x_target_1, y_target_1, pen=target_pen)

    def update_path(self):
        global animation_frame, u1, u_x, u_y, x_animation, y_animation, t_animation, t_all, h_val, k_val
        widgets.animation_progress_bar.setProperty("value", 0)
        path_pen = pg.mkPen(color=(0, 170, 0), width=4)

        widgets.Graph_widget.clear()
        Graph.plot_target(Graph)

        if is_time_stamp:
            widgets.Graph_widget.plot(x_animation, y_animation,
                                   pen=path_pen, symbol='+', symbolSize=20, symbolBrush=('b'))
        if not is_time_stamp:
            widgets.Graph_widget.plot(x_animation, y_animation,
                                   pen=path_pen)

        widgets.Graph_widget.setXRange(-1, h_val + 1)
        widgets.Graph_widget.setYRange(-1, k_val + 1)

        widgets.time_used_display.setText(str(np.around(t_all, 4)) + " sec")
        widgets.s_x_display.setText(str(np.around(x_animation[animation_frame-1], 4))+" meter")
        widgets.s_y_display.setText(str(np.around(y_animation[animation_frame-1], 4))+" meter")

        widgets.animation_progress_bar.setProperty("value", 100)
        widgets.percent_label.setText("100%")
        print("stop!")



class Path(object):
    def __init__(self):
        global u1
        global firing_angle
        global err_tag

        u1 = 5.21
        firing_angle = 45
        pass

    def set_speed_value(self):
        global err_tag, u1, u_x, u_y

        ########################### SPEED INPUT ###########################
        if widgets.speed_input.text() != '' and widgets.speed_input.text()[0] == '-':
            err_tag = 1
            u1 = -999
            widgets.start_btn.setEnabled(False)
        if widgets.speed_input.text() == '':
            err_tag = 0
            u1 = 0
            widgets.start_btn.setEnabled(True)
        if widgets.speed_input.text() != '' and widgets.speed_input.text()[0] != '-' and len(
                widgets.speed_input.text()) >= 1:
            err_tag = 0
            u1 = float(widgets.speed_input.text())
            widgets.start_btn.setEnabled(True)
        # u_x = u1 * np.cos((np.pi / 180) * self.adapted_firing_angle)
        # u_y = u1 * np.sin((np.pi / 180) * self.adapted_firing_angle)

    def set_angle_value(self):
        global err_tag, firing_angle

        ########################### ANGLE INPUT ###########################
        if widgets.angle_input.text() != '' and widgets.angle_input.text()[0] == '-':
            err_tag = 2
            firing_angle = 0  # set error
            widgets.start_btn.setEnabled(False)

        if widgets.angle_input.text() != '' and widgets.angle_input.text()[0] != '-' and not float(
                widgets.angle_input.text()) <= 90:
            err_tag = 2
            firing_angle = 0  # set error
            widgets.start_btn.setEnabled(False)

        if widgets.angle_input.text() == '':
            err_tag = 0
            firing_angle = 0
            widgets.start_btn.setEnabled(True)

        if widgets.angle_input.text() != '' and widgets.angle_input.text()[0] != '-' and len(
                widgets.angle_input.text()) >= 1 and float(widgets.angle_input.text()) <= 90:
            err_tag = 0
            firing_angle = float(widgets.angle_input.text())
            widgets.start_btn.setEnabled(True)

    def calc_shooting_value(self):
        global animation_frame, u1, u_x, u_y, x_animation, y_animation, t_animation, t_all

        animation_frame = 1
        u_x = u1 * np.cos((np.pi / 180) * firing_angle)
        u_y = u1 * np.sin((np.pi / 180) * firing_angle)

        t_all = (u_y + np.sqrt(((-1 * u_y) ** 2) - (4 * 4.9 * (-0.4)))) / (2 * 4.9)
        t_animation = np.arange(0, t_all, 0.005)  # every 5 milliseconds
        x_animation = u_x * t_animation
        y_animation = 0.4 + u_y * t_animation + 0.5 * (-9.81) * (t_animation ** 2)

        Graph.update_path(Graph)




class Target(object):
    def set_target_position(self):
        global err_tag, x_target_1, y_target_1, h_val, k_val

        if widgets.pos_x_input.text() != '' and widgets.pos_x_input.text()[0] == '-':
            err_tag = 3
            h_val = -999
            widgets.start_btn.setEnabled(False)
        if widgets.pos_y_input.text() != '' and widgets.pos_y_input.text()[0] == '-':
            err_tag = 3
            k_val = -999
            widgets.start_btn.setEnabled(False)

        if widgets.pos_x_input.text() == '':
            err_tag = 0
            h_val = 0
            widgets.start_btn.setEnabled(True)
        if widgets.pos_y_input.text() == '':
            err_tag = 0
            k_val = 0
            widgets.start_btn.setEnabled(True)

        if widgets.pos_x_input.text() != '' and widgets.pos_x_input.text()[0] != '-' and len(
                widgets.pos_x_input.text()) >= 1:
            err_tag = 0
            h_val = float(widgets.pos_x_input.text())
            widgets.start_btn.setEnabled(True)
        if widgets.pos_x_input.text() != '' and widgets.pos_x_input.text()[0] != '-' and len(
                widgets.pos_y_input.text()) >= 1:
            err_tag = 0
            k_val = float(widgets.pos_y_input.text())
            widgets.start_btn.setEnabled(True)

        if h_val == -999 or k_val == -999:
            x_target_1 = [0, 0, 0]
            y_target_1 = [0, 0, 0]

        elif h_val != -999 or k_val != -999:
            x_target_1 = [h_val - 0.2, h_val, h_val + 0.2]
            y_target_1 = [k_val + 0.05, k_val, k_val + 0.05]

        print(h_val, k_val, x_target_1, y_target_1)


class Option(object):
    def time_stamp_onclick(self):
        global is_time_stamp

        if is_time_stamp:
            is_time_stamp = False
        else:
            is_time_stamp = True
        print('time stamp: ', is_time_stamp)

    def save_calculation(self):
        global t_animation, x_animation, y_animation

        df = pd.DataFrame(
            {
                'Time': t_animation,
                'X': x_animation,
                'Y': y_animation
            }
        )

        f_type = widgets.file_type_select.currentText()
        print(f_type)
        print(QDateTime.currentDateTime().toPyDateTime())

        date_time_name = dt.now().strftime("%d-%m-%Y_%H-%M-%S")
        if f_type == "CSV":
            df.to_csv(r"D:\G8_App_v2\file_save\export_"+str(date_time_name)+".csv", index=False, header=True)
        if f_type == "TXT":
            df.to_csv(r"D:\G8_App_v2\file_save\export_"+str(date_time_name)+".txt", index=False, header=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
