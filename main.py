import socket
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.button import Button

from plyer import accelerometer
from plyer import gyroscope

from IPPopup import IPPopup

import Functions, Constants


class PhoneControllerApp(App):

    def __init__(self):

        super(PhoneControllerApp, self).__init__()

        self.socket = self.get_socket(host_ip=Constants.host_ip, port=Constants.port)
        self.box_layout = BoxLayout(pos_hint={'center_x': .5, 'center_y': .5})
        self.ip_popup_button = IPPopupButton(init_host_ip=Constants.host_ip, phone_controller_app=self)
        self.accelerometer_label = Label(text="accelerometer_label", color=(1, 1, 1, 1))

        self.sensor_cond = self.get_sensor_cond()
        Clock.schedule_interval(self.update, .1)  # 24 calls per second

    def build(self):
        Functions.add_to_layout(
            self.box_layout,
            self.ip_popup_button,
            self.accelerometer_label
        )
        return self.box_layout

    def get_sensor_cond(self):
        try:
            accelerometer.enable()
            gyroscope.enable()
            return True
        except:
            print("Failed to start accelerometer")
            return False

    def get_data(self):
        try:
            if self.sensor_cond:
                return "A:{}|G:{}".format(accelerometer.acceleration, gyroscope.orientation)
            return "Sensors failed to initialize"
        except:
            return "No data"

    def update(self, dt):

        data = self.get_data()

        try:
            # self.socket.sendall(bytes(data))
            self.socket.sendall(bytes(data, "ascii"))
            # data = self.s.recv(1024)
            # print('Received', repr(data))
        except:
            print("Server died")

        self.accelerometer_label.text = data
        print(data)

    def get_socket(self, host_ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host_ip, port))
        except:
            print("Couldn't create a new socket")
        return s

    def update_socket(self, new_ip):
        self.socket.close()
        self.socket = self.get_socket(host_ip=new_ip, port=Constants.port)


class IPPopupButton(Button):

    def __init__(self, init_host_ip, phone_controller_app):
        super(IPPopupButton, self).__init__(
            text="IP Button",
        )
        self.ip_popup = IPPopup(init_host_ip=init_host_ip, phone_controller_app=phone_controller_app)

    def on_press(self):
        self.ip_popup.open()


def main():

    PhoneControllerApp().run()


main()
