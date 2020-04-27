import socket
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from plyer import accelerometer
from plyer import gyroscope


def add_to_layout(layout, *widget_list):
    for widget in widget_list:
        layout.add_widget(widget)
    return layout


# host = socket.gethostname()
host = "192.168.1.27"
port = 12345  # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


class ACSApp(App):

    def __init__(self):

        super(ACSApp, self).__init__()

        self.box_layout = BoxLayout(

        )

        self.accelerometer_label = Label(
            text="accelerometer_label",
            pos_hint={'center_x': .5, 'center_y': .5},
            color=(1, 1, 1, 1)
        )

        self.sensor_cond = False
        try:
            accelerometer.enable()
            gyroscope.enable()
            self.sensor_cond = True
        except:
            print("Failed to start accelerometer")

        Clock.schedule_interval(self.update, .1)  # 24 calls per second

    def build(self):

        add_to_layout(
            self.box_layout,
            self.accelerometer_label
        )

        return self.box_layout

    def update(self, dt):
        try:
            txt = "Accelerometer does not exist"
            if self.sensor_cond:
                txt = "Accelerometer:\nX = %.2f\nY = %.2f\nZ = %2.f " % (
                    accelerometer.acceleration[0],  # X
                    accelerometer.acceleration[1],  # Y
                    accelerometer.acceleration[2]   # Z
                )
        except:
            txt = "Cannot read accelerometer"

        s.sendall(bytes("A:{}|G:{}".format(accelerometer.acceleration, gyroscope.orientation)))
        # data = s.recv(1024)
        # print('Received', repr(data))

        self.accelerometer_label.text = txt
        print(self.accelerometer_label.text)


def main():

    ACSApp().run()


main()
