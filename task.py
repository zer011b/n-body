#!/usr/bin/python3
#-*- coding: utf-8 -*-

# compare with http://www.andreasfaisst.ch/Simulationen/Nbody/2body.php

# import system libs
# подключение системных библиотек
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QCheckBox, QComboBox
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPointF
from math import exp, sqrt
from time import sleep
import random

# constants
# константы
G = 1
#G = 6.67408 * (10 ** (-11))

# default values for global variables
# глобальные переменные с их значениями по умолчанию

# число тел
N = 2
# number of points
# число точек по времени
T = 50
# numerical step
# разностный шаг по времени
dt = 0.1
# mass
# масса тела
m = [1] * N

# default window position
# начальная позиция окна
window0x = 0
window0y = 0

# default window size
# начальные размеры окна
window_sizex = 900
window_sizey = 700

# lists with numerical values
# списки со значениями координат, полученных численно
x = [0] * N
y = [0] * N
# списки со значениями скоростей, полученных численно
vx = [0] * N
vy = [0] * N

x0 = [0] * N
y0 = [0] * N
vx0 = [0] * N
vy0 = [0] * N

color = [QColor()] * N

norm_r_ij = [[0 for x in range(N)] for y in range(N)]
r_ij_x = [[0 for x in range(N)] for y in range(N)]
r_ij_y = [[0 for x in range(N)] for y in range(N)]

eps = 0.001

current_body_index=0

# some window modifiers
diffxL=50
diffxR=250
diffyU=50
diffyD=50

area_sizex = 200
area_sizey = 200

area_startx = -100
area_starty = -100

