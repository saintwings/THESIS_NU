from configobj import ConfigObj
import glob
import os

path = './Postures/posture_set_bye'

for filename in glob.glob(os.path.join(path, '*.ini')):
    print(filename)

