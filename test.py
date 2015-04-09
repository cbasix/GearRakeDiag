from copy import deepcopy
from Cython.Compiler.MemoryView import empty_slice
from connect import Connector
import time

__author__ = 'cyberxix'
import unittest
import config

connector = None


class SimpleSWTestCase(unittest.TestCase):
    def setUp(self):
        global connector
        if connector is None:
            connector = Connector()
            time.sleep(5)
            connector.request_simulate_input_mode(True)
            connector.request_simulate_output_mode(True)
            time.sleep(3)
            connector.request_log_active(True)
            connector.request_input_listener_active(True)
            connector.request_output_listener_active(True)

        self.connector = connector  # Connector()

        self.connector.request_simulate_input_mode(True)
        self.connector.request_simulate_output_mode(True)

        time.sleep(0.5)
        self.connector.clear()

        self.connector.register_input_observer(self)
        self.connector.register_output_observer(self)
        self.connector.register_log_observer(self)

    def tearDown(self):
        self.connector.remove_input_observer(self)
        self.connector.remove_output_observer(self)
        self.connector.remove_log_observer(self)

        # self.connector.request_log_active(False)
        # self.connector.request_input_listener_active(False)
        # self.connector.request_output_listener_active(False)

        # self.connector.request_simulate_input_mode(False)
        # self.connector.request_simulate_output_mode(False)

        # self.connector.close()


