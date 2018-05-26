from test import SimpleSWTestCase
import config
import time
from simulator import HayRotaryRake


class SimulatiorTest(SimpleSWTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rake = HayRotaryRake()
        self.outputs = {}
        self.inputs = {}

    def on_output(self, output_id, value):
        name = config.get_output_name(output_id)
        self.outputs[name] = value
        print(str(time.time())+": <Output> "+name+" id: " + str(output_id) + " value: " + str(value))

    def on_input(self, input_id, value):
        name = config.get_input_name(input_id)
        self.inputs[name] = value
        print(str(time.time())+": <Input> "+name+" id: " + str(input_id) + " value: " + str(value))

    def on_log(self, input_type, input_id, value, additional_info):
        type_name = config.get_type_name(input_type)

        print(str(time.time())+": <Event> type: "+type_name+"(" + str(input_type) + ") id: " + str(input_id) + " value: " + str(
            value) + " additional_info: " + str(additional_info))

    def test_simulator(self):
        self.connector.request_all_output_values()
        for i in range(40):
            self.connector.read_frames()
            time.sleep(0.10)

        self.connector.request_all_input_values()
        for i in range(50):
            self.connector.read_frames()
            time.sleep(0.10)

        print("---- STARTING TICK ----")
        self.tick()

        #self.connector.simulate_manual_input(config.get_input_id("IN_SPINNER_LEFT_AUTO_THIRD"), 1)
        print("---- SIMULATE MOD FRAME BUTTON ----")
        self.connector.simulate_manual_input(config.get_input_id("IN_MOD_OU_FRAME"), 1)
        time.sleep(0.10)
        self.connector.simulate_manual_input(config.get_input_id("IN_MOD_OU_FRAME"), 0)
        time.sleep(0.10)
        print("---- SIMULATE MULTI DOWN ----")
        self.connector.simulate_manual_input(config.get_input_id("IN_AUTO_WORK"), 1)
        #self.connector.simulate_manual_input(config.get_input_id("IN_MULTI_DOWN"), 0)
        time.sleep(0.10)

        for i in range(500):
            self.tick()

    def tick(self):

        self.connector.read_frames()
        simulated_active_sensors, unused = self.rake.tick(self.outputs)
        for input_name, value in self.inputs.items():
            if input_name.startswith("SENS_"):
                if input_name in simulated_active_sensors and value == 0:
                    self.connector.simulate_sensor_input(config.get_input_id(input_name), 1)
                elif input_name not in simulated_active_sensors and value == 1:
                    self.connector.simulate_sensor_input(config.get_input_id(input_name), 0)
        time.sleep(0.05)
        self.connector.read_frames()