# QT widget to draw GUI
# Виджет для рисования графического интерфейса
class TaskWidget (QWidget):

    # constructor of TaskWidget
    # конструктор объектов класса TaskWidget
    def __init__(self, app):
        # call constructor on parent object
        # функция super() возвращает родительский объект, и мы вызываем его конструктор
        super().__init__()

        # create GUI
        # вызываем функцию, создающую графический интерфейс
        self.initUI()
        self.timestep = 0
        self.app = app


    def change_body(self, index):
      global current_body_index
      current_body_index = index

      self.le3.setText(str(m[current_body_index]))
      self.le4.setText(str(x0[current_body_index]))
      self.le5.setText(str(y0[current_body_index]))
      self.le6.setText(str(vx0[current_body_index]))
      self.le7.setText(str(vy0[current_body_index]))

      self.sb.setText("Сохранить для " + str(current_body_index) + " тела")

    def update_area(self, maxx, maxy, minx, miny):
      global area_sizex, area_sizey, area_startx, area_starty

      if maxx - minx < 0.05 * area_sizex or maxx - minx > 0.95 * area_sizex \
         or minx <= area_startx or maxx >= area_startx + area_sizex:
        area_sizex = 10*(maxx - minx)
        if area_sizex == 0:
          area_sizex = 200
        area_startx = (maxx + minx)/2 - area_sizex/2

      if maxy - miny < 0.05 * area_sizey or maxy - miny > 0.95 * area_sizey \
         or miny <= area_starty or maxy >= area_starty + area_sizey:
        area_sizey = 10*(maxy - miny)
        if area_sizey == 0:
          area_sizey = 200
        area_starty = (maxy + miny)/2 - area_sizey/2


    def save_body(self):
      # get values from editor windows
      # получаем введенные значения
      m[current_body_index]=float(self.le3.text())
      x0[current_body_index]=float(self.le4.text())
      y0[current_body_index]=float(self.le5.text())
      vx0[current_body_index]=float(self.le6.text())
      vy0[current_body_index]=float(self.le7.text())

      color[current_body_index] = QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255))

      for i in range(0,N):
        x[i] = x0[i]
        y[i] = y0[i]
        vx[i] = vx0[i]
        vy[i] = vy0[i]

      self.update_area(max(x), max(y), min(x), min(y))
      self.update()


    # функция для обновления r_ij
    def update_r_ij(self):
      for i in range(0,N):
        for j in range(0,N):
          r_ij_x[i][j] = x[j] - x[i];
          r_ij_y[i][j] = y[j] - y[i];
          norm_r_ij[i][j] = (r_ij_x[i][j]) ** 2 + (r_ij_y[i][j]) ** 2

    def calculate_r_ij_sum_x(self, index):
      sum=0
      for j in range(0,N):
        sum += m[j] * r_ij_x[index][j] / sqrt((norm_r_ij[index][j] + eps ** 2) ** 3)
      return sum

    def calculate_r_ij_sum_y(self, index):
      sum=0
      for j in range(0,N):
        sum += m[j] * r_ij_y[index][j] / sqrt((norm_r_ij[index][j] + eps ** 2) ** 3)
      return sum


    # функция для расчета одного временного шага
    def calculate_step(self):
      for i in range(0,N):
        x[i] = x[i] + dt * vx[i]
        y[i] = y[i] + dt * vy[i]

      self.update_r_ij()

      for i in range(0,N):
        vx[i] = vx[i] + dt * G * self.calculate_r_ij_sum_x(i)
        vy[i] = vy[i] + dt * G * self.calculate_r_ij_sum_y(i)

      self.update_area(max(x), max(y), min(x), min(y))
      self.update()
      #sleep(0.05)
      self.app.processEvents()


    # функция для проведения вычислений
    def calculate(self):
      self.timestep = 0
      self.update_r_ij()

      for i in range(0,N):
        vx[i] = vx[i] + dt * G / 2 * self.calculate_r_ij_sum_x(i)
        vy[i] = vy[i] + dt * G / 2 * self.calculate_r_ij_sum_y(i)

      for self.timestep in range(0, T):
        print(str(self.timestep) + ': (' + str(x[0]) + ',' + str(y[0])+'); (' + str(x[1]) + ',' + str(y[1]) + ')')
        self.calculate_step()


    # button click handler
    # функция для обработки нажатия кнопки
    def button_click (self):
      global T, dt
      self.pb.setEnabled(False)
      self.pb.setText("Подождите")

      # get values from editor windows
      # получаем введенные значения
      T=int(self.le1.text())
      dt=float(self.le2.text())

      # calculate numerical and exact solutions
      # вычисляем численное и точное решения
      self.calculate()
      self.pb.setText("Расчет")
      self.pb.setEnabled(True)


    # create GUI
    # функция для создания графического интерфейса
    def initUI(self):
        # geometry of window
        # задание геометрии окна и заголовка
        self.setGeometry(window0x, window0y, window_sizex, window_sizey)
        #self.setWindowTitle('Gravity')
        self.setWindowTitle('Моделирование гравитационного взаимодействия N тел')

        # button for calculation
        # кнопка для начала расчета
        self.pb = QPushButton("Расчет", self)
        self.pb.move (window_sizex - 180, 550)
        self.pb.clicked.connect(self.button_click)
        self.pb.setFixedWidth (150)

        self.sb = QPushButton("Сохранить для " + str(current_body_index) + " тела", self)
        self.sb.move (window_sizex - 185, 125)
        self.sb.clicked.connect(self.save_body)

        self.сb = QComboBox(self)
        elements=[''] * N
        for i in range(0,N):
          elements[i]='Тело ' + str(i)
        self.сb.addItems(elements)
        self.сb.move (window_sizex - 100, 90)
        self.сb.currentIndexChanged.connect(self.change_body)

        # edit fields
        # поля для ввода параметров
        self.le1 = QLineEdit(str(T), self)
        self.le1.move (window_sizex - 180, 430)
        self.le1.setFixedWidth (150)

        self.le2 = QLineEdit(str(dt), self)
        self.le2.move (window_sizex - 180, 510)
        self.le2.setFixedWidth (150)

        self.le3 = QLineEdit(str(m[current_body_index]), self)
        self.le3.move (window_sizex - 100, 190)
        self.le3.setFixedWidth (75)

        self.le4 = QLineEdit(str(x[current_body_index]), self)
        self.le4.move (window_sizex - 100, 220)
        self.le4.setFixedWidth (75)

        self.le5 = QLineEdit(str(y[current_body_index]), self)
        self.le5.move (window_sizex - 100, 250)
        self.le5.setFixedWidth (75)

        self.le6 = QLineEdit(str(vx[current_body_index]), self)
        self.le6.move (window_sizex - 100, 280)
        self.le6.setFixedWidth (75)

        self.le7 = QLineEdit(str(vy[current_body_index]), self)
        self.le7.move (window_sizex - 100, 310)
        self.le7.setFixedWidth (75)

        # show widget
        # показать виджет
        self.show()


    # convert x coordinate to position
    # функция для преобразования координаты x в позицию на экране
    def xToPos(self,val):
        return diffxL + self.shiftx * (val - area_startx)


    # convert y coordinate to position
    # функция для преобразования координаты y в позицию на экране
    def yToPos(self,val):
        return diffyD + self.shifty * (val - area_starty)


    # init shift coefficients
    # функция для вычисления коэффициентов для рисования
    def initShifts(self):
        self.shiftx = (window_sizex - diffxL - diffxR) / area_sizex
        self.shifty = (window_sizey - diffyD - diffyU) / area_sizey


    # draw strings
    # функция для рисования имен параметров
    def drawStrings(self, qp):
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)

        # draw strings
        # рисование имен параметров
        qp.drawText (QPointF(window_sizex - 148, 420), "число шагов T")
        qp.drawText (QPointF(window_sizex - 167, 500), "шаг по времени dt")
        qp.drawText (QPointF(window_sizex - 178, 206), "масса m =")
        qp.drawText (QPointF(window_sizex - 138, 236), "x0 =")
        qp.drawText (QPointF(window_sizex - 138, 266), "y0 =")
        qp.drawText (QPointF(window_sizex - 146, 296), "vx0 =")
        qp.drawText (QPointF(window_sizex - 146, 326), "vy0 =")

        qp.drawText (QPointF(700, 650), "Текущий шаг: " + str(self.timestep))

        #qp.drawText (QPointF(100, 650), "Тело 0: r(" + str(x[0]) + ", " + str(y[0]) + "); v(" + str(vx[0]) + ", " + str(vy[0])+ ")")
        #qp.drawText (QPointF(100, 670), "Тело 1: r(" + str(x[1]) + ", " + str(y[1]) + "); v(" + str(vx[1]) + ", " + str(vy[1])+ ")")

        qp.drawLine(window_sizex - 200, 80, window_sizex - 200, 350)
        qp.drawLine(window_sizex - 200, 80, window_sizex - 10, 80)
        qp.drawLine(window_sizex - 10, 80, window_sizex - 10, 350)
        qp.drawLine(window_sizex - 200, 350, window_sizex - 10, 350)

        qp.drawLine(window_sizex - 200, 400, window_sizex - 200, 600)
        qp.drawLine(window_sizex - 200, 400, window_sizex - 10, 400)
        qp.drawLine(window_sizex - 10, 400, window_sizex - 10, 600)
        qp.drawLine(window_sizex - 200, 600, window_sizex - 10, 600)


    # paint of widget
    # функция рисования для виджета
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()


    # paint axes and lines
    # функция рисования осей и решений
    def drawLines(self, qp):
        # calculate shift coefficients
        # посчитаем коэффициент для рисования
        self.initShifts()

        # draw strings
        # рисование имен параметров
        self.drawStrings(qp)

        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)

        # draw axes
        # рисование обозначений осей
        qp.drawText (QPointF(window_sizex - diffxR + 10, diffyD + 5), "X")
        qp.drawText (QPointF(diffxL - 15, window_sizey - diffyU + 20), "Y")

        qp.drawText (QPointF(diffxL, diffyD - 5), str(area_startx))
        qp.drawText (QPointF(window_sizex - diffxR - 30, diffyD - 5), str(area_startx + area_sizex))

        #qp.drawText (QPointF(self.xToPos(0) + 5, diffy), str(max(y_exact)))
        #qp.drawText (QPointF(self.xToPos(0) + 5, window_sizey - diffy), str(min(y_exact)))
        #qp.drawText (QPointF(self.xToPos(x_exact[N-1]) - 5, self.yToPos(0) + 20), str(x_exact[N-1]))

        # draw axes
        # рисование осей
        pen = QPen(Qt.black, 2, Qt.DashLine)
        qp.setPen(pen)

        qp.drawLine(diffxL, diffyD, window_sizex - diffxR, diffyD)
        qp.drawLine(diffxL, diffyD, diffxL, window_sizey - diffyU)
        qp.drawLine(window_sizex - diffxR, diffyD, window_sizex - diffxR, window_sizey - diffyU)
        qp.drawLine(diffxL, window_sizey - diffyU, window_sizex - diffxR, window_sizey - diffyU)

        # draw numerical solution
        # рисование численного решения
        pen = QPen(Qt.red, 10, Qt.SolidLine)
        qp.setPen(pen)

        for i in range(0,N):
          pen = QPen(color[i], 10, Qt.SolidLine)
          qp.setPen(pen)
          qp.drawPoint(self.xToPos(x[i]), self.yToPos(y[i]))


# starting point
# начало выполнения программы
if __name__ == '__main__':

    # create application
    # создание объекта приложения
    app = QApplication(sys.argv)

    # create TaskWidget object and call its constructor
    # создаем объект TaskWidget и вызываем его конструктор
    ex = TaskWidget (app)

    # launch app cycle
    # запуск основного цикла событий
    sys.exit(app.exec_())
