from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import Functions


class IPPopup(Popup):

    def __init__(self, init_host_ip, phone_controller_app):

        self.init_ip = init_host_ip
        self.phone_controller_app = phone_controller_app

        self.box_layout = BoxLayout(
            orientation='vertical',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.ip_input = self.get_ip_input()
        self.refresh_ip_button = RefreshIPButton(ip_popup=self, phone_controller_app=phone_controller_app)
        Functions.add_to_layout(
            self.box_layout,
            self.ip_input,
            self.refresh_ip_button
        )

        super(IPPopup, self).__init__(
            title="IP Popup",
            content=self.box_layout,
            size_hint=(.9, .9),
            auto_dismiss=False
        )

    def get_ip_input(self):
        ip_input = TextInput(
            text=self.init_ip,
            # size_hint=(.7, None),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        return ip_input

    def get_ip(self):
        return self.ip_input.text


class RefreshIPButton(Button):

    def __init__(self, ip_popup, phone_controller_app):
        super(RefreshIPButton, self).__init__(
            text="Submit",
            # size_hint=(.3, None),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.ip_popup = ip_popup
        self.phone_controller_app = phone_controller_app

    def on_press(self):
        self.phone_controller_app.update_socket(self.ip_popup.get_ip())
        self.ip_popup.dismiss()
