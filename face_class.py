from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.Qt import QWidget, QLabel, QHBoxLayout, QRadioButton, QCheckBox,\
    QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QButtonGroup
import requests

class LeftWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(LeftWidget,self).__init__(parent)
        
        Port_widget = QWidget()
        Port_hbox = QHBoxLayout()
        port_label = QLabel("COM Port: ")
        self.port = Qt.QTextEdit()
        self.port.setMaximumSize(100, 25)
        self.port.setReadOnly(True)
        Port_hbox.addWidget(port_label)
        Port_hbox.addWidget(self.port)
        Port_widget.setLayout(Port_hbox)
        
        uart_widget = QWidget()
        uart_hbox = QtWidgets.QHBoxLayout()
        uart_label = QLabel("UART: ")
        self.uart = Qt.QTextEdit()
        self.uart.setMaximumSize(100, 25)
        uart_hbox.addWidget(uart_label)
        uart_hbox.addWidget(self.uart)
        uart_widget.setLayout(uart_hbox)
        
        qr_widget = QWidget()
        qr_hbox = QtWidgets.QHBoxLayout()
        qr_label = QLabel("QR Code: ")
        self.qr = Qt.QTextEdit()
        self.qr.setMaximumSize(150, 25)
        qr_hbox.addWidget(qr_label)
        qr_hbox.addWidget(self.qr)
        qr_widget.setLayout(qr_hbox)
        
        device_id_widget = QWidget()
        device_id_hbox = QtWidgets.QHBoxLayout()
        device_id_label = QLabel("Label ID: ")
        self.device_id = Qt.QTextEdit()
        self.device_id.setMaximumSize(150, 25)
        device_id_hbox.addWidget(device_id_label)
        device_id_hbox.addWidget(self.device_id)
        device_id_widget.setLayout(device_id_hbox)
        
        self.pixelLabel = self.createPixmapLabel()
        self.pixelLabel.setScaledContents(True)
#         self.pixelLabel.devicePixelRatioFScale()
        
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.pixelLabel)
        left_layout.addWidget(Port_widget)
        left_layout.addWidget(uart_widget)
#         left_layout.addWidget(device_id_widget)
#         left_layout.addWidget(qr_widget)
        self.setLayout(left_layout)
        
    
    def createPixmapLabel(self):
        label = QtWidgets.QLabel()
        label.setEnabled(True)
        label.setAlignment(QtCore.Qt.AlignVCenter)
#         label.setFrameShape(QtWidgets.QFrame.Box)
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        label.setBackgroundRole(QtGui.QPalette.Base)
        label.setAutoFillBackground(False)
        label.setMinimumSize(132, 132)
        label.setMaximumSize(200, 200)
        return label
    
    def setIcon(self, icon):
        self.icon = icon
        self.updatePixelmapLabels()
        
    def updatePixelLabel(self):
        state = Qt.QIcon.On
        mode = Qt.QIcon.Normal
        pixmap = self.icon.pixmap(self.size, mode, state)
        self.pixelLabel.setPixmap(pixmap)
        
    def update(self,port,uart, qr):
#         self.qr.clear()
        self.uart.clear()
        self.port.clear()
        self.uart.append(uart)
        self.port.append(port)
#         self.qr.append(qr)
        
    def com_set(self):
        print(self.port.toPlainText())
        return "" 
        
        
        
