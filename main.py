from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
# from PySide2.QtCore import QTimer
# import os
import requests, time
from PyQt5.QtCore import pyqtSignal, QObject, QThread, pyqtSignal, QTimer
from requests.models import Response
from random import randint
import numpy as np

# BASE = "http://192.168.1.160:5000"
BASE = "http://10.0.0.17:5000"


class MainWindow(QtWidgets.QMainWindow):
    data = np.empty(100)
    ptr = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('window_view.ui', self)

    

        self.button_a.clicked.connect(self.button_a_toggle)
        self.button_a_go.clicked.connect(self.door_a_put)
        self.button_b.clicked.connect(self.button_b_toggle)
        self.button_b_go.clicked.connect(self.door_b_put)
        self.button_c.clicked.connect(self.button_c_toggle)
        self.button_c_go.clicked.connect(self.door_c_put)
        self.button_d.clicked.connect(self.button_d_toggle)
        self.button_d_go.clicked.connect(self.door_d_put)
        self.button_reel_en.clicked.connect(self.reel_enable)
        self.button_reelOff.clicked.connect(self.reel_off)
        self.button_reel_calib.clicked.connect(self.reel_calib)
        self.button_reelPanic.clicked.connect(self.reel_off)
        self.button_400V_onoff.clicked.connect(self.button_400V_toggle)
        self.button_Ziehl_onoff.clicked.connect(self.button_Ziehl_toggle)
        self.polling()

        self.graphicsView_1.setDownsampling(mode='peak')
        self.graphicsView_1.setClipToView(True)
        self.graphicsView_1.setRange(xRange=[-100, 0])
        self.graphicsView_1.setLimits(xMax=0)
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphicsView_1.plot(pen=pen)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start(100)



    def update_plot_data(self):
        self.data[self.ptr] = value_220i
        self.ptr += 1
        if self.ptr >= self.data.shape[0]:
            tmp = self.data
            self.data = np.empty(self.data.shape[0] * 10)
            self.data[:tmp.shape[0]] = tmp
        self.data_line.setData(self.data[:self.ptr])
        self.data_line.setPos(-self.ptr, 0)

# DOOR A CONTROL
    door_a_state = 1
    def button_a_toggle(self):
        if self.button_a.text() == "Open":
            self.button_a.setText("Close")
            self.door_a_state = -1
        else: 
            self.button_a.setText("Open")
            self.door_a_state = 1
    
    def door_a_put(self):
        if self.door_a_state == -1:
            requests.put(BASE + "/door_control?door=a", {
            'velocity':'-' + self.line_speed_a.text(),
            'duration':self.line_timeA.text()
            })
        else:
            requests.put(BASE + "/door_control?door=a", {
            'velocity':self.line_speed_a.text(),
            'duration':self.line_timeA.text()
            })

# DOOR B CONTROL
    door_b_state = 1
    def button_b_toggle(self):    
        if self.button_b.text() == "Open":
            self.button_b.setText("Close")
            self.door_b_state = -1
        else: 
            self.button_b.setText("Open")
            self.door_b_state = 1
    
    def door_b_put(self):
        if self.door_b_state == -1:
            requests.put(BASE + "/door_control?door=b", {
            'velocity':'-' + self.line_speed_b.text(),
            'duration':self.line_timeB.text()
            })
        else:
            requests.put(BASE + "/door_control?door=b", {
            'velocity':self.line_speed_b.text(),
            'duration':self.line_timeB.text()
            })

# DOOR C CONTROL
    door_c_state = 1
    def button_c_toggle(self):   
        if self.button_c.text() == "Open":
            self.button_c.setText("Close")
            self.door_c_state = -1
        else: 
            self.button_c.setText("Open")
            self.door_c_state = 1
    
    def door_c_put(self):
        if self.door_c_state == -1:
            requests.put(BASE + "/door_control?door=c", {
            'velocity':'-' + self.line_speed_c.text(),
            'duration':self.line_timeC.text()
            })
        else:
            requests.put(BASE + "/door_control?door=c", {
            'velocity':self.line_speed_c.text(),
            'duration':self.line_timeC.text()
            })

