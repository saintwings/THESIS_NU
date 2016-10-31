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

            if deviceType == "Rx":
                    (positionL, positionH) = self.rxPacketConversion(goalPos)
            elif deviceType == "Ex":
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

