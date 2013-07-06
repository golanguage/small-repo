import sys
import time
from PySide import QtCore, QtGui

import vid93
from pythonconsolewidget import PythonConsoleWidget 
class LCDRange(QtGui.QWidget):
    def __init__(self, text=None, range=1000,parent=None):
        self.name=text
        if isinstance(text, QtGui.QWidget):
            parent = text
            text = None

        QtGui.QWidget.__init__(self, parent)

        self.init(range)

        if text:
            self.setText(text)

    def init(self,range):
        lcd = QtGui.QLCDNumber(4)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, range)
        self.slider.setValue(0)
        self.label = QtGui.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
                     lcd, QtCore.SLOT("display(int)"))
        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
                     self, QtCore.SIGNAL("valueChanged(int)"))
        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
                     self, QtCore.SLOT("setValue(int)"))

        layout = QtGui.QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setFocusProxy(self.slider)

    def value(self):
        return self.slider.value()

    def setValue(self, value):
        self.slider.setValue(value)
        if (self.name == 'speed'):
                vid93.set_speed(value)
        elif (self.name == 'speed'):
                 vid93.set_rpm(value)

    def text(self):
        return self.label.text()

    def setRange(self, minValue, maxValue):
        #~ if minValue < 0 or maxValue > 99 or minValue > maxValue:
            #~ QtCore.qWarning("LCDRange::setRange(%d, %d)\n"
                    #~ "\tRange must be 0..99\n"
                    #~ "\tand minValue must not be greater than maxValue" % (minValue, maxValue))
            #~ return

        self.slider.setRange(minValue, maxValue)

    def setText(self, text):
        self.label.setText(text)

class WorkerThread(QtCore.QThread):


    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.restart = False
        self.abort = False

    def stop(self):
        self.mutex.lock()
        self.abort = True
        self.condition.wakeOne()
        self.mutex.unlock()

        self.wait()

    def worker(self):
        locker = QtCore.QMutexLocker(self.mutex)


        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)
        else:
            self.restart = True
            self.condition.wakeOne()

    def run(self):
        while True:
                self.mutex.lock()

                self.mutex.unlock()
                
                time.sleep(1)
                print(vid93.dataset_age('obdii','fast'))



                #if self.restart:
                #        break
                if self.abort:
                        return


                #if not self.restart:
                        #self.emit(QtCore.SIGNAL("renderedImage(const QImage &, double)"), image, scaleFactor)
                #        pass


                self.mutex.lock()
                #if not self.restart:
                #        self.condition.wait(self.mutex)
                #self.restart = False
                self.mutex.unlock()



class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.thread = WorkerThread()

        quit = QtGui.QPushButton("&Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(quit, QtCore.SIGNAL("clicked()"),
                     QtGui.qApp, QtCore.SLOT("quit()"))

        speed_widget = LCDRange("speed",200)
        speed_widget.setRange(0, 150)

        
        rpm_widget = LCDRange("rpm",5000)
        rpm_widget.setRange(0, 3000)


        console=PythonConsoleWidget()
        
        shoot = QtGui.QPushButton("&Shoot")
        shoot.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(shoot, QtCore.SIGNAL("clicked()"), self.thread.worker)
        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(shoot)
        topLayout.addStretch(1)

        leftLayout = QtGui.QVBoxLayout()
        leftLayout.addWidget(speed_widget)
        leftLayout.addWidget(rpm_widget)

        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(quit, 0, 0)
        gridLayout.addLayout(topLayout, 0, 1)
        gridLayout.addLayout(leftLayout, 1, 0)
        gridLayout.addWidget(console, 1, 1, 2, 1)
        gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)

        speed_widget.setValue(60)
        rpm_widget.setValue(100)
        
        speed_widget.setFocus()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = MyWidget()
    widget.setGeometry(100, 100, 500, 355)
    widget.show()
    r = app.exec_()
    widget.thread.stop()
    sys.exit(r)