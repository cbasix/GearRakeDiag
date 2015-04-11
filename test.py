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

    frame_down = [
        ["SEND", "SENS_FRAME_UP", 0],
        ["SENDMSG", "MSG_TSKPART_FRAME_DOWN", 1],
        # short up
        ["RECEIVE", "OUT_FRAME_UP", 1],
        ["RECEIVE", "OUT_PRESSURE", 1],
        ["RECEIVE", "OUT_FRAME_UP", 0],
        ["RECEIVE", "OUT_PRESSURE", 0],


        # open framelock
        ["RECEIVE", "OUT_FRAME_LOCK_UP", 1],
        ["RECEIVE", "OUT_PRESSURE", 1],
        ["SEND", "SENS_FRAME_LOCK_OPEN", 1],
        ["RECEIVE", "OUT_FRAME_LOCK_UP", 0],


        # frame down
        ["RECEIVE", "OUT_FRAME_DOWN", 1],
        ["WAIT", "", 3],
        ["SENDMSG", "MSG_TSKPART_FRAME_DOWN", 0],
        ["RECEIVE", "OUT_FRAME_DOWN", 0],


        # framelock close
        ["RECEIVE", "OUT_FRAME_LOCK_DOWN", 1],
        ["SEND", "SENS_FRAME_LOCK_OPEN", 0],
        ["SEND", "SENS_FRAME_LOCK_CLOSED", 1],
        ["RECEIVE", "OUT_FRAME_LOCK_DOWN", 0],
        ["RECEIVE", "OUT_PRESSURE", 0],

    ]

    def test_frame_down(self):
        print("\nSTART TEST frame_down")
        self.start(self.frame_down, 2, 5)

    auto_work_init_v1 = [
        # both weelteles already out
        ["SEND", "SENS_WEEL_TELE_RIGHT_OUT", 1],
        ["SEND", "SENS_WEEL_TELE_LEFT_OUT", 1],
    ]
    auto_work_init_v2 = [
        ["SEND", "SENS_WEEL_TELE_RIGHT_OUT", 0],
        ["SEND", "SENS_WEEL_TELE_LEFT_OUT", 1],
    ]
    auto_work_init_v3 = [
        ["SEND", "SENS_WEEL_TELE_RIGHT_OUT", 1],
        ["SEND", "SENS_WEEL_TELE_LEFT_OUT", 0],
    ]
    auto_work_init_v4 = [
        ["SEND", "SENS_WEEL_TELE_RIGHT_OUT", 0],
        ["SEND", "SENS_WEEL_TELE_LEFT_OUT", 0],
    ]

    auto_work_start = [
        ["SEND", "IN_AUTO_WORK", 1],
        ["WAIT", "", 6],
        ["SEND", "IN_AUTO_WORK", 0],

        ["RECEIVE", "LED_AUTO_WORK", 1],

    ]

    auto_work_weel_tele_v1 = [
    ]

    auto_work_weel_tele_v234 = [
        ["RECEIVE", "OUT_PRESSURE", 1],
        ["RECEIVE", "OUT_FRAME_UP", 1],
        ["RECEIVE", "OUT_PRESSURE", 0],
        ["RECEIVE", "OUT_FRAME_UP", 0],

        ["RECEIVE", "OUT_FRAME_LOCK_UP", 1],
        ["SEND", "SENS_FRAME_LOCK_CLOSED", 0],
        ["RECEIVE", "LED_FRAME_LOCK", 1],
        ["SEND", "SENS_FRAME_LOCK_OPEN", 1],
        ["RECEIVE", "OUT_FRAME_LOCK_UP", 0],

        ["RECEIVE", "OUT_FRAME_DOWN", 1],
        ["SEND", "SENS_FRAME_GROUND", 1],
        ["RECEIVE", "OUT_FRAME_DOWN", 0],

        ["RECEIVE", "OUT_FRAME_LOCK_DOWN", 1],
        ["SEND", "SENS_FRAME_LOCK_OPEN", 0],
        ["SEND", "SENS_FRAME_LOCK_CLOSED", 1],
        ["RECEIVE", "LED_FRAME_LOCK", 0],
    ]

    auto_work_weel_tele_left_v34 = [
        ["RECEIVE", "OUT_WEEL_TELE_LEFT_OUT", 1],
        ["SEND", "SENS_WEEL_TELE_LEFT_OUT", 0],
        ["SEND", "SENS_WEEL_TELE_LEFT_IN", 1],
        ["RECEIVE", "OUT_WEEL_TELE_LEFT_OUT", 0],
    ]

    auto_work_weel_tele_right_v24 = [
        ["RECEIVE", "OUT_WEEL_TELE_LEFT_OUT", 1],
        ["SEND", "SENS_WEEL_TELE_LEFT_OUT", 0],
        ["SEND", "SENS_WEEL_TELE_LEFT_IN", 1],
        ["RECEIVE", "OUT_WEEL_TELE_LEFT_OUT", 0],
    ]

    auto_work_up_v234 = [
        ["RECEIVE", "OUT_FRAME_UP", 1],
        ["SEND", "SENS_FRAME_UP", 0],
        ["RECEIVE", "OUT_FRAME_UP", 0],

        ["RECEIVE", "OUT_SPINNER_REAR_UP", 1],
        ["RECEIVE", "OUT_SPINNER_REAR_UP", 0],
        ["RECEIVE", "OUT_SPINNER_REAR_DOWN", 1],
        ["RECEIVE", "OUT_SPINNER_REAR_DOWN", 0],
    ]
    
    auto_work_init_l1 = [
        # top INIT SENS
        ["SEND", "SENS_SPINNER_LEFT_UP", 1],
        ["SEND", "SENS_SPINNER_LEFT_THIRD", 1],
        ["SEND", "SENS_SPINNER_LEFT_TELE_IN", 1],
    ]
    
    auto_work_init_l2 = [
        # between up and third INIT SENS
        ["SEND", "SENS_SPINNER_LEFT_UP", 0],
        ["SEND", "SENS_SPINNER_LEFT_THIRD", 1],
        ["SEND", "SENS_SPINNER_LEFT_TELE_IN", 1],
    ]
    
    auto_work_third_l2 = [
        # go to third
        ["RECEIVE", "OUT_SPINNER_LEFT_DOWN", 1],
        ["SEND", "SENS_SPINNER_LEFT_THIRD", 0],
        ["RECEIVE", "OUT_SPINNER_LEFT_DOWN", 0],

        # tele left out
        ["RECEIVE", "OUT_SPINNER_LEFT_TELE_OUT", 1],
        ["SEND", "SENS_SPINNER_LEFT_TELE_IN", 0],
        ["SEND", "SENS_SPINNER_LEFT_TELE_OUT", 1],
        ["RECEIVE", "OUT_SPINNER_LEFT_TELE_OUT", 0],
    ]
    
    auto_work_init_l3 = [
        # between bottom and third INIT SENS
        ["SEND", "SENS_SPINNER_LEFT_UP", 0],
        ["SEND", "SENS_SPINNER_LEFT_THIRD", 0],
    ]
    
    auto_work_third_l3 = [
        # go to third
        ["RECEIVE", "OUT_SPINNER_LEFT_UP", 1],
        ["SEND", "SENS_SPINNER_LEFT_THIRD", 1],
        ["RECEIVE", "OUT_SPINNER_LEFT_UP", 0],

         # tele left out
        ["RECEIVE", "OUT_SPINNER_LEFT_TELE_OUT", 1],
        ["SEND", "SENS_SPINNER_LEFT_TELE_IN", 0],
        ["SEND", "SENS_SPINNER_LEFT_TELE_OUT", 1],
        ["RECEIVE", "OUT_SPINNER_LEFT_TELE_OUT", 0],
    ]
    
    auto_work_init_r1 = [
        # top INIT SENS
        ["SEND", "SENS_SPINNER_RIGHT_UP", 1],
        ["SEND", "SENS_SPINNER_RIGHT_THIRD", 1],
        ["SEND", "SENS_SPINNER_RIGHT_TELE_IN", 1],
    ]
    
    auto_work_init_r2 = [
        # between up and third INIT SENS
        ["SEND", "SENS_SPINNER_RIGHT_UP", 0],
        ["SEND", "SENS_SPINNER_RIGHT_THIRD", 1],
        ["SEND", "SENS_SPINNER_RIGHT_TELE_IN", 1],
    ]
    
    auto_work_third_r2 = [
        # go to third
        ["RECEIVE", "OUT_SPINNER_RIGHT_DOWN", 1],
        ["SEND", "SENS_SPINNER_RIGHT_THIRD", 0],
        ["RECEIVE", "OUT_SPINNER_RIGHT_DOWN", 0],

        # tele RIGHT out
        ["RECEIVE", "OUT_SPINNER_RIGHT_TELE_OUT", 1],
        ["SEND", "SENS_SPINNER_RIGHT_TELE_IN", 0],
        ["SEND", "SENS_SPINNER_RIGHT_TELE_OUT", 1],
        ["RECEIVE", "OUT_SPINNER_RIGHT_TELE_OUT", 0],
    ]
    
    auto_work_init_r3 = [
        # between bottom and third INIT SENS
        ["SEND", "SENS_SPINNER_RIGHT_UP", 0],
        ["SEND", "SENS_SPINNER_RIGHT_THIRD", 0],
    ]
    
    auto_work_third_r3 = [
        # go to third
        ["RECEIVE", "OUT_SPINNER_RIGHT_UP", 1],
        ["SEND", "SENS_SPINNER_RIGHT_THIRD", 1],
        ["RECEIVE", "OUT_SPINNER_RIGHT_UP", 0],

         # tele RIGHT out
        ["RECEIVE", "OUT_SPINNER_RIGHT_TELE_OUT", 1],
        ["SEND", "SENS_SPINNER_RIGHT_TELE_IN", 0],
        ["SEND", "SENS_SPINNER_RIGHT_TELE_OUT", 1],
        ["RECEIVE", "OUT_SPINNER_RIGHT_TELE_OUT", 0],
    ]

    auto_work_end = [
        # END
        ["RECEIVE", "LED_AUTO_WORK", 0],
        # Really? Why?
        ["RECEIVE", "OUT_FRAME_LOCK_DOWN", 0],
    ]

    def test_x_auto_1(self):
        # build test array  version (all done)
        local_test = self.auto_work_init_v1[:]
        local_test = self.combine_append(local_test, self.auto_work_init_l1)
        local_test = self.combine_append(local_test, self.auto_work_init_r1)
        local_test = self.combine_append(local_test, self.auto_work_up_v234)
        local_test = self.combine_append(local_test, self.auto_work_start)
        local_test = self.combine_append(local_test, self.auto_work_end)
        
        print("\nSTART TEST auto work 1")
        print(str(local_test))
        self.start(local_test, 3, 5, True)

    def test_x_auto_2(self):
        # build test array  version (v2 l1 r1)
        local_test = self.auto_work_init_v2[:]
        local_test = self.combine_append(local_test, self.auto_work_init_l1)
        local_test = self.combine_append(local_test, self.auto_work_init_r1)
        local_test = self.combine_append(local_test, self.auto_work_start)
        local_test = self.combine_append(local_test, self.auto_work_weel_tele_v234)
        local_test = self.combine_append(local_test, self.auto_work_weel_tele_right_v24)
        local_test = self.combine_append(local_test, self.auto_work_up_v234)
        local_test = self.combine_append(local_test, self.auto_work_end)

        print("\nSTART TEST auto work 2")
        print(str(local_test))
        self.start(local_test, 3, 5, True)


    def test_w_auto_simple(self):
        # build test array  version (v2 l1 r1)
        local_test = [
            # alles fertig außer rahmen und hinterer schwader
            ["SEND", "SENS_SPINNER_RIGHT_UP", 1],
            ["SEND", "SENS_SPINNER_LEFT_UP", 1],
            ["SEND", "SENS_WEEL_TELE_RIGHT_OUT", 1],
            ["SEND", "SENS_WEEL_TELE_LEFT_OUT", 1],
            ["SEND", "SENS_FRAME_UP", 0],

            ["SEND", "IN_AUTO_WORK", 1],
            ["WAIT", "", 5.1],
            ["RECEIVE", "LED_AUTO_WORK", 1],

            ["RECEIVE", "OUT_FRAME_UP", 1],
            ["SEND", "SENS_FRAME_UP", 1],
            ["RECEIVE", "OUT_FRAME_UP", 0],

            ["RECEIVE", "OUT_SPINNER_REAR_FLOAT", 1],
            ["RECEIVE", "OUT_SPINNER_REAR_FLOAT", 0],
            ["RECEIVE", "OUT_SPINNER_REAR_UP", 1],
            ["RECEIVE", "OUT_SPINNER_REAR_UP", 0],

            ["RECEIVE", "LED_AUTO_WORK", 0],
        ]


        print("\nSTART TEST auto work simple")
        print(str(local_test))
        self.start(local_test, 15, 5, ignore_pressure=True)


    def combine_parallel(self, list1, list2):
        count = 0
        new_list = []
        for i in range(0, max(len(list1), len(list2))):
            if len(list1) >= i:
                new_list[count] = list1[i]
            if len(list2) >= i:
                new_list[count+1] = list2[i]
            count += 2
        return new_list

    def combine_append(self, list1, list2):
        new_list = []
        new_list.extend(list1)
        new_list.extend(list2)
        return new_list


    def start(self, test_, error_count_max=0, empty_count_max=1, ignore_pressure=False):
        self.i = 0
        self.error_count = 0
        self.empty_count = 0
        self.error_count_max = error_count_max
        self.empty_count_max = empty_count_max
        self.continueListen = True
        self.test = test_
        self.ignore_pressure = ignore_pressure

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

            if current_test[0] == "SENDMSG":
                print("NEXT MUST BE <MESSAGE> "+current_test[1]+" id: " + str(config.get_message_id(current_test[1])) + " value: " + str(current_test[2]))
                self.connector.simulate_message(config.get_message_id(current_test[1]), current_test[2])
                self.i += 1
                self.error_count = 0
                self.empty_count = 0

            elif current_test[0] == "RECEIVE":

                if output_id is None:
                    time.sleep(1)
                    self.empty_count += 1
                    print("STEP:"+str(self.i)+" GOT NONE WHILE LOOP")
                elif output_id == config.get_output_id(current_test[1]) and value == current_test[2]:
                    self.i += 1
                    self.error_count = 0
                    self.empty_count = 0
                    print("STEP:"+str(self.i)+" GOT CORRECT <Output> "+current_test[1]+" id: " + str(config.get_output_id(current_test[1])) + " value: " + str(current_test[2]))

                else:
                    print("STEP:"+str(self.i)+" WAITING FOR <Output> "+current_test[1]+" id: " + str(config.get_output_id(current_test[1])) + " value: " + str(current_test[2]) +
                    " BUT GOT : <Output> "+config.get_output_name(output_id)+" id: " + str(output_id) + " value: " + str(value))

                    self.error_count += 1
                    self.empty_count = 0

            elif current_test[0] == "WAIT":
                time.sleep(current_test[2])
                self.i += 1
                self.error_count = 0
                self.empty_count = 0

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
        if name == "OUT_PRESSURE" and self.ignore_pressure:
            return
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