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
import random

# constants
# константы

# минимальное расстояние между телами
eps = 0.001

# безразмерная константа G
G = 1
# размерная константа G
# G = 6.67408 * (10 ** (-11))

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
# масса тел
m = []

# default window position
# начальная позиция окна
window0x = 0
window0y = 0

# default window size
# начальные размеры окна
window_sizex = 900
window_sizey = 700

# отступы от границ окна
diffxL=50
diffxR=250
diffyU=50
diffyD=50

# начальный размер области для отображения
area_sizex = 200
area_sizey = 200

# начальные координаты левого верхнего угла области для отображения
area_startx = -100
area_starty = -100

# lists with numerical values
# списки со значениями координат, полученных численно
x = []
y = []
# списки со значениями скоростей, полученных численно
vx = []
vy = []

# списки с начальными координатами
x0 = []
y0 = []

# списки с начальными скоростями
vx0 = []
vy0 = []

# список с цветами тел для отображения
color = []

# список с квадратами норм расстояний между телами
norm_r_ij = []

# списки с компонентами радиус-векторов тел
r_ij_x = []
r_ij_y = []

# список с сохраненными точками траекторий
trajectory_x=[]
trajectory_y=[]

# шаг для сохранения траектории
trajectory_step=10

# индекс текущего выбранного тела в списке в интерфейсе
current_body_index=0

# флаги для отображения
# флаг, показывать траектории или нет
showTrajectory = True
# флаг, показывать имена и координаты или нет
showNames = False

