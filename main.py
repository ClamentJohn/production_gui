'''
    A quick demo of the production GUI for Carnot technologies
    @author: Clament John

    @fix: Include flash script
    @attention: windows port compatibility
'''

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import serial, queue, requests, json
from com_monitor import ComMonitorThread
from livedatafeed import LiveDataFeed
from face_class import LeftWidget,MiddleWidget,RightWidget, BasicWidget
from serial_read import serial_ports
from utils import get_all_from_queue, get_item_from_queue
import time, os



class ProdGui(QMainWindow):
    def __init__(self, parent = None):
        super(ProdGui, self).__init__(parent)
        
        # counters
        self.face_count = 0
        self.device_count = 1
        self.current_device_no = 1
        
        # Create the queues for data transfer from serial
        self.q_Data = None
        self.q_Error = None
        # Create (serial) event monitor flag
        self.event_monitor = False
        self.com_monitor = None
        # Create a data class
        self.livefeed = LiveDataFeed()
        self.value_samples = []
        # Create a Timer Class
        self.timer = QTimer()
        
        #Init the UI
        self.create_main_frame()
        self.create_menu()
        
        #text file we will be saving in
        # ACC | GSM | GSM_SNR | RTC | SD | NRF_SPI | STN | V_BAT | GPS | GPS_ANT | NRF-ACC | NRF_SD | NRF_OTA
        self.failed_checks = {"acc":0,"gsm":0,"gsm_snr":0,"rtc":0,"sd":0,"nrf_spi":0,"stn":0,"v_bat":0,
                              "gps":0,"gps_ant":0,"nrf_acc":0,"nrf_sd":0,"nrf_ota":0}
        
        self.setWindowTitle("Carnot Production")
        
        #advanced stuff
        self.advanced_set = False
        self.timer_counter = 0
        self.small_string_flag = 0
        
    def create_main_frame(self):
        self.createFaces()
        self.create_next_button()
        self.create_status_bar()
        
        self.leftGroupBox.setEnabled(False)
        self.middleGroupBox.setEnabled(False)
        self.rightGroupBox.setEnabled(False)
        self.basicGroupBox.setEnabled(False)
        self.leftGroupBox.hide()
        self.middleGroupBox.hide()
        self.rightGroupBox.hide()
        
        self.basic.pixelLabel.setPixmap(QPixmap("images/logo.png"))
        self.left.pixelLabel.setPixmap(QPixmap("images/logo.png"))
        self.basic.saveToText.clicked.connect(self.on_save_txt)
        self.basic.submitButton.clicked.connect(self.on_submit)
        self.basic.device_text.append(str(self.current_device_no))
        self.basic.nextButton.clicked.connect(self.on_flash_button)
