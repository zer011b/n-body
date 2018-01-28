#!/usr/bin/python3
#-*- coding: utf-8 -*-

# import system libs
# подключение системных библиотек
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QCheckBox, QComboBox
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPointF
from math import exp, sqrt

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
m = [0] * N

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


    # функция для обновления r_ij
    def update_r_ij():
      for i in range(0,N):
        for j in range(0,N):
          r_ij_x[i][j] = x[j] - x[i];
          r_ij_y[i][j] = y[j] - y[i];
          norm_r_ij[i][j] = (r_ij_x[i][j]) ** 2 + (r_ij_y[i][j]) ** 2

    def calculate_r_ij_sum_x(index):
      sum=0
      for j in range(0,N):
        sum += m[j] * r_ij_x[index][j] / math.sqrt((norm_r_ij[index][j] + eps ** 2) ** 3)
      return sum

    def calculate_r_ij_sum_y(index):
      sum=0
      for j in range(0,N):
        sum += m[j] * r_ij_y[index][j] / math.sqrt((norm_r_ij[index][j] + eps ** 2) ** 3)
      return sum


    # функция для расчета одного временного шага
    def calculate_step():
      for i in range(0,N):
        x[i] = x[i] + dt * vx[i]
        y[i] = y[i] + dt * vy[i]

      update_r_ij()

      for i in range(0,N):
        vx[i] = vx[i] + dt * G * calculate_r_ij_sum_x(i)
        vy[i] = vy[i] + dt * G * calculate_r_ij_sum_y(i)

      self.update()


    # функция для проведения вычислений
    def calculate():
      timestep = 0
      update_r_ij()

      for i in range(0,N):
        vx[i] = vx[i] + dt * G / 2 * calculate_r_ij_sum_x(i)
        vy[i] = vy[i] + dt * G / 2 * calculate_r_ij_sum_y(i)

      for timestep in range(0, T):
        calculate_step()


    # button click handler
    # функция для обработки нажатия кнопки
    def button_click (self):
      global N, dt, k, m, x0, y0, vx0, vy0, useAirResistance

      self.pb.setEnabled(False)
      button.setText("Подождите")

      # get values from editor windows
      # получаем введенные значения
      dt=float(self.le2.text())

      # calculate numerical and exact solutions
      # вычисляем численное и точное решения
      calculate()
      button.setText("Расчет")
      self.pb.setEnabled(True)


    # create GUI
    # функция для создания графического интерфейса
    def initUI(self):
        # geometry of window
        # задание геометрии окна и заголовка
        self.setGeometry(window0x, window0y, window_sizex, window_sizey)
        #self.setWindowTitle('Gravity')
        self.setWindowTitle('Движение тела в поле силы тяжести')

        # toggle for resistance
        # задание переключателя режима с/без сопротивления
        #self.cb = QCheckBox('Use air resistance', self)
        self.cb = QCheckBox('Использовать сопротивление воздуха', self)
        self.cb.move(330, 40)
        self.cb.toggle ()
        self.cb.stateChanged.connect(self.changeUseAirResistance)

        # button for calculation
        # кнопка для начала расчета
        #self.pb = QPushButton("calculate", self)
        self.pb = QPushButton("Расчет", self)
        self.pb.move (20, 10)
        self.pb.clicked.connect(self.button_click)

        self.сb = QComboBox(self)
        self.сb.addItems(['Первый порядок точности', 'Второй порядок точности'])
        self.сb.move (20, 40)
        self.сb.currentIndexChanged.connect(self.change_order)

        # edit fields
        # поля для ввода параметров
        self.le1 = QLineEdit(str(N), self)
        self.le1.move (140, 10)
        self.le1.setFixedWidth (50)

        self.le2 = QLineEdit(str(dt), self)
        self.le2.move (230, 10)
        self.le2.setFixedWidth (50)

        self.le3 = QLineEdit(str(k), self)
        self.le3.move (330, 10)
        self.le3.setFixedWidth (50)

        self.le4 = QLineEdit(str(m), self)
        self.le4.move (430, 10)
        self.le4.setFixedWidth (50)

        self.le5 = QLineEdit(str(x0), self)
        self.le5.move (530, 10)
        self.le5.setFixedWidth (50)

        self.le6 = QLineEdit(str(y0), self)
        self.le6.move (630, 10)
        self.le6.setFixedWidth (50)

        self.le7 = QLineEdit(str(vx0), self)
        self.le7.move (730, 10)
        self.le7.setFixedWidth (50)

        self.le8 = QLineEdit(str(vy0), self)
        self.le8.move (830, 10)
        self.le8.setFixedWidth (50)

        # show widget
        # показать виджет
        self.show()


    # convert x coordinate to position
    # функция для преобразования координаты x в позицию на экране
    def xToPos(self,val):
        return diffx + self.shiftx * val


    # convert y coordinate to position
    # функция для преобразования координаты y в позицию на экране
    def yToPos(self,val):
        return diffy + self.shifty * max(y_exact) - self.shifty * val


    # init shift coefficients
    # функция для вычисления коэффициентов для рисования
    def initShifts(self):
        maxx = max(x_exact)
        if maxx == 0:
          maxx = 1

        maxy = max(y_exact)
        if maxy == 0:
          maxy = 1

        miny = min(y_exact)
        if miny == 0:
          miny = 1

        self.shiftx = (window_sizex - 2*diffx) / maxx
        self.shifty = (window_sizey - 2*diffy) / (maxy - miny)


    # draw strings
    # функция для рисования имен параметров
    def drawStrings(self, qp):
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)

        # draw strings
        # рисование имен параметров
        qp.drawText (QPointF(120, 28), "N=")
        qp.drawText (QPointF(206, 28), "dt=")
        qp.drawText (QPointF(310, 28), "k=")
        qp.drawText (QPointF(405, 28), "m=")
        qp.drawText (QPointF(503, 28), "x0=")
        qp.drawText (QPointF(603, 28), "y0=")
        qp.drawText (QPointF(697, 28), "vx0=")
        qp.drawText (QPointF(797, 28), "vy0=")

        pen = QPen(Qt.red, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawText (QPointF(700, 60), "Численное решение")

        pen = QPen(Qt.green, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawText (QPointF(700, 80), "Точное решение")

        pen = QPen(Qt.red, 4, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawText (QPointF(20, 650), "Норма разности точного и численного решений: " + str(norm))


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

        qp.drawText (QPointF(self.xToPos(0) + 5, diffy), str(max(y_exact)))
        qp.drawText (QPointF(self.xToPos(0) + 5, window_sizey - diffy), str(min(y_exact)))
        qp.drawText (QPointF(self.xToPos(x_exact[N-1]) - 5, self.yToPos(0) + 20), str(x_exact[N-1]))

        # draw axes
        # рисование осей
        pen = QPen(Qt.black, 2, Qt.DashLine)
        qp.setPen(pen)

        qp.drawLine(self.xToPos(0), self.yToPos(0), self.xToPos(x_exact[N-1]), self.yToPos(0))
        qp.drawLine(self.xToPos(0), window_sizey - diffy, self.xToPos(0), diffy)

        # draw numerical solution
        # рисование численного решения
        pen = QPen(Qt.red, 1, Qt.SolidLine)
        qp.setPen(pen)

        for i in range(1,N):
          qp.drawLine(self.xToPos(x[i-1]), self.yToPos(y[i-1]), self.xToPos(x[i]), self.yToPos(y[i]))

        # draw exact solution
        # рисование точного решения
        pen = QPen(Qt.green, 1, Qt.SolidLine)
        qp.setPen(pen)

        for i in range(1,N):
          qp.drawLine(self.xToPos(x_exact[i-1]), self.yToPos(y_exact[i-1]), self.xToPos(x_exact[i]), self.yToPos(y_exact[i]))


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
