import sys
import time
from PySide import QtCore, QtGui
import serial
from time import gmtime, strftime

import os
import binascii

import vid93
from pythonconsolewidget import PythonConsoleWidget

mytimetmp = strftime("%Y%m%dT%H%M%S", gmtime())
myport = 'COM6'

j1939_FLI1_list = ['00 00 00 00 00 00 00 00', '10 00 00 00 00 00 00 00',
'40 00 00 00 00 00 00 00', '00 01 00 00 00 00 00 00', '00 00 00 01 00 00 00 00',
'f0 00 00 00 00 00 00 00']
j1939_FLI2_list = ['00 00 00 01 00 00 00 00', '00 00 00 09 00 00 00 00',
'00 00 00 11 00 00 00 00', '00 00 00 81 00 00 00 00', '00 00 00 00 00 00 00 00']
j1939_ACC1_list = ['00 00 00 00 00 00 00 00', '00 00 00 00 00 00 40 00','00 40 00 00 00 00 00 00']


class ByteSettingSwitch(QtGui.QWidget):
    def __init__(self, text=None, parent=None):
        self.name = text
        if isinstance(text, QtGui.QWidget):
            parent = text
            text = None
        QtGui.QWidget.__init__(self, parent)
        self.init(text)
        if text:
            self.setText(text)

    def init(self, name):
        self.label = QtGui.QLabel()
        #self.label.setText(name)
        ###
        list_name = name + '_' + 'list'
        index1 = 0
        button_group = QtGui.QButtonGroup(self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        for item in eval(list_name):

            byte_str1 = QtGui.QLineEdit()
            byte_str1.setText(item)
            radio = QtGui.QRadioButton(name + str(index1))
            button_group.addButton(radio)
            layout.addWidget(radio)
            layout.addWidget(byte_str1)

            #radio.clicked.connect[QtGui.QAbstractButton](self.setValue(byte_str1.text()))
            index1 += 1
        self.setLayout(layout)
        button_group.buttonClicked[QtGui.QAbstractButton].connect(self.setValue)

        self.setLayout(layout)

    def setValue(self, button):
        str1 = button.text()
        name = str1[:-1]
        index = int(str1[-1])
        eval('vid93.' + name)['value'] = eval(name + '_list')[index]

    def text(self):
        return self.label.text()

    def setText(self, text):
        self.label.setText(text)


class LCDRange(QtGui.QWidget):
    def __init__(self, text=None, range=1000, parent=None):
        self.name = text
        if isinstance(text, QtGui.QWidget):
            parent = text
            text = None

        QtGui.QWidget.__init__(self, parent)

        self.init(range)

        if text:
            self.setText(text)

    def init(self, range):
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
        elif (self.name == 'rpm'):
            vid93.set_rpm(value)
        elif(self.name == 'engineLoad'):
            vid93.set_engineLoad(value)
        elif(self.name == 'throttlePosition'):
            vid93.set_throttlePosition(value)
        elif(self.name == 'coolantTemperature'):
            vid93.set_coolantTemperature(value)

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
        self.vidport = "COM1"

    def stop(self):
        self.mutex.lock()
        self.abort = True
        self.alive = False
        self.condition.wakeOne()
        self.mutex.unlock()

        self.wait()

    def worker(self):
        locker = QtCore.QMutexLocker(self.mutex)
        self.vidport = "COM6"

        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)
        else:
            self.restart = True
            self.condition.wakeOne()

    def createrespond(self, cmd, data, protocol, loghandle):
                if cmd == b'\x80':
                    #ping
                    respone = b'\xaa\x80\x01\x02'
                elif cmd == b'\x81':
                    #Perform OBD Protocol Search
                    if protocol == "j1708":
                        respone = b'\xaa\x81\x03\x14\x01\x01'
                    elif protocol == 'j1939':
                        respone = b'\xaa\x81\x03\x15\x01\x01'
                    else:
                        respone = b'\xaa\x81\x03\x11\x01\x01'
                elif cmd == b'\x84':
                    #Get VIN
                    respone = b'\xaa\x84\x09\x31\x32\x33\x34\x35\x36\x37\x38\x39'
                elif cmd == b'\x90':
                    #Get VID Application Version
                    respone = b'\xaa\x90\x02\x11\x11'
                elif cmd == b'\x91':
                    #Get Vehicle Battery Voltage
                    respone = b'\xaa\x91\x02\x0c\x0c'
                elif cmd == b'\x96':
                    #Get Bootloader Version/Type
                    #continue
                    respone = b'\xaa\x96\x01\x00'
                elif cmd == b'\x97':
                    #Get Bootloader Version/Type
                    respone = b'\xaa\x97\x01\x00'
                elif cmd == b'\xf0':
                    #Get Bootloader Version/Type
                    respone = b'\xaa\xf0\x01\x31'
                elif cmd == b'\xf4':
                    #Set Read/Write Address
                    respone = b'\xaa\xf4\x00'
                elif cmd == b'\xf8':
                    #Read Data from EEPROM
                    respone = b'\xaa\xf8\x20\x31\x32\x33\x34\x35\x36\x37\x38\x31\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                    respone = b'\xaa\xf8\x20\x4f\x44\x41\x36\x41\x45\x31\x34\x30\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                    #respone = b'\xaa\xf8\x0f\x31\x32\x33\x34\x35\x36\x37\x38\x39\x30\x31\x32\x33\x34\x35'
                    #respone = b'\xaa\xf8\x20\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x30\x31'
                elif cmd == b'\xfe':
                    #Launch Bootloader (start prog.)
                    respone = b'\xaa\xfe\x00'
                elif cmd == b'\xff':
                    #Launch Application (end prog.)
                    respone = b'\xaa\xff\x00'
                elif cmd == b'\x93':
                    print(data[0])
                    if data[0] == 3:
                        dataset = 'fast'

                    elif data[0] == 2:
                        dataset = 'slow'

                    elif data[0] == 4:
                        dataset = 'molileye'
                    respone = bytes.fromhex(vid93.dataset_age(protocol, dataset))
                else :
                    return "xxxx"

                summ = 0
                for byt in respone:
                    summ = summ + byt
                summ = summ % 256
                ddd = bytearray(1)
                ddd[0] = summ
                all_respone = respone + ddd
                print('respond: ', end='')
                tmpstring = ""
                for bb in all_respone:
                    print('%02x ' % bb, end='')
                    ttt = hex(bb)
                    tmpstring = tmpstring + " " + ttt
                loghandle.write(tmpstring + "\n")
                return all_respone

    def run(self):
        logdir = os.path.join("D:\\", "work", "log")
        logname = "con" + mytimetmp + ".log"
        logpath = os.path.join(logdir, logname)
        mylog = open(logpath, "w")

        #vidport = "COM6"
        vidselect = "ext"

        serial_p = serial.Serial(port=myport, timeout=3, baudrate=57600)
        self.alive = True
        #repr_mode=0
        protocol = "j1939"
        lenth = -1
        msgcount = 1
        try:

            while self.alive:
                if self.abort:
                    return
                self.mutex.lock()
                self.mutex.unlock()



                #print(vid93.dataset_age('obdii','fast'))
                #self.startport()
                print("")
                data = serial_p.read(1)
                if (data == b'\xb5'):
                    vidselect = "ext"
                    print("B5:", end='')
                elif (data == b'\xb6'):
                    print("B6:", end='')
                    vidselect = "int"
                else:
                    print(data)
                    continue
                cmd = serial_p.read(1)
                print("command:", end='')
                print(cmd, end=', ')
                #cmd=data
                lenth00 = serial_p.read(1)
                lenth = ord(lenth00)
                print("len:", end='')
                print(lenth, end=', ')
                if lenth > 30:
                    print("skip")
                    continue
                data = serial_p.read(lenth + 1)
                print("data:", end='')
                #print(data)
                for bb in data:
                    print('%02x ' % bb, end='')
                if (vidselect == "int"):
                    continue

                tmpstring = self.createrespond(cmd, data, protocol, mylog)
                print(tmpstring)
                if tmpstring !="xxxx":
                    serial_p.write(tmpstring)

                
                msgcount = msgcount + 1

            mylog.close()

        except serial.SerialException:
            print('SerialException')
            self.alive = False
            serial_p.close()
            mylog.close()
            raise

        return msgcount


