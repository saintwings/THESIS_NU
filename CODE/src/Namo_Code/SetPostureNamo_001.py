from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
from SetPostureNamoUI_QT5 import Ui_Form
import time
import serial
import sys
import serial.tools.list_ports
from configobj import ConfigObj


class NamoMainWindow(QtWidgets.QMainWindow,Ui_Form):

    def __init__(self,parent = None):
        super(NamoMainWindow, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitVariable()
        self.InitUI()
        self.SetButtonAndSpinCtrlDisable()

    ## work ##
    def InitVariable(self):
        self.int_keyframeSelected = 1
        self.bool_comportConnected = False
        self.int_numberOfKeyframe = 0
        self.str_fileName = None
        self.str_fileNameNumber = None
        self.str_comport = 'com3'
        self.str_baudrate = 115200
        self.int_keyframe = 0
        self.int_motorID = 0
        self.bool_activeKeyframe =[False for x in range (30)]

        ## load center ##
        file_center = open('./Postures/motor_center.txt', 'r')
        self.int_motorCenterValue = file_center.read()
        file_center.close()
        self.int_motorCenterValue = self.int_motorCenterValue.split('\n')
        for x in range (17):
            self.int_motorCenterValue[x] = int(self.int_motorCenterValue[x])

        ## load motor type ##
        file_type = open('./Postures/motor_type.txt', 'r')
        self.str_motorType = file_type.read()
        file_type.close()
        self.str_motorType = self.str_motorType.split('\n')

        ## initial motor value ##
        self.int_old_motorValue = [self.int_motorCenterValue[x] for x in range (17)]
        self.int_backup_motorValue = [self.int_motorCenterValue[x] for x in range (17)]
        self.int_motorValue = [[self.int_motorCenterValue[x] for x in range (17)] for y in range (30)]

        self.dic_motorIndexID = {'id1':0,'id2':1,'id3':2,'id4':3,'id5':4,'id6':5, 'id7':6,
                                 'id11':7,'id12':8,'id13':9,'id14':10,'id15':11,'id16':12,'id17':13,
                                 'id21':14,'id22':15,'id23':16}

        self.int_time = [20 for x in range (30)]

        self.int_list_id_motor_left = [1, 2, 3, 4, 5, 6, 7]
        self.int_list_id_motor_right = [11, 12, 13, 14, 15, 16, 17]
        self.int_list_id_motor_head = [21, 22, 23]
        self.int_list_id_motor_all = self.int_list_id_motor_left + self.int_list_id_motor_right + self.int_list_id_motor_head

    # work
    def InitUI(self):

        self.SetMotorCenterLabel()

        baudrateList = ['9600','115200','1000000']
        self.ui.baudrate_comboBox.addItems(baudrateList)

        postureList = ['Salute','Wai','Bye','SideInvite','p1','p2','p3','p4','p5','p6','p7','p8','p9','p10']
        postureNumber = [str(i) for i in range(1,11)]
        self.ui.posture_comboBox.addItems(postureList)
        self.ui.posture_number_comboBox.addItems(postureNumber)

        self.str_fileName = postureList[0]
        self.str_fileNameNumber = postureNumber[0]

        self.keyframeList = [str(i) for i in range(1,31)]

        self.ui.keyFrame_comboBox.addItems(self.keyframeList)

        self.ui.connectionStatus_label.setText("Status : Disconnect")

        self.ui.activeKeyframe_checkBox.clicked.connect(self.ActiveKeyframe_CheckBox)
        self.ui.keyFrame_comboBox.activated[str].connect(self.OnSelect_ComboboxKeyframe)
        self.ui.posture_comboBox.activated[str].connect(self.OnSelect_ComboboxPosture)
        self.ui.posture_number_comboBox.activated[str].connect(self.OnSelect_ComboboxPostureNumber)
        self.ui.comport_comboBox.activated[str].connect(self.OnSelect_ComboboxComport)
        self.ui.baudrate_comboBox.activated[str].connect(self.OnSelect_ComboboxBaudrate)

        self.ui.comport_comboBox.currentIndexChanged[str].connect(self.OnIndexChange_ComboboxComport)

        self.ui.connect_Button.clicked.connect(self.OnButton_connect)
        self.ui.loadPosture_pushButton.clicked.connect(self.OnButton_Load)
        self.ui.savePosture_pushButton.clicked.connect(self.OnButton_Save)
        self.ui.setReady_Button.clicked.connect(self.OnButton_ready)
        self.ui.playAll_Button.clicked.connect(self.OnButton_playAll)
        self.ui.setTime_pushButton.clicked.connect(self.OnButton_time)

        self.ui.play_pushButton.clicked.connect(self.OnButton_play)

        ## connect button Set ##
        self.ui.setAll_pushButton.clicked.connect(self.OnButton_setAll)
        self.ui.setLAll_pushButton.clicked.connect(self.OnButton_setLAll)
        self.ui.setRAll_pushButton.clicked.connect(self.OnButton_setRAll)
        self.ui.setHAll_pushButton.clicked.connect(self.OnButton_setHAll)

        for id in self.int_list_id_motor_all:
            eval("self.ui.motor{}Set_pushButton".format(id)).clicked.connect(lambda ignore, id=id: self.OnButton_Set(id))

        ## connect button get ##
        self.ui.getAll_pushButton.clicked.connect(self.OnButton_getAll)
        self.ui.getLAll_pushButton.clicked.connect(self.OnButton_getLAll)
        self.ui.getRAll_pushButton.clicked.connect(self.OnButton_getRAll)
        self.ui.getHAll_pushButton.clicked.connect(self.OnButton_getHAll)

        for id in self.int_list_id_motor_all:
            eval("self.ui.motor{}Get_pushButton".format(id)).clicked.connect(lambda ignore,  id=id: self.OnButton_Get(id))

        ## connect button distorque ##
        self.ui.disTAll_pushButton.clicked.connect(self.OnButton_DisableTorqueAll)
        self.ui.disTLAll_pushButton.clicked.connect(self.OnButton_DisableTorqueLAll)
        self.ui.disTRAll_pushButton.clicked.connect(self.OnButton_DisableTorqueRAll)
        self.ui.disTHAll_pushButton.clicked.connect(self.OnButton_DisableTorqueHAll)

        for id in self.int_list_id_motor_all:
            eval("self.ui.motor{}DisT_pushButton".format(id)).clicked.connect(lambda ignore,  id=id: self.OnButton_DisableTorque(id))

        self.ui.saveCenter_pushButton.clicked.connect(self.OnButton_SaveCenter)

        self.Search_Comport()

        self.ui.saveFile_pushButton.clicked.connect(self.OnButton_saveFile)
        self.ui.loadFile_pushButton.clicked.connect(self.OnButton_loadFile)


    def OnButton_saveFile(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', './Postures/',"OBJ (*.ini)")


        print(fname)
        print("save file")
        if fname[0]:
            config = ConfigObj()
            config.filename = fname[0]
            config['Posture_Name'] = fname[0]
            config['Keyframe_Amount'] = self.int_numberOfKeyframe
            config['Keyframe_Time'] = self.int_time[:self.int_numberOfKeyframe]
            config['Keyframe_Value'] = {}
            for i in range(self.int_numberOfKeyframe):
                config['Keyframe_Value']['Keyframe_' + str(i)] = self.int_motorValue[i]
            config.write()







        # print("Save")
        # print(self.str_fileName)
        # print(self.str_fileNameNumber)
        #
        # self.ui.fileName_label.setText(self.str_fileName + self.str_fileNameNumber)
        #
        # config = ConfigObj()
        # config.filename = './Postures/' + self.str_fileName + self.str_fileNameNumber + '.ini'
        # config['Posture_Name'] = self.str_fileName + self.str_fileNameNumber
        # config['Keyframe_Amount'] = self.int_numberOfKeyframe
        # config['Keyframe_Time'] = self.int_time[:self.int_numberOfKeyframe]
        # config['Keyframe_Value'] = {}
        # for i in range(self.int_numberOfKeyframe):
        #     config['Keyframe_Value']['Keyframe_' + str(i)] = self.int_motorValue[i]
        # config.write()


    def OnButton_loadFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './Postures',"OBJ (*.ini)")

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                print("file name", fname[0])
                config = ConfigObj(fname[0])
                self.ui.fileName_label.setText((fname[0].split("/")[len(fname[0].split("/"))-1]))

                self.int_numberOfKeyframe = int(config['Keyframe_Amount'])
                self.ui.numOfKeyframeStatus_label.setText(str(self.int_numberOfKeyframe))
                for i in range(int(self.int_numberOfKeyframe)):
                    self.bool_activeKeyframe[i] = True
                    self.int_motorValue[i] = list(map(int, config['Keyframe_Value']['Keyframe_' + str(i)]))

                    self.int_time[i] = int(config['Keyframe_Time'][i])

                for i in range(int(self.int_numberOfKeyframe), 30):
                    self.bool_activeKeyframe[i] = False

                self.SetValueKeyframeToShow()

    print("load file")

    def Search_Comport(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            self.ui.comport_comboBox.addItem(p[0])

    def OnIndexChange_ComboboxComport(self,text):
        self.str_comport = str(text)
        print(self.str_comport)

    def OnButton_Delete(self):
        #self.ui.keyFrame_comboBox.
        #self.int_backup_motorValue
        #self.int_keyframeSelected
        pass

    def OnButton_DisableTorqueAll(self):
        print("DisableTorqueAll")
        for id in self.int_list_id_motor_all:
            self.setDisableMotorTorque(id)
            time.sleep(0.015)

    def OnButton_DisableTorqueLAll(self):
        print("DisableTorque_L_All")
        for id in self.int_list_id_motor_left:
            self.setDisableMotorTorque(id)
            time.sleep(0.015)

    def OnButton_DisableTorqueRAll(self):
        print("DisableTorque_R_All")
        for id in self.int_list_id_motor_right:
            print(id)
            self.setDisableMotorTorque(id)
            time.sleep(0.015)

    def OnButton_DisableTorqueHAll(self):
        print("DisableTorque_H_All")
        for id in self.int_list_id_motor_head:
            self.setDisableMotorTorque(id)

    def OnButton_DisableTorque(self,id):
        print("DisableTorque ID " + str(id))
        self.setDisableMotorTorque(id)

    def OnButton_Get(self, id):
        print("get ID = " + str(id))
        eval("self.ui.motor{}Value_spinBox.setValue(self.getMotorPosition(id))".format(id))

    def OnButton_getAll(self):
        print("getAll")
        for id in self.int_list_id_motor_all:
            eval("self.ui.motor{}Value_spinBox.setValue(self.getMotorPosition(id))".format(id))
            time.sleep(0.015)

    def OnButton_getLAll(self):
        print("get_L_All")
        for id in self.int_list_id_motor_left:
            eval("self.ui.motor{}Value_spinBox.setValue(self.getMotorPosition(id))".format(id))
            time.sleep(0.015)

    def OnButton_getRAll(self):
        print("get_R_All")
        for id in self.int_list_id_motor_right:
            eval("self.ui.motor{}Value_spinBox.setValue(self.getMotorPosition(id))".format(id))
            time.sleep(0.015)

    def OnButton_getHAll(self):
        print("get_H_All")
        for id in self.int_list_id_motor_head:
            eval("self.ui.motor{}Value_spinBox.setValue(self.getMotorPosition(id))".format(id))
            time.sleep(0.015)

    def OnButton_Set(self, id):
        print("set id=",id)
        self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id' + str(id)]] = eval("self.ui.motor{}Value_spinBox.value()".format(id))
        self.setDeviceMoving( self.str_comport, self.str_baudrate, id, "Ex", self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id' + str(id)]], 1023, 1023)
        self.int_old_motorValue[self.dic_motorIndexID['id' + str(id)]] = self.int_motorValue[self.GetOrderKeyframe() - 1][self.dic_motorIndexID['id' + str(id)]]

    def OnButton_play(self):
        print("play...")

        self.SetButtonAndSpinCtrlDisable()

        for id in self.int_list_id_motor_all:
             self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))] = eval("self.ui.motor{}Value_spinBox.value()".format(id))

        time_start = time.time()
        time_finish = time_start + float(self.int_time[self.GetOrderKeyframe() - 1])/10
        in_time = True

        print(time_start)
        print(time_finish)
        print('Wait....')
        while in_time:
            time_current = time.time()
            if time_current >= time_finish:
                for id in self.int_list_id_motor_all:
                    self.setDeviceMoving(self.str_comport, self.str_baudrate, id, "Ex",self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))],1023, 1023)

                for id in self.int_list_id_motor_all:
                    self.int_old_motorValue[eval("self.dic_motorIndexID['id{}']".format(id))] = self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))]

                in_time = False

            else:
                for id in self.int_list_id_motor_all:
                    self.setDeviceMoving(self.str_comport, self.str_baudrate, id, "Ex", self.InterpolateMotorValue(self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))],self.int_old_motorValue[eval("self.dic_motorIndexID['id{}']".format(id))], time_finish, time_start, time_current),1023, 1023)

            time.sleep(0.015)

        print('Finished')
        self.SetButtonAndSpinCtrlEnable()

    def OnButton_setLAll(self):
        print("set L all")
        for id in self.int_list_id_motor_left:
            self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))] = eval("self.ui.motor{}Value_spinBox.value()".format(id))
            self.setDeviceMoving(self.str_comport, self.str_baudrate, id, "Ex",self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))], 1023, 1023)
            self.int_old_motorValue[eval("self.dic_motorIndexID['id{}']".format(id))] = self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))]
            time.sleep(0.015)

    def OnButton_setRAll(self):
        print("set R all")
        for id in self.int_list_id_motor_right:
            self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))] = eval("self.ui.motor{}Value_spinBox.value()".format(id))
            self.setDeviceMoving(self.str_comport, self.str_baudrate, id, "Ex",self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))], 1023, 1023)
            self.int_old_motorValue[eval("self.dic_motorIndexID['id{}']".format(id))] = self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))]
            time.sleep(0.015)

    def OnButton_setHAll(self):
        print("set H all")
        for id in self.int_list_id_motor_head:
            self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))] = eval("self.ui.motor{}Value_spinBox.value()".format(id))
            self.setDeviceMoving(self.str_comport, self.str_baudrate, id, "Ex",self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))], 1023, 1023)
            self.int_old_motorValue[eval("self.dic_motorIndexID['id{}']".format(id))] = self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))]
            time.sleep(0.015)

    def OnButton_setAll(self):
        print("set all")
        for id in self.int_list_id_motor_all:
            self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))] = eval("self.ui.motor{}Value_spinBox.value()".format(id))
            self.setDeviceMoving(self.str_comport, self.str_baudrate, id, "Ex",self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))], 1023, 1023)
            self.int_old_motorValue[eval("self.dic_motorIndexID['id{}']".format(id))] = self.int_motorValue[self.GetOrderKeyframe() - 1][eval("self.dic_motorIndexID['id{}']".format(id))]
            time.sleep(0.015)

    def OnButton_time(self):
        self.int_time[self.GetOrderKeyframe() - 1] = self.ui.keyframeTime_spinBox.value()
        print(self.int_time[self.GetOrderKeyframe() - 1])

    def OnButton_ready(self):
        print("ready...")

        self.SetButtonAndSpinCtrlDisable()

        if self.int_numberOfKeyframe == 0:
            print('Error!! Number of keyframe = 0 ')
        else:
            time_start = time.time()
            time_finish = time_start + float(self.int_time[0])/10
            in_time = True

            print(time_start)
            print(time_finish)
            print('Wait....')
            while in_time:
                time_current = time.time()
                if time_current >= time_finish:

                    for id in self.int_list_id_motor_all:
                        self.setDeviceMoving(self.str_comport, self.str_baudrate, id, "Ex",self.int_motorValue[0][eval("self.dic_motorIndexID['id{}']".format(id))], 200, 200)
                        self.int_old_motorValue[eval("self.dic_motorIndexID['id{}']".format(id))] = self.int_motorValue[0][eval("self.dic_motorIndexID['id{}']".format(id))]

                    in_time = False

                else:
                    for id in self.int_list_id_motor_all:
                        self.setDeviceMoving(self.str_comport, self.str_baudrate, id, "Ex", self.InterpolateMotorValue(self.int_motorValue[0][eval("self.dic_motorIndexID['id{}']".format(id))],self.int_old_motorValue[eval("self.dic_motorIndexID['id{}']".format(id))], time_finish, time_start,time_current), 200, 200)

                time.sleep(0.015)
            print('Finished')
        self.SetButtonAndSpinCtrlEnable()

    def OnButton_playAll(self):
        print("play all")
        self.SetButtonAndSpinCtrlDisable()

        if self.int_numberOfKeyframe == 0:
            print('Error!! Number of keyframe = 0 ')
        else:
            self.SetButtonAndSpinCtrlDisable()
            for x in range(self.int_numberOfKeyframe):
                time_start = time.time()
                time_finish = time_start + float(self.int_time[x])/10
                in_time = True

                print(time_start)
                print(time_finish)
                print('keyframe = '+ str(x+1))
                print('Time = '+ str(self.int_time[x]))
                print('Wait....')
                while in_time:
                    time_current = time.time()
                    if time_current >= time_finish:
                        for id in self.int_list_id_motor_all:
                            self.setDeviceMoving(self.str_comport, self.str_baudrate, id, "Ex",self.int_motorValue[x][eval("self.dic_motorIndexID['id{}']".format(id))], 1023, 1023)
                            self.int_old_motorValue[eval("self.dic_motorIndexID['id{}']".format(id))] = self.int_motorValue[x][eval("self.dic_motorIndexID['id{}']".format(id))]

                        in_time = False

                    else:
                        for id in self.int_list_id_motor_all:
                            self.setDeviceMoving(self.str_comport, self.str_baudrate, id, "Ex",self.InterpolateMotorValue(self.int_motorValue[x][eval("self.dic_motorIndexID['id{}']".format(id))],self.int_old_motorValue[eval("self.dic_motorIndexID['id{}']".format(id))], time_finish,time_start, time_current), 1023, 1023)

                    time.sleep(0.015)

                print('Finished')
        self.SetButtonAndSpinCtrlEnable()

    def OnButton_Load(self):
        print("Load")
        print(self.str_fileName)
        print(self.str_fileNameNumber)

        self.ui.fileName_label.setText(self.str_fileName + self.str_fileNameNumber + "[std pos]")

        filename = './Postures/' + str(self.str_fileName) + str(self.str_fileNameNumber)+ '.ini'

        config = ConfigObj(filename)
        self.int_numberOfKeyframe = int(config['Keyframe_Amount'])
        self.ui.numOfKeyframeStatus_label.setText(str(self.int_numberOfKeyframe))

        for i in range(int(self.int_numberOfKeyframe)):
            self.bool_activeKeyframe[i] = True
            self.int_motorValue[i] = list(map(int, config['Keyframe_Value']['Keyframe_' + str(i)]))

            self.int_time[i] = int(config['Keyframe_Time'][i])

        for i in range(int(self.int_numberOfKeyframe), 30):
            self.bool_activeKeyframe[i] = False

        self.SetValueKeyframeToShow()

    def OnButton_Save(self):
        print("Save")
        print(self.str_fileName)
        print(self.str_fileNameNumber)

        self.ui.fileName_label.setText(self.str_fileName + self.str_fileNameNumber)

        config = ConfigObj()
        config.filename = './Postures/' + self.str_fileName + self.str_fileNameNumber +'.ini'
        config['Posture_Name'] = self.str_fileName + self.str_fileNameNumber
        config['Keyframe_Amount'] = self.int_numberOfKeyframe
        config['Keyframe_Time'] = self.int_time[:self.int_numberOfKeyframe]
        config['Keyframe_Value'] = {}
        for i in range(self.int_numberOfKeyframe):
            config['Keyframe_Value']['Keyframe_' + str(i)] = self.int_motorValue[i]
        config.write()

    def SetMotorCenterLabel(self):
        for id in self.int_list_id_motor_all:
            eval("self.ui.motor{}center_label.setText(str(self.int_motorCenterValue[self.dic_motorIndexID['id'+str(id)]]))".format(id))

    def OnButton_SaveCenter(self):
        file_center = open('./Postures/motor_center.txt', 'w')
        for id in self.int_list_id_motor_all:
            self.int_motorCenterValue[eval("self.dic_motorIndexID['id{}']".format(id))] = eval("self.ui.motor{}Value_spinBox.value()".format(id))

        for y in range (17):
                file_center.write(str(self.int_motorCenterValue[y])+'\n')

        file_center.close()

        self.SetMotorCenterLabel()

    def OnSelect_ComboboxPosture(self,text):
        self.str_fileName = text
        print(self.str_fileName)

    def OnSelect_ComboboxPostureNumber(self,text):
        self.str_fileNameNumber = text
        print(self.str_fileNameNumber)

    # work 90%
    def OnButton_connect(self):
        print("connect clicked")
        if self.bool_comportConnected == False:
            self.bool_comportConnected = True
            self.serialDevice = serial.Serial(port = self.str_comport, baudrate = self.str_baudrate, timeout=0)
            self.ui.connectionStatus_label.setText("Status : Connected")
            self.ui.connect_Button.setText("Disconnect")
        else:
            self.bool_comportConnected = False
            self.serialDevice.close()
            self.ui.connectionStatus_label.setText("Status : Disconnected")
            self.ui.connect_Button.setText("Connect")

    def OnSelect_ComboboxComport(self,text):
        self.str_comport = str(text)
        print(self.str_comport)

    def OnSelect_ComboboxBaudrate(self,text):
        self.str_baudrate = str(text)
        print(self.str_baudrate)

    def OnSelect_ComboboxKeyframe(self,text):
        self.int_keyframeSelected = int(text)
        print(self.int_keyframeSelected)
        self.SetValueKeyframeToShow()

    # work 50%
    def SetValueKeyframeToShow(self):
        keyframe = self.int_keyframeSelected

        self.int_keyframeSelected = keyframe

        print("keyframe selected = ")
        print(self.int_keyframeSelected)
        print(type(keyframe))
        print(self.bool_activeKeyframe)

        if self.bool_activeKeyframe[keyframe-1] == True:
            self.ui.activeKeyframe_checkBox.setChecked(2)
            self.SetButtonAndSpinCtrlEnable()
            for id in self.int_list_id_motor_all:
                eval("self.ui.motor{}Value_spinBox".format(id)).setValue(self.int_motorValue[keyframe - 1][eval("self.dic_motorIndexID['id{}']".format(id))])

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
        print(self.ui.activeKeyframe_checkBox.checkState())

        if self.ui.activeKeyframe_checkBox.checkState() == 2:
            print("Checked")

            self.CheckPreviousKeyframe(self.int_keyframeSelected)
            self.int_numberOfKeyframe = self.int_keyframeSelected

            self.ui.numOfKeyframeStatus_label.setText(str(self.int_numberOfKeyframe))

        else:
            print("Unchecked")

            self.CheckNextKeyframe(self.int_keyframeSelected)
            self.int_numberOfKeyframe = (self.int_keyframeSelected - 1)

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

        for id in self.int_list_id_motor_all:
            eval("self.ui.motor{}Value_spinBox.setEnabled(True)".format(id))
            eval("self.ui.motor{}value_dial.setEnabled(True)".format(id))
            eval("self.ui.motor{}Set_pushButton.setEnabled(True)".format(id))
            eval("self.ui.motor{}Get_pushButton.setEnabled(True)".format(id))
            eval("self.ui.motor{}DisT_pushButton.setEnabled(True)".format(id))

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

        for id in self.int_list_id_motor_all:
            eval("self.ui.motor{}Value_spinBox.setDisabled(True)".format(id))
            eval("self.ui.motor{}value_dial.setDisabled(True)".format(id))
            eval("self.ui.motor{}Set_pushButton.setDisabled(True)".format(id))
            eval("self.ui.motor{}Get_pushButton.setDisabled(True)".format(id))
            eval("self.ui.motor{}DisT_pushButton.setDisabled(True)".format(id))

    def GetOrderKeyframe(self):
        for index, kf in enumerate(self.keyframeList):
            if self.int_keyframeSelected == int(kf):
                orderKeyframe = index+1
        return orderKeyframe


    def setReadMotorPacket(self,deviceID,Offset,Length):
        readPacket = [0xFF, 0xFF, deviceID, 0x04, 0x02, Offset, Length]
        checkSumOrdList = readPacket[2:]
        checkSumOrdListSum = sum(checkSumOrdList)
        computedCheckSum = ( ~(checkSumOrdListSum%256) ) % 256
        readPacket.append(computedCheckSum)
        self.serialDevice.write(readPacket)
        print(readPacket)

    def getMotorQueryResponse( self, deviceID, Length ):

            queryData = 0
            responsePacketSize = Length + 6
            responsePacket = self.serialDevice.read(self.serialDevice.inWaiting())

            if len(responsePacket) == responsePacketSize:

                    print("responsePacket=",responsePacket)

                    responseID = responsePacket[2]
                    errorByte = responsePacket[4]

                    ### python 3
                    if responseID == deviceID and errorByte == 0:
                        if Length == 2:
                            queryData = responsePacket[5] + 256 * responsePacket[6]
                        elif Length == 1:
                            queryData = responsePacket[5]
                            # print "Return data:", queryData
                    else:
                            print("Error response:", responseID, errorByte)
            print("queryData=", queryData)
            return queryData

    def get(self,deviceID, address, Length):

            self.setReadMotorPacket(deviceID, address, Length)
            time.sleep(0.02)
            data = self.getMotorQueryResponse(deviceID, Length)
            return data

    def getMotorPosition(self,id):
            data = self.get(id,36,2)
            return data

    def rxPacketConversion( self,value ):
            if value < 1024 and value >= 0:
                    hiByte = int(value/256)
                    loByte = value%256
            else:
                    print("rxPacketConversion: value out of range", value)
            return loByte, hiByte

    def exPacketConversion( self,value ):
            if value < 4096 and value >= 0:
                    hiByte = int(value/256)
                    loByte = value%256
            else:
                    print("exPacketConversion: value out of range", value)
            return loByte, hiByte

    def setDisableMotorTorque(self,deviceID):
            Offset = 0x18
            Packet = [0xFF, 0xFF, deviceID, 0x04, 0x03, Offset, 0x00]
            checkSumOrdList = Packet[2:]
            checkSumOrdListSum = sum(checkSumOrdList)
            computedCheckSum = ( ~(checkSumOrdListSum%256) ) % 256
            Packet.append(computedCheckSum)
            self.serialDevice.write(Packet)
            print(Packet)

    def setDeviceMoving( self,Port, Baud, deviceID, deviceType, goalPos, goalSpeed, maxTorque):

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


            checkSumOrdList = syncWritePacket[2:]
            checkSumOrdListSum = sum(checkSumOrdList)
            computedCheckSum = ( ~(checkSumOrdListSum%256) ) % 256
            syncWritePacket.append(computedCheckSum)
            self.serialDevice.write(syncWritePacket)


            print(syncWritePacket,"goalPos =",goalPos)

    def InterpolateMotorValue(self,finish_value,start_value,finish_time,start_time,current_time):
        motor_value = int((finish_value - start_value)*(current_time-start_time)/(finish_time - start_time)+start_value)
        return motor_value

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = NamoMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())

