import random
import time

class DegreeOfFreedom(object):
    def __init__(self, positive_output, negative_output, start_position=0, speed=1):
        assert 0 <= start_position <= 100
        self.positive_output = positive_output
        self.negative_output = negative_output
        self.speed = speed

        self.position = start_position
        self.sensors = []
        self.dependencys = []

    def tick(self, outputs):
        simulated_active_sensors = []

        #  todo check for pressure ... if outputs["OUT_PRESSURE"]:
        if outputs[self.positive_output] or outputs[self.negative_output]:
            # if up and down are active there is something very wrong!
            assert outputs[self.positive_output] != outputs[self.negative_output]

            is_up = outputs[self.positive_output]

            for degree_of_freedom, condition in self.dependencys:
                if not condition(self.position, degree_of_freedom.position, is_up):
                    break
            else:
                if is_up :
                    self.position += self.speed
                else:
                    self.position -= self.speed

                self.position = min(self.position, 100)
                self.position = max(self.position, 0)

        for sensor_name, condition in self.sensors:
            if condition(self.position):
                simulated_active_sensors.append(sensor_name)

        return simulated_active_sensors

    def add_sensor(self, sensor_name, condition):
        self.sensors.append((sensor_name, condition))

    def add_dependency(self, degree_of_freedom, condition):
        self.dependencys.append((degree_of_freedom, condition))

    def get_position(self):
        return self.position + random.randint(-2, 2)


class HayRotaryRake(object):
    def __init__(self):
        self.degrees_of_freedom = []

        self.spinner_left = DegreeOfFreedom("OUT_SPINNER_LEFT_UP", "OUT_SPINNER_LEFT_FLOAT", 90)
        self.spinner_left.add_sensor("SENS_SPINNER_LEFT_THIRD", lambda pos: pos > 33)
        self.spinner_left.add_sensor("SENS_SPINNER_LEFT_UP", lambda pos: pos > 98)
        self.degrees_of_freedom.append(self.spinner_left)

        self.spinner_right = DegreeOfFreedom("OUT_SPINNER_RIGHT_UP", "OUT_SPINNER_RIGHT_FLOAT", 90)
        self.spinner_right.add_sensor("SENS_SPINNER_RIGHT_THIRD", lambda pos: pos > 33)
        self.spinner_right.add_sensor("SENS_SPINNER_RIGHT_UP", lambda pos: pos > 98)
        self.degrees_of_freedom.append(self.spinner_right)

        self.spinner_back = DegreeOfFreedom("OUT_SPINNER_REAR_UP", "OUT_SPINNER_REAR_FLOAT", 100)
        self.spinner_back.add_sensor("SENS_SPINNER_REAR_UP", lambda pos: pos > 98)
        self.degrees_of_freedom.append(self.spinner_back)

        self.spinner_tele_left = DegreeOfFreedom("OUT_SPINNER_LEFT_TELE_OUT", "OUT_SPINNER_LEFT_TELE_IN", 0)
        self.spinner_tele_left.add_sensor("SENS_SPINNER_LEFT_TELE_OUT", lambda pos: pos > 98)
        self.spinner_tele_left.add_sensor("SENS_SPINNER_LEFT_TELE_IN", lambda pos: pos < 2)
        self.degrees_of_freedom.append(self.spinner_tele_left)

        self.spinner_tele_right = DegreeOfFreedom("OUT_SPINNER_RIGHT_TELE_OUT", "OUT_SPINNER_RIGHT_TELE_IN", 0)
        self.spinner_tele_right.add_sensor("SENS_SPINNER_RIGHT_TELE_OUT", lambda pos: pos > 98)
        self.spinner_tele_right.add_sensor("SENS_SPINNER_RIGHT_TELE_IN", lambda pos: pos < 2)
        self.degrees_of_freedom.append(self.spinner_tele_right)

        self.frame_lock = DegreeOfFreedom("OUT_FRAME_LOCK_UP", "OUT_FRAME_LOCK_DOWN", 0, speed=50)
        self.frame_lock.add_sensor("SENS_FRAME_LOCK_OPEN", lambda pos: pos > 98)
        self.frame_lock.add_sensor("SENS_FRAME_LOCK_CLOSED", lambda pos: pos < 2)
        self.degrees_of_freedom.append(self.frame_lock)

        self.frame = DegreeOfFreedom("OUT_FRAME_UP", "OUT_FRAME_DOWN", 100)
        self.frame.add_sensor("SENS_FRAME_UP", lambda pos: pos > 98)  # todo correct values
        self.frame.add_sensor("SENS_FRAME_MIDDLE", lambda pos: pos < 60)
        self.frame.add_sensor("SENS_FRAME_LOW", lambda pos: pos < 40)
        self.frame.add_sensor("SENS_FRAME_GROUND", lambda pos: pos < 2)
        #frame can only go down if framelock is open (>90)
        self.frame.add_dependency(self.frame_lock, lambda frame_pos, framelock_pos, is_up: is_up or framelock_pos > 90)
        self.degrees_of_freedom.append(self.frame)

        self.wheel_tele_left = DegreeOfFreedom("OUT_WEEL_TELE_LEFT_OUT", "OUT_WEEL_TELE_LEFT_IN", 0)
        self.wheel_tele_left.add_sensor("SENS_WEEL_TELE_LEFT_OUT", lambda pos: pos > 98)
        self.wheel_tele_left.add_sensor("SENS_WEEL_TELE_LEFT_IN", lambda pos: pos < 2)
        self.degrees_of_freedom.append(self.wheel_tele_left)

        self.wheel_tele_right = DegreeOfFreedom("OUT_WEEL_TELE_RIGHT_OUT", "OUT_WEEL_TELE_RIGHT_IN", 0)
        self.wheel_tele_right.add_sensor("SENS_WEEL_TELE_RIGHT_OUT", lambda pos: pos > 98)
        self.wheel_tele_right.add_sensor("SENS_WEEL_TELE_RIGHT_IN", lambda pos: pos < 2)
        self.degrees_of_freedom.append(self.wheel_tele_right)

        self.steer = DegreeOfFreedom("OUT_STEER_LEFT", "OUT_STEER_RIGHT", 0)
        self.steer.add_sensor("SENS_WEEL_TRACK_MIDDLE", lambda pos: 45 < pos < 55)
        self.degrees_of_freedom.append(self.steer)

    def tick(self, outputs):
        simulated_active_sensors = []
        print("\n------{}-------------------------------".format(time.time()))
        for d in self.degrees_of_freedom:
            simulated_active_sensors.extend(d.tick(outputs))
            print("{}: {}".format("_".join(d.positive_output.split("_")[:-1]), d.position))
        return simulated_active_sensors, self.degrees_of_freedom