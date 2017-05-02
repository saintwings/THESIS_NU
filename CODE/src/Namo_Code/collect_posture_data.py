from configobj import ConfigObj
import glob
import os

path = './Postures/posture_set_bye'

for filename in glob.glob(os.path.join(path, '*.ini')):
    print(filename)


    config = ConfigObj(filename)
    print(config['Keyframe_Time'])
    # self.int_numberOfKeyframe = int(config['Keyframe_Amount'])
    # self.ui.numOfKeyframeStatus_label.setText(str(self.int_numberOfKeyframe))
    #
    # for i in range(int(self.int_numberOfKeyframe)):
    #     self.bool_activeKeyframe[i] = True
    #     self.int_motorValue[i] = list(map(int, config['Keyframe_Value']['Keyframe_' + str(i)]))
    #
    #     self.int_time[i] = int(config['Keyframe_Time'][i])
    #
    # for i in range(int(self.int_numberOfKeyframe), 30):
    #     self.bool_activeKeyframe[i] = False

