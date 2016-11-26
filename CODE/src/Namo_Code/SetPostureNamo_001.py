from PyQt4 import QtCore, QtGui
from SetPostureNamoUI import Ui_Form
import time
import serial
import sys
import serial.tools.list_ports
from configobj import ConfigObj


class NamoMainWindow(QtGui.QMainWindow,Ui_Form):
    def __init__(self,parent = None):
        super(NamoMainWindow, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        #self.ctimer = QtCore.QTimer()
        #self.stimer = QtCore.QTimer()

        self.InitVariable()
        self.InitUI()
        self.SetButtonAndSpinCtrlDisable()


    # work 50%
    def InitVariable(self):
        self.str_keyframeSelected ='Keyframe1'
        self.int_keyframeSelected = 0
        self.bool_comportConnected = False
        self.int_numberOfKeyframe = 0
        self.str_fileName = None
        self.str_fileNameNumber = None
        self.str_comport = 'com3'
        self.str_baudrate = 115200
        self.int_keyframe = 0
        self.int_motorID = 0
        self.bool_activeKeyframe =[False for x in range (30)]
        file_center = open('./Postures/motor_center.txt', 'r')
        self.int_motorCenterValue = file_center.read()
        file_center.close()
        self.int_motorCenterValue = self.int_motorCenterValue.split('\n')
        print  self.int_motorCenterValue
        #cast motorCenterValue from str to int#
        for x in range (17):
            self.int_motorCenterValue[x] = int(self.int_motorCenterValue[x])
        file_type = open('./Postures/motor_type.txt', 'r')
        self.str_motorType = file_type.read()
        file_type.close()
        self.str_motorType = self.str_motorType.split('\n')
        #print self.int_motorCenterValue
        #print len(self.int_motorCenterValue)
        ##self.int_motorValue[keyframe0-14][motorID0-17]##
        self.int_old_motorValue = [self.int_motorCenterValue[x] for x in range (17)]
        self.int_backup_motorValue = [self.int_motorCenterValue[x] for x in range (17)]
        self.int_motorValue = [[self.int_motorCenterValue[x] for x in range (17)] for y in range (30)]

        self.dic_motorIndexID = {'id1':0,'id2':1,'id3':2,'id4':3,'id5':4,'id6':5, 'id7':6,
                                 'id11':7,'id12':8,'id13':9,'id14':10,'id15':11,'id16':12,'id17':13,
                                 'id21':14,'id22':15,'id23':16}
        self.int_time = [20 for x in range (30)]



    # work
    def InitUI(self):

        self.SetMotorCenterLabel()

        baudrateList = ['9600','115200','1000000']
        self.ui.baudrate_comboBox.addItems(baudrateList)

        postureList = ['Salute','Wai','Bye','SideInvite','p1','p2','p3','p4','p5','p6','p7','p8','p9','p10']
        postureNumber = ['1','2','3','4','5','6','7','8','9','10']
        self.ui.posture_comboBox.addItems(postureList)
        self.ui.posture_number_comboBox.addItems(postureNumber)

        self.str_fileName = postureList[0]
        self.str_fileNameNumber = postureNumber[0]

        keyframeList = ['Keyframe1','Keyframe2','Keyframe3','Keyframe4','Keyframe5','Keyframe6','Keyframe7','Keyframe8','Keyframe9','Keyframe10',
                        'Keyframe11','Keyframe12','Keyframe13','Keyframe14','Keyframe15','Keyframe16','Keyframe17','Keyframe18','Keyframe19','Keyframe20',
                        'Keyframe21','Keyframe22','Keyframe23','Keyframe24','Keyframe25','Keyframe26','Keyframe27','Keyframe28','Keyframe29','Keyframe30',]
        self.ui.keyFrame_comboBox.addItems(keyframeList)

        self.ui.connectionStatus_label.setText("Status : Disconnect")

        #self.ui.keyframeTime_spinBox.setValue(10)

        #QtCore.QObject.connect(self.ui.activeKeyframe_checkBox,QtCore.SIGNAL("stateChanged(int)"), self.ActiveKeyframe_CheckBox)
        QtCore.QObject.connect(self.ui.activeKeyframe_checkBox,QtCore.SIGNAL("clicked()"), self.ActiveKeyframe_CheckBox)

        QtCore.QObject.connect(self.ui.keyFrame_comboBox,QtCore.SIGNAL('activated(QString)'),self.OnSelect_ComboboxKeyframe)
        QtCore.QObject.connect(self.ui.posture_comboBox,QtCore.SIGNAL('activated(QString)'),self.OnSelect_ComboboxPosture)
        QtCore.QObject.connect(self.ui.posture_number_comboBox, QtCore.SIGNAL('activated(QString)'),self.OnSelect_ComboboxPostureNumber)
        QtCore.QObject.connect(self.ui.comport_comboBox,QtCore.SIGNAL('activated(QString)'),self.OnSelect_ComboboxComport)
        QtCore.QObject.connect(self.ui.baudrate_comboBox,QtCore.SIGNAL('activated(QString)'),self.OnSelect_ComboboxBaudrate)

        QtCore.QObject.connect(self.ui.comport_comboBox,QtCore.SIGNAL('currentIndexChanged(QString)'),self.OnIndexChange_ComboboxComport)

        QtCore.QObject.connect(self.ui.connect_Button,QtCore.SIGNAL("clicked()"), self.OnButton_connect)
        QtCore.QObject.connect(self.ui.loadPosture_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_Load)
        QtCore.QObject.connect(self.ui.savePosture_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_Save)
        QtCore.QObject.connect(self.ui.setReady_Button,QtCore.SIGNAL("clicked()"), self.OnButton_ready)
        QtCore.QObject.connect(self.ui.playAll_Button,QtCore.SIGNAL("clicked()"), self.OnButton_playAll)
        QtCore.QObject.connect(self.ui.setTime_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_time)
        QtCore.QObject.connect(self.ui.setAll_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_setAll)
        QtCore.QObject.connect(self.ui.setLAll_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_setLAll)
        QtCore.QObject.connect(self.ui.setRAll_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_setRAll)
        QtCore.QObject.connect(self.ui.setHAll_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_setHAll)
        QtCore.QObject.connect(self.ui.play_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_play)

        QtCore.QObject.connect(self.ui.motor1Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id1Set)
        QtCore.QObject.connect(self.ui.motor2Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id2Set)
        QtCore.QObject.connect(self.ui.motor3Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id3Set)
        QtCore.QObject.connect(self.ui.motor4Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id4Set)
        QtCore.QObject.connect(self.ui.motor5Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id5Set)
        QtCore.QObject.connect(self.ui.motor6Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id6Set)
        QtCore.QObject.connect(self.ui.motor7Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id7Set)

        QtCore.QObject.connect(self.ui.motor11Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id11Set)
        QtCore.QObject.connect(self.ui.motor12Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id12Set)
        QtCore.QObject.connect(self.ui.motor13Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id13Set)
        QtCore.QObject.connect(self.ui.motor14Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id14Set)
        QtCore.QObject.connect(self.ui.motor15Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id15Set)
        QtCore.QObject.connect(self.ui.motor16Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id16Set)
        QtCore.QObject.connect(self.ui.motor17Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id17Set)

        QtCore.QObject.connect(self.ui.motor21Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id21Set)
        QtCore.QObject.connect(self.ui.motor22Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id22Set)
        QtCore.QObject.connect(self.ui.motor23Set_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id23Set)

        QtCore.QObject.connect(self.ui.getAll_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_getAll)
        QtCore.QObject.connect(self.ui.getLAll_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_getLAll)
        QtCore.QObject.connect(self.ui.getRAll_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_getRAll)
        QtCore.QObject.connect(self.ui.getHAll_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_getHAll)

        QtCore.QObject.connect(self.ui.motor1Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id1Get)
        QtCore.QObject.connect(self.ui.motor2Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id2Get)
        QtCore.QObject.connect(self.ui.motor3Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id3Get)
        QtCore.QObject.connect(self.ui.motor4Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id4Get)
        QtCore.QObject.connect(self.ui.motor5Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id5Get)
        QtCore.QObject.connect(self.ui.motor6Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id6Get)
        QtCore.QObject.connect(self.ui.motor7Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id7Get)

        QtCore.QObject.connect(self.ui.motor11Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id11Get)
        QtCore.QObject.connect(self.ui.motor12Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id12Get)
        QtCore.QObject.connect(self.ui.motor13Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id13Get)
        QtCore.QObject.connect(self.ui.motor14Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id14Get)
        QtCore.QObject.connect(self.ui.motor15Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id15Get)
        QtCore.QObject.connect(self.ui.motor16Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id16Get)
        QtCore.QObject.connect(self.ui.motor17Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id17Get)

        QtCore.QObject.connect(self.ui.motor21Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id21Get)
        QtCore.QObject.connect(self.ui.motor22Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id22Get)
        QtCore.QObject.connect(self.ui.motor23Get_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id23Get)

        QtCore.QObject.connect(self.ui.motor1DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id1DisableTorque)
        QtCore.QObject.connect(self.ui.motor2DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id2DisableTorque)
        QtCore.QObject.connect(self.ui.motor3DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id3DisableTorque)
        QtCore.QObject.connect(self.ui.motor4DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id4DisableTorque)
        QtCore.QObject.connect(self.ui.motor5DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id5DisableTorque)
        QtCore.QObject.connect(self.ui.motor6DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id6DisableTorque)
        QtCore.QObject.connect(self.ui.motor7DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id7DisableTorque)

        QtCore.QObject.connect(self.ui.motor11DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id11DisableTorque)
        QtCore.QObject.connect(self.ui.motor12DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id12DisableTorque)
        QtCore.QObject.connect(self.ui.motor13DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id13DisableTorque)
        QtCore.QObject.connect(self.ui.motor14DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id14DisableTorque)
        QtCore.QObject.connect(self.ui.motor15DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id15DisableTorque)
        QtCore.QObject.connect(self.ui.motor16DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id16DisableTorque)
        QtCore.QObject.connect(self.ui.motor17DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id17DisableTorque)

        QtCore.QObject.connect(self.ui.motor21DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id21DisableTorque)
        QtCore.QObject.connect(self.ui.motor22DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id22DisableTorque)
        QtCore.QObject.connect(self.ui.motor23DisT_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_id23DisableTorque)

        QtCore.QObject.connect(self.ui.disTAll_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_DisableTorqueAll)
        QtCore.QObject.connect(self.ui.disTLAll_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_DisableTorqueLAll)
        QtCore.QObject.connect(self.ui.disTRAll_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_DisableTorqueRAll)
        QtCore.QObject.connect(self.ui.disTHAll_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_DisableTorqueHAll)

        QtCore.QObject.connect(self.ui.saveCenter_pushButton,QtCore.SIGNAL("clicked()"), self.OnButton_SaveCenter)

        self.Search_Comport()


    def Search_Comport(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            self.ui.comport_comboBox.addItem(p[0])


    def OnIndexChange_ComboboxComport(self,text):
        self.str_comport = str(text)
        print self.str_comport

    def OnButton_Delete(self):
        #self.ui.keyFrame_comboBox.
        #self.int_backup_motorValue
        #self.int_keyframeSelected
        pass

    def OnButton_DisableTorqueAll(self):
        self.setDisableMotorTorque(1)
        self.setDisableMotorTorque(2)
        self.setDisableMotorTorque(3)
        self.setDisableMotorTorque(4)
        self.setDisableMotorTorque(5)
        self.setDisableMotorTorque(6)
        self.setDisableMotorTorque(7)

        self.setDisableMotorTorque(11)
        self.setDisableMotorTorque(12)
        self.setDisableMotorTorque(13)
        self.setDisableMotorTorque(14)
        self.setDisableMotorTorque(15)
        self.setDisableMotorTorque(16)
        self.setDisableMotorTorque(17)

        self.setDisableMotorTorque(21)
        self.setDisableMotorTorque(22)
        self.setDisableMotorTorque(23)

    def OnButton_DisableTorqueLAll(self):
        self.setDisableMotorTorque(1)
        self.setDisableMotorTorque(2)
        self.setDisableMotorTorque(3)
        self.setDisableMotorTorque(4)
        self.setDisableMotorTorque(5)
        self.setDisableMotorTorque(6)
        self.setDisableMotorTorque(7)

    def OnButton_DisableTorqueRAll(self):
        self.setDisableMotorTorque(11)
        self.setDisableMotorTorque(12)
        self.setDisableMotorTorque(13)
        self.setDisableMotorTorque(14)
        self.setDisableMotorTorque(15)
        self.setDisableMotorTorque(16)
        self.setDisableMotorTorque(17)

    def OnButton_DisableTorqueHAll(self):
        self.setDisableMotorTorque(21)
        self.setDisableMotorTorque(22)
        self.setDisableMotorTorque(23)


    def OnButton_id1DisableTorque(self):
        self.setDisableMotorTorque(1)

    def OnButton_id2DisableTorque(self):
        self.setDisableMotorTorque(2)

    def OnButton_id3DisableTorque(self):
        self.setDisableMotorTorque(3)

    def OnButton_id4DisableTorque(self):
        self.setDisableMotorTorque(4)

    def OnButton_id5DisableTorque(self):
        self.setDisableMotorTorque(5)

    def OnButton_id6DisableTorque(self):
        self.setDisableMotorTorque(6)

    def OnButton_id7DisableTorque(self):
        self.setDisableMotorTorque(7)

    def OnButton_id11DisableTorque(self):
        self.setDisableMotorTorque(11)

    def OnButton_id12DisableTorque(self):
        self.setDisableMotorTorque(12)

    def OnButton_id13DisableTorque(self):
        self.setDisableMotorTorque(13)

    def OnButton_id14DisableTorque(self):
        self.setDisableMotorTorque(14)

    def OnButton_id15DisableTorque(self):
        self.setDisableMotorTorque(15)

    def OnButton_id16DisableTorque(self):
        self.setDisableMotorTorque(16)

    def OnButton_id17DisableTorque(self):
        self.setDisableMotorTorque(17)

    def OnButton_id21DisableTorque(self):
        self.setDisableMotorTorque(21)

    def OnButton_id22DisableTorque(self):
        self.setDisableMotorTorque(22)

    def OnButton_id23DisableTorque(self):
        self.setDisableMotorTorque(23)

    def OnButton_id1Get(self):
        self.ui.motor1Value_spinBox.setValue(self.getMotorPosition(1))

    def OnButton_id2Get(self):
        self.ui.motor2Value_spinBox.setValue(self.getMotorPosition(2))

    def OnButton_id3Get(self):
        self.ui.motor3Value_spinBox.setValue(self.getMotorPosition(3))

    def OnButton_id4Get(self):
        self.ui.motor4Value_spinBox.setValue(self.getMotorPosition(4))

    def OnButton_id5Get(self):
        self.ui.motor5Value_spinBox.setValue(self.getMotorPosition(5))

    def OnButton_id6Get(self):
        self.ui.motor6Value_spinBox.setValue(self.getMotorPosition(6))

    def OnButton_id7Get(self):
        self.ui.motor7Value_spinBox.setValue(self.getMotorPosition(7))

    def OnButton_id11Get(self):
        self.ui.motor11Value_spinBox.setValue(self.getMotorPosition(11))

    def OnButton_id12Get(self):
        self.ui.motor12Value_spinBox.setValue(self.getMotorPosition(12))

    def OnButton_id13Get(self):
        self.ui.motor13Value_spinBox.setValue(self.getMotorPosition(13))

    def OnButton_id14Get(self):
        self.ui.motor14Value_spinBox.setValue(self.getMotorPosition(14))

    def OnButton_id15Get(self):
        self.ui.motor15Value_spinBox.setValue(self.getMotorPosition(15))

    def OnButton_id16Get(self):
        self.ui.motor16Value_spinBox.setValue(self.getMotorPosition(16))

    def OnButton_id17Get(self):
        self.ui.motor17Value_spinBox.setValue(self.getMotorPosition(17))

    def OnButton_id21Get(self):
        self.ui.motor21Value_spinBox.setValue(self.getMotorPosition(21))

    def OnButton_id22Get(self):
        self.ui.motor22Value_spinBox.setValue(self.getMotorPosition(22))

    def OnButton_id23Get(self):
        self.ui.motor23Value_spinBox.setValue(self.getMotorPosition(23))

    def OnButton_getAll(self):
        self.ui.motor1Value_spinBox.setValue(self.getMotorPosition(1))
        self.ui.motor2Value_spinBox.setValue(self.getMotorPosition(2))
        self.ui.motor3Value_spinBox.setValue(self.getMotorPosition(3))
        self.ui.motor4Value_spinBox.setValue(self.getMotorPosition(4))
        self.ui.motor5Value_spinBox.setValue(self.getMotorPosition(5))
        self.ui.motor6Value_spinBox.setValue(self.getMotorPosition(6))
        self.ui.motor7Value_spinBox.setValue(self.getMotorPosition(7))

        self.ui.motor11Value_spinBox.setValue(self.getMotorPosition(11))
        self.ui.motor12Value_spinBox.setValue(self.getMotorPosition(12))
        self.ui.motor13Value_spinBox.setValue(self.getMotorPosition(13))
        self.ui.motor14Value_spinBox.setValue(self.getMotorPosition(14))
        self.ui.motor15Value_spinBox.setValue(self.getMotorPosition(15))
        self.ui.motor16Value_spinBox.setValue(self.getMotorPosition(16))
        self.ui.motor17Value_spinBox.setValue(self.getMotorPosition(17))

        self.ui.motor21Value_spinBox.setValue(self.getMotorPosition(21))
        self.ui.motor22Value_spinBox.setValue(self.getMotorPosition(22))
        self.ui.motor23Value_spinBox.setValue(self.getMotorPosition(23))

    def OnButton_getLAll(self):
        self.ui.motor1Value_spinBox.setValue(self.getMotorPosition(1))
        self.ui.motor2Value_spinBox.setValue(self.getMotorPosition(2))
        self.ui.motor3Value_spinBox.setValue(self.getMotorPosition(3))
        self.ui.motor4Value_spinBox.setValue(self.getMotorPosition(4))
        self.ui.motor5Value_spinBox.setValue(self.getMotorPosition(5))
        self.ui.motor6Value_spinBox.setValue(self.getMotorPosition(6))
        self.ui.motor7Value_spinBox.setValue(self.getMotorPosition(7))

    def OnButton_getRAll(self):
        self.ui.motor11Value_spinBox.setValue(self.getMotorPosition(11))
        self.ui.motor12Value_spinBox.setValue(self.getMotorPosition(12))
        self.ui.motor13Value_spinBox.setValue(self.getMotorPosition(13))
        self.ui.motor14Value_spinBox.setValue(self.getMotorPosition(14))
        self.ui.motor15Value_spinBox.setValue(self.getMotorPosition(15))
        self.ui.motor16Value_spinBox.setValue(self.getMotorPosition(16))
        self.ui.motor17Value_spinBox.setValue(self.getMotorPosition(17))

    def OnButton_getHAll(self):
        self.ui.motor21Value_spinBox.setValue(self.getMotorPosition(21))
        self.ui.motor22Value_spinBox.setValue(self.getMotorPosition(22))
        self.ui.motor23Value_spinBox.setValue(self.getMotorPosition(23))

    def OnButton_id1Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']] = self.ui.motor1Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 1, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id1']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']]
        print self.ui.motor1Value_spinBox.value()

    def OnButton_id2Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']] = self.ui.motor2Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 2, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id2']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']]
        print self.ui.motor2Value_spinBox.value()

    def OnButton_id3Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']] = self.ui.motor3Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 3, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id3']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']]
        print self.ui.motor3Value_spinBox.value()

    def OnButton_id4Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']] = self.ui.motor4Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 4, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id4']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']]
        print self.ui.motor4Value_spinBox.value()

    def OnButton_id5Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']] = self.ui.motor5Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 5, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id5']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']]
        print self.ui.motor5Value_spinBox.value()

    def OnButton_id6Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']] = self.ui.motor6Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 6, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id6']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']]
        print self.ui.motor6Value_spinBox.value()

    def OnButton_id7Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']] = self.ui.motor7Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 7, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id7']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']]
        print self.ui.motor7Value_spinBox.value()

    def OnButton_id11Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']] = self.ui.motor11Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 11, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id11']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']]
        print self.ui.motor11Value_spinBox.value()

    def OnButton_id12Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']] = self.ui.motor12Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 12, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id12']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']]
        print self.ui.motor12Value_spinBox.value()

    def OnButton_id13Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']] = self.ui.motor13Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 13, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id13']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']]
        print self.ui.motor13Value_spinBox.value()

    def OnButton_id14Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']] = self.ui.motor14Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 14, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id14']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']]
        print self.ui.motor14Value_spinBox.value()

    def OnButton_id15Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']] = self.ui.motor15Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 15, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id15']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']]
        print self.ui.motor15Value_spinBox.value()

    def OnButton_id16Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']] = self.ui.motor16Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 16, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id16']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']]
        print self.ui.motor16Value_spinBox.value()

    def OnButton_id17Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']] = self.ui.motor17Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 17, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id17']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']]
        print self.ui.motor17Value_spinBox.value()

    def OnButton_id21Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']] = self.ui.motor21Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 21, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id21']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']]
        print self.ui.motor21Value_spinBox.value()

    def OnButton_id22Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']] = self.ui.motor22Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 22, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id22']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']]
        print self.ui.motor22Value_spinBox.value()

    def OnButton_id23Set(self):
        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']] = self.ui.motor23Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 23, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id23']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']]
        print self.ui.motor23Value_spinBox.value()

    def OnButton_play(self):

        self.SetButtonAndSpinCtrlDisable()

        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']] = self.ui.motor1Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']] = self.ui.motor2Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']] = self.ui.motor3Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']] = self.ui.motor4Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']] = self.ui.motor5Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']] = self.ui.motor6Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']] = self.ui.motor7Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']] = self.ui.motor11Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']] = self.ui.motor12Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']] = self.ui.motor13Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']] = self.ui.motor14Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']] = self.ui.motor15Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']] = self.ui.motor16Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']] = self.ui.motor17Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']] = self.ui.motor21Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']] = self.ui.motor22Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']] = self.ui.motor23Value_spinBox.value()



        time_start = time.time()
        time_finish = time_start + float(self.int_time[self.GetOrderKeyframe() - 1])/10
        in_time = True

        print time_start
        print time_finish
        print 'Wait....'
        while in_time:
            time_current = time.time()
            if time_current >= time_finish:
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 1, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 2, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 3, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 4, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 5, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 6, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 7, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 11, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 12, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 13, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 14, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 15, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 16, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 17, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 21, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 22, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']], 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 23, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']], 1023, 1023)


                self.int_old_motorValue[self.dic_motorIndexID['id1']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']]
                self.int_old_motorValue[self.dic_motorIndexID['id2']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']]
                self.int_old_motorValue[self.dic_motorIndexID['id3']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']]
                self.int_old_motorValue[self.dic_motorIndexID['id4']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']]
                self.int_old_motorValue[self.dic_motorIndexID['id5']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']]
                self.int_old_motorValue[self.dic_motorIndexID['id6']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']]
                self.int_old_motorValue[self.dic_motorIndexID['id7']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']]
                self.int_old_motorValue[self.dic_motorIndexID['id11']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']]
                self.int_old_motorValue[self.dic_motorIndexID['id12']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']]
                self.int_old_motorValue[self.dic_motorIndexID['id13']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']]
                self.int_old_motorValue[self.dic_motorIndexID['id14']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']]
                self.int_old_motorValue[self.dic_motorIndexID['id15']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']]
                self.int_old_motorValue[self.dic_motorIndexID['id16']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']]
                self.int_old_motorValue[self.dic_motorIndexID['id17']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']]
                self.int_old_motorValue[self.dic_motorIndexID['id21']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']]
                self.int_old_motorValue[self.dic_motorIndexID['id22']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']]
                self.int_old_motorValue[self.dic_motorIndexID['id23']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']]

                in_time = False

            else:
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 1, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']],self.int_old_motorValue[self.dic_motorIndexID['id1']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 2, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']],self.int_old_motorValue[self.dic_motorIndexID['id2']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 3, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']],self.int_old_motorValue[self.dic_motorIndexID['id3']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 4, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']],self.int_old_motorValue[self.dic_motorIndexID['id4']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 5, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']],self.int_old_motorValue[self.dic_motorIndexID['id5']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 6, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']],self.int_old_motorValue[self.dic_motorIndexID['id6']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 7, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']],self.int_old_motorValue[self.dic_motorIndexID['id7']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 11, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']],self.int_old_motorValue[self.dic_motorIndexID['id11']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 12, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']],self.int_old_motorValue[self.dic_motorIndexID['id12']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 13, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']],self.int_old_motorValue[self.dic_motorIndexID['id13']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 14, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']],self.int_old_motorValue[self.dic_motorIndexID['id14']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 15, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']],self.int_old_motorValue[self.dic_motorIndexID['id15']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 16, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']],self.int_old_motorValue[self.dic_motorIndexID['id16']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 17, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']],self.int_old_motorValue[self.dic_motorIndexID['id17']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 21, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']],self.int_old_motorValue[self.dic_motorIndexID['id21']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 22, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']],self.int_old_motorValue[self.dic_motorIndexID['id22']],time_finish,time_start,time_current), 1023, 1023)
                self.setDeviceMoving( self.str_comport, self.str_baudrate, 23, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']],self.int_old_motorValue[self.dic_motorIndexID['id23']],time_finish,time_start,time_current), 1023, 1023)

            time.sleep(0.015)




        print 'Finished'
        self.SetButtonAndSpinCtrlEnable()

    def OnButton_setLAll(self):

        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']] = self.ui.motor1Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']] = self.ui.motor2Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']] = self.ui.motor3Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']] = self.ui.motor4Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']] = self.ui.motor5Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']] = self.ui.motor6Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']] = self.ui.motor7Value_spinBox.value()

        self.setDeviceMoving( self.str_comport, self.str_baudrate, 1, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 2, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 3, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 4, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 5, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 6, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 7, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']], 1023, 1023)

        self.int_old_motorValue[self.dic_motorIndexID['id1']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']]
        self.int_old_motorValue[self.dic_motorIndexID['id2']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']]
        self.int_old_motorValue[self.dic_motorIndexID['id3']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']]
        self.int_old_motorValue[self.dic_motorIndexID['id4']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']]
        self.int_old_motorValue[self.dic_motorIndexID['id5']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']]
        self.int_old_motorValue[self.dic_motorIndexID['id6']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']]
        self.int_old_motorValue[self.dic_motorIndexID['id7']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']]






    def OnButton_setRAll(self):

        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']] = self.ui.motor11Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']] = self.ui.motor12Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']] = self.ui.motor13Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']] = self.ui.motor14Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']] = self.ui.motor15Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']] = self.ui.motor16Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']] = self.ui.motor17Value_spinBox.value()

        self.setDeviceMoving( self.str_comport, self.str_baudrate, 11, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 12, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 13, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 14, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 15, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 16, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 17, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']], 1023, 1023)

        self.int_old_motorValue[self.dic_motorIndexID['id11']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']]
        self.int_old_motorValue[self.dic_motorIndexID['id12']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']]
        self.int_old_motorValue[self.dic_motorIndexID['id13']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']]
        self.int_old_motorValue[self.dic_motorIndexID['id14']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']]
        self.int_old_motorValue[self.dic_motorIndexID['id15']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']]
        self.int_old_motorValue[self.dic_motorIndexID['id16']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']]
        self.int_old_motorValue[self.dic_motorIndexID['id17']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']]



    def OnButton_setHAll(self):

        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']] = self.ui.motor21Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']] = self.ui.motor22Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']] = self.ui.motor23Value_spinBox.value()
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 21, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 22, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 23, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']], 1023, 1023)

        self.int_old_motorValue[self.dic_motorIndexID['id21']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']]
        self.int_old_motorValue[self.dic_motorIndexID['id22']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']]
        self.int_old_motorValue[self.dic_motorIndexID['id23']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']]



    def OnButton_setAll(self):

        #self.int_time[self.GetOrderKeyframe() - 1] = self.spinctrl_time.GetValue()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']] = self.ui.motor1Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']] = self.ui.motor2Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']] = self.ui.motor3Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']] = self.ui.motor4Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']] = self.ui.motor5Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']] = self.ui.motor6Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']] = self.ui.motor7Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']] = self.ui.motor11Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']] = self.ui.motor12Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']] = self.ui.motor13Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']] = self.ui.motor14Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']] = self.ui.motor15Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']] = self.ui.motor16Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']] = self.ui.motor17Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']] = self.ui.motor21Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']] = self.ui.motor22Value_spinBox.value()
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']] = self.ui.motor23Value_spinBox.value()



        self.setDeviceMoving( self.str_comport, self.str_baudrate, 1, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 2, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 3, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 4, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 5, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 6, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 7, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 11, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 12, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 13, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 14, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 15, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 16, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 17, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 21, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 22, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']], 1023, 1023)
        self.setDeviceMoving( self.str_comport, self.str_baudrate, 23, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']], 1023, 1023)


        self.int_old_motorValue[self.dic_motorIndexID['id11']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id11']]
        self.int_old_motorValue[self.dic_motorIndexID['id12']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id12']]
        self.int_old_motorValue[self.dic_motorIndexID['id13']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id13']]
        self.int_old_motorValue[self.dic_motorIndexID['id14']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id14']]
        self.int_old_motorValue[self.dic_motorIndexID['id15']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id15']]
        self.int_old_motorValue[self.dic_motorIndexID['id16']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id16']]
        self.int_old_motorValue[self.dic_motorIndexID['id17']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id17']]

        self.int_old_motorValue[self.dic_motorIndexID['id1']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id1']]
        self.int_old_motorValue[self.dic_motorIndexID['id2']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id2']]
        self.int_old_motorValue[self.dic_motorIndexID['id3']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id3']]
        self.int_old_motorValue[self.dic_motorIndexID['id4']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id4']]
        self.int_old_motorValue[self.dic_motorIndexID['id5']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id5']]
        self.int_old_motorValue[self.dic_motorIndexID['id6']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id6']]
        self.int_old_motorValue[self.dic_motorIndexID['id7']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id7']]

        self.int_old_motorValue[self.dic_motorIndexID['id21']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id21']]
        self.int_old_motorValue[self.dic_motorIndexID['id22']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id22']]
        self.int_old_motorValue[self.dic_motorIndexID['id23']] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id23']]




    def OnButton_time(self):
        self.int_time[self.GetOrderKeyframe() - 1] = self.ui.keyframeTime_spinBox.value()
        print self.int_time[self.GetOrderKeyframe() - 1]

    def OnButton_ready(self):
        if self.int_numberOfKeyframe == 0:
            print 'Error!! Number of keyframe = 0 '
        else:
            time_start = time.time()
            time_finish = time_start + float(self.int_time[0])/10
            in_time = True

            print time_start
            print time_finish
            print 'Wait....'
            while in_time:
                time_current = time.time()
                if time_current >= time_finish:
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 1, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id1']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 2, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id2']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 3, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id3']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 4, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id4']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 5, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id5']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 6, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id6']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 7, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id7']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 11, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id11']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 12, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id12']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 13, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id13']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 14, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id14']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 15, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id15']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 16, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id16']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 17, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id17']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 21, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id21']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 22, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id22']], 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 23, "Ex", self.int_motorValue[0][self.dic_motorIndexID['id23']], 200, 200)

                    self.int_old_motorValue[self.dic_motorIndexID['id1']] = self.int_motorValue[0][self.dic_motorIndexID['id1']]
                    self.int_old_motorValue[self.dic_motorIndexID['id2']] = self.int_motorValue[0][self.dic_motorIndexID['id2']]
                    self.int_old_motorValue[self.dic_motorIndexID['id3']] = self.int_motorValue[0][self.dic_motorIndexID['id3']]
                    self.int_old_motorValue[self.dic_motorIndexID['id4']] = self.int_motorValue[0][self.dic_motorIndexID['id4']]
                    self.int_old_motorValue[self.dic_motorIndexID['id5']] = self.int_motorValue[0][self.dic_motorIndexID['id5']]
                    self.int_old_motorValue[self.dic_motorIndexID['id6']] = self.int_motorValue[0][self.dic_motorIndexID['id6']]
                    self.int_old_motorValue[self.dic_motorIndexID['id7']] = self.int_motorValue[0][self.dic_motorIndexID['id7']]
                    self.int_old_motorValue[self.dic_motorIndexID['id11']] = self.int_motorValue[0][self.dic_motorIndexID['id11']]
                    self.int_old_motorValue[self.dic_motorIndexID['id12']] = self.int_motorValue[0][self.dic_motorIndexID['id12']]
                    self.int_old_motorValue[self.dic_motorIndexID['id13']] = self.int_motorValue[0][self.dic_motorIndexID['id13']]
                    self.int_old_motorValue[self.dic_motorIndexID['id14']] = self.int_motorValue[0][self.dic_motorIndexID['id14']]
                    self.int_old_motorValue[self.dic_motorIndexID['id15']] = self.int_motorValue[0][self.dic_motorIndexID['id15']]
                    self.int_old_motorValue[self.dic_motorIndexID['id16']] = self.int_motorValue[0][self.dic_motorIndexID['id16']]
                    self.int_old_motorValue[self.dic_motorIndexID['id17']] = self.int_motorValue[0][self.dic_motorIndexID['id17']]
                    self.int_old_motorValue[self.dic_motorIndexID['id21']] = self.int_motorValue[0][self.dic_motorIndexID['id21']]
                    self.int_old_motorValue[self.dic_motorIndexID['id22']] = self.int_motorValue[0][self.dic_motorIndexID['id22']]
                    self.int_old_motorValue[self.dic_motorIndexID['id23']] = self.int_motorValue[0][self.dic_motorIndexID['id23']]


                    in_time = False

                else:
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 1, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id1']],self.int_old_motorValue[self.dic_motorIndexID['id1']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 2, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id2']],self.int_old_motorValue[self.dic_motorIndexID['id2']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 3, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id3']],self.int_old_motorValue[self.dic_motorIndexID['id3']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 4, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id4']],self.int_old_motorValue[self.dic_motorIndexID['id4']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 5, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id5']],self.int_old_motorValue[self.dic_motorIndexID['id5']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 6, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id6']],self.int_old_motorValue[self.dic_motorIndexID['id6']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 7, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id7']],self.int_old_motorValue[self.dic_motorIndexID['id7']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 11, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id11']],self.int_old_motorValue[self.dic_motorIndexID['id11']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 12, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id12']],self.int_old_motorValue[self.dic_motorIndexID['id12']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 13, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id13']],self.int_old_motorValue[self.dic_motorIndexID['id13']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 14, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id14']],self.int_old_motorValue[self.dic_motorIndexID['id14']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 15, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id15']],self.int_old_motorValue[self.dic_motorIndexID['id15']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 16, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id16']],self.int_old_motorValue[self.dic_motorIndexID['id16']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 17, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id17']],self.int_old_motorValue[self.dic_motorIndexID['id17']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 21, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id21']],self.int_old_motorValue[self.dic_motorIndexID['id21']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 22, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id22']],self.int_old_motorValue[self.dic_motorIndexID['id22']],time_finish,time_start,time_current), 200, 200)
                    self.setDeviceMoving( self.str_comport, self.str_baudrate, 23, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][self.dic_motorIndexID['id23']],self.int_old_motorValue[self.dic_motorIndexID['id23']],time_finish,time_start,time_current), 200, 200)

                time.sleep(0.015)
            print 'Finished'

    def OnButton_playAll(self):

        if self.int_numberOfKeyframe == 0:
            print 'Error!! Number of keyframe = 0 '
        else:
            self.SetButtonAndSpinCtrlDisable()
            for x in range(self.int_numberOfKeyframe):
                time_start = time.time()
                time_finish = time_start + float(self.int_time[x])/10
                in_time = True

                print time_start
                print time_finish
                print 'keyframe = '+ str(x+1)
                print 'Time = '+ str(self.int_time[x])
                print 'Wait....'
                while in_time:
                    time_current = time.time()
                    if time_current >= time_finish:
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 1, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id1']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 2, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id2']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 3, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id3']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 4, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id4']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 5, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id5']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 6, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id6']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 7, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id7']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 11, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id11']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 12, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id12']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 13, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id13']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 14, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id14']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 15, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id15']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 16, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id16']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 17, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id17']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 21, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id21']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 22, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id22']], 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 23, "Ex", self.int_motorValue[x][self.dic_motorIndexID['id23']], 1023, 1023)


                        self.int_old_motorValue[self.dic_motorIndexID['id1']] = self.int_motorValue[x][self.dic_motorIndexID['id1']]
                        self.int_old_motorValue[self.dic_motorIndexID['id2']] = self.int_motorValue[x][self.dic_motorIndexID['id2']]
                        self.int_old_motorValue[self.dic_motorIndexID['id3']] = self.int_motorValue[x][self.dic_motorIndexID['id3']]
                        self.int_old_motorValue[self.dic_motorIndexID['id4']] = self.int_motorValue[x][self.dic_motorIndexID['id4']]
                        self.int_old_motorValue[self.dic_motorIndexID['id5']] = self.int_motorValue[x][self.dic_motorIndexID['id5']]
                        self.int_old_motorValue[self.dic_motorIndexID['id6']] = self.int_motorValue[x][self.dic_motorIndexID['id6']]
                        self.int_old_motorValue[self.dic_motorIndexID['id7']] = self.int_motorValue[x][self.dic_motorIndexID['id7']]
                        self.int_old_motorValue[self.dic_motorIndexID['id11']] = self.int_motorValue[x][self.dic_motorIndexID['id11']]
                        self.int_old_motorValue[self.dic_motorIndexID['id12']] = self.int_motorValue[x][self.dic_motorIndexID['id12']]
                        self.int_old_motorValue[self.dic_motorIndexID['id13']] = self.int_motorValue[x][self.dic_motorIndexID['id13']]
                        self.int_old_motorValue[self.dic_motorIndexID['id14']] = self.int_motorValue[x][self.dic_motorIndexID['id14']]
                        self.int_old_motorValue[self.dic_motorIndexID['id15']] = self.int_motorValue[x][self.dic_motorIndexID['id15']]
                        self.int_old_motorValue[self.dic_motorIndexID['id16']] = self.int_motorValue[x][self.dic_motorIndexID['id16']]
                        self.int_old_motorValue[self.dic_motorIndexID['id17']] = self.int_motorValue[x][self.dic_motorIndexID['id17']]
                        self.int_old_motorValue[self.dic_motorIndexID['id21']] = self.int_motorValue[x][self.dic_motorIndexID['id21']]
                        self.int_old_motorValue[self.dic_motorIndexID['id22']] = self.int_motorValue[x][self.dic_motorIndexID['id22']]
                        self.int_old_motorValue[self.dic_motorIndexID['id23']] = self.int_motorValue[x][self.dic_motorIndexID['id23']]


                        in_time = False

                    else:
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 1, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id1']],self.int_old_motorValue[self.dic_motorIndexID['id1']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 2, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id2']],self.int_old_motorValue[self.dic_motorIndexID['id2']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 3, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id3']],self.int_old_motorValue[self.dic_motorIndexID['id3']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 4, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id4']],self.int_old_motorValue[self.dic_motorIndexID['id4']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 5, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id5']],self.int_old_motorValue[self.dic_motorIndexID['id5']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 6, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id6']],self.int_old_motorValue[self.dic_motorIndexID['id6']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 7, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id7']],self.int_old_motorValue[self.dic_motorIndexID['id7']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 11, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id11']],self.int_old_motorValue[self.dic_motorIndexID['id11']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 12, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id12']],self.int_old_motorValue[self.dic_motorIndexID['id12']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 13, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id13']],self.int_old_motorValue[self.dic_motorIndexID['id13']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 14, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id14']],self.int_old_motorValue[self.dic_motorIndexID['id14']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 15, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id15']],self.int_old_motorValue[self.dic_motorIndexID['id15']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 16, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id16']],self.int_old_motorValue[self.dic_motorIndexID['id16']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 17, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id17']],self.int_old_motorValue[self.dic_motorIndexID['id17']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 21, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id21']],self.int_old_motorValue[self.dic_motorIndexID['id21']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 22, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id22']],self.int_old_motorValue[self.dic_motorIndexID['id22']],time_finish,time_start,time_current), 1023, 1023)
                        self.setDeviceMoving( self.str_comport, self.str_baudrate, 23, "Ex", self.InterpolateMotorValue(self.int_motorValue[x][self.dic_motorIndexID['id23']],self.int_old_motorValue[self.dic_motorIndexID['id23']],time_finish,time_start,time_current), 1023, 1023)

                    time.sleep(0.015)




                print 'Finished'
            self.SetButtonAndSpinCtrlEnable()


    def OnButton_Load(self):
        print "Load"
        print self.str_fileName
        print self.str_fileNameNumber

        self.ui.fileName_label.setText(self.str_fileName + self.str_fileNameNumber)

        filename = './Postures/' + str(self.str_fileName) + str(self.str_fileNameNumber)
        #filename = self.str_fileName        print filename
        config = ConfigObj(filename)
        self.int_numberOfKeyframe = int(config['Keyframe_Amount'])
        self.ui.numOfKeyframeStatus_label.setText(str(self.int_numberOfKeyframe))

        for i in range(int(self.int_numberOfKeyframe)):
            self.bool_activeKeyframe[i] = True
            self.int_motorValue[i] = map(int, config['Keyframe_Value']['Keyframe_' + str(i)])
            self.int_time[i] = int(config['Keyframe_Time'][i])

        for i in range(int(self.int_numberOfKeyframe), 30):
            self.bool_activeKeyframe[i] = False



        self.SetValueKeyframeToShow()


    def OnButton_Save(self):
        print "Save"
        print self.str_fileName
        print self.str_fileNameNumber

        self.ui.fileName_label.setText(self.str_fileName + self.str_fileNameNumber)

        config = ConfigObj()
        config.filename = './Postures/' + self.str_fileName + self.str_fileNameNumber
        config['Posture_Name'] = self.str_fileName + self.str_fileNameNumber
        config['Keyframe_Amount'] = self.int_numberOfKeyframe
        config['Keyframe_Time'] = self.int_time[:self.int_numberOfKeyframe]
        config['Keyframe_Value'] = {}
        for i in range(self.int_numberOfKeyframe):
            config['Keyframe_Value']['Keyframe_' + str(i)] = self.int_motorValue[i]
        config.write()


    def SetMotorCenterLabel(self):
        self.ui.motor1center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id1']]))
        self.ui.motor2center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id2']]))
        self.ui.motor3center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id3']]))
        self.ui.motor4center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id4']]))
        self.ui.motor5center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id5']]))
        self.ui.motor6center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id6']]))
        self.ui.motor7center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id7']]))

        self.ui.motor11center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id11']]))
        self.ui.motor12center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id12']]))
        self.ui.motor13center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id13']]))
        self.ui.motor14center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id14']]))
        self.ui.motor15center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id15']]))
        self.ui.motor16center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id16']]))
        self.ui.motor17center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id17']]))

        self.ui.motor21center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id21']]))
        self.ui.motor22center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id22']]))
        self.ui.motor23center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id23']]))



    def OnButton_SaveCenter(self):
        file_center = open('./Postures/motor_center.txt', 'w')
        self.int_motorCenterValue[self.dic_motorIndexID['id1']] = self.ui.motor1Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id2']] = self.ui.motor2Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id3']] = self.ui.motor3Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id4']] = self.ui.motor4Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id5']] = self.ui.motor5Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id6']] = self.ui.motor6Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id7']] = self.ui.motor7Value_spinBox.value()

        self.int_motorCenterValue[self.dic_motorIndexID['id11']] = self.ui.motor11Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id12']] = self.ui.motor12Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id13']] = self.ui.motor13Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id14']] = self.ui.motor14Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id15']] = self.ui.motor15Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id16']] = self.ui.motor16Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id17']] = self.ui.motor17Value_spinBox.value()

        self.int_motorCenterValue[self.dic_motorIndexID['id21']] = self.ui.motor21Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id22']] = self.ui.motor22Value_spinBox.value()
        self.int_motorCenterValue[self.dic_motorIndexID['id23']] = self.ui.motor23Value_spinBox.value()

        for y in range (17):
                file_center.write(str(self.int_motorCenterValue[y])+'\n')

        file_center.close()

        self.SetMotorCenterLabel()




    def OnSelect_ComboboxPosture(self,text):
        self.str_fileName = text
        print self.str_fileName

    def OnSelect_ComboboxPostureNumber(self,text):
        self.str_fileNameNumber = text
        print self.str_fileNameNumber

    # work 90%
    def OnButton_connect(self):
        print "connect clicked"
        if self.bool_comportConnected == False:
            self.bool_comportConnected = True
            self.serialDevice = serial.Serial(self.str_comport, self.str_baudrate,8,'N',1,0,0,0,0)
            self.ui.connectionStatus_label.setText("Status : Connected")
            self.ui.connect_Button.setText("Disconnect")
        else:
            self.bool_comportConnected = False
            self.serialDevice.close()
            self.ui.connectionStatus_label.setText("Status : Disconnected")
            self.ui.connect_Button.setText("Connect")

    def OnSelect_ComboboxComport(self,text):
        self.str_comport = str(text)
        print self.str_comport

    def OnSelect_ComboboxBaudrate(self,text):
        self.str_baudrate = str(text)
        print self.str_baudrate

    def OnSelect_ComboboxKeyframe(self,text):
        self.str_keyframeSelected = text
        print self.str_keyframeSelected
        self.SetValueKeyframeToShow()

    # work 50%
    def SetValueKeyframeToShow(self):
        if self.str_keyframeSelected == 'Keyframe1':
            keyframe = 1
        elif self.str_keyframeSelected == 'Keyframe2':
            keyframe = 2
        elif self.str_keyframeSelected == 'Keyframe3':
            keyframe = 3
        elif self.str_keyframeSelected == 'Keyframe4':
            keyframe = 4
        elif self.str_keyframeSelected == 'Keyframe5':
            keyframe = 5
        elif self.str_keyframeSelected == 'Keyframe6':
            keyframe = 6
        elif self.str_keyframeSelected == 'Keyframe7':
            keyframe = 7
        elif self.str_keyframeSelected == 'Keyframe8':
            keyframe = 8
        elif self.str_keyframeSelected == 'Keyframe9':
            keyframe = 9
        elif self.str_keyframeSelected == 'Keyframe10':
            keyframe = 10
        elif self.str_keyframeSelected == 'Keyframe11':
            keyframe = 11
        elif self.str_keyframeSelected == 'Keyframe12':
            keyframe = 12
        elif self.str_keyframeSelected == 'Keyframe13':
            keyframe = 13
        elif self.str_keyframeSelected == 'Keyframe14':
            keyframe = 14
        elif self.str_keyframeSelected == 'Keyframe15':
            keyframe = 15
        elif self.str_keyframeSelected == 'Keyframe16':
            keyframe = 16
        elif self.str_keyframeSelected == 'Keyframe17':
            keyframe = 17
        elif self.str_keyframeSelected == 'Keyframe18':
            keyframe = 18
        elif self.str_keyframeSelected == 'Keyframe19':
            keyframe = 19
        elif self.str_keyframeSelected == 'Keyframe20':
            keyframe = 20
        elif self.str_keyframeSelected == 'Keyframe21':
            keyframe = 21
        elif self.str_keyframeSelected == 'Keyframe22':
            keyframe = 22
        elif self.str_keyframeSelected == 'Keyframe23':
            keyframe = 23
        elif self.str_keyframeSelected == 'Keyframe24':
            keyframe = 24
        elif self.str_keyframeSelected == 'Keyframe25':
            keyframe = 25
        elif self.str_keyframeSelected == 'Keyframe26':
            keyframe = 26
        elif self.str_keyframeSelected == 'Keyframe27':
            keyframe = 27
        elif self.str_keyframeSelected == 'Keyframe28':
            keyframe = 28
        elif self.str_keyframeSelected == 'Keyframe29':
            keyframe = 29
        elif self.str_keyframeSelected == 'Keyframe30':
            keyframe = 30

        self.int_keyframeSelected = keyframe

        print "keyframe selected = "
        print self.int_keyframeSelected
        #self.ui.activeKeyframe_checkBox.setChecked(self.bool_activeKeyframe[keyframe-1])
        print self.bool_activeKeyframe

        if self.bool_activeKeyframe[keyframe-1] == True:
            self.ui.activeKeyframe_checkBox.setChecked(2)
            self.SetButtonAndSpinCtrlEnable()
            self.ui.motor1Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id1']])
            self.ui.motor2Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id2']])
            self.ui.motor3Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id3']])
            self.ui.motor4Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id4']])
            self.ui.motor5Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id5']])
            self.ui.motor6Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id6']])
            self.ui.motor7Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id7']])

            self.ui.motor11Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id11']])
            self.ui.motor12Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id12']])
            self.ui.motor13Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id13']])
            self.ui.motor14Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id14']])
            self.ui.motor15Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id15']])
            self.ui.motor16Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id16']])
            self.ui.motor17Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id17']])

            self.ui.motor21Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id21']])
            self.ui.motor22Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id22']])
            self.ui.motor23Value_spinBox.setValue(self.int_motorValue[keyframe-1][self.dic_motorIndexID['id23']])

            self.ui.keyframeTime_spinBox.setValue(self.int_time[keyframe-1])
        else:
            self.ui.activeKeyframe_checkBox.setChecked(0)
            self.SetButtonAndSpinCtrlDisable()

    def CheckPreviousKeyframe(self,currentKeyframe):
        if currentKeyframe == 1:
            self.bool_activeKeyframe[currentKeyframe-1] = True
            self.SetValueKeyframeToShow()
        else:
            self.bool_activeKeyframe[0] = True
            bool_getActiveKeyframe = False
            int_searchKeyframe = currentKeyframe - 1
            while(bool_getActiveKeyframe == False):
                if self.bool_activeKeyframe[int_searchKeyframe - 1] == True:
                    bool_getActiveKeyframe = True
                else:
                    int_searchKeyframe = int_searchKeyframe - 1
            for i in range (int_searchKeyframe+1,currentKeyframe+1):
                self.bool_activeKeyframe[i-1] = True
                for j in range (17):
                    self.int_motorValue[i-1][j] = self.int_motorValue[int_searchKeyframe-1][j]
            #self.SetValueKeyframeToShow(currentKeyframe)
            self.SetValueKeyframeToShow()



    def CheckNextKeyframe(self,currentKeyframe):
        if currentKeyframe == 30:
            self.bool_activeKeyframe[currentKeyframe-1] = False
            self.SetValueKeyframeToShow()
        else:
            self.bool_activeKeyframe[29] = False
            bool_getNotActiveKeyframe = False
            int_searchKeyframe = currentKeyframe + 1
            while(bool_getNotActiveKeyframe == False):
                if self.bool_activeKeyframe[int_searchKeyframe - 1] == False:
                    bool_getNotActiveKeyframe = True
                else:
                    int_searchKeyframe = int_searchKeyframe + 1
            for i in range (currentKeyframe,int_searchKeyframe+1):
                self.bool_activeKeyframe[i-1] = False
                for j in range (17):
                    self.int_motorValue[i-1][j] = self.int_motorCenterValue[j]
            #self.SetValueKeyframeToShow(currentKeyframe)
            self.SetValueKeyframeToShow()




    def ActiveKeyframe_CheckBox(self):
        print self.ui.activeKeyframe_checkBox.checkState()

        if self.ui.activeKeyframe_checkBox.checkState() == 2:
            print"Checked"

            if self.str_keyframeSelected == 'Keyframe1':
                #self.bool_activeKeyframe[0] = True
                self.CheckPreviousKeyframe(1)
                self.int_numberOfKeyframe = 1
            elif self.str_keyframeSelected == 'Keyframe2':
                #self.bool_activeKeyframe[1] = True
                self.CheckPreviousKeyframe(2)
                self.int_numberOfKeyframe = 2
            elif self.str_keyframeSelected == 'Keyframe3':
                #self.bool_activeKeyframe[2] = True
                self.CheckPreviousKeyframe(3)
                self.int_numberOfKeyframe = 3
            elif self.str_keyframeSelected == 'Keyframe4':
                #self.bool_activeKeyframe[3] = True
                self.CheckPreviousKeyframe(4)
                self.int_numberOfKeyframe = 4
            elif self.str_keyframeSelected == 'Keyframe5':
                #self.bool_activeKeyframe[4] = True
                self.CheckPreviousKeyframe(5)
                self.int_numberOfKeyframe = 5
            elif self.str_keyframeSelected == 'Keyframe6':
                #self.bool_activeKeyframe[5] = True
                self.CheckPreviousKeyframe(6)
                self.int_numberOfKeyframe = 6
            elif self.str_keyframeSelected == 'Keyframe7':
                #self.bool_activeKeyframe[6] = True
                self.CheckPreviousKeyframe(7)
                self.int_numberOfKeyframe = 7
            elif self.str_keyframeSelected == 'Keyframe8':
                #self.bool_activeKeyframe[7] = True
                self.CheckPreviousKeyframe(8)
                self.int_numberOfKeyframe = 8
            elif self.str_keyframeSelected == 'Keyframe9':
                #self.bool_activeKeyframe[8] = True
                self.CheckPreviousKeyframe(9)
                self.int_numberOfKeyframe = 9
            elif self.str_keyframeSelected == 'Keyframe10':
                #self.bool_activeKeyframe[9] = True
                self.CheckPreviousKeyframe(10)
                self.int_numberOfKeyframe = 10
            elif self.str_keyframeSelected == 'Keyframe11':
                #self.bool_activeKeyframe[10] = True
                self.CheckPreviousKeyframe(11)
                self.int_numberOfKeyframe = 11
            elif self.str_keyframeSelected == 'Keyframe12':
                #self.bool_activeKeyframe[11] = True
                self.CheckPreviousKeyframe(12)
                self.int_numberOfKeyframe = 12
            elif self.str_keyframeSelected == 'Keyframe13':
                #self.bool_activeKeyframe[12] = True
                self.CheckPreviousKeyframe(13)
                self.int_numberOfKeyframe = 13
            elif self.str_keyframeSelected == 'Keyframe14':
                #self.bool_activeKeyframe[13] = True
                self.CheckPreviousKeyframe(14)
                self.int_numberOfKeyframe = 14
            elif self.str_keyframeSelected == 'Keyframe15':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(15)
                self.int_numberOfKeyframe = 15
            elif self.str_keyframeSelected == 'Keyframe16':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(16)
                self.int_numberOfKeyframe = 16
            elif self.str_keyframeSelected == 'Keyframe17':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(17)
                self.int_numberOfKeyframe = 17
            elif self.str_keyframeSelected == 'Keyframe18':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(18)
                self.int_numberOfKeyframe = 18
            elif self.str_keyframeSelected == 'Keyframe19':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(19)
                self.int_numberOfKeyframe = 19
            elif self.str_keyframeSelected == 'Keyframe20':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(20)
                self.int_numberOfKeyframe = 20
            elif self.str_keyframeSelected == 'Keyframe21':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(21)
                self.int_numberOfKeyframe = 21
            elif self.str_keyframeSelected == 'Keyframe22':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(22)
                self.int_numberOfKeyframe = 22
            elif self.str_keyframeSelected == 'Keyframe23':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(23)
                self.int_numberOfKeyframe = 23
            elif self.str_keyframeSelected == 'Keyframe24':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(24)
                self.int_numberOfKeyframe = 24
            elif self.str_keyframeSelected == 'Keyframe25':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(25)
                self.int_numberOfKeyframe = 25
            elif self.str_keyframeSelected == 'Keyframe26':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(26)
                self.int_numberOfKeyframe = 26
            elif self.str_keyframeSelected == 'Keyframe27':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(27)
                self.int_numberOfKeyframe = 27
            elif self.str_keyframeSelected == 'Keyframe28':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(28)
                self.int_numberOfKeyframe = 28
            elif self.str_keyframeSelected == 'Keyframe29':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(29)
                self.int_numberOfKeyframe = 29
            elif self.str_keyframeSelected == 'Keyframe30':
                #self.bool_activeKeyframe[14] = True
                self.CheckPreviousKeyframe(30)
                self.int_numberOfKeyframe = 30

            #self.text_atSub0_numberOfKeyframe.SetLabel(str(self.int_numberOfKeyframe))
            self.ui.numOfKeyframeStatus_label.setText(str(self.int_numberOfKeyframe))

        else:
            print "Unchecked"
            if self.str_keyframeSelected == 'Keyframe1':
                #self.bool_activeKeyframe[0] = False
                self.CheckNextKeyframe(1)
                self.int_numberOfKeyframe = 0
            elif self.str_keyframeSelected == 'Keyframe2':
                #self.bool_activeKeyframe[1] = False
                self.CheckNextKeyframe(2)
                self.int_numberOfKeyframe = 1
            elif self.str_keyframeSelected == 'Keyframe3':
                #self.bool_activeKeyframe[2] = False
                self.CheckNextKeyframe(3)
                self.int_numberOfKeyframe = 2
            elif self.str_keyframeSelected == 'Keyframe4':
                #self.bool_activeKeyframe[3] = False
                self.CheckNextKeyframe(4)
                self.int_numberOfKeyframe = 3
            elif self.str_keyframeSelected == 'Keyframe5':
                #self.bool_activeKeyframe[4] = False
                self.CheckNextKeyframe(5)
                self.int_numberOfKeyframe = 4
            elif self.str_keyframeSelected == 'Keyframe6':
                #self.bool_activeKeyframe[5] = False
                self.CheckNextKeyframe(6)
                self.int_numberOfKeyframe = 5
            elif self.str_keyframeSelected == 'Keyframe7':
                #self.bool_activeKeyframe[6] = False
                self.CheckNextKeyframe(7)
                self.int_numberOfKeyframe = 6
            elif self.str_keyframeSelected == 'Keyframe8':
                #self.bool_activeKeyframe[7] = False
                self.CheckNextKeyframe(8)
                self.int_numberOfKeyframe = 7
            elif self.str_keyframeSelected == 'Keyframe9':
                #self.bool_activeKeyframe[8] = False
                self.CheckNextKeyframe(9)
                self.int_numberOfKeyframe = 8
            elif self.str_keyframeSelected == 'Keyframe10':
                #self.bool_activeKeyframe[9] = False
                self.CheckNextKeyframe(10)
                self.int_numberOfKeyframe = 9
            elif self.str_keyframeSelected == 'Keyframe11':
                #self.bool_activeKeyframe[10] = False
                self.CheckNextKeyframe(11)
                self.int_numberOfKeyframe = 10
            elif self.str_keyframeSelected == 'Keyframe12':
                #self.bool_activeKeyframe[11] = False
                self.CheckNextKeyframe(12)
                self.int_numberOfKeyframe = 11
            elif self.str_keyframeSelected == 'Keyframe13':
                #self.bool_activeKeyframe[12] = False
                self.CheckNextKeyframe(13)
                self.int_numberOfKeyframe = 12
            elif self.str_keyframeSelected == 'Keyframe14':
                #self.bool_activeKeyframe[13] = False
                self.CheckNextKeyframe(14)
                self.int_numberOfKeyframe = 13
            elif self.str_keyframeSelected == 'Keyframe15':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(15)
                self.int_numberOfKeyframe = 14
            elif self.str_keyframeSelected == 'Keyframe16':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(16)
                self.int_numberOfKeyframe = 15
            elif self.str_keyframeSelected == 'Keyframe17':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(17)
                self.int_numberOfKeyframe = 16
            elif self.str_keyframeSelected == 'Keyframe18':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(18)
                self.int_numberOfKeyframe = 17
            elif self.str_keyframeSelected == 'Keyframe19':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(19)
                self.int_numberOfKeyframe = 18
            elif self.str_keyframeSelected == 'Keyframe20':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(20)
                self.int_numberOfKeyframe = 19
            elif self.str_keyframeSelected == 'Keyframe21':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(21)
                self.int_numberOfKeyframe = 20
            elif self.str_keyframeSelected == 'Keyframe22':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(22)
                self.int_numberOfKeyframe = 21
            elif self.str_keyframeSelected == 'Keyframe23':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(23)
                self.int_numberOfKeyframe = 22
            elif self.str_keyframeSelected == 'Keyframe24':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(24)
                self.int_numberOfKeyframe = 23
            elif self.str_keyframeSelected == 'Keyframe25':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(25)
                self.int_numberOfKeyframe = 24
            elif self.str_keyframeSelected == 'Keyframe26':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(26)
                self.int_numberOfKeyframe = 25
            elif self.str_keyframeSelected == 'Keyframe27':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(27)
                self.int_numberOfKeyframe = 26
            elif self.str_keyframeSelected == 'Keyframe28':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(28)
                self.int_numberOfKeyframe = 27
            elif self.str_keyframeSelected == 'Keyframe29':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(29)
                self.int_numberOfKeyframe = 28
            elif self.str_keyframeSelected == 'Keyframe30':
                #self.bool_activeKeyframe[14] = False
                self.CheckNextKeyframe(30)
                self.int_numberOfKeyframe = 29

            self.ui.numOfKeyframeStatus_label.setText(str(self.int_numberOfKeyframe))

    def SetButtonAndSpinCtrlEnable(self):

        self.ui.setAll_pushButton.setEnabled(True)
        self.ui.setLAll_pushButton.setEnabled(True)
        self.ui.setRAll_pushButton.setEnabled(True)
        self.ui.setHAll_pushButton.setEnabled(True)

        self.ui.getAll_pushButton.setEnabled(True)
        self.ui.getLAll_pushButton.setEnabled(True)
        self.ui.getRAll_pushButton.setEnabled(True)
        self.ui.getHAll_pushButton.setEnabled(True)

        self.ui.disTAll_pushButton.setEnabled(True)
        self.ui.disTLAll_pushButton.setEnabled(True)
        self.ui.disTRAll_pushButton.setEnabled(True)
        self.ui.disTHAll_pushButton.setEnabled(True)

        self.ui.deleteKeyframe_pushButton.setEnabled(True)
        self.ui.duplicateKeyframe_pushButton.setEnabled(True)
        self.ui.previousSwitchKeyframe_pushButton.setEnabled(True)
        self.ui.nextSwitchKeyframe_pushButton.setEnabled(True)
        self.ui.play_pushButton.setEnabled(True)
        self.ui.playAll_Button.setEnabled(True)
        self.ui.setReady_Button.setEnabled(True)
        self.ui.setTime_pushButton.setEnabled(True)
        self.ui.setAll_pushButton.setEnabled(True)
        self.ui.keyframeTime_spinBox.setEnabled(True)

        self.ui.motor1Value_spinBox.setEnabled(True)
        self.ui.motor1value_dial.setEnabled(True)
        self.ui.motor1Set_pushButton.setEnabled(True)
        self.ui.motor1Get_pushButton.setEnabled(True)
        self.ui.motor1DisT_pushButton.setEnabled(True)

        self.ui.motor2Value_spinBox.setEnabled(True)
        self.ui.motor2value_dial.setEnabled(True)
        self.ui.motor2Set_pushButton.setEnabled(True)
        self.ui.motor2Get_pushButton.setEnabled(True)
        self.ui.motor2DisT_pushButton.setEnabled(True)

        self.ui.motor3Value_spinBox.setEnabled(True)
        self.ui.motor3value_dial.setEnabled(True)
        self.ui.motor3Set_pushButton.setEnabled(True)
        self.ui.motor3Get_pushButton.setEnabled(True)
        self.ui.motor3DisT_pushButton.setEnabled(True)

        self.ui.motor4Value_spinBox.setEnabled(True)
        self.ui.motor4value_dial.setEnabled(True)
        self.ui.motor4Set_pushButton.setEnabled(True)
        self.ui.motor4Get_pushButton.setEnabled(True)
        self.ui.motor4DisT_pushButton.setEnabled(True)

        self.ui.motor5Value_spinBox.setEnabled(True)
        self.ui.motor5value_dial.setEnabled(True)
        self.ui.motor5Set_pushButton.setEnabled(True)
        self.ui.motor5Get_pushButton.setEnabled(True)
        self.ui.motor5DisT_pushButton.setEnabled(True)

        self.ui.motor6Value_spinBox.setEnabled(True)
        self.ui.motor6value_dial.setEnabled(True)
        self.ui.motor6Set_pushButton.setEnabled(True)
        self.ui.motor6Get_pushButton.setEnabled(True)
        self.ui.motor6DisT_pushButton.setEnabled(True)

        self.ui.motor7Value_spinBox.setEnabled(True)
        self.ui.motor7value_dial.setEnabled(True)
        self.ui.motor7Set_pushButton.setEnabled(True)
        self.ui.motor7Get_pushButton.setEnabled(True)
        self.ui.motor7DisT_pushButton.setEnabled(True)

        self.ui.motor11Value_spinBox.setEnabled(True)
        self.ui.motor11value_dial.setEnabled(True)
        self.ui.motor11Set_pushButton.setEnabled(True)
        self.ui.motor11Get_pushButton.setEnabled(True)
        self.ui.motor11DisT_pushButton.setEnabled(True)

        self.ui.motor12Value_spinBox.setEnabled(True)
        self.ui.motor12value_dial.setEnabled(True)
        self.ui.motor12Set_pushButton.setEnabled(True)
        self.ui.motor12Get_pushButton.setEnabled(True)
        self.ui.motor12DisT_pushButton.setEnabled(True)

        self.ui.motor13Value_spinBox.setEnabled(True)
        self.ui.motor13value_dial.setEnabled(True)
        self.ui.motor13Set_pushButton.setEnabled(True)
        self.ui.motor13Get_pushButton.setEnabled(True)
        self.ui.motor13DisT_pushButton.setEnabled(True)

        self.ui.motor14Value_spinBox.setEnabled(True)
        self.ui.motor14value_dial.setEnabled(True)
        self.ui.motor14Set_pushButton.setEnabled(True)
        self.ui.motor14Get_pushButton.setEnabled(True)
        self.ui.motor14DisT_pushButton.setEnabled(True)

        self.ui.motor15Value_spinBox.setEnabled(True)
        self.ui.motor15value_dial.setEnabled(True)
        self.ui.motor15Set_pushButton.setEnabled(True)
        self.ui.motor15Get_pushButton.setEnabled(True)
        self.ui.motor15DisT_pushButton.setEnabled(True)

        self.ui.motor16Value_spinBox.setEnabled(True)
        self.ui.motor16value_dial.setEnabled(True)
        self.ui.motor16Set_pushButton.setEnabled(True)
        self.ui.motor16Get_pushButton.setEnabled(True)
        self.ui.motor16DisT_pushButton.setEnabled(True)

        self.ui.motor17Value_spinBox.setEnabled(True)
        self.ui.motor17value_dial.setEnabled(True)
        self.ui.motor17Set_pushButton.setEnabled(True)
        self.ui.motor17Get_pushButton.setEnabled(True)
        self.ui.motor17DisT_pushButton.setEnabled(True)

        self.ui.motor21Value_spinBox.setEnabled(True)
        self.ui.motor21value_dial.setEnabled(True)
        self.ui.motor21Set_pushButton.setEnabled(True)
        self.ui.motor21Get_pushButton.setEnabled(True)
        self.ui.motor21DisT_pushButton.setEnabled(True)

        self.ui.motor22Value_spinBox.setEnabled(True)
        self.ui.motor22value_dial.setEnabled(True)
        self.ui.motor22Set_pushButton.setEnabled(True)
        self.ui.motor22Get_pushButton.setEnabled(True)
        self.ui.motor22DisT_pushButton.setEnabled(True)

        self.ui.motor23Value_spinBox.setEnabled(True)
        self.ui.motor23value_dial.setEnabled(True)
        self.ui.motor23Set_pushButton.setEnabled(True)
        self.ui.motor23Get_pushButton.setEnabled(True)
        self.ui.motor23DisT_pushButton.setEnabled(True)


    def SetButtonAndSpinCtrlDisable(self):

        self.ui.setAll_pushButton.setDisabled(True)
        self.ui.setLAll_pushButton.setDisabled(True)
        self.ui.setRAll_pushButton.setDisabled(True)
        self.ui.setHAll_pushButton.setDisabled(True)

        self.ui.getAll_pushButton.setDisabled(True)
        self.ui.getLAll_pushButton.setDisabled(True)
        self.ui.getRAll_pushButton.setDisabled(True)
        self.ui.getHAll_pushButton.setDisabled(True)

        self.ui.disTAll_pushButton.setDisabled(True)
        self.ui.disTLAll_pushButton.setDisabled(True)
        self.ui.disTRAll_pushButton.setDisabled(True)
        self.ui.disTHAll_pushButton.setDisabled(True)

        self.ui.deleteKeyframe_pushButton.setDisabled(True)
        self.ui.duplicateKeyframe_pushButton.setDisabled(True)
        self.ui.previousSwitchKeyframe_pushButton.setDisabled(True)
        self.ui.nextSwitchKeyframe_pushButton.setDisabled(True)
        self.ui.play_pushButton.setDisabled(True)
        self.ui.playAll_Button.setDisabled(True)
        self.ui.setReady_Button.setDisabled(True)
        self.ui.setTime_pushButton.setDisabled(True)
        self.ui.setAll_pushButton.setDisabled(True)
        self.ui.keyframeTime_spinBox.setDisabled(True)


        self.ui.motor1Value_spinBox.setDisabled(True)
        self.ui.motor1value_dial.setDisabled(True)
        self.ui.motor1Set_pushButton.setDisabled(True)
        self.ui.motor1Get_pushButton.setDisabled(True)
        self.ui.motor1DisT_pushButton.setDisabled(True)

        self.ui.motor2Value_spinBox.setDisabled(True)
        self.ui.motor2value_dial.setDisabled(True)
        self.ui.motor2Set_pushButton.setDisabled(True)
        self.ui.motor2Get_pushButton.setDisabled(True)
        self.ui.motor2DisT_pushButton.setDisabled(True)

        self.ui.motor3Value_spinBox.setDisabled(True)
        self.ui.motor3value_dial.setDisabled(True)
        self.ui.motor3Set_pushButton.setDisabled(True)
        self.ui.motor3Get_pushButton.setDisabled(True)
        self.ui.motor3DisT_pushButton.setDisabled(True)

        self.ui.motor4Value_spinBox.setDisabled(True)
        self.ui.motor4value_dial.setDisabled(True)
        self.ui.motor4Set_pushButton.setDisabled(True)
        self.ui.motor4Get_pushButton.setDisabled(True)
        self.ui.motor4DisT_pushButton.setDisabled(True)

        self.ui.motor5Value_spinBox.setDisabled(True)
        self.ui.motor5value_dial.setDisabled(True)
        self.ui.motor5Set_pushButton.setDisabled(True)
        self.ui.motor5Get_pushButton.setDisabled(True)
        self.ui.motor5DisT_pushButton.setDisabled(True)

        self.ui.motor6Value_spinBox.setDisabled(True)
        self.ui.motor6value_dial.setDisabled(True)
        self.ui.motor6Set_pushButton.setDisabled(True)
        self.ui.motor6Get_pushButton.setDisabled(True)
        self.ui.motor6DisT_pushButton.setDisabled(True)

        self.ui.motor7Value_spinBox.setDisabled(True)
        self.ui.motor7value_dial.setDisabled(True)
        self.ui.motor7Set_pushButton.setDisabled(True)
        self.ui.motor7Get_pushButton.setDisabled(True)
        self.ui.motor7DisT_pushButton.setDisabled(True)

        self.ui.motor11Value_spinBox.setDisabled(True)
        self.ui.motor11value_dial.setDisabled(True)
        self.ui.motor11Set_pushButton.setDisabled(True)
        self.ui.motor11Get_pushButton.setDisabled(True)
        self.ui.motor11DisT_pushButton.setDisabled(True)

        self.ui.motor12Value_spinBox.setDisabled(True)
        self.ui.motor12value_dial.setDisabled(True)
        self.ui.motor12Set_pushButton.setDisabled(True)
        self.ui.motor12Get_pushButton.setDisabled(True)
        self.ui.motor12DisT_pushButton.setDisabled(True)

        self.ui.motor13Value_spinBox.setDisabled(True)
        self.ui.motor13value_dial.setDisabled(True)
        self.ui.motor13Set_pushButton.setDisabled(True)
        self.ui.motor13Get_pushButton.setDisabled(True)
        self.ui.motor13DisT_pushButton.setDisabled(True)

        self.ui.motor14Value_spinBox.setDisabled(True)
        self.ui.motor14value_dial.setDisabled(True)
        self.ui.motor14Set_pushButton.setDisabled(True)
        self.ui.motor14Get_pushButton.setDisabled(True)
        self.ui.motor14DisT_pushButton.setDisabled(True)

        self.ui.motor15Value_spinBox.setDisabled(True)
        self.ui.motor15value_dial.setDisabled(True)
        self.ui.motor15Set_pushButton.setDisabled(True)
        self.ui.motor15Get_pushButton.setDisabled(True)
        self.ui.motor15DisT_pushButton.setDisabled(True)

        self.ui.motor16Value_spinBox.setDisabled(True)
        self.ui.motor16value_dial.setDisabled(True)
        self.ui.motor16Set_pushButton.setDisabled(True)
        self.ui.motor16Get_pushButton.setDisabled(True)
        self.ui.motor16DisT_pushButton.setDisabled(True)

        self.ui.motor17Value_spinBox.setDisabled(True)
        self.ui.motor17value_dial.setDisabled(True)
        self.ui.motor17Set_pushButton.setDisabled(True)
        self.ui.motor17Get_pushButton.setDisabled(True)
        self.ui.motor17DisT_pushButton.setDisabled(True)

        self.ui.motor21Value_spinBox.setDisabled(True)
        self.ui.motor21value_dial.setDisabled(True)
        self.ui.motor21Set_pushButton.setDisabled(True)
        self.ui.motor21Get_pushButton.setDisabled(True)
        self.ui.motor21DisT_pushButton.setDisabled(True)

        self.ui.motor22Value_spinBox.setDisabled(True)
        self.ui.motor22value_dial.setDisabled(True)
        self.ui.motor22Set_pushButton.setDisabled(True)
        self.ui.motor22Get_pushButton.setDisabled(True)
        self.ui.motor22DisT_pushButton.setDisabled(True)

        self.ui.motor23Value_spinBox.setDisabled(True)
        self.ui.motor23value_dial.setDisabled(True)
        self.ui.motor23Set_pushButton.setDisabled(True)
        self.ui.motor23Get_pushButton.setDisabled(True)
        self.ui.motor23DisT_pushButton.setDisabled(True)

    def GetOrderKeyframe(self):
        if self.str_keyframeSelected == 'Keyframe1':
            orderKeyframe = 1
        elif self.str_keyframeSelected == 'Keyframe2':
            orderKeyframe = 2
        elif self.str_keyframeSelected == 'Keyframe3':
            orderKeyframe = 3
        elif self.str_keyframeSelected == 'Keyframe4':
            orderKeyframe = 4
        elif self.str_keyframeSelected == 'Keyframe5':
            orderKeyframe = 5
        elif self.str_keyframeSelected == 'Keyframe6':
            orderKeyframe = 6
        elif self.str_keyframeSelected == 'Keyframe7':
            orderKeyframe = 7
        elif self.str_keyframeSelected == 'Keyframe8':
            orderKeyframe = 8
        elif self.str_keyframeSelected == 'Keyframe9':
            orderKeyframe = 9
        elif self.str_keyframeSelected == 'Keyframe10':
            orderKeyframe = 10
        elif self.str_keyframeSelected == 'Keyframe11':
            orderKeyframe = 11
        elif self.str_keyframeSelected == 'Keyframe12':
            orderKeyframe = 12
        elif self.str_keyframeSelected == 'Keyframe13':
            orderKeyframe = 13
        elif self.str_keyframeSelected == 'Keyframe14':
            orderKeyframe = 14
        elif self.str_keyframeSelected == 'Keyframe15':
            orderKeyframe = 15
        elif self.str_keyframeSelected == 'Keyframe16':
            orderKeyframe = 16
        elif self.str_keyframeSelected == 'Keyframe17':
            orderKeyframe = 17
        elif self.str_keyframeSelected == 'Keyframe18':
            orderKeyframe = 18
        elif self.str_keyframeSelected == 'Keyframe19':
            orderKeyframe = 19
        elif self.str_keyframeSelected == 'Keyframe20':
            orderKeyframe = 20
        elif self.str_keyframeSelected == 'Keyframe21':
            orderKeyframe = 21
        elif self.str_keyframeSelected == 'Keyframe22':
            orderKeyframe = 22
        elif self.str_keyframeSelected == 'Keyframe23':
            orderKeyframe = 23
        elif self.str_keyframeSelected == 'Keyframe24':
            orderKeyframe = 24
        elif self.str_keyframeSelected == 'Keyframe25':
            orderKeyframe = 25
        elif self.str_keyframeSelected == 'Keyframe26':
            orderKeyframe = 26
        elif self.str_keyframeSelected == 'Keyframe27':
            orderKeyframe = 27
        elif self.str_keyframeSelected == 'Keyframe28':
            orderKeyframe = 28
        elif self.str_keyframeSelected == 'Keyframe29':
            orderKeyframe = 29
        elif self.str_keyframeSelected == 'Keyframe30':
            orderKeyframe = 30


        return orderKeyframe


    def setReadMotorPacket(self,deviceID,Offset,Length):
        readPacket = [0xFF, 0xFF, deviceID, 0x04, 0x02, Offset, Length]
        checkSumOrdList = readPacket[2:]
        checkSumOrdListSum = sum(checkSumOrdList)
        computedCheckSum = ( ~(checkSumOrdListSum%256) ) % 256
        readPacket.append(computedCheckSum)
        #print readPacket
        str_packet = ''
        str_packet = str_packet.join([chr(c) for c in readPacket])
        self.serialDevice.write(str_packet)
        #print str_packet

    def getMotorQueryResponse( self, deviceID, Length ):

            queryData = 0
            responsePacketSize = Length + 6
            #responsePacket = readAllData(serialDevice)
            responsePacket = self.serialDevice.read(self.serialDevice.inWaiting())
            #responsePacket = serialDevice.read(responsePacketSize)
            #print 'Response packet = %s' % repr( [ ord(c) for c in responsePacket ] )
            # parse packet
            #print "Lenght of response:", len(responsePacket)
            if len(responsePacket) == responsePacketSize:
                                    #       finished reading
                    responseID = ord(responsePacket[2])
                    errorByte = ord(responsePacket[4])
                    #print deviceID, responseID, errorByte
                    if responseID == deviceID and errorByte == 0:
                            if Length == 2:
                                    queryData = ord(responsePacket[5]) + 256*ord(responsePacket[6])
                            elif Length == 1:
                                    queryData = ord(responsePacket[5])
                            #print "Return data:", queryData
                    else:
                            print "Error response:", responseID, errorByte
            return queryData

    def get(self,deviceID, address, Length):

            #serialDevice = serial.Serial(Port, Baud,8,'N',1,0,0,0,0)
            self.setReadMotorPacket(deviceID, address, Length)
            time.sleep(0.02)
            data = self.getMotorQueryResponse(deviceID, Length)
            #serialDevice.close()
            return data

    def getMotorPosition(self,id):
            data = self.get(id,36,2)
            return data

    def rxPacketConversion( self,value ):
            if value < 1024 and value >= 0:
                    hiByte = int(value/256)
                    loByte = value%256
            else:
                    print "rxPacketConversion: value out of range", value
            return loByte, hiByte

    def exPacketConversion( self,value ):
            if value < 4096 and value >= 0:
                    hiByte = int(value/256)
                    loByte = value%256
            else:
                    print "exPacketConversion: value out of range", value
            return loByte, hiByte

    def setDisableMotorTorque(self,deviceID):
            Offset = 0x18
            Packet = [0xFF, 0xFF, deviceID, 0x04, 0x03, Offset, 0x00]
            checkSumOrdList = Packet[2:]
            checkSumOrdListSum = sum(checkSumOrdList)
            computedCheckSum = ( ~(checkSumOrdListSum%256) ) % 256
            Packet.append(computedCheckSum)
            #print readPacket
            str_packet = ''
            str_packet = str_packet.join([chr(c) for c in Packet])
            self.serialDevice.write(str_packet)


    def setDeviceMoving( self,Port, Baud, deviceID, deviceType, goalPos, goalSpeed, maxTorque):


            #serialDevice = serial.Serial(Port, Baud,8,'N',1,0,0,0,0)
            # for our use offset should be 0x1E, length 6 byte
            # which are Goal position, Moving speed, Torque limit
            Offset = 0x1E
            Length = 6
            numberOfServo = 1
            packetLength = int((6+1)*numberOfServo+4)
            (goalSpeedL,goalSpeedH) = self.rxPacketConversion(goalSpeed)
            (maxTorqueL,maxTorqueH) = self.rxPacketConversion(maxTorque)

            syncWritePacket = [0xFF, 0xFF, 0xFE, packetLength, 0x83, Offset, Length]

            if deviceType == "Rx" or deviceType == "Ax":
                    (positionL, positionH) = self.rxPacketConversion(goalPos)
            elif deviceType == "Ex" or deviceType == "Mx":
                    (positionL, positionH) = self.exPacketConversion(goalPos)
            parameterList = [deviceID, positionL, positionH, goalSpeedL,goalSpeedH,maxTorqueL,maxTorqueH]
            for parameter in parameterList:
                    syncWritePacket.append(parameter)

            #print syncWritePacket

            checkSumOrdList = syncWritePacket[2:]
            checkSumOrdListSum = sum(checkSumOrdList)
            computedCheckSum = ( ~(checkSumOrdListSum%256) ) % 256
            syncWritePacket.append(computedCheckSum)

            #print syncWritePacket

            str_packet = ''
            str_packet = str_packet.join([chr(c) for c in syncWritePacket])
            self.serialDevice.write(str_packet)

            #print "Already set"

            #print str_packet
            #serialDevice.close()


    def InterpolateMotorValue(self,finish_value,start_value,finish_time,start_time,current_time):
        motor_value = int((finish_value - start_value)*(current_time-start_time)/(finish_time - start_time)+start_value)
        #print motor_value
        return motor_value

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = NamoMainWindow()


    MainWindow.show()
    sys.exit(app.exec_())

