__author__ = 'cyberxix'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GObject
import cairo
import config
from connect import Connector
import time
from simulator import HayRotaryRake
from gui_glade import draw_object

class FlowBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="SwDiag")
        self.set_border_width(10)
        self.set_default_size(600, 800)

        self.rake = HayRotaryRake()
        self.degrees_of_freedom = []
        self.outputs = {}
        self.inputs = {}

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(800, 400)
        self.drawing_area.connect('draw', drawSimulation, self.inputs)

        try:
            self.conn = Connector("/dev/ttyACM{i}", 9600)
            self.conn.register_input_observer(self)
            self.conn.register_log_observer(self)
            self.conn.register_output_observer(self)

            integer_id = GObject.timeout_add(50, self.read)

            GObject.timeout_add(10000, self.activate)
        except Exception as e:
            print(e)

        #self.set_geometry_hints(self.scroll_txt_log,-1,-1)
        self.show_all()

    def read(self):
        self.conn.read_frames()
        return True

    def activate(self):

        self.conn.request_log_active(True)
        self.conn.request_input_listener_active(True)
        self.conn.request_output_listener_active(True)

        self.conn.request_all_input_values()
        self.conn.request_simulate_manual_input_mode(True)
        self.conn.request_simulate_sensor_input_mode(True)
        self.conn.request_simulate_output_mode(True)

        self.conn.request_all_output_values()
        self.conn.request_all_input_values()

        integer_id = GObject.timeout_add(100, self.tick)
        return False

    def tick(self):

        self.conn.read_frames()
        simulated_active_sensors, self.degrees_of_freedom = self.rake.tick(self.outputs)
        for input_name, value in self.inputs.items():
            if input_name.startswith("SENS_"):
                if input_name in simulated_active_sensors and value == 0:
                    self.conn.simulate_sensor_input(config.get_input_id(input_name), 1)
                elif input_name not in simulated_active_sensors and value == 1:
                    self.conn.simulate_sensor_input(config.get_input_id(input_name), 0)
        time.sleep(0.05)
        self.conn.read_frames()

        # start redraw
        self.drawing_area.queue_draw()
        return True

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


def drawSimulation(w, cr, degrees_of_freedom):
    line = (
        (0.0, 0.0),
        (0.1, 0.1),
    )

    cr.set_line_width(0.005)
    cr.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    # cr.set_font_size(0.013)
    cr.set_font_size(0.018)

    draw_object(cr, 0.5, 0.5, line, *color_black)



if __name__ == '__main__':
    win = FlowBoxWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()