class MiddleWidget(QtWidgets.QWidget):
    def __init__(self, Vread = "12.6" , parent = None):
        super(MiddleWidget,self).__init__()
        
        #Vread = "12.6"
        string_VBat = Vread + " V"
        
        # the 3rd row
        voltage_box_widget = QWidget()
        voltage_hbox = QHBoxLayout()
        voltage_mcu = QWidget()
        voltage_mcu_layout = QtWidgets.QHBoxLayout()
        label1 = QLabel("MCU voltage: ")
        self.text1 = Qt.QTextEdit()
        self.text1.append(string_VBat)
        self.text1.setMaximumSize(100, 25)
        self.text1.setReadOnly(True)
        voltage_mcu_layout.addWidget(label1)
        voltage_mcu_layout.addWidget(self.text1)
        voltage_mcu.setLayout(voltage_mcu_layout)
        voltage_user = QWidget()
        voltage_user_layout = QtWidgets.QHBoxLayout()
        label2 = QLabel("User Input: ")
        self.text2 = Qt.QTextEdit()
        self.text2.setMaximumSize(100, 25)
        voltage_user_layout.addWidget(label2)
        voltage_user_layout.addWidget(self.text2)
        voltage_user.setLayout(voltage_user_layout)
        voltage_hbox.addWidget(voltage_mcu)
        voltage_hbox.addWidget(voltage_user)
        voltage_box_widget.setLayout(voltage_hbox)
        
        # The 1st row
        stm_stn_id = QWidget()
        stm_stn_id_layout = QtWidgets.QVBoxLayout()
        STM_id_widget = QWidget()
        STM_id_layout = QtWidgets.QHBoxLayout()
        stm_id_label = QLabel("STM ID: ")
        self.stm_id_var = Qt.QTextEdit()
        self.stm_id_var.setMaximumSize(250,25)
        self.stm_id_var.setReadOnly(True)
        STM_id_layout.addWidget(stm_id_label)
        STM_id_layout.addWidget(self.stm_id_var)
        STM_id_widget.setLayout(STM_id_layout)
        stn_id_widget = QWidget()
        stn_id_layout = QtWidgets.QHBoxLayout()
        stn_id_label = QLabel("NRF ID: ")
        self.stn_id_var = Qt.QTextEdit()
        self.stn_id_var.setMaximumSize(250,25)
        self.stn_id_var.setReadOnly(True)
        stn_id_layout.addWidget(stn_id_label)
        stn_id_layout.addWidget(self.stn_id_var)
        stn_id_widget.setLayout(stn_id_layout)
        stm_stn_id_layout.addWidget(STM_id_widget)
        stm_stn_id_layout.addWidget(stn_id_widget)
        stm_stn_id.setLayout(stm_stn_id_layout)
        
        # The 2nd row
        stn_fw_version = QWidget()
        stn_fw_version_layout = QtWidgets.QHBoxLayout()
        stn_version_widget = QWidget()
        stn_version_layout = QtWidgets.QHBoxLayout()
        stn_version_label = QLabel("NRF Ver: ")
        self.stn_version_var = Qt.QTextEdit()
        self.stn_version_var.setMaximumSize(100,25)
        self.stn_version_var.setReadOnly(True)
        stn_version_layout.addWidget(stn_version_label)
        stn_version_layout.addWidget(self.stn_version_var)
        stn_version_widget.setLayout(stn_version_layout)
        fw_version_widget = QWidget()
        fw_version_layout = QtWidgets.QHBoxLayout()
        fw_version_label = QLabel("STM Ver: ")
        self.fw_version_var = Qt.QTextEdit()
        self.fw_version_var.setMaximumSize(100,25)
        self.fw_version_var.setReadOnly(True)
        fw_version_layout.addWidget(fw_version_label)
        fw_version_layout.addWidget(self.fw_version_var)
        fw_version_widget.setLayout(fw_version_layout)
        stn_fw_version_layout.addWidget(stn_version_widget)
        stn_fw_version_layout.addWidget(fw_version_widget)
        stn_fw_version.setLayout(stn_fw_version_layout)
        
        #vertical layout 1.
        middle_1 = QWidget()
        middle_1_layout= QVBoxLayout()
        middle_1_layout.addWidget(stm_stn_id)
        middle_1_layout.addWidget(stn_fw_version)
#         middle_1_layout.addWidget(voltage_box_widget)
        middle_1.setLayout(middle_1_layout)
        
        #vertical layout for status
        middle_2 = QWidget()
        # make a buttongroup
        middle_2_layout = QVBoxLayout()
