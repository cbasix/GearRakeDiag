__author__ = 'cyberxix'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
import math
import config

scale = 1
color_text = (0.3, 0.3, 0.3)
color_border = (0.3, 0.7, 0.7)
color_wheel = (0.3, 0.3, 0.3)
color_arrow = (0.3, 0.3, 0.3)
color_frame = (0.9, 0.9, 0.9)
color_cylinder = (0.2, 0.7, 0.7)
color_on = (0, 1, 0)
color_off = (1, 0, 0)
last_event = 0

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

def top_view(cr, leds):

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

    leds = (
        (leds[config.get_input_id("SENS_WEEL_TELE_LEFT_OUT")], (0.19, 0.184), "Radtele li ausgefahren"),
        (leds[config.get_input_id("SENS_WEEL_TELE_LEFT_IN")], (0.19, 0.307), "Radtele li eingefahren"),
        (leds[config.get_input_id("SENS_WEEL_TELE_RIGHT_IN")], (0.19, 0.386), "Radtele re eingefahren"),
        (leds[config.get_input_id("SENS_WEEL_TELE_RIGHT_OUT")], (0.19, 0.517), "Radtele re ausgefahren"),
        (leds[config.get_input_id("SENS_SPINNER_LEFT_TELE_OUT")], (0.57, 0.18), "Kreiseltele li ausgefahren"),
        (leds[config.get_input_id("SENS_SPINNER_LEFT_TELE_IN")], (0.57, 0.3), "Kreiseltele li eingefahren"),
        (leds[config.get_input_id("SENS_SPINNER_RIGHT_TELE_IN")], (0.57, 0.4), "Kreiseltele re eingefahren"),
        (leds[config.get_input_id("SENS_SPINNER_RIGHT_TELE_OUT")], (0.57, 0.52), "Kreiseltele re ausgefahren"),
        (leds[config.get_input_id("SENS_WEEL_TRACK_MIDDLE")], (0.37, 0.68), "Rad gerade"),
    )

    draw_leds(cr, leds)

    # arrow
    arrow = (
        (0.02, 0.00),
        (0.04, 0.02),
        (0.03, 0.02),
        (0.03, 0.07),
        (0.04, 0.07),
        (0.02, 0.09),
        (0.00, 0.07),
        (0.01, 0.07),
        (0.01, 0.02),
        (0.00, 0.02),
    )

    draw_object(cr, 0.25, 0.2, arrow, color_border, color_arrow)
    draw_object(cr, 0.25, 0.41, arrow, color_border, color_arrow)
    draw_object(cr, 0.63, 0.2, arrow, color_border, color_arrow)
    draw_object(cr, 0.63, 0.41, arrow, color_border, color_arrow)

def draw_leds(cr, leds):
    for led in leds:
        cr.move_to(led[1][0]+0.015, led[1][1])
        cr.arc(led[1][0], led[1][1], 0.015, 0, 2 * math.pi)
        color = color_on if led[0] else color_off
        cr.set_source_rgb(*color)
        cr.fill_preserve()
        cr.set_source_rgb(*color_border)
        cr.stroke()

        # text
        cr.set_source_rgb(*color_text)
        x_bearing, y_bearing, width, height = cr.text_extents(led[2])[:4]
        cr.move_to(led[1][0] - width - x_bearing - 0.018, led[1][1] - height / 2 - y_bearing)
        cr.show_text(led[2])

spinner_up = (
(0.0, 0.0),
(0.0, 0.25),
(0.12, 0.25),
(0.12, 0.0),
)

frame = (
(0.0, 0.0),
(0.3, 0.0),
(0.3, 0.03),
(0.0, 0.03),
)

wheel = (
(0.0, 0.0),
(0.0, 0.15),
(0.1, 0.15),
(0.1, 0.0),
)

tele = (
(0.0, 0.0),
(0.0, 0.2),
(0.02, 0.2),
(0.02, 0.0),
)

spinner_left = (
(0.07, 0.00),
(0.02, 0.09),
(0.23, 0.18),
(0.27, 0.09),
)