class Tests(SimpleSWTestCase):

    spinner_left_test = [
        ["SEND", "IN_SPINNER_LEFT_UP", 1],
        ["RECEIVE", "OUT_SPINNER_LEFT_UP", 1],
        ["RECEIVE", "OUT_PRESSURE", 1],

        ["SEND", "IN_SPINNER_LEFT_UP", 0],
        ["RECEIVE", "OUT_SPINNER_LEFT_UP", 0],
        ["RECEIVE", "OUT_PRESSURE", 0],

        ["SEND", "IN_SPINNER_LEFT_FLOAT", 1],
        ["RECEIVE", "OUT_SPINNER_LEFT_FLOAT", 1],
        ["RECEIVE", "LED_SPINNER_LEFT_FLOAT", 1],
        ["SEND", "IN_SPINNER_LEFT_FLOAT", 0],
        # float must stay on
        ["SEND", "IN_SPINNER_LEFT_UP", 1],
        ["RECEIVE", "OUT_SPINNER_LEFT_UP", 1],
        ["RECEIVE", "OUT_SPINNER_LEFT_FLOAT", 0],
        ["RECEIVE", "LED_SPINNER_LEFT_FLOAT", 0],
        ["RECEIVE", "OUT_PRESSURE", 1],

        ["SEND", "IN_SPINNER_LEFT_UP", 0],
        ["RECEIVE", "OUT_SPINNER_LEFT_UP", 0],
        ["RECEIVE", "OUT_PRESSURE", 0],
    ]

    def test_spinner_left(self):
        print("\nSTART TEST test_spinner_left")
        self.start(self.spinner_left_test)

    spinner_right_test = [
        ["SEND", "IN_SPINNER_RIGHT_UP", 1],
        ["RECEIVE", "OUT_SPINNER_RIGHT_UP", 1],
        ["RECEIVE", "OUT_PRESSURE", 1],

        ["SEND", "IN_SPINNER_RIGHT_UP", 0],
        ["RECEIVE", "OUT_SPINNER_RIGHT_UP", 0],
        ["RECEIVE", "OUT_PRESSURE", 0],

        ["SEND", "IN_SPINNER_RIGHT_FLOAT", 1],
        ["RECEIVE", "OUT_SPINNER_RIGHT_FLOAT", 1],
        ["RECEIVE", "LED_SPINNER_RIGHT_FLOAT", 1],
        ["SEND", "IN_SPINNER_RIGHT_FLOAT", 0],
        # float must stay on
        ["SEND", "IN_SPINNER_RIGHT_UP", 1],
        ["RECEIVE", "OUT_SPINNER_RIGHT_UP", 1],
        ["RECEIVE", "OUT_SPINNER_RIGHT_FLOAT", 0],
        ["RECEIVE", "LED_SPINNER_RIGHT_FLOAT", 0],
        ["RECEIVE", "OUT_PRESSURE", 1],

        ["SEND", "IN_SPINNER_RIGHT_UP", 0],
        ["RECEIVE", "OUT_SPINNER_RIGHT_UP", 0],
        ["RECEIVE", "OUT_PRESSURE", 0],
    ]

    def test_spinner_right(self):
        print("\nSTART TEST test_spinner_right")
        self.start(self.spinner_right_test)

    spinner_both_up = [
        ["SEND", "IN_SPINNER_RIGHT_UP", 1],
        ["SEND", "IN_SPINNER_LEFT_UP", 1],

        ["RECEIVE", "OUT_PRESSURE", 1],
        ["RECEIVE", "OUT_SPINNER_RIGHT_UP", 1],
        ["RECEIVE", "OUT_SPINNER_LEFT_UP", 1],

        ["SEND", "SENS_SPINNER_LEFT_THIRD", 1],
        ["RECEIVE", "OUT_SPINNER_LEFT_UP", 0],

        ["SEND", "SENS_SPINNER_RIGHT_THIRD", 1],
        ["RECEIVE", "OUT_SPINNER_RIGHT_UP", 0],
        ["RECEIVE", "OUT_PRESSURE", 0],

    ]

    def test_spinner_both_up(self):
        # run normal test
        print("\nSTART TEST test_spinner_both_up")
        self.start(self.spinner_both_up, 0, 10)

    def test_spinner_both_up_top(self):
        #change test top sensors instead of third
        spinner_both_top = deepcopy(self.spinner_both_up)
        spinner_both_top[5] = ["SEND", "SENS_SPINNER_LEFT_UP", 1]
        spinner_both_top[7] = ["SEND", "SENS_SPINNER_RIGHT_UP", 1]
        #run changed test
        print("\nSTART TEST test_spinner_both_up_top")
        self.start(spinner_both_top, 5)

    def start(self, test_, error_count_max=0, empty_count_max=1):
        self.i = 0
        self.error_count = 0
        self.empty_count = 0
        self.test = test_
        self.error_count_max = error_count_max
        self.empty_count_max = empty_count_max
        self.continueListen = True

        while self.continueListen:
            if not self.process(None, None):
                self.continueListen = False
            self.connector.read_frames()

    def process(self, output_id, value):

        if self.continueListen:
            current_test = self.test[self.i]
            if current_test[0] == "SEND":
                print("NEXT MUST BE <Input> "+current_test[1]+" id: " + str(config.get_input_id(current_test[1])) + " value: " + str(current_test[2]))
                self.connector.simulate_manual_input(config.get_input_id(current_test[1]), current_test[2])
                self.i += 1
                self.error_count = 0
                self.empty_count = 0

            elif current_test[0] == "RECEIVE":

                if output_id is None:
                    time.sleep(1)
                    self.empty_count += 1
                    print("GOT NONE WHILE LOOP")
                elif output_id == config.get_output_id(current_test[1]) and value == current_test[2]:
                    self.i += 1
                    self.error_count = 0
                    self.empty_count = 0
                    print("GOT CORRECT <Output> "+current_test[1]+" id: " + str(config.get_output_id(current_test[1])) + " value: " + str(current_test[2]))

                else:
                    print("WAITING FOR <Output> "+current_test[1]+" id: " + str(config.get_output_id(current_test[1])) + " value: " + str(current_test[2]) +
                    "BUT GOT : <Output> "+config.get_output_name(output_id)+" id: " + str(output_id) + " value: " + str(value))

                    self.error_count += 1

            if self.error_count > self.error_count_max:
                print("Error count reached at step: " + str(self.i) + str(current_test))
                self.fail("Error count reached at step: " + str(self.i) + str(current_test))
                # return False
            if self.empty_count > self.empty_count_max:
                print("Empty count reached at step: " + str(self.i) + str(current_test))
                self.fail("Empty count reached at step: " + str(self.i) + str(current_test))
                # return False

            elif self.i == len(self.test)-1:
                return False

            else:
                return True
        else:
            return False

    def on_output(self, output_id, value):
        name = config.get_output_name(output_id)
        print("<Output> "+name+" id: " + str(output_id) + " value: " + str(value))
        if not self.process(output_id, value):
            self.continueListen = False

    def on_log(self, input_type, input_id, value, additional_info):
        type_name = config.get_type_name(input_type)

        print(" <Event> type: "+type_name+"(" + str(input_type) + ") id: " + str(input_id) + " value: " + str(
            value) + " additional_info: " + str(additional_info))

    def on_input(self, input_id, value):
        name = config.get_input_name(input_id)
        print("<Input> "+name+" id: " + str(input_id) + " value: " + str(value))

if __name__ == '__main__':
    unittest.main()