#         status_group = QButtonGroup()
#         status_group.setExclusive(False)
#         STN_radio = QRadioButton("STN")
#         GSM_radio = QRadioButton("GSM")
#         SD_radio = QRadioButton("SD")
#         Acc_radio = QRadioButton("Acc")
#         status_group.addButton(STN_radio)
#         status_group.addButton(GSM_radio)
#         status_group.addButton(SD_radio)
#         status_group.addButton(Acc_radio)

        self.STN_radio = QCheckBox("STN")
        self.GSM_radio = QCheckBox("GSM")
        self.SD_radio = QCheckBox("SD")
        self.Acc_radio = QCheckBox("Acc")
        self.GSM_snr_radio = QCheckBox("GSM_SNR")
        self.RTC_radio = QCheckBox("RTC")
        self.NRF_spi_radio = QCheckBox("NRF-SPI")
        self.GPS_radio = QCheckBox("GPS")
        self.GPS_ant_radio = QCheckBox("GPS-ANT")
        self.NRF_acc_radio = QCheckBox("NRF-ACC")
        self.NRF_SD_radio = QCheckBox("NRF-SD")
        self.NRF_OTA_radio = QCheckBox("OTA")
        
        #self.STN_radio.
        
        middle_2_layout.addWidget(self.STN_radio)
        middle_2_layout.addWidget(self.GSM_radio)
        middle_2_layout.addWidget(self.SD_radio)
        middle_2_layout.addWidget(self.Acc_radio)
        middle_2_layout.addWidget(self.GSM_snr_radio)
        middle_2_layout.addWidget(self.RTC_radio)
        middle_2_layout.addWidget(self.NRF_spi_radio)
        middle_2_layout.addWidget(self.GPS_radio)
        middle_2_layout.addWidget(self.GPS_ant_radio)
        middle_2_layout.addWidget(self.NRF_acc_radio)
        middle_2_layout.addWidget(self.NRF_SD_radio)
        middle_2_layout.addWidget(self.NRF_OTA_radio)
        
        middle_2.setLayout(middle_2_layout)
        
        #final horixaontal layout
        middle_layout = QHBoxLayout()
        middle_layout.addWidget(middle_1)
        middle_layout.addWidget(middle_2)
        self.setLayout(middle_layout)
        
        
    def update_middle(self, stm_ver, stm_id, stn_fw, gsm_ver, ccid, nrf_id_low, nrf_id_high,nrf_ver, hw_b_no):
        '''STM_FW | STM_ID | STN_FW | GSM_Ver | CCID | NRF_ID_low | NRF_ID_high | NRF_Version'''
        self.stm_id_var.clear()
        self.stn_id_var.clear()
        self.stn_version_var.clear()
        self.fw_version_var.clear()
        self.stm_id_var.append(stm_id)
        nrf_id = nrf_id_low + nrf_id_high
        self.stn_id_var.append(nrf_id)
        self.fw_version_var.append(stm_ver)
        self.stn_version_var.append(nrf_ver)
        
    def update_middle_status(self, McuV):
        pass
#         self.text1.clear()
#         self.text1.append(McuV)
        
    def update_status_flags(self, STN,GSM,ACC,RTC,SPI,
                            GSM_SNR,SD,GPS,GPS_ant, NRF_ACC,
                            NRF_SD, NRF_OTA):
        #Caution: NOOB coding below
        '''ACC | GSM | GSM_SNR | RTC | SD | NRF_SPI | STN | V_BAT |
             GPS | GPS_ANT | NRF-ACC | NRF_SD | NRF_OTA
        '''
        if STN == "1":
            self.STN_radio.setChecked(True)
        else:
            self.STN_radio.setChecked(False)
        if ACC == "1":
            self.Acc_radio.setChecked(True)
        else:
            self.Acc_radio.setChecked(False)
        if SD == "1":
            self.SD_radio.setChecked(True)
        else:
            self.SD_radio.setChecked(False)
        if GSM == "1":
            self.GSM_radio.setChecked(True)
        else:
            self.GSM_radio.setChecked(False)
        
        if int(GSM_SNR) > 15:
            self.GSM_snr_radio.setChecked(True)
        else:
            self.GSM_snr_radio.setChecked(False)
        if RTC == "1":
            self.RTC_radio.setChecked(True)
        else:
            self.RTC_radio.setChecked(False)
        if SPI == "1":
            self.NRF_spi_radio.setChecked(True)
        else:
            self.NRF_spi_radio.setChecked(False)
        if GPS == "1":
            self.GPS_radio.setChecked(True)
        else:
            self.GPS_radio.setChecked(False)
            
        if GPS_ant == "3":
            self.GPS_ant_radio.setChecked(True)
        else:
            self.GPS_ant_radio.setChecked(False)
        if NRF_ACC == "1":
            self.NRF_acc_radio.setChecked(True)
        else:
            self.NRF_acc_radio.setChecked(False)
            
        if NRF_SD == "1":
            self.NRF_SD_radio.setChecked(True)
        else:
            self.NRF_SD_radio.setChecked(False)
        if NRF_OTA == "1":
            self.NRF_OTA_radio.setChecked(True)
        else:
            self.NRF_OTA_radio.setChecked(False)
        
        
class RightWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(RightWidget,self).__init__()
        
        self.submitButton = QtWidgets.QPushButton("Submit to Server")
        self.saveToText = QtWidgets.QPushButton("Save to Txt")
        self.nextButton = QtWidgets.QPushButton("Flash device")
        
        self.pixelLabel = self.createPixmapLabel()
        self.pixelLabel.setScaledContents(True)
        
        self.submitButton.clicked.connect(self.on_submit)
        self.saveToText.clicked.connect(self.on_text)
        
        layout = QVBoxLayout()
        layout.addWidget(self.pixelLabel)
        layout.addWidget(self.submitButton)
        layout.addWidget(self.saveToText)
        layout.addWidget(self.nextButton)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(layout)
        
    def on_submit(self):
        self.update_pixmap()
        print("Submitting to Server\n")
        
    def on_text(self):
        print("Saving data to text")
        
    def createPixmapLabel(self):
        label = QtWidgets.QLabel()
        label.setEnabled(False)
        label.setAlignment(QtCore.Qt.AlignCenter)
