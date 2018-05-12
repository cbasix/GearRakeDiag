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
color_output_border = (1, 0.27, 0)
color_wheel = (0.3, 0.3, 0.3)
color_arrow = (0.3, 0.3, 0.3)
color_frame = (0.9, 0.9, 0.9)
color_cylinder = (0.2, 0.7, 0.7)
color_on = (0, 1, 0)
color_off = (1, 0, 0)
color_unknown = (0.8, 0.8, 0.8)
last_event = 0

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onClick(self, button):
        print("Hello World!")

def build():
    builder = Gtk.Builder()
    builder.add_from_file("gui.glade")
    # builder.connect_signals(Handler())
    return builder

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
        (leds[config.get_input_id("SENS_WEEL_TELE_LEFT_OUT")], (0.19, 0.184), config.get_input_description("SENS_WEEL_TELE_LEFT_OUT")),
        (leds[config.get_input_id("SENS_WEEL_TELE_LEFT_IN")], (0.19, 0.307), config.get_input_description("SENS_WEEL_TELE_LEFT_IN")),
        (leds[config.get_input_id("SENS_WEEL_TELE_RIGHT_IN")], (0.19, 0.386), config.get_input_description("SENS_WEEL_TELE_RIGHT_IN")),
        (leds[config.get_input_id("SENS_WEEL_TELE_RIGHT_OUT")], (0.19, 0.517), config.get_input_description("SENS_WEEL_TELE_RIGHT_OUT")),
        (leds[config.get_input_id("SENS_SPINNER_LEFT_TELE_OUT")], (0.57, 0.18), config.get_input_description("SENS_SPINNER_LEFT_TELE_OUT")),
        (leds[config.get_input_id("SENS_SPINNER_LEFT_TELE_IN")], (0.57, 0.3), config.get_input_description("SENS_SPINNER_LEFT_TELE_IN")),
        (leds[config.get_input_id("SENS_SPINNER_RIGHT_TELE_IN")], (0.57, 0.4), config.get_input_description("SENS_SPINNER_RIGHT_TELE_IN")),
        (leds[config.get_input_id("SENS_SPINNER_RIGHT_TELE_OUT")], (0.57, 0.52), config.get_input_description("SENS_SPINNER_RIGHT_TELE_OUT")),
        (leds[config.get_input_id("SENS_WEEL_TRACK_MIDDLE")], (0.37, 0.68), config.get_input_description("SENS_WEEL_TRACK_MIDDLE")),
    )

    draw_leds(cr, leds)

    # arrow
    draw_object(cr, 0.25, 0.2, arrow, color_border, color_arrow)
    draw_object(cr, 0.25, 0.41, arrow, color_border, color_arrow)
    draw_object(cr, 0.63, 0.2, arrow, color_border, color_arrow)
    draw_object(cr, 0.63, 0.41, arrow, color_border, color_arrow)

def draw_leds(cr, leds, input=True):
    for led in leds:
        cr.move_to(led[1][0]+0.015, led[1][1])
        if input:
            cr.arc(led[1][0], led[1][1], 0.015, 0, 2 * math.pi)
        else:
            cr.arc(led[1][0], led[1][1], 0.015, math.pi, 2 * math.pi)
        color = color_unknown if led[0] is None else color_on if led[0] else color_off
        cr.set_source_rgb(*color)
        cr.fill_preserve()
        if input:
            cr.set_source_rgb(*color_border)
        else:
            cr.set_source_rgb(*color_output_border)
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
        (led_status[config.get_input_id("SENS_SPINNER_LEFT_UP")], (0.34, 0.05), config.get_input_description("SENS_SPINNER_LEFT_UP")),
        (led_status[config.get_input_id("SENS_SPINNER_RIGHT_UP")], (0.66, 0.05), config.get_input_description("SENS_SPINNER_RIGHT_UP")),
        (led_status[config.get_input_id("SENS_SPINNER_LEFT_THIRD")], (0.14, 0.21), config.get_input_description("SENS_SPINNER_LEFT_THIRD")),
        (led_status[config.get_input_id("SENS_SPINNER_RIGHT_THIRD")], (0.85, 0.20), config.get_input_description("SENS_SPINNER_RIGHT_THIRD")),
    )

    draw_leds(cr, leds)