# флаг, идет ли сейчас расчет или нет
isCalculation = False
# флаг, требуется ли остановить вычисления или нет
doStopCalculation = False

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

        # задаем начальный шаг
        self.timestep = 0

        # сохраняем объект приложения для дальнейшего доступа
        self.app = app


    # функция для обработки нажатия на кнопку изменения числа тел
    def change_number_of_bodies(self):
      global N

      # обновляем значение из графического интерфейса
      N=int(self.le0.text())

      # задаем списки согласно новому N
      init_lists()

      # обновляем список выбора тел в интерфейсе
      elements=[''] * N
      for i in range(0,N):
        elements[i]='Тело ' + str(i)
      self.сb.clear()
      self.сb.addItems(elements)

      self.timestep = 0

      # обновляем интерфейс
      self.update()


    # функция для обработки выбора тела в интерфейсе
    def change_body(self, index):
      global current_body_index

      # задаем индекс текущего тела
      current_body_index = index

      # обновляем значения в интерфейсе согласно сохраненным
      self.le3.setText(str(m[current_body_index]))
      self.le4.setText(str(x0[current_body_index]))
      self.le5.setText(str(y0[current_body_index]))
      self.le6.setText(str(vx0[current_body_index]))
      self.le7.setText(str(vy0[current_body_index]))

      # обновляем текст кнопки сохранения
      self.sb.setText("Сохранить для " + str(current_body_index) + " тела")


    # функция для вычисления видимой области
    def update_area(self, maxx, maxy, minx, miny, force = False):
      global area_sizex, area_sizey, area_startx, area_starty

      # вычисляем минимальные и максимальные координаты
      left=min(minx, miny)
      right=max(maxx, maxy)

      # если координаты вышли за пределы области, или занимаемая площадь стала большой,
      # или необходимо обновить видимую область независимо от этих условий, то
      # обновляем видимую область
      if right - left > 0.95 * area_sizex \
         or left <= area_startx or right >= area_startx + area_sizex \
         or force == True:

        # задаем видимую область как удвоенное расстояние между минимальной и максимальной координатами
        area_sizex = 2*(right - left)
        if area_sizex == 0:
          area_sizex = 10
        area_startx = (left + right)/2 - area_sizex/2

        area_sizey=area_sizex
        area_starty=area_startx


    # функция для обработки нажатия на кнопку сохранения параметров для тела
    def save_body(self):
      # get values from editor windows
      # получаем введенные значения
      m[current_body_index]=float(self.le3.text())
      x0[current_body_index]=float(self.le4.text())
      y0[current_body_index]=float(self.le5.text())
      vx0[current_body_index]=float(self.le6.text())
      vy0[current_body_index]=float(self.le7.text())

      # сохраняем текущие значения
      x[current_body_index] = x0[current_body_index]
      y[current_body_index] = y0[current_body_index]
      vx[current_body_index] = vx0[current_body_index]
      vy[current_body_index] = vy0[current_body_index]

      # обновляем видимую область
      self.update_area(max(x), max(y), min(x), min(y))
      self.update()


    # функция для обновления радиус-векторов
    def update_r_ij(self):
      # обходим все пары тел и вычисляем радиус-вектора
      for i in range(0,N):
        for j in range(0,N):
          r_ij_x[i][j] = x[j] - x[i];
          r_ij_y[i][j] = y[j] - y[i];
          norm_r_ij[i][j] = (r_ij_x[i][j]) ** 2 + (r_ij_y[i][j]) ** 2


    # вспомогательная функция для вычислений
    def calculate_r_ij_sum_x(self, index):
      sum=0
      for j in range(0,N):
        sum += m[j] * r_ij_x[index][j] / sqrt((norm_r_ij[index][j] + eps ** 2) ** 3)
      return sum


    # вспомогательная функция для вычислений
    def calculate_r_ij_sum_y(self, index):
      sum=0
      for j in range(0,N):
        sum += m[j] * r_ij_y[index][j] / sqrt((norm_r_ij[index][j] + eps ** 2) ** 3)
      return sum


    # функция для расчета одного временного шага
    def calculate_step(self):
      # обновляем координаты
      for i in range(0,N):
        x[i] = x[i] + dt * vx[i]
        y[i] = y[i] + dt * vy[i]

      # обновляем радиус-векторы
      self.update_r_ij()

      # обновляем скорости
      for i in range(0,N):
        vx[i] = vx[i] + dt * G * self.calculate_r_ij_sum_x(i)
        vy[i] = vy[i] + dt * G * self.calculate_r_ij_sum_y(i)

      # обновляем видимую область
      self.update_area(max(x), max(y), min(x), min(y))
      self.update()

      # разрешаем обработчику событий обработать события интерфейса
      self.app.processEvents()


    # функция для проведения вычислений
    def calculate(self):
      global x, y, vx, vy

      # задаем начальные координаты и скорости
      for i in range(0,N):
        x[i] = x0[i]
        y[i] = y0[i]
        vx[i] = vx0[i]
        vy[i] = vy0[i]

      # задаем начальный шаг
      self.timestep = 0

      # обновляем видимую область
      self.update_area(max(x), max(y), min(x), min(y), True)

      # обновляем радиус-векторы
      self.update_r_ij()

      # выполняем начальный шаг для вычисления скоростей
      for i in range(0,N):
        vx[i] = vx[i] + dt * G / 2 * self.calculate_r_ij_sum_x(i)
        vy[i] = vy[i] + dt * G / 2 * self.calculate_r_ij_sum_y(i)

      # выполняем шаги
      for self.timestep in range(0, T):
        # вычисляем шаг
        self.calculate_step()

        # выходим из цикла, если необходимо остановить вычисления
        if doStopCalculation:
          break

        # если текущий шаг кратен количеству шагов для сохранения траектории, то сохраняем
        if self.timestep % trajectory_step == 0:
          current=int(self.timestep / trajectory_step)
          for i in range(0,N):
            trajectory_x[i][current] = x[i]
            trajectory_y[i][current] = y[i]


    # button click handler
    # функция для обработки нажатия кнопки
    def button_click (self):
      global T, dt, trajectory_x, trajectory_y, doStopCalculation, isCalculation

      # если кнопка нажата и идет расчет, то нужно остановить расчет
      if isCalculation:
        doStopCalculation = True
        isCalculation = False
        return

      # начинаем расчет
      isCalculation = True
      doStopCalculation = False

      # делаем кнопки недоступными
      self.sb.setEnabled(False)
      self.nb.setEnabled(False)
      self.pb.setText("Стоп")

      # get values from editor windows
      # получаем введенные значения
      T=int(self.le1.text())
      dt=float(self.le2.text())

      # задаем списки со значениями для траекторий
      count=max(int(T / trajectory_step), 1)
      for i in range(0,N):
        trajectory_x[i] = [0] * count
        trajectory_y[i] = [0] * count

      # calculate numerical and exact solutions
      # вычисляем численное и точное решения
      self.calculate()

      # делаем кнопки доступными
      self.pb.setText("Расчет")
      self.sb.setEnabled(True)
      self.nb.setEnabled(True)

      # заканчиваем расчет
      isCalculation = False
      doStopCalculation = False


    # функция для обработки нажатия на кнопку показа/выключения траектории
    def changeShowTrajectory (self, state):
      global showTrajectory
      # задаем режим согласно переключателю в графическом интерфейсе
      if state == Qt.Checked:
        showTrajectory=True
      else:
        showTrajectory=False
      self.update()


    # функция для обработки нажатия на кнопку показа/выключения номеров тел и координат
    def changeShowNames (self, state):
      global showNames
      # задаем режим согласно переключателю в графическом интерфейсе
      if state == Qt.Checked:
        showNames=True
      else:
        showNames=False
      self.update()


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

        # кнопка для сохранения параметров для текущего тела
        self.sb = QPushButton("Сохранить для " + str(current_body_index) + " тела", self)
        self.sb.move (window_sizex - 185, 125)
        self.sb.clicked.connect(self.save_body)

        # кнопка для сохранения числа тел
        self.nb = QPushButton("Сохранить N", self)
        self.nb.move (window_sizex - 180, 40)
        self.nb.clicked.connect(self.change_number_of_bodies)
        self.nb.setFixedWidth (170)

        # элемент список с выбором тела
        self.сb = QComboBox(self)
        elements=[''] * N
        for i in range(0,N):
          elements[i]='Тело ' + str(i)
        self.сb.addItems(elements)
        self.сb.move (window_sizex - 100, 90)
        self.сb.currentIndexChanged.connect(self.change_body)

        # кнопка показа траектории
        self.checkBox = QCheckBox("Показать траекторию", self)
        self.checkBox.move(diffxL, window_sizey - 40)
        self.checkBox.toggle ()
        self.checkBox.stateChanged.connect(self.changeShowTrajectory)

        # кнопка показа координат
        self.checkBox1 = QCheckBox("Показать координаты", self)
        self.checkBox1.move(diffxL + 200, window_sizey - 40)
        self.checkBox1.stateChanged.connect(self.changeShowNames)

        # edit fields
        # поля для ввода параметров
        self.le0 = QLineEdit(str(N), self)
        self.le0.move (window_sizex - 80, 10)
        self.le0.setFixedWidth (70)

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
        qp.drawText (QPointF(window_sizex - 180, 28), "число тел N = ")
        qp.drawText (QPointF(window_sizex - 148, 420), "число шагов T")
        qp.drawText (QPointF(window_sizex - 167, 500), "шаг по времени dt")
        qp.drawText (QPointF(window_sizex - 178, 206), "масса m =")
        qp.drawText (QPointF(window_sizex - 138, 236), "x0 =")
        qp.drawText (QPointF(window_sizex - 138, 266), "y0 =")
        qp.drawText (QPointF(window_sizex - 146, 296), "vx0 =")
        qp.drawText (QPointF(window_sizex - 146, 326), "vy0 =")

        qp.drawText (QPointF(700, 650), "Текущий шаг: " + str(self.timestep))

        # рисование границ областей
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
        qp.drawText (QPointF(diffxL - 20, window_sizey - diffyU), "Y")

        qp.drawText (QPointF(diffxL, diffyD - 5), str(int(area_startx)))
        qp.drawText (QPointF(window_sizex - diffxR - 30, diffyD - 5), str(int(area_startx + area_sizex)))

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

          # рисование имени тела
          if showNames:
            qp.drawText (QPointF(self.xToPos(x[i]), self.yToPos(y[i])), "#" + str(i) + ":(" + "{0:.2f}".format(x[i]) + "," + "{0:.2f}".format(y[i]) + ")")

          # рисование траектории
          if showTrajectory:
            pen = QPen(Qt.black, 1, Qt.DashLine)
            qp.setPen(pen)

            count=int(self.timestep / trajectory_step)
            for j in range(0,count):
              qp.drawPoint(self.xToPos(trajectory_x[i][j]), self.yToPos(trajectory_y[i][j]))


