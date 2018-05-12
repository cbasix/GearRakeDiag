__author__ = 'cyberxix'
import time
import serial
import struct

if __name__ == "__main__":
    # configure the serial connections (the parameters differs on the device you are connecting to)
    i = 0
    done = False
    while(done == False and i < 15):
        try:
            ser = serial.Serial(
                port='/dev/ttyACM'+str(i),
                baudrate=9600,#115200, # 9600,
                #parity=serial.PARITY_ODD,
                #stopbits=serial.STOPBITS_TWO,
                #bytesize=serial.SEVENBITS
            )
            done = True
            print("/dev/ttyACM"+str(i))
        except:
            i += 1

    #ser.open()
    ser.isOpen()

    print('Enter your commands below.\r\nInsert "99" to leave the application.')

    while 1 :
        out = b''
        # get keyboard input
        commandd = int(input("Command>> "))
        if commandd != 0:
            arg1 = int(input("Arg1>> "))
            arg2 = int(input("Arg2>> "))
            arg3 = int(input("Arg3>> "))
            arg4 = int(input("Arg4>> "))
        else:
            arg1 = 0
            arg2 = 0
            arg3 = 0
            arg4 = 0
            # Python 3 users
        if commandd == 99:
            ser.close()
            exit()

        elif commandd != 0:
             # send the character to the device
            # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
            print(">> Sending: " + str(commandd) +" "+str(arg1) +" "+str(arg2) +" "+str(arg3) +" "+str(arg4) +" \n\r")
            frame = struct.pack("!hhhhh", commandd, arg1, arg2, arg3, arg4)
            ser.write(frame)
            print(str(frame))

            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(1)



        if ser.inWaiting() >= 10:
            out = ser.read(10)

            frame = struct.unpack("!hhhhh", out)
            commandd = frame[0]
            arg1 = frame[1]
            arg2 = frame[2]
            arg3 = frame[3]
            arg4 = frame[3]

            #if commandd != 0:
            print(">> Received: " + str(commandd) +" "+str(arg1) +" "+str(arg2) +" "+str(arg3) +" "+str(arg4) +" \n\r")

