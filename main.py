import socket
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

PORT = 5000


class ChatApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = None
        self.connected = False
        self.buffer = b""

    def build(self):
        self.title = "Edy P2P Chat"

        root = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=8
        )

        # IP
        ip_row = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=5
        )

        self.ip_input = TextInput(
            hint_text="Server IP",
            multiline=False
        )

        self.connect_button = Button(
            text="Connect",
            size_hint_x=None,
            width=110
        )

        self.connect_button.bind(
            on_press=self.connect_button_pressed
        )

        ip_row.add_widget(self.ip_input)
        ip_row.add_widget(self.connect_button)

        root.add_widget(ip_row)

        # Status
        self.status = Label(
            text="Disconnected",
            size_hint_y=None,
            height=35
        )

        root.add_widget(self.status)

        # Messages
        scroll = ScrollView()

        self.messages = Label(
            text="",
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        self.messages.bind(
            texture_size=self.update_message_height
        )

        scroll.add_widget(self.messages)

        root.add_widget(scroll)

        # Message input
        message_row = BoxLayout(
            size_hint_y=None,
            height=55,
            spacing=5
        )

        self.message_input = TextInput(
            hint_text="Message...",
            multiline=False
        )

        send_button = Button(
            text="Send",
            size_hint_x=None,
            width=90
        )

        send_button.bind(
            on_press=self.send_message
        )

        self.message_input.bind(
            on_text_validate=self.send_message
        )

        message_row.add_widget(self.message_input)
        message_row.add_widget(send_button)

        root.add_widget(message_row)

        return root

    def update_message_height(self, *_):
        self.messages.height = max(
            self.messages.texture_size[1],
            100
        )

    def add_message(self, message):
        def update(_):
            if self.messages.text:
                self.messages.text += "\n"

            self.messages.text += message

        Clock.schedule_once(update)

    def set_status(self, text):
        Clock.schedule_once(
            lambda _: setattr(self.status, "text", text)
        )

    def connect_button_pressed(self, *_):

        if self.connected:
            self.disconnect()
            return

        ip = self.ip_input.text.strip()

        if not ip:
            self.set_status("Enter server IP")
            return

        self.connect_button.disabled = True
        self.set_status("Connecting...")

        threading.Thread(
            target=self.connect_worker,
            args=(ip,),
            daemon=True
        ).start()

    def connect_worker(self, ip):

        try:
            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(10)

            sock.connect(
                (ip, PORT)
            )

            sock.settimeout(None)

            self.client = sock
            self.connected = True
            self.buffer = b""

            self.set_status(
                f"Connected: {ip}:{PORT}"
            )

            Clock.schedule_once(
                self.connection_ui
            )

            threading.Thread(
                target=self.receive_messages,
                daemon=True
            ).start()

        except Exception as e:

            self.client = None
            self.connected = False

            self.set_status(
                f"Connection failed: {e}"
            )

            Clock.schedule_once(
                self.connection_ui
            )

    def connection_ui(self, *_):

        self.connect_button.disabled = False

        if self.connected:
            self.connect_button.text = "Disconnect"
        else:
            self.connect_button.text = "Connect"

    def receive_messages(self):

        while self.connected and self.client:

            try:

                data = self.client.recv(4096)

                if not data:
                    break

                self.buffer += data

                while b"\n" in self.buffer:

                    raw, self.buffer = self.buffer.split(
                        b"\n",
                        1
                    )

                    if raw:

                        message = raw.decode(
                            "utf-8",
                            errors="replace"
                        )

                        self.add_message(
                            "Other: " + message
                        )

            except (
                ConnectionResetError,
                BrokenPipeError,
                OSError
            ):

                break

        self.connected = False
        self.client = None

        self.set_status("Connection lost")

        Clock.schedule_once(
            self.connection_ui
        )

    def send_message(self, *_):

        if not self.connected or not self.client:
            self.set_status("Not connected")
            return

        message = self.message_input.text.strip()

        if not message:
            return

        if message.lower() == "/exit":
            self.disconnect()
            return

        try:

            self.client.sendall(
                (message + "\n").encode("utf-8")
            )

            self.add_message(
                "You: " + message
            )

            self.message_input.text = ""

        except (
            ConnectionResetError,
            BrokenPipeError,
            OSError
        ):

            self.disconnect()

    def disconnect(self):

        self.connected = False

        if self.client:

            try:
                self.client.shutdown(
                    socket.SHUT_RDWR
                )
            except OSError:
                pass

            try:
                self.client.close()
            except OSError:
                pass

        self.client = None

        self.set_status("Disconnected")

        self.connect_button.text = "Connect"
        self.connect_button.disabled = False

    def on_stop(self):
        self.disconnect()


if __name__ == "__main__":
    ChatApp().run()
