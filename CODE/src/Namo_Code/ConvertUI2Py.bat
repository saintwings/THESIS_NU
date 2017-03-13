@echo off
call pyuic4 -x SetPostureNamoUI.ui -o SetPostureNamoUI.py

pyuic5 -x SetPostureNamoUI_QT5.ui -o SetPostureNamoUI_QT5.py
