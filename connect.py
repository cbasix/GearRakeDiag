import time
import serial
import struct

DIAG_ERROR = 1

DIAG_GET_SETTING = 10
DIAG_SET_SETTING = 11
DIAG_GET_ALL_SETTINGS = 12

DIAG_SIMULATE_MANUAL_INPUT = 21
DIAG_SIMULATE_MSG = 22
DIAG_SIMULATE_SENSOR_INPUT = 23

DIAG_GET_ALL_ERRORS = 32
DIAG_CLEAR_ALL_ERRORS = 34

DIAG_GET_ALL_IN_VALUES = 41
DIAG_GET_ALL_OUT_VALUES = 42

DIAG_SET_LOG_LISTENER = 50

DIAG_SET_IN_LISTENER = 60
DIAG_SET_OUT_LISTENER = 61

DIAG_SIMULATE_MANUAL_INPUT_MODE = 71
DIAG_SIMULATE_OUTPUT_MODE = 72
DIAG_SIMULATE_SENSOR_INPUT_MODE = 73

TYPE_SENSOR = 1
TYPE_MANUAL = 2
TYPE_MESSAGE = 3



class Connector:
    def __init__(self, port='/dev/ttyACM{i}', baudrate=9600):
        self.__input_observers = []
        self.__output_observers = []
        self.__log_observers = []
        self.__setting_observers = []
        self.__error_observers = []

        self.inputs = []
        self.outputs = []
        self.errors = []

        self.ser = None

        if "{i}" in port:
            for i in range(0, 15):
                try:

                    self.ser = serial.Serial(
                        port=port.replace("{i}", str(i)),
                        baudrate=baudrate,
                    )

                    print("Verbindung erfolgreich auf Port: " + port.replace("{i}", str(i)) + "\n")
                    break
                except:
                    print("Keine Verbindung auf Port: " + port.replace("{i}", str(i)) + "\n")
        else:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
            )

        if self.ser == None:
            print("No connected device found")

        if not self.ser.isOpen():
            self.ser.open()

        self.ser.setTimeout(300)

    def flush(self):
        self.ser.flush()

    def clear(self):
        i = self.ser.inWaiting()
        self.ser.read(i)

    def register_input_observer(self, input_observer):
        self.__input_observers.append(input_observer)

    def register_output_observer(self, output_observer):
        self.__output_observers.append(output_observer)

    def register_log_observer(self, log_observer):
        self.__log_observers.append(log_observer)

    def register_setting_observer(self, setting_observer):
        self.__setting_observers.append(setting_observer)

    def register_error_observer(self, error_observer):
        self.__error_observers.append(error_observer)

    def remove_input_observer(self, input_observer):
        self.__input_observers.remove(input_observer)

    def remove_output_observer(self, output_observer):
        self.__output_observers.remove(output_observer)

    def remove_log_observer(self, log_observer):
        self.__log_observers.remove(log_observer)

    def remove_setting_observer(self, setting_observer):
        self.__setting_observers.remove(setting_observer)

    def remove_error_observer(self, error_observer):
        self.__error_observers.remove(error_observer)

    def request_all_settings(self):
        self.send_frame(DIAG_GET_ALL_SETTINGS, 0, 0, 0, 0)

    def request_setting(self, setting_id):
        self.send_frame(DIAG_GET_SETTING, setting_id, 0, 0, 0)

    def write_setting(self, setting_id, value):
        self.send_frame(DIAG_SET_SETTING, setting_id, value, 0, 0)

    def request_all_errors(self):
        self.send_frame(DIAG_GET_ALL_ERRORS, 0, 0, 0, 0)

    def simulate_sensor_input(self, input_id, value):
        self.send_frame(DIAG_SIMULATE_SENSOR_INPUT, TYPE_SENSOR, input_id, value, 0)

    def simulate_manual_input(self, input_id, value):
        self.send_frame(DIAG_SIMULATE_MANUAL_INPUT, TYPE_MANUAL, input_id, value, 0)

    def simulate_message(self, input_id, value):
        self.send_frame(DIAG_SIMULATE_MSG, TYPE_MESSAGE, input_id, value, 0)


    def request_all_input_values(self):
        self.send_frame(DIAG_GET_ALL_IN_VALUES, 0, 0, 0, 0)

    def request_all_output_values(self):
        self.send_frame(DIAG_GET_ALL_OUT_VALUES, 0, 0, 0, 0)

    def request_log_active(self, active):
        self.send_frame(DIAG_SET_LOG_LISTENER, active, 0, 0, 0)


    def request_input_listener_active(self, active):
        self.send_frame(DIAG_SET_IN_LISTENER, active, 0, 0, 0)

    def request_output_listener_active(self, active):
        self.send_frame(DIAG_SET_OUT_LISTENER, active, 0, 0, 0)


    def request_simulate_manual_input_mode(self, active):
        self.send_frame(DIAG_SIMULATE_MANUAL_INPUT_MODE, active, 0, 0, 0)

    def request_simulate_sensor_input_mode(self, active):
        self.send_frame(DIAG_SIMULATE_SENSOR_INPUT_MODE, active, 0, 0, 0)

    def request_simulate_output_mode(self, active):
        self.send_frame(DIAG_SIMULATE_OUTPUT_MODE, active, 0, 0, 0)


    def send_frame(self, command, arg1, arg2, arg3, arg4):
        frame = struct.pack("!hhhhh", command, arg1, arg2, arg3, arg4)
        #0x1b is escape character! protocol is STX/ETX based so STX(=\x02) and ETX(=\03)must be escaped
        packed_frame = frame.replace(b'\x1b', b'\x1b\x1b')
        packed_frame = packed_frame.replace(b'\x02', b'\x1b\x02')
        packed_frame = packed_frame.replace(b'\x03', b'\x1b\x03')


        packed_frame = b'\x02' + packed_frame + b'\x03'  # Add start character and append termination Character

        print('OUT: '+str(packed_frame))

        self.ser.write(packed_frame)
        self.ser.flush()
        time.sleep(0.15)


        #wait for ack
        #ack = self.ser.read(1)
        #if ack != b'\x06':
        #    print('ERROR Waited for ACK but got: {}'.format(ack))
        #    self.ser.read(self.ser.inWaiting())
        #else:
        #    print('Got ACK: {}'.format(ack))



        # print("Ausgang: "+str(frame))

    def close(self):
        self.ser.close()

    def read_frames(self):
        while self.ser.inWaiting() >= 12:
            frame_complete = False
            escaped = False
            frame = b''

            while not frame_complete:
                got = self.ser.read(1)
                if got == b'\x1b' and not escaped:
                    escaped = True
                elif got == b'\x02' and not escaped:
                    frame = b''
                elif got == b'\x03' and not escaped:
                    frame_complete = True
                else:
                    frame = frame + got
                    escaped = False


            # print("Eingang: "+str(out))
            frame_ary = struct.unpack("!hhhhh", frame)
            command = frame_ary[0]
            arg1 = frame_ary[1]
            arg2 = frame_ary[2]
            arg3 = frame_ary[3]
            arg4 = frame_ary[4]


            if command == DIAG_SET_IN_LISTENER or command == DIAG_GET_ALL_IN_VALUES:
                input_id = arg1
                value = arg2

                for observer in self.__input_observers:
                    observer.on_input(input_id, value)

            elif command == DIAG_SET_OUT_LISTENER or command == DIAG_GET_ALL_OUT_VALUES:
                output_id = arg1
                value = arg2

                for observer in self.__output_observers:
                    observer.on_output(output_id, value)

            elif command == DIAG_SET_LOG_LISTENER:
                input_type = arg1
                input_id = arg2
                value = arg3
                additional_info = arg4

                for observer in self.__log_observers:
                    observer.on_log(input_type, input_id, value, additional_info)

            elif command == DIAG_GET_ALL_ERRORS:

                error_id = arg1
                input_id = arg2
                value = arg3
                additional_info = arg4

                for observer in self.__output_observers:
                    observer.on_log(error_id, input_id, value, additional_info)

            elif command == DIAG_GET_SETTING or command == DIAG_GET_ALL_SETTINGS:
                setting_id = arg1
                setting_value = arg2

                for observer in self.__setting_observers:
                    observer.on_setting(setting_id, setting_value)

            elif command == DIAG_ERROR:
                print('ERROR Response: {} {} {} {} {}'.format(command, arg1, arg2, arg3, arg4))
            else:
                print('Unknown Response: {} {} {} {} {}'.format(command, arg1, arg2, arg3, arg4))