# функция для иниицализации списков согласно новому значению параметра N
def init_lists():
  global x, y, vx, vy, x0, y0, vx0, vy0, m, color, norm_r_ij, r_ij_x, r_ij_y, trajectory_x, trajectory_y
  x = [0] * N
  y = [0] * N
  vx = [0] * N
  vy = [0] * N

  x0 = [0] * N
  y0 = [0] * N
  vx0 = [0] * N
  vy0 = [0] * N

  m = [1] * N
  # задаем произвольные цвета для рисования тел
  color = [QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255)) for x in  range(N)]

  norm_r_ij = [[0 for x in range(N)] for y in range(N)]
  r_ij_x = [[0 for x in range(N)] for y in range(N)]
  r_ij_y = [[0 for x in range(N)] for y in range(N)]

  trajectory_x = [[0] for y in range(N)]
  trajectory_y = [[0] for y in range(N)]


# функция для инициализации начальных значений
# Пример: тело, вращающееся вокруг другого тела
def init_default():
  global x, y, vx, vy, x0, y0, vx0, vy0, m
  x0[0] = x[0] = 0
  y0[0] = y[0] = 0
  x0[1] = x[1] = -100
  y0[1] = y[1] = 0

  vx0[0] = vx[0] = 0
  vy0[0] = vy[0] = 0
  vx0[1] = vx[1] = 0
  vy0[1] = vy[1] = 1

  m[0] = 100
  m[1] = 0


# starting point
# начало выполнения программы
if __name__ == '__main__':

    # инициализируем списки и начальные значения
    init_lists()
    init_default()

    # create application
    # создание объекта приложения
    app = QApplication(sys.argv)

    # create TaskWidget object and call its constructor
    # создаем объект TaskWidget и вызываем его конструктор
    ex = TaskWidget (app)

    # launch app cycle
    # запуск основного цикла событий
    sys.exit(app.exec_())