spinner_right = (
(0.0, 0.17),
(0.05, 0.26),
(0.25, 0.15),
(0.19, 0.05),
)
def front_view(cr, led_status):
    # wheels
    draw_object(cr, 0.25, 0.35, wheel, color_border, color_wheel)
    draw_object(cr, 0.65, 0.35, wheel, color_border, color_wheel)

    # frame
    draw_object(cr, 0.35, 0.35, frame, color_border, color_frame)

    # tele
    draw_object(cr, 0.36, 0.15, tele, color_border, color_frame)
    draw_object(cr, 0.62, 0.15, tele, color_border, color_frame)

    # spinner up
    draw_object(cr, 0.28, 0.0, spinner_up, color_border, None)
    draw_object(cr, 0.6, 0.0, spinner_up, color_border, None)

    # spinner left
    draw_object(cr, 0.05, 0.15, spinner_left, color_border, None)

    # spinner right
    draw_object(cr, 0.68, 0.07, spinner_right, color_border, None)

    # leds
    leds = (
        (led_status[config.get_input_id("SENS_SPINNER_LEFT_UP")], (0.34, 0.05), "Kreisel li oben"),
        (led_status[config.get_input_id("SENS_SPINNER_RIGHT_UP")], (0.66, 0.05), "Kreisel re oben"),
        (led_status[config.get_input_id("SENS_SPINNER_LEFT_THIRD")], (0.14, 0.21), "Kreisel li 1/3"),
        (led_status[config.get_input_id("SENS_SPINNER_RIGHT_THIRD")], (0.85, 0.20), "Kreisel re 1/3 "),
    )

    draw_leds(cr, leds)

def side_view(cr, leds):
    # wheel
    draw_object(cr, 0.25, 0.35, wheel, color_border, color_wheel)

    # frame

    # frame arrow

    # cylinder

    # cylinder arrow

    # leds


def draw_object(cr, x, y, object, border_color=None, fill_color=None):
    i = 0
    for point in object:
        if i == 0:
            cr.move_to(point[0] + x, point[1] + y)
            i =+ 1
        else:
            cr.line_to(point[0] + x, point[1] + y)
    cr.close_path()

    if border_color:

        if fill_color:
            cr.set_source_rgb(*border_color)
            cr.stroke_preserve()
            cr.set_source_rgb(*fill_color)
            cr.fill()
        else:
            cr.set_source_rgb(*border_color)
            cr.stroke()

def drawFront(w, cr, data):
    OnDraw(w, cr)
    front_view(cr, data)

def drawTop(w, cr, data):
    OnDraw(w, cr)
    top_view(cr, data)

def drawSide(w, cr, data):
    OnDraw(w, cr)
    side_view(cr, data)

def OnDraw(w, cr):
    global scale

    # normalize with regard do image aspect
    scale = min(w.get_allocated_width(), w.get_allocated_height()*(1/0.8))
    #cr.translate(10, 10)
    #cr.scale(scale-20, scale-20)
    cr.scale(scale, scale)

    #defaults
    cr.set_line_width(0.005)
    cr.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(0.013)

    # draw grid
    # for x in range(0, 100, 5):
    #     cr.set_source_rgb(0,0,0)
    #     cr.move_to(x/100, 0)
    #     cr.line_to(x/100, 0.8)
    #     cr.stroke()
    # for y in range(0, 80, 5):
    #     cr.set_source_rgb(0,0,0)
    #     cr.move_to(0, y/100)
    #     cr.line_to(1, y/100)
    #     cr.stroke()


    # todo continue here
    # top_view(cr)
    # front_view(cr)
    # side_view(cr)

def on_click(widget, event):
    global last_event

    if event.type == Gdk.EventType.BUTTON_PRESS:
        if last_event + 100 < event.time:
            last_event = event.time
            print('(' + str(round(event.x / scale, 2)) + ', ' + str(round(event.y / scale, 2)) + '),') # + ' ' + str(event.state))
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