__author__ = 'cyberxix'
# from tkinter import *
# import ttk
from connect import Connector
import configparser
from config import config


class App:
    def __init__(self, master):
        self.style = ttk.Style()

        self.frame = PanedWindow(master)
        print(self.style.theme_names())
        self.style.theme_use('clam')

        self.frame.pack(fill=BOTH, expand=1)

        self.button = Button(
            self.frame, text="", fg="red", command=self.frame.quit, width=15
        )
        self.frame.add(self.button)

        self.hi_there = Button(self.frame, text="Hello", command=self.say_hi)
        self.frame.add(self.hi_there)
        self.hi_there2 = Button(self.frame, text="Hello2", command=self.say_hi)
        self.frame.add(self.hi_there2)

    def say_hi(self):
        print("hi there, everyone!")


class Gui:
    def __init__(self):
        # theme stuff
        self.root = Tk()
        self.root.title("SwDiag")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.buildMainWindow()
        self.buildSimulateInput()

        self.conn = None
        #try:
        i = 0;
        done = False
        while done == False and i < 15:
            try:
                port = '/dev/ttyACM' + str(i)
                self.conn = Connector(port, 9600)  #read from config
                done = True
                print("/dev/ttyACM" + str(i))
                self.log_txt.insert("1.0", "SUCCESS opening serial port: " + port + "\n")
            except:
                self.log_txt.insert("1.0", "Error opening serial port: " + port + "\n")
                i += 1

        self.conn.register_input_observer(self)
        self.conn.register_log_observer(self)
        self.conn.register_output_observer(self)

        self.conn.request_log_active(True)
        self.conn.request_input_listener_active(True)
        self.conn.request_output_listener_active(True)
        self.conn.request_all_input_values()
        self.conn.request_all_output_values()
        #except:
        #    self.log_txt.insert("1.0","Error opening serial port: "+'/dev/ttyACM0'+"\n")

        self.timer()
        self.root.mainloop()

    def buildMainWindow(self):
        # init up-down panned window
        self.frameset_ud = ttk.PanedWindow(self.root)
        self.frameset_lr = ttk.PanedWindow(self.frameset_ud, orient=HORIZONTAL)

        self.in_out = Frame(self.frameset_ud, width=20)
        #self.in_out_scroll = ttk.Scrollbar( self.frameset_ud, orient=VERTICAL, command=self.in_out_list.yview)
        self.tabbed = ttk.Notebook(self.frameset_ud, height=600, width=800)

        #self.frm_log = ttk.Frame(self.frameset_ud)
        self.log_txt = Text(self.frameset_ud, height=10)
        #self.log_scroll = ttk.Scrollbar( self.frameset_ud, orient=VERTICAL, command=self.log_txt.yview)

        #adding them together
        self.frameset_ud.pack(fill=BOTH, expand=1)
        self.frameset_ud.add(self.frameset_lr, weight=100)
        self.frameset_ud.add(self.log_txt, weight=10)

        self.frameset_lr.add(self.tabbed, weight=100)
        self.frameset_lr.add(self.in_out, weight=10)
        #self.in_out_list. state["disabled"]


        #self.in_out_list['yscrollcommand'] = self.in_out_scroll.set
        #self.log_txt['yscrollcommand'] = self.log_scroll.set




        self.frm_inputs = ttk.Frame(self.tabbed,
                                    padding="3 3 12 12")  # first page, which would get widgets gridded into it
        self.frm_settings = ttk.Frame(self.tabbed)  # second page
        self.frm_errors = ttk.Frame(self.tabbed)
        self.tabbed.add(self.frm_inputs, text='Eingabesimulation', sticky=N+E+S+W)
        self.tabbed.add(self.frm_settings, text='Einstellungen')
        self.tabbed.add(self.frm_errors, text='Fehler')

        self.log_txt.insert("1.0", "Hallo und Willkommen\n")
        self.log_txt.tag_configure('output', foreground="blue")
        self.log_txt.tag_configure('input', foreground="green")
        self.log_txt.tag_configure('log', foreground="grey")

        #self.hi_there = Button(self.frameset_ud, text="Hello")
        #self.frameset_ud.add(self.hi_there)

        #in_out bar on right side

        #listbox.configure(yscrollcommand=s.set)

        #self.frameset_ud.add(self.button)


        #in_out bar on right side
        #self.frameset_ud.add()

    def timer(self):
        self.readSerial();

        self.root.after(200, self.timer)

    def readSerial(self):
        if (self.conn):
            self.conn.read_frames()


    def on_output(self, output_id, value):
        self.log_txt.insert("1.0", "<Output> id: " + str(output_id) + " value: " + str(value) + "\n", ('output'))

        existing_slaves = self.in_out.grid_slaves(row=output_id, column=0)
        if(len(existing_slaves) ==  1):
            existing_slaves[0]["text"]="OUT id: " + str(output_id) + " value: " + str(value)
        else:
            Label(self.in_out, text="OUT id: " + str(output_id) + " value: " + str(value)).grid(row=output_id, column=0)

    def on_input(self, input_id, value):
        self.log_txt.insert("1.0", "<Input> id: " + str(input_id) + " value: " + str(value) + "\n", ('input'))

        existing_slaves = self.in_out.grid_slaves(row=input_id, column=1)
        if(len(existing_slaves) ==  1):
            existing_slaves[0]["text"]="IN id: " + str(input_id) + " value: " + str(value)
        else:
            Label(self.in_out, text="IN id: " + str(input_id) + " value: " + str(value)).grid(row=input_id, column=1)


    def on_log(self, input_type, input_id, value, additional_info):
        self.log_txt.insert("1.0", " <Event> type: " + str(input_type) + " id: " + str(input_id) + " value: " + str(
            value) + " additional_info: " + str(additional_info) + "\n", ('log'))

    def buildSimulateInput(self):
        c = 5
        r = len(config["input"])*2 // 5

        cCol = 0
        cRow = 0
        for input_ in config["input"]:
            ttk.Button(self.frm_inputs, text=input_["name"]+" ON", command=lambda inid=input_["id"]: self.simulate_input(inid, 1)).grid(column=cCol,
                                                                                     row=cRow,
                                                                                     ipady=3,
                                                                                     ipadx=3,
                                                                                     pady=3,
                                                                                     padx=3,
                                                                                     sticky=W+E)
            ttk.Button(self.frm_inputs, text=input_["name"]+" OFF", command=lambda inid=input_["id"]: self.simulate_input(inid, 0)).grid(column=cCol,
                                                                                     row=cRow+1,
                                                                                     ipady=3,
                                                                                     ipadx=3,
                                                                                     pady=3,
                                                                                     padx=3,
                                                                                     sticky=W+E)
            cCol += 1
            if cCol >= c:
                cCol = 0
                cRow += 2

    def simulate_input(self, input_id, value):
        self.conn.simulate_manual_input(input_id, value)


# app = App(root)
gui = Gui()