#         self.left.device_id.append(str(self.current_device_no))
        
        self.main_frame = QWidget()
        
        face_widget = QWidget()
        face_layout = QHBoxLayout()
        face_layout.addWidget(self.leftGroupBox);
        face_layout.addWidget(self.middleGroupBox);
        face_layout.addWidget(self.rightGroupBox);
        face_layout.addWidget(self.basicGroupBox)
        face_widget.setLayout(face_layout)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(face_widget)
        main_layout.addWidget(self.next_button)
        self.main_frame.setLayout(main_layout)
        self.setCentralWidget(self.main_frame)
        
    def on_flash_button(self):
        
        print("\n\nFlashing NRF\n")
        os.system("flashNRF.cmd")
        os.system('testing_main1.cmd')
        time.sleep(5)
    
    def create_menu(self):
        self.menu = self.menuBar().addMenu("&File")
        
        self.start_qc = self.create_action("Start &QC", 
                                           shortcut = "Ctrl+Q", slot = self.on_start, 
                                           tip = "Start the QC process")
        self.advanced = self.create_action("&Advanced", 
                                           shortcut = "Ctrl+C", slot = self.on_advanced, 
                                           tip = "Super Saiyan")
        self.menu.addAction(self.start_qc)
        self.menu.addAction(self.advanced) 
        
     
    def createFaces(self):
        self.leftGroupBox = QGroupBox("Step 1")
        self.left = LeftWidget()
        layout1 = QVBoxLayout()
        layout1.addWidget(self.left)
        self.leftGroupBox.setLayout(layout1)
        self.leftGroupBox.setMaximumSize(400, 450)
        
        self.middleGroupBox = QGroupBox("Step 2")
        self.middle = MiddleWidget()
        layout2 = QVBoxLayout()
        layout2.addWidget(self.middle)
        self.middleGroupBox.setLayout(layout2)
        self.middleGroupBox.setMaximumSize(450, 450)
        
        self.rightGroupBox = QGroupBox("Step 3")
        self.right = RightWidget()
        layout3 = QVBoxLayout()
        layout3.addWidget(self.right)
        self.rightGroupBox.setLayout(layout3)
        self.rightGroupBox.setMaximumSize(400, 450)
        # adding the next device button the right widget
        self.right.nextButton.clicked.connect(self.new_device)
        
        self.basicGroupBox = QGroupBox("Carnot")
        self.basic = BasicWidget()
        layout4 = QVBoxLayout()
        layout4.addWidget(self.basic)
        self.basicGroupBox.setLayout(layout4)
        self.basicGroupBox.setMinimumSize(400, 550)
        self.basicGroupBox.setMaximumSize(400, 1000)
        #self.basic.nextButton.clicked.connect(self.new_device())
        
    
    def create_next_button(self):
        self.next_button = QPushButton("Next")
        #self.next_button.clicked.connect(self.__next_face)
        self.next_button.clicked.connect(self.new_device)
        self.next_button.setEnabled(False)
        
    def create_status_bar(self):
        self.status_text = QLabel("Idle  (No QC?)")
        #self.statusBar().addWidget(self.status_text)
    
    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action   
        
    def new_device(self):
        
        #inclease device number
        self.basic.device_text.clear()
        self.basic.device_text.append(str(int(self.current_device_no) + 1))
        self.current_device_no = int(self.current_device_no) + 1
        #disable the buttons
        self.basic.saveToText.setEnabled(False)
        self.basic.submitButton.setEnabled(False)
        self.basic.nextButton.setEnabled(False) 
        self.basic.pixelLabel.setPixmap(QPixmap("images/logo.png"))
        #refresh_face
        #self.update_faces()
        '''
        self.leftGroupBox.setEnabled(False)
        self.middleGroupBox.setEnabled(False)
        self.rightGroupBox.setEnabled(False)
        self.leftGroupBox.setEnabled(True)
        self.next_button.setEnabled(True)
        print("device count:", self.device_count, '\n')
        self.left.update(self.on_serial_ports(),"Checked", qr_code(self.device_count))
        '''
        
    def __next_face(self):
        
        if self.face_count == 0:
            self.middleGroupBox.setEnabled(True)
            self.face_count += 1
            self.update_faces()
        elif self.face_count == 1:
            self.rightGroupBox.setEnabled(True)
            self.face_count = 0
            self.next_button.setEnabled(False)
            self.device_count += 1
            
            
    def on_serial_ports(self):
        ''' get a list of ports available.
        '''
        
        port_list = serial_ports()
        if len(port_list) == 0:
            QMessageBox.critical(self, "Check Connection",
                                  "Device Not Connected")
            return
        port = port_list
        return port
    
    def on_timer(self):
        """Executed periodically when qc update timer is launched""" 
        self.read_serial_data()
        
    def on_advanced(self):
        self.leftGroupBox.show()
        self.middleGroupBox.show()
        self.advanced_set = True
        if self.basicGroupBox.isEnabled():
            self.leftGroupBox.setEnabled(True)
            self.middleGroupBox.setEnabled(True)
        else:
            self.leftGroupBox.setEnabled(False)
            self.middleGroupBox.setEnabled(False)
    
    def on_start(self):
        ''' Start session -> on_serial_ports, then com_monitor
        thread 
        '''
        # this will call the flashing cmd scripts
        print("\n\nFlashing NRF\n")
        os.system("flashNRF.cmd")
        os.system("testing_main1.cmd")
        # so on start we will flash the device
        #then we sleep for 5 seconds so that the system is ready
        time.sleep(5)
        
        self.basicGroupBox.setEnabled(True)
        self.next_button.setEnabled(True)