#         label.setFrameShape(QtWidgets.QFrame.Box)
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        label.setBackgroundRole(QtGui.QPalette.Base)
        label.setAutoFillBackground(True)
        label.setMinimumSize(132, 132)
        label.setMaximumSize(200, 200)
        return label
    
    def update_pixmap(self):
        pixmap = QPixmap("wave_apple.jpg")
        self.pixelLabel.setEnabled(True)
        self.pixelLabel.setPixmap(pixmap)
        self.show()


class BasicWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(BasicWidget,self).__init__()
        
        self.submitButton = QtWidgets.QPushButton("Submit to Server")
        self.saveToText = QtWidgets.QPushButton("Save to Txt")
        self.nextButton = QtWidgets.QPushButton("Flash device")
        
        self.submitButton.setEnabled(False)
        self.saveToText.setEnabled(False)
        self.nextButton.setEnabled(False)
        
        voltage_box_widget = QWidget()
        voltage_hbox = QHBoxLayout()
        voltage_mcu = QWidget()
        voltage_mcu_layout = QtWidgets.QHBoxLayout()
        label1 = QLabel("MCU voltage: ")
        self.text1 = Qt.QTextEdit()
#         self.text1.append("12.6")
        self.text1.setMaximumSize(100, 25)
        self.text1.setReadOnly(True)
        voltage_mcu_layout.addWidget(label1)
        voltage_mcu_layout.addWidget(self.text1)
        voltage_mcu.setLayout(voltage_mcu_layout)
        voltage_user = QWidget()
        voltage_user_layout = QtWidgets.QHBoxLayout()
        label2 = QLabel("User Input: ")
        self.text2 = Qt.QTextEdit()
        self.text2.setMaximumSize(100, 25)
        voltage_user_layout.addWidget(label2)
        voltage_user_layout.addWidget(self.text2)
        voltage_user.setLayout(voltage_user_layout)
        voltage_hbox.addWidget(voltage_mcu)
        voltage_hbox.addWidget(voltage_user)
        voltage_box_widget.setLayout(voltage_hbox)
        
        # QR code
        qr_widget = QWidget()
        qr_hbox = QtWidgets.QHBoxLayout()
        qr_label = QLabel("QR Code: ")
        self.qr = Qt.QTextEdit()
        self.qr.setMaximumSize(150, 25)
        qr_hbox.addWidget(qr_label)
        qr_hbox.addWidget(self.qr)
        qr_widget.setLayout(qr_hbox)
        
        device_number = QWidget()
        device_no_layout = QtWidgets.QHBoxLayout()
        device_number_label = QLabel("Device No: ")
        self.device_text = Qt.QTextEdit()
#         self.device_text.append("0012")
        self.device_text.setMaximumSize(100, 25)
        self.device_text.setReadOnly(False)
        device_no_layout.addWidget(device_number_label)
        device_no_layout.addWidget(self.device_text)
        device_number.setLayout(device_no_layout)
        
        self.pixelLabel = self.createPixmapLabel()
        self.pixelLabel.setScaledContents(True)
        self.pixelLabel.setAlignment(QtCore.Qt.AlignCenter)
        
#         self.submitButton.clicked.connect(self.on_submit)
#         self.saveToText.clicked.connect(self.on_text)
        
        layout = QVBoxLayout()
        layout.addWidget(self.pixelLabel,QtCore.Qt.AlignCenter)
        layout.addWidget(device_number)
        layout.addWidget(qr_widget)
        layout.addWidget(voltage_box_widget)
        layout.addWidget(self.submitButton)
        layout.addWidget(self.saveToText)
        layout.addWidget(self.nextButton)
#         layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(layout)
        
    def on_submit(self):
        r = requests.get('https://api.github.com/events')
        print(r)
        print("Submitting to Server\n")
        
    def on_text(self):
        self.f = open("devices.txt","w+")
        print("Saving data to text")
        
    def createPixmapLabel(self):
        label = QtWidgets.QLabel()
        label.setEnabled(True)
        label.setAlignment(QtCore.Qt.AlignCenter)
#         label.setFrameShape(QtWidgets.QFrame.Box)
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        label.setBackgroundRole(QtGui.QPalette.Base)
        label.setAutoFillBackground(False)
        label.setMinimumSize(132, 132)
        label.setMaximumSize(200, 200)
        return label
    