side_frame = (
(0.0, 0.0),
(0.30, 0.08),
(0.60, 0.0),
(0.60, 0.02),
(0.30, 0.10),
(0.0, 0.02),
)
rear_frame = (
(0.0, 0.0),
(0.01, 0.0),
(0.01, 0.01),
(0.08, 0.01),
(0.08, 0.02),
(0.08, 0.02),
(0.00, 0.02),
)

frame_lock = (
(0.0, 0.0),
(0.02, 0.0),
(0.02, -0.01),
(0.08, -0.01),
(0.08, 0.02),
(0.02, 0.02),
(0.02, 0.01),
(0.00, 0.01),
)

def side_view(cr, input_status):
    # wheel
    cr.arc(0.3, 0.4, 0.07, 0, 2 * math.pi)
    cr.set_source_rgb(*color_wheel)
    cr.fill_preserve()
    cr.set_source_rgb(*color_border)
    cr.stroke()

    # frame
    draw_object(cr, 0.37, 0.4, side_frame, color_border, color_frame)
    draw_object(cr, 0.14, 0.39, rear_frame, color_border, color_frame)

    # frame arrows
    draw_object(cr, 0.80, 0.35, arrow, color_border, color_arrow)
    # rear arrow
    draw_object(cr, 0.14, 0.30, arrow, color_border, color_arrow)

    # frame lock cylinder
    draw_object(cr, 0.60, 0.20, frame_lock, color_border, color_frame)
    # frame lock cylinder arrow
    draw_object(cr, 0.80, 0.16, arrow, color_border, color_arrow)

    # leds
    leds = (
        (input_status[config.get_input_id("SENS_FRAME_UP")], (0.67, 0.34), config.get_input_description("SENS_FRAME_UP")),
        (input_status[config.get_input_id("SENS_FRAME_MIDDLE")], (0.67, 0.39), config.get_input_description("SENS_FRAME_MIDDLE")),
        (input_status[config.get_input_id("SENS_FRAME_LOW")], (0.67, 0.44), config.get_input_description("SENS_FRAME_LOW")),
        (input_status[config.get_input_id("SENS_FRAME_GROUND")], (0.67, 0.49), config.get_input_description("SENS_FRAME_GROUND")),

        (input_status[config.get_input_id("SENS_FRAME_LOCK_OPEN")], (0.67, 0.18), config.get_input_description("SENS_FRAME_LOCK_OPEN")),
        (input_status[config.get_input_id("SENS_FRAME_LOCK_CLOSED")], (0.67, 0.23), config.get_input_description("SENS_FRAME_LOCK_CLOSED")),
        (input_status[config.get_input_id("SENS_SPINNER_REAR_UP")], (0.16, 0.26), config.get_input_description("SENS_SPINNER_REAR_UP")),

    )

    draw_leds(cr, leds)

    # outputs = (
    #     (output_status[config.get_input_id("SENS_FRAME_UP")], (0.67, 0.34), config.get_input_description("SENS_FRAME_UP")),
    # )
    # draw_leds(cr, outputs, input=False)