#         self.basic.pixelLabel.setPixmap(QPixmap("images/cross-1.png"))
        self.basic.pixelLabel.setEnabled(True)
        
        if self.advanced_set:
            self.leftGroupBox.setEnabled(True)
            self.middleGroupBox.setEnabled(True)
        
        if self.com_monitor is not None and self.left.com_set() == "":
            return
        self.q_Data = queue.Queue()
        self.q_Error = queue.Queue()
        self.com_monitor = ComMonitorThread(
            self.q_Data,
            self.q_Error,
            self.on_serial_ports(),
            9600)
        self.com_monitor.start()
        
        com_error = get_item_from_queue(self.q_Error)
        if com_error is not None:
            QMessageBox.critical(self, 'ComMonitorThread error',
                com_error)
            self.com_monitor = None
            
        self.event_monitor = True
        
        self.timer = QTimer()
#         self.connect(self.timer, SIGNAL('timeout()'), self.on_timer)
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(500.0)
        
        #self.status_text.setText("Bad Batch")
        
    def read_serial_data(self):
        """Called periodically to see if serial buffer
        data available"""
        
        ''' each qdata has a list which with-in has a list with 
        single character plus time stamp.
        '''
        #[STAT]: ACC | GSM | GSM_SNR | RTC | SD | NRF_SPI | STN | GPS | GPS_ANT | NRF-ACC
        #[INFO]: STM_FW | STM_ID | STN_FW | GSM_Ver | CCID | NRF_ID_low | NRF_ID_high
        
        b = []
        self.timer_counter += 1
        #every 1 sec
        if self.timer_counter > 2:
            self.timer_counter = 0
            qdata = list(get_all_from_queue(self.q_Data))
            print(qdata)
            if len(qdata) > 0 and b'S' in qdata[0][0]:
                qdata = qdata[1:] #skip the first S
                if len(qdata) > 70:
                    self.left.update(self.on_serial_ports(),"Checked", qr_code(self.device_count))
                for i_a in qdata:
                    if b'\r' in i_a:
                        break
                    b.append(i_a[0])
                #TODO: there is a glich in the code, if we do advanced while running the QC,
                # we only get a portion of the UART string
                if len(b) > 120:
                    if b[1] == b'A':
                        #in b we dont need the last 3 values \r \n and b'S'
                        #and in the bedinning we dont need b'TAT'
                        data = []
#                         print(b)
                        for i in range(0,len(b)):
                            data.append(b[i].decode("utf-8"))
                            
                        #find position of "I" for STAT string ending
                        #find position of "S" or "\r" for INFT string ending
