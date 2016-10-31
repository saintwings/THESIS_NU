import serial.tools.list_ports
import plotly.plotly
# ports = list(serial.tools.list_ports.comports())
# for p in ports:
#     print p
#     print p[0]


try:

    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print p
        print p[0]
except ImportError:
    print"aaa"
    
if ports ==  None :
    print 'aaa'
    
else :
    print 'bbb'