# DOOR D CONTROL
    door_d_state = 1
    def button_d_toggle(self):  
        if self.button_d.text() == "Open":
            self.button_d.setText("Close")
            self.door_d_state = -1
        else: 
            self.button_d.setText("Open")
            self.door_d_state = 1
    
    def door_d_put(self):
        if self.door_d_state == -1:
            requests.put(BASE + "/door_control?door=d", {
            'velocity':'-' + self.line_speed_d.text(),
            'duration':self.line_timeD.text()
            })
        else:
            requests.put(BASE + "/door_control?door=d", {
            'velocity':self.line_speed_d.text(),
            'duration':self.line_timeD.text()
            })

# 400V CONTROL
    def button_400V_toggle(self):
        is_on = 0      
        if self.button_400V_onoff.text() == "400V OFF":
            self.button_400V_onoff.setText("400V ON")
            self.button_400V_onoff.setStyleSheet("color: rgb(255, 255, 255);background-color: rgb(0, 170, 0);")
            is_on = 1
        else: 
            self.button_400V_onoff.setText("400V OFF")
            is_on = 0
            self.button_400V_onoff.setStyleSheet("color: rgb(0, 0, 0);background-color: rgb(222, 222, 222);")
        requests.put(BASE + "/400v_regulator_control?is_on="+str(is_on), {})

# ZIEHL CONTROL
    def button_Ziehl_toggle(self):
        is_on = 1      
        if self.button_Ziehl_onoff.text() == "Ziehl OFF":
            self.button_Ziehl_onoff.setText("Ziehl ON")
            self.button_Ziehl_onoff.setStyleSheet("color: rgb(255, 255, 255);background-color: rgb(0, 170, 0);")
            is_on = 0
        else: 
            self.button_Ziehl_onoff.setText("Ziehl OFF")
            is_on = 1
            self.button_Ziehl_onoff.setStyleSheet("color: rgb(0, 0, 0);background-color: rgb(222, 222, 222);")
        requests.put(BASE + "/ZIEHL_control?enabled="+str(is_on), {})

# REEL CONTROL
    def reel_enable(self):
        self.button_reel_en.setStyleSheet("color: rgb(255, 255, 255);background-color: rgb(0, 170, 0);")
        requests.post(BASE + "/set_winch?mode=regular", {
            'tension':self.line_tension.text(),    
            'velocity':self.line_speed_reel.text()
        })
    
    def reel_off(self):
        self.button_reel_en.setStyleSheet("color: rgb(0, 0, 0);background-color: rgb(222, 222, 222);")
        requests.post(BASE + "/set_winch?mode=disable", {
            'tension':'0',    
        })

    def reel_calib(self):
        requests.post(BASE + "/set_winch?mode=calib&calib_winch?set_edge=rolled", {
            'tension':'0', 
        })
        
    def polling(self):
        self.worker = WorkerThread()
        self.worker.start()
        self.worker.update_polling.connect(self.polling_update)

    def polling_update(self,val):
        global value_220i
        value_24v = round(val.json()["24v_vout"]/850*24,1)
        self.lcd_24V.setProperty("value", value_24v)
        value_220i = round(val.json()["220vac_ain"]/175,2)
        self.lcd_220V_i.setProperty("value", value_220i)
        value_400i = round((val.json()["400v_aout"]-20)/30.5,2)
        self.lcd_400V_i.setProperty("value", value_400i)
        value_tension = round((val.json()["load_cell"]-680)*11.2,0)
        self.lcd_tension.setProperty("value", value_tension)
        # value_rope = round(val.json()["TotalRope"]/100,2)
        # self.lcd_cableOut.setProperty("value", value_rope)
        # self.progressBar.setProperty("value", value_rope)

class WorkerThread(QThread):
    update_polling = pyqtSignal(Response)
    def run(self):
        while True:
            poll = requests.get(BASE + "/data?param=400v_aout&param=24v_vout&param=220vac_ain&param=load_cell", {})
            self.update_polling.emit(poll)
            time.sleep(0.1)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()