class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.thread = WorkerThread()

        quit = QtGui.QPushButton("&Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(quit, QtCore.SIGNAL("clicked()"),
                     QtGui.qApp, QtCore.SLOT("quit()"))

        speed_widget = LCDRange("speed", 200)
        speed_widget.setRange(0, 150)

        rpm_widget = LCDRange("rpm", 6000)
        rpm_widget.setRange(0, 6000)

        load_widget = LCDRange("engineLoad", 100)
        load_widget.setRange(0, 100)

        throttle_widget = LCDRange("throttlePosition", 100)
        throttle_widget.setRange(0, 100)

        tempt_widget = LCDRange("coolantTemperature", 100)
        tempt_widget.setRange(-40, 100)

        brake_button = QtGui.QPushButton('brake', self)
        brake_button.setCheckable(True)
        brake_button.clicked[bool].connect(self.setSwitch)

        clutch_button = QtGui.QPushButton('clutch', self)
        clutch_button.setCheckable(True)
        clutch_button.clicked[bool].connect(self.setSwitch)

        console = PythonConsoleWidget()

        middleLayout = QtGui.QVBoxLayout()
        middleLayout.addWidget(brake_button)
        middleLayout.addWidget(clutch_button)
        middleLayout.addWidget(console)
        fli1_widget = ByteSettingSwitch('j1939_FLI1')
        middleLayout.addWidget(fli1_widget)
        fli2_widget = ByteSettingSwitch('j1939_FLI2')
        middleLayout.addWidget(fli2_widget)
        acc1_widget = ByteSettingSwitch('j1939_ACC1')
        middleLayout.addWidget(acc1_widget)
        availablePort = []
        for i in range(256):
                try:
                        s = serial.Serial(i)
                        availablePort.append((i, s.portstr))
                        s.close()
                        #explicit close 'cause of delayed GC in java
                except serial.SerialException:
                    pass
        for n, s in availablePort:
            print("(%d) %s" % (n, s))

        self.portBox= QtGui.QComboBox()


        shoot = QtGui.QPushButton("&Shoot")
        shoot.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(shoot, QtCore.SIGNAL("clicked()"), self.thread.worker)
        topLayout = QtGui.QHBoxLayout()
        self.portBox= QtGui.QComboBox()
        for n, s in availablePort:
            self.portBox.addItem(s)
        self.portBox.setCurrentIndex(0)
        self.connect(self.portBox, QtCore.SIGNAL("activated()"), self.setPort())
        topLayout.addWidget(self.portBox)
        topLayout.addWidget(shoot)
        topLayout.addStretch(1)

        leftLayout = QtGui.QVBoxLayout()
        leftLayout.addWidget(speed_widget)
        leftLayout.addWidget(rpm_widget)
        leftLayout.addWidget(load_widget)
        leftLayout.addWidget(throttle_widget)
        leftLayout.addWidget(tempt_widget)

        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(quit, 0, 0)
        gridLayout.addLayout(topLayout, 0, 1)
        gridLayout.addLayout(leftLayout, 1, 0)
        gridLayout.addLayout(middleLayout, 1, 1)
        #gridLayout.addWidget(console, 1, 2, 2, 1)
        gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)

        speed_widget.setValue(20)
        rpm_widget.setValue(500)
        load_widget.setValue(60)
        throttle_widget.setValue(70)
        tempt_widget.setValue(10)

        speed_widget.setFocus()

    def setSwitch(self, pressed):
        source = self.sender()
        if source.text() == "brake":
            vid93.swtich('brake', pressed)
        elif source.text() == "clutch":
            vid93.swtich('clutch', pressed)
        else:
            pass
    def setPort(self):
        myport=self.portBox.currentText()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = MyWidget()
    widget.setGeometry(100, 100, 500, 355)
    widget.show()
    r = app.exec_()
    widget.thread.stop()
    sys.exit(r)