def input_view(cr, led_status):
    # leds
    leds = (
        (led_status[config.get_input_id("IN_SPINNER_LEFT_UP")], (0.30, 0.57), config.get_input_description("IN_SPINNER_LEFT_UP")),
        (led_status[config.get_input_id("IN_SPINNER_LEFT_FLOAT")], (0.30, 0.43), config.get_input_description("IN_SPINNER_LEFT_FLOAT")),
        (led_status[config.get_input_id("IN_SPINNER_LEFT_TELE_OUT")], (0.23, 0.48), config.get_input_description("IN_SPINNER_LEFT_TELE_OUT")),
        (led_status[config.get_input_id("IN_SPINNER_LEFT_TELE_IN")], (0.37, 0.52), config.get_input_description("IN_SPINNER_LEFT_TELE_IN")),
        (led_status[config.get_input_id("IN_SPINNER_LEFT_AUTO_THIRD")], (0.30, 0.50), config.get_input_description("IN_SPINNER_LEFT_AUTO_THIRD")),

        (led_status[config.get_input_id("IN_SPINNER_RIGHT_UP")], (0.70, 0.57), config.get_input_description("IN_SPINNER_RIGHT_UP")),
        (led_status[config.get_input_id("IN_SPINNER_RIGHT_FLOAT")], (0.70, 0.43), config.get_input_description("IN_SPINNER_RIGHT_FLOAT")),
        (led_status[config.get_input_id("IN_SPINNER_RIGHT_TELE_OUT")], (0.77, 0.52), config.get_input_description("IN_SPINNER_RIGHT_TELE_OUT")),
        (led_status[config.get_input_id("IN_SPINNER_RIGHT_TELE_IN")], (0.63, 0.48), config.get_input_description("IN_SPINNER_RIGHT_TELE_IN")),
        (led_status[config.get_input_id("IN_SPINNER_RIGHT_AUTO_THIRD")], (0.70, 0.50), config.get_input_description("IN_SPINNER_RIGHT_AUTO_THIRD")),

        (led_status[config.get_input_id("IN_MULTI_UP")], (0.80, 0.77), config.get_input_description("IN_MULTI_UP")),
        (led_status[config.get_input_id("IN_MULTI_DOWN")], (0.80, 0.63), config.get_input_description("IN_MULTI_DOWN")),
        (led_status[config.get_input_id("IN_MULTI_RIGHT")], (0.87, 0.72), config.get_input_description("IN_MULTI_RIGHT")),
        (led_status[config.get_input_id("IN_MULTI_LEFT")], (0.73, 0.68), config.get_input_description("IN_MULTI_LEFT")),
        (led_status[config.get_input_id("IN_MULTI_PRESS")], (0.80, 0.70), config.get_input_description("IN_MULTI_PRESS")),

        (led_status[config.get_input_id("IN_AUTO_TRANSPORT")], (0.20, 0.08), config.get_input_description("IN_AUTO_TRANSPORT")),
        (led_status[config.get_input_id("IN_AUTO_LOW")], (0.50, 0.08), config.get_input_description("IN_AUTO_LOW")),
        (led_status[config.get_input_id("IN_AUTO_WORK")], (0.80, 0.08), config.get_input_description("IN_AUTO_WORK")),

        (led_status[config.get_input_id("IN_MOD_LR_STEER")], (0.75, 0.25), config.get_input_description("IN_MOD_LR_STEER")),
        (led_status[config.get_input_id("IN_MOD_LR_WEEL_RIGHT_TELE")], (0.75, 0.30), config.get_input_description("IN_MOD_LR_WEEL_RIGHT_TELE")),
        (led_status[config.get_input_id("IN_MOD_LR_WEEL_LEFT_TELE")], (0.70, 0.33), config.get_input_description("IN_MOD_LR_WEEL_LEFT_TELE")),

        (led_status[config.get_input_id("IN_MOD_OU_SPINNER_BACK")], (0.25, 0.25), config.get_input_description("IN_MOD_OU_SPINNER_BACK")),
        (led_status[config.get_input_id("IN_MOD_OU_FRAME")], (0.25, 0.30), config.get_input_description("IN_MOD_OU_FRAME")),

        (led_status[config.get_input_id("IN_SPINNER_REAR_UP")], (0.2, 0.70), config.get_input_description("IN_SPINNER_REAR_UP")),
        (led_status[config.get_input_id("IN_SPINNER_REAR_DOWN")], (0.2, 0.74), config.get_input_description("IN_SPINNER_REAR_DOWN")),


    )

    draw_leds(cr, leds)


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

def drawFront(w, cr, inputs):
    OnDraw(w, cr)
    front_view(cr, inputs)

def drawTop(w, cr, inputs):
    OnDraw(w, cr)
    top_view(cr, inputs)

def drawSide(w, cr, inputs):
    OnDraw(w, cr)
    side_view(cr, inputs)

def drawInput(w, cr, inputs):
    OnDraw(w, cr)
    input_view(cr, inputs)

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