#!/usr/bin/python3
#-*- coding: utf-8 -*-

# import system libs
# подключение системных библиотек
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QCheckBox, QComboBox
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPointF
from math import exp, sqrt
from time import sleep

# constants
# константы
G = 6.67408 * (10 ** (-11))

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
window0x = 50
window0y = 50

# default window size
# начальные размеры окна
window_sizex = 950
window_sizey = 700

# lists with numerical values
# списки со значениями координат, полученных численно
x = [0] * N
y = [0] * N
# списки со значениями скоростей, полученных численно
vx = [0] * N
vy = [0] * N

norm_r_ij = [[0] * N] * N
r_ij_x = [[0] * N] * N
r_ij_y = [[0] * N] * N

eps = 0.001

current_body_index=0

# some window modifiers
diffx=50
diffy=100

# QT widget to draw GUI
# Виджет для рисования графического интерфейса
class TaskWidget (QWidget):

    # constructor of TaskWidget
    # конструктор объектов класса TaskWidget
    def __init__(self):
        # call constructor on parent object
        # функция super() возвращает родительский объект, и мы вызываем его конструктор
        super().__init__()

        # create GUI
        # вызываем функцию, создающую графический интерфейс
        self.initUI()
        self.timestep = 0


    def change_body(self, index):
      global current_body_index
      current_body_index = index

      self.le3.setText(str(m[current_body_index]))
      self.le4.setText(str(x[current_body_index]))
      self.le5.setText(str(y[current_body_index]))
      self.le6.setText(str(vx[current_body_index]))
      self.le7.setText(str(vy[current_body_index]))

      self.sb.setText("Сохранить значения для " + str(current_body_index) + " тела")


    def save_body(self):
      # get values from editor windows
      # получаем введенные значения
      m[current_body_index]=float(self.le3.text())
      x[current_body_index]=float(self.le4.text())
      y[current_body_index]=float(self.le5.text())
      vx[current_body_index]=float(self.le6.text())
      vy[current_body_index]=float(self.le7.text())
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

      self.update()
      sleep(0.1)


    # функция для проведения вычислений
    def calculate(self):
      self.timestep = 0
      self.update_r_ij()

      for i in range(0,N):
        vx[i] = vx[i] + dt * G / 2 * self.calculate_r_ij_sum_x(i)
        vy[i] = vy[i] + dt * G / 2 * self.calculate_r_ij_sum_y(i)

      for self.timestep in range(0, T):
        print(str(self.timestep) + ' ' + str(x[0]))
        self.calculate_step()


    # button click handler
    # функция для обработки нажатия кнопки
    def button_click (self):
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
        self.pb.move (20, 10)
        self.pb.clicked.connect(self.button_click)

        self.sb = QPushButton("Сохранить значения для " + str(current_body_index) + " тела", self)
        self.sb.move (20, 50)
        self.sb.clicked.connect(self.save_body)

        self.сb = QComboBox(self)
        elements=[''] * N
        for i in range(0,N):
          elements[i]='Тело ' + str(i)
        self.сb.addItems(elements)
        self.сb.move (130, 10)
        self.сb.currentIndexChanged.connect(self.change_body)

        # edit fields
        # поля для ввода параметров
        self.le1 = QLineEdit(str(T), self)
        self.le1.move (240, 10)
        self.le1.setFixedWidth (50)

        self.le2 = QLineEdit(str(dt), self)
        self.le2.move (330, 10)
        self.le2.setFixedWidth (50)

        self.le3 = QLineEdit(str(m[current_body_index]), self)
        self.le3.move (430, 10)
        self.le3.setFixedWidth (50)

        self.le4 = QLineEdit(str(x[current_body_index]), self)
        self.le4.move (530, 10)
        self.le4.setFixedWidth (50)

        self.le5 = QLineEdit(str(y[current_body_index]), self)
        self.le5.move (630, 10)
        self.le5.setFixedWidth (50)

        self.le6 = QLineEdit(str(vx[current_body_index]), self)
        self.le6.move (730, 10)
        self.le6.setFixedWidth (50)

        self.le7 = QLineEdit(str(vy[current_body_index]), self)
        self.le7.move (830, 10)
        self.le7.setFixedWidth (50)

        # show widget
        # показать виджет
        self.show()


    # convert x coordinate to position
    # функция для преобразования координаты x в позицию на экране
    def xToPos(self,val):
        return diffx + self.shiftx * max(x) - self.shiftx * val


    # convert y coordinate to position
    # функция для преобразования координаты y в позицию на экране
    def yToPos(self,val):
        return diffy + self.shifty * max(y) - self.shifty * val


    # init shift coefficients
    # функция для вычисления коэффициентов для рисования
    def initShifts(self):
        maxx = max(x)
        minx = min(x)

        maxy = max(y)
        miny = min(y)

        if maxx == minx:
          maxx = minx + 1
        if maxy == miny:
          maxy = miny + 1

        self.shiftx = (window_sizex - 2*diffx) / (maxx - minx)
        self.shifty = (window_sizey - 2*diffy) / (maxy - miny)


    # draw strings
    # функция для рисования имен параметров
    def drawStrings(self, qp):
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)

        # draw strings
        # рисование имен параметров
        qp.drawText (QPointF(220, 28), "T=")
        qp.drawText (QPointF(306, 28), "dt=")
        qp.drawText (QPointF(405, 28), "m=")
        qp.drawText (QPointF(503, 28), "x0=")
        qp.drawText (QPointF(603, 28), "y0=")
        qp.drawText (QPointF(697, 28), "vx0=")
        qp.drawText (QPointF(797, 28), "vy0=")

        qp.drawText (QPointF(700, 50), str(self.timestep))


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
        qp.drawText (QPointF(self.xToPos(0) + 5, self.yToPos(0) - 5), "O")
        qp.drawText (QPointF(window_sizex - diffx, self.yToPos(0) - 5), "X")
        qp.drawText (QPointF(self.xToPos(0) - 10, diffy), "Y")

        #qp.drawText (QPointF(self.xToPos(0) + 5, diffy), str(max(y_exact)))
        #qp.drawText (QPointF(self.xToPos(0) + 5, window_sizey - diffy), str(min(y_exact)))
        #qp.drawText (QPointF(self.xToPos(x_exact[N-1]) - 5, self.yToPos(0) + 20), str(x_exact[N-1]))

        # draw axes
        # рисование осей
        pen = QPen(Qt.black, 2, Qt.DashLine)
        qp.setPen(pen)

        qp.drawLine(diffx, self.yToPos(0), window_sizex - diffx, self.yToPos(0))
        qp.drawLine(self.xToPos(0), window_sizey - diffy, self.xToPos(0), diffy)

        # draw numerical solution
        # рисование численного решения
        pen = QPen(Qt.red, 10, Qt.SolidLine)
        qp.setPen(pen)

        for i in range(0,N):
          qp.drawPoint(self.xToPos(x[i]), self.yToPos(y[i]))


# starting point
# начало выполнения программы
if __name__ == '__main__':

    # create application
    # создание объекта приложения
    app = QApplication(sys.argv)

    # create TaskWidget object and call its constructor
    # создаем объект TaskWidget и вызываем его конструктор
    ex = TaskWidget ()

    # launch app cycle
    # запуск основного цикла событий
    sys.exit(app.exec_())