#                         print(data)
                        if "I" in data:
                            data_stat = data[4:(data.index("I")-1)]
                            data_info = data[data.index("I")+5:]
                            print(data_stat)
                            print(data_info)
                            data_stat = "".join(data_stat)
                            data_info = "".join(data_info)
                            data_stat = data_stat.split(",")
                            data_info = data_info.split(",")
                            # now we have our data in the above variables
                            '''ACC | GSM | GSM_SNR | RTC | SD | NRF_SPI | STN | V_BAT | GPS | GPS_ANT | NRF-ACC | NRF_SD | NRF_OTA
                               STM_FW | STM_ID | STN_FW | GSM_Ver | CCID | NRF_ID_low | NRF_ID_high
                            '''
                            print(data_stat)
                            print(data_info)
                            self.livefeed.add_status(data_stat)
                            self.livefeed.add_info(data_info)
                            self.update_faces()
                else:
                    self.small_string_flag += 1
                    if self.small_string_flag > 10:
                        QMessageBox.information(self, "Check Connections", "Receiving less data, maybe NRF SPI has failed")
                        self.small_string_flag = 5
            else:
                pass
            
        self.current_device_no = self.basic.device_text.toPlainText()
        if self.current_device_no != "":
            self.basic.qr.clear()
            self.basic.qr.append(qr_code(self.current_device_no))
        #the following is for data from Teensy
        '''data = qdata[0]
        data = data[0].decode("utf-8")
        data_stat = "".join(data[5:34])
        data_info = ''.join(data[41:])
        
        data_stat = data_stat.split(",")
        data_info = data_info.split(",")
        print(data_stat)
        print(data_info)
        self.livefeed.add_status(data_stat)
        self.livefeed.add_info(data_info)
        self.update_faces()'''
        
        
    def update_faces(self):
        '''ACC | GSM | GSM_SNR | RTC | SD | NRF_SPI | STN | V_BAT | GPS | GPS_ANT | NRF-ACC | NRF_SD | NRF_OTA
           STM_FW | STM_ID | STN_FW | GSM_Ver | CCID | NRF_ID_low | NRF_ID_high | NRF_Version
        '''
        if self.livefeed.has_new_status:
            data_status = self.livefeed.read_status()
            #update battery voltage
            self.basic.text1.clear()
            self.basic.text1.append(data_status[7])
            #read info
            data_info = self.livefeed.read_info()
            if self.check_stm_status(data_status,data_info):
                print("All stats good")
            else:
                print("Error\n")
                   
        if self.livefeed.has_new_info:
            data_info = self.livefeed.read_info()
        else:
            pass
        
        '''if self.livefeed.has_new_status:
            data_status = self.livefeed.read_status()
            if self.check_stm_status(data_status):
                self.middle.update_middle_status(data_status[-1])
            else:
                print("Error\n")
            
#             self.middle.update_middle(data[0], data[1], data[2], data[3:])   
        if self.livefeed.has_new_info:
            data_info = self.livefeed.read_info()
            #format stm_id, nrf_id, stm_ver, nrf_ver
            if self.check_stm_status(data_status):
                self.middle.update_middle(data_info[1], data_info[-1], data_info[0], data_info[2])
            else:
                print("Error\n")
        else:
            pass'''
        
    def check_stm_status(self,data,info):
        '''ACC | GSM | GSM_SNR | RTC | SD | NRF_SPI | STN | V_BAT | GPS | GPS_ANT | NRF-ACC | NRF_SD | NRF_OTA
           STM_FW | STM_ID | STN_FW | GSM_Ver | CCID | NRF_ID_low | NRF_ID_high | NRF_version
        '''
        #this is used for teensy debugging
        #[STAT]: //ACC | GSM | GSM_SNR | RTC | SD | NRF_SPI | STN | V_BAT | GPS | GPS_ANT | NRF-ACC | NRF_SD | NRF_OTA
        #self.middle.update_status_flags(data[6], data[1], data[0], data[3], data[5],data[2],
        #                                data[4], data[7], data[8], data[9])
        if self.advanced_set:
            print(info[8])
            if 'S' not in info[8]:
                self.middle.update_middle(*info)
                self.middle.update_status_flags(data[6], data[1], data[0], data[3], data[5], data[2],
                                                 data[4], data[8], data[9], data[10], data[11], data[12])
            else:
                print("Bad info string received\n")
        
        
        #print(data)
        if '0' in data:
            print(data)
            number_fails = data.count('0')
            fail = ""
            failed_devices = []
            if data[0] == '0':
                failed_devices.append("ACC")
            if data[1] == '0':
                failed_devices.append("GSM")
            if data[2] == '0':
                failed_devices.append("GSM-SNR")
            if data[3] == '0':
                failed_devices.append("RTC")
            if data[4] == '0':
                failed_devices.append("SD")
            if data[5] == '0':
                failed_devices.append("NRF-SPI")
            if data[6] == '0':
                failed_devices.append("STN")
            if data[7] == '0':
                failed_devices.append("GPS")
            if data[8] == '0':
                failed_devices.append("GPS-ANT")
            if data[9] == '0':
                failed_devices.append("NRF-ACC")
            print(failed_devices)
            fail = " ".join(failed_devices)
            print(fail)
            
            QMessageBox.critical(self, "Device Modules Failed", "%s module(s) failed"% fail)
            self.basic.pixelLabel.setPixmap(QPixmap("images/cross-1.png"))
            #TODO: Disable this popup from comming again and again
            return 0
        elif int(data[2]) < 12:
            QMessageBox.critical(self, "GSM Antenna", "Please reconnect it")
        else:
            #TODO: Enable all the buttons
            self.basic.pixelLabel.setPixmap(QPixmap("images/tick-black.png"))
            self.basic.submitButton.setEnabled(True)
            self.basic.saveToText.setEnabled(True)
            self.basic.nextButton.setEnabled(True)
            return 1
        
    def on_submit(self):
        self.basic.pixelLabel.setPixmap(QPixmap("images/wait_1.jpg"))
        time.sleep(1)
        data_status = self.livefeed.read_status()
        data_info = self.livefeed.read_info()
        user_input_voltage = self.basic.text2.toPlainText()
        if user_input_voltage != "":
            user_input_voltage = float(user_input_voltage)
        else:
            QMessageBox.information(self, "Please enter value", "Measure the voltage value.")
            return
        if data_info[4] == "":
            print("no ccid") 
            data_info[4] = "123456789"
        if data_info[3] == "":
            print("No gsm version")
            data_info[3] = 255
        if data_info[2] == "":
            print("no STN version")
            data_info[2] = "255"
            
            
        '''
            stms_i = stnFlag
            nrfs_st= string of nrf_sd+unplug+gps+acc
            nrfs_i = gps
            gsmv = gsm version
            
            gpsv = we dont currently have gps version
            
        '''
        stm_status_bk = str(data_status[0]+data_status[1]+data_status[3]+data_status[4]+data_status[5]+data_status[6]+
                            data_status[7]+data_status[8]+data_status[9])
        data_to_backend = {"lb":int(self.current_device_no), "pc":str(qr_code(int(self.current_device_no))),
                           "flg":1, "stm":str(data_info[1]), "stmv": int(data_info[0]),
                           "nrf":str(data_info[5] + data_info[6]), "nrfv":int(data_info[-1]),
                            "simcc":str(data_info[4]), "stms_st":stm_status_bk,
                           "stms_i":int(data_status[6]), "nrfs_st": "1111","nrfs_i": int(data_status[8]),
                            "gsmv": data_info[3] ,"pwr": data_status[7],"hbn":int(data_info[-1]),
                            "stnv":str(data_info[2]),"gpsv":"123456789A", "vltDevice":int(user_input_voltage)}
        
        print(data_to_backend)
        r = requests.post('http://carnot-staging.herokuapp.com/devices/log/', data = json.dumps(data_to_backend), 
                          headers = {"ApiKey":"JXn8e6C29jhZ065i8wyQktY33YD3s9zy"})
        #print(r.content)
        y = r.content.decode("utf-8")
        # now we have a string
        if "true" in y:
            QMessageBox.information(self, "Server", "Data saved to backed")
            self.new_device()
        else:
            QMessageBox.critical(self, "Server", "Check internet connection")
    
    def on_save_txt(self):
        data_status = self.livefeed.read_status()
        data_info = self.livefeed.read_info()
        self.local_file = open("carnot_device.csv","a+")
        self.local_file.write("%d, " % int(self.current_device_no))
        self.local_file.write("%s, " % (qr_code(int(self.current_device_no))))
        for i in data_info:
            self.local_file.write("%s, " % i)
        for i in data_status:
            print(i)
            self.local_file.write("%s, " % (data_status))
        self.local_file.write("\r\n")
        self.local_file.close()
        

def qr_code(label):
    qr_code_ret = "ABCD";
    with open("myfile.txt") as fp:
        for i, line in enumerate(fp):
            if (i == label) or (str(i) == label):
                qr_code_ret = line;
                break;
        fp.close()
        answer = qr_code_ret.split(',')
        #print answer[0];
    return answer[0];

def check_for_internet():
    try:
        r = requests.get('http://google.com')
        print("Internet connection")
        return True
    except ConnectionError:
        print("Connection Error\n")
        return False

def main():
    app = QApplication(sys.argv)
    
    mainW = ProdGui()
    mainW.show()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()
