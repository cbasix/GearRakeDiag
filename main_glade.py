__author__ = 'cyberxix'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
import math

scale = 1
color_border = (0.3, 0.8, 0.8)
color_wheel = (0.3, 0.3, 0.3)
color_frame = (0.9, 0.9, 0.9)
color_cylinder = (0.2, 0.7, 0.7)

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onClick(self, button):
        print("Hello World!")

def build():
    builder = Gtk.Builder()
    builder.add_from_file("main.glade")
    # builder.connect_signals(Handler())
    return builder

def top_view(cr):

    # wheels
    y_offsets = [0.05, 0.55]
    for offset in y_offsets:
        cr.rectangle(0.2, offset, 0.2, 0.1)
        cr.set_source_rgb(*color_wheel)
        cr.fill_preserve()
        cr.set_source_rgb(*color_border)
        cr.stroke()

    # spinner
    y_offsets = [0.15, 0.55]
    for offset in y_offsets:
        # cr.set_line_cap(cairo.LINE_CAP_ROUND)
        # cr.set_source_rgb(0, 0, 0)
        cr.arc(0.6, offset, 0.15, 0, 2 * math.pi)
        # cr.fill_preserve()
        cr.set_source_rgb(*color_border)
        cr.stroke()

    # frames
    frames = (
        (0.3 - 0.05 / 2, 0.15, 0.05, 0.5 - 2 * 0.05),
        (0.3 + 0.05 / 2, 0.35 - 0.05 / 2, 0.6, 0.05)
    )
    for frame in frames:
        cr.rectangle(*frame)
        cr.set_source_rgb(*color_frame)
        cr.fill_preserve()
        cr.set_source_rgb(*color_border)
        cr.stroke()

    # cylinders
    cylinders = (
        (0.22, 0.17, 0.015, 0.15),
        (0.22, 0.38, 0.015, 0.15),
        (0.6, 0.17, 0.015, 0.15),
        (0.6, 0.38, 0.015, 0.15),
    )
    for cylinder in cylinders:
        cr.rectangle(*cylinder)
        cr.set_source_rgb(*color_cylinder)
        cr.fill_preserve()
        cr.set_source_rgb(*color_border)
        cr.stroke()

def OnDraw(w, cr):
    global scale

    # normalize with regard do image aspect
    scale = min(w.get_allocated_width(), w.get_allocated_height()*(1/0.8))
    cr.scale(scale, scale)

    #defaults
    cr.set_line_width(0.005)

    # draw grid
    for x in range(0, 100, 5):
        cr.set_source_rgb(0,0,0)
        cr.move_to(x/100, 0)
        cr.line_to(x/100, 0.8)
        cr.stroke()
    for y in range(0, 80, 5):
        cr.set_source_rgb(0,0,0)
        cr.move_to(0, y/100)
        cr.line_to(1, y/100)
        cr.stroke()


    # todo continue here

def on_click(widget, event):
    if event.type == Gdk.EventType.BUTTON_PRESS:
        print('Position: (' + str(round(event.x / scale, 3)) + ', ' + str(round(event.y / scale, 3)) + ')') # + ' ' + str(event.state))
        #print(dir(event))



if __name__ == '__main__':
    builder = build()
    drawing_area = builder.get_object("drawingarea1")
    drawing_area.connect('draw', OnDraw)
    #eventbox = builder.get_object("eventbox1")


    window = builder.get_object("applicationwindow1")
    window.connect("delete-event", Gtk.main_quit)
    window.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
    window.connect('button-press-event', on_click)

    window.show_all()
    Gtk.main()