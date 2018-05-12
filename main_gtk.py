__author__ = 'cyberxix'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GObject
from config import config, get_input_name, get_output_name, get_type_name
from connect import Connector
from gui_glade import drawFront, drawTop, drawSide, drawInput
import random

class FlowBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="SwDiag")
        self.set_border_width(10)
        self.set_default_size(600, 800)
        self.inputs = [None for i in config["input"]]

        #self.grd_main = Gtk.Grid()
        #print(dir(self.grd_main))#.set_weight(1)
        #self.add(self.grd_main)

        notebook = Gtk.Notebook()
        self.add(notebook)
        # self.grd_main.attach(notebook, 0, 0, 18, 2)

        #header = Gtk.HeaderBar(title="Flow Box")
        #header.set_subtitle("Sample FlowBox app")
        #header.props.show_close_button = True

        #self.set_titlebar(header)

        # graphical views
        scroll_sensors = Gtk.ScrolledWindow()
        scroll_sensors.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll_sensors.set_hexpand(True)
        scroll_sensors.set_vexpand(True)

        self.flow_sensors = Gtk.FlowBox()
        self.flow_sensors.set_valign(Gtk.Align.START)
        self.flow_sensors.set_max_children_per_line(2)
        self.flow_sensors.set_selection_mode(Gtk.SelectionMode.NONE)

        # draw top
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(350, 350)
        self.drawing_area.connect('draw', drawTop, self.inputs)
        # button.connect("toggled", self.on_button_toggled, input_["id"])
        self.flow_sensors.add(self.drawing_area)

        #draw front
        self.drawing_area2 = Gtk.DrawingArea()
        self.drawing_area2.set_size_request(350, 350)
        self.drawing_area2.connect('draw', drawFront, self.inputs)
        # button.connect("toggled", self.on_button_toggled, input_["id"])
        self.flow_sensors.add(self.drawing_area2)

        #draw side
        self.drawing_area3 = Gtk.DrawingArea()
        self.drawing_area3.set_size_request(350, 350)
        self.drawing_area3.connect('draw', drawSide, self.inputs)
        # button.connect("toggled", self.on_button_toggled, input_["id"])
        self.flow_sensors.add(self.drawing_area3)

        # draw input
        self.drawing_area4 = Gtk.DrawingArea()
        self.drawing_area4.set_size_request(350, 350)
        self.drawing_area4.connect('draw', drawInput, self.inputs)
        # button.connect("toggled", self.on_button_toggled, input_["id"])
        self.flow_sensors.add(self.drawing_area4)


        scroll_sensors.add(self.flow_sensors)

        lbl_sim_input = Gtk.Label("Sensoren")
        notebook.append_page(scroll_sensors, lbl_sim_input)

        #Simulate input
        scroll_sim_input = Gtk.ScrolledWindow()
        scroll_sim_input.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll_sim_input.set_hexpand(True)
        scroll_sim_input.set_vexpand(True)

        self.flow_sim_input = Gtk.FlowBox()
        self.flow_sim_input.set_valign(Gtk.Align.START)
        self.flow_sim_input.set_max_children_per_line(20)
        self.flow_sim_input.set_selection_mode(Gtk.SelectionMode.NONE)

        self.create_flow_sim_input(self.flow_sim_input)
        scroll_sim_input.add(self.flow_sim_input)

        #lbl_sim_input = Gtk.Label("Eingabesimulation")
        #notebook.append_page(scroll_sim_input, lbl_sim_input)

        self.create_txt_log()
        lbl_log = Gtk.Label("Log")
        notebook.append_page(self.scroll_txt_log, lbl_log)

        try:
            self.conn = Connector("/dev/ttyACM{i}", 9600)
            self.conn.register_input_observer(self)
            self.conn.register_log_observer(self)
            self.conn.register_output_observer(self)

            integer_id = GObject.timeout_add(200, self.read)
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
        self.conn.request_simulate_manual_input_mode(False)
        self.conn.request_simulate_sensor_input_mode(False)
        self.conn.request_simulate_output_mode(False)

        self.conn.request_all_output_values()
        self.conn.request_all_input_values()

        return False

    def create_txt_log(self):
        self.scroll_txt_log = Gtk.ScrolledWindow()
        self.scroll_txt_log.set_hexpand(True)
        self.scroll_txt_log.set_vexpand(True)

        #self.scroll_txt_log.set_size_request(-1, 50)
        #self.grid.attach(scroll_txt_log, 0, 1, 3, 1)
        #parent.attach(self.scroll_txt_log, 0, 19, 25, 2)

        self.txt_log = Gtk.TextView()
        self.txt_log.set_editable(False)
        self.scroll_txt_log.add(self.txt_log)

        self.txt_log_buf = self.txt_log.get_buffer()
        self.txt_log_buf.set_text("Hallo und Wilkommen")


        self.tag_bold = self.txt_log_buf.create_tag("bold", weight=Pango.Weight.BOLD)
        self.tag_italic = self.txt_log_buf.create_tag("italic", style=Pango.Style.ITALIC)
        self.tag_underline = self.txt_log_buf.create_tag("underline", underline=Pango.Underline.SINGLE)
        self.tag_found = self.txt_log_buf.create_tag("found", background="yellow")

        self.tag_input = self.txt_log_buf.create_tag("input", foreground="green")
        self.tag_output = self.txt_log_buf.create_tag("output", foreground="blue")
        self.tag_error = self.txt_log_buf.create_tag("error", background="yellow")


    def txt_log_add(self, text, tag=None):
        begin_iter = self.txt_log_buf.get_start_iter()
        self.txt_log_buf.insert(begin_iter, text)
        end_iter = self.txt_log_buf.get_start_iter()
        self.txt_log_buf.apply_tag(tag, begin_iter, end_iter)


    def create_flow_sim_input(self, flowbox, manual=True):
        for input_ in config["input"]:
            if manual and input_["name"].startswith("IN_") or not manual and input_["name"].startswith("SENS_"):
                button = Gtk.ToggleButton(input_["description"])
                button.connect("toggled", self.on_button_toggled, input_["id"])

                flowbox.add(button)

    def on_button_toggled(self, button, input_id):
        if button.get_active():
            state = 1
        else:
            state = 0
        # manual and sensor inputs are using the same id set so it doesnt matter which simulate method is called
        self.conn.simulate_manual_input(input_id, state)
        print("Input (", input_id, ") was turned", state, "\n")

    def on_output(self, output_id, value):
        name = get_output_name(output_id)
        self.txt_log_add("<Output> "+name+" id: " + str(output_id) + " value: " + str(value) + "\n", self.tag_output)

        # existing_slaves = self.in_out.grid_slaves(row=output_id, column=0)
        # if(len(existing_slaves) ==  1):
        #     existing_slaves[0]["text"]="OUT id: " + str(output_id) + " value: " + str(value)
        # else:
        #     Label(self.in_out, text="OUT id: " + str(output_id) + " value: " + str(value)).grid(row=output_id, column=0)

    def on_input(self, input_id, value):
        self.inputs[input_id] = value
        self.flow_sensors.queue_draw()
        try:
            name = get_input_name(input_id)
        except Exception:
            name = "NoNameDefined"
        self.txt_log_add("<Input> "+name+" id: " + str(input_id) + " value: " + str(value) + "\n", self.tag_input)

        # existing_slaves = self.in_out.grid_slaves(row=input_id, column=1)
        # if(len(existing_slaves) ==  1):
        #     existing_slaves[0]["text"]="IN id: " + str(input_id) + " value: " + str(value)
        # else:
        #     Label(self.in_out, text="IN id: " + str(input_id) + " value: " + str(value)).grid(row=input_id, column=1)


    def on_log(self, input_type, input_id, value, additional_info):
        type_name = get_type_name(input_type)

        self.txt_log_add(" <Event> type: "+type_name+"(" + str(input_type) + ") id: " + str(input_id) + " value: " + str(
            value) + " additional_info: " + str(additional_info) + "\n", self.tag_italic)


win = FlowBoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()