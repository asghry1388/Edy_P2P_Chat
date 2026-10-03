import socket
import threading
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


PORT = 5000
BUFFER = 4096


class ChatApp(App):
    def build(self):
        self.title = "Edy P2P Chat"
        self.sock = None
        self.conn = None
        self.running = False
        self.role = None

        try:
            Window.size = (430, 760)
        except Exception:
            pass

        root = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))

        title = Label(
            text="[b]EDY P2P CHAT[/b]",
            markup=True,
            size_hint_y=None,
            height=dp(48),
            font_size="22sp",
        )
        root.add_widget(title)

        self.status = Label(
            text="Disconnected",
            size_hint_y=None,
            height=dp(32),
        )
        root.add_widget(self.status)

        top = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(6))
        self.ip_input = TextInput(
            hint_text="Server IP / Tailscale IP",
            multiline=False,
        )
        top.add_widget(self.ip_input)

        connect_btn = Button(text="Connect")
        connect_btn.bind(on_release=self.connect_client)
        top.add_widget(connect_btn)
        root.add_widget(top)

        buttons = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(6))

        server_btn = Button(text="Start Server")
        server_btn.bind(on_release=self.start_server)
        buttons.add_widget(server_btn)

        disconnect_btn = Button(text="Disconnect")
        disconnect_btn.bind(on_release=self.disconnect)
        buttons.add_widget(disconnect_btn)

        root.add_widget(buttons)

        self.scroll = ScrollView()
        self.messages = Label(
            text="",
            markup=True,
            halign="left",
            valign="top",
            size_hint_y=None,
            text_size=(None, None),
        )
        self.messages.bind(
            texture_size=lambda instance, value: setattr(
                instance, "height", max(dp(10), value[1])
            )
        )
        self.scroll.add_widget(self.messages)
        root.add_widget(self.scroll)

        bottom = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(6))
        self.message_input = TextInput(
            hint_text="Write a message...",
            multiline=False,
        )
        self.message_input.bind(on_text_validate=self.send_message)
        bottom.add_widget(self.message_input)

        send_btn = Button(text="Send", size_hint_x=None, width=dp(90))
        send_btn.bind(on_release=self.send_message)
        bottom.add_widget(send_btn)

        root.add_widget(bottom)

        return root

    def set_status(self, text):
        Clock.schedule_once(lambda dt: setattr(self.status, "text", text))

    def add_message(self, who, message):
        def update(dt):
            prefix = "[b]You:[/b]" if who == "You" else "[b]Other:[/b]"
            self.messages.text += f"{prefix} {message}\n"
            self.messages.texture_update()
            Clock.schedule_once(
                lambda _: setattr(self.scroll, "scroll_y", 0), 0
            )
        Clock.schedule_once(update)

    def start_server(self, *_):
        if self.running:
            self.set_status("Already running")
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("0.0.0.0", PORT))
            self.sock.listen(1)

            self.running = True
            self.role = "server"
            self.set_status(f"Waiting on port {PORT}...")

            threading.Thread(target=self.accept_connection, daemon=True).start()
        except Exception as e:
            self.cleanup_socket()
            self.show_error(str(e))

    def accept_connection(self):
        try:
            conn, address = self.sock.accept()
            self.conn = conn
            self.set_status(f"Connected: {address[0]}:{address[1]}")
            self.add_message("Other", "Connected.")
            threading.Thread(target=self.receive_loop, daemon=True).start()
        except Exception as e:
            if self.running:
                self.set_status("Server error")
                self.show_error(str(e))

    def connect_client(self, *_):
        ip = self.ip_input.text.strip()

        if not ip:
            self.show_error("Enter the server IP first.")
            return

        if self.running:
            self.set_status("Already connected/running")
            return

        threading.Thread(
            target=self.client_connect_thread,
            args=(ip,),
            daemon=True,
        ).start()

    def client_connect_thread(self, ip):
        try:
            self.set_status("Connecting...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(12)
            s.connect((ip, PORT))
            s.settimeout(None)

            self.conn = s
            self.running = True
            self.role = "client"

            self.set_status("Connected")
            self.add_message("Other", "Connected.")
            threading.Thread(target=self.receive_loop, daemon=True).start()
        except Exception as e:
            self.running = False
            self.show_error(str(e))
            self.set_status("Connection failed")

    def receive_loop(self):
        buffer = b""

        while self.running and self.conn:
            try:
                data = self.conn.recv(BUFFER)
                if not data:
                    break

                buffer += data

                while b"\n" in buffer:
                    raw, buffer = buffer.split(b"\n", 1)
                    if raw:
                        self.add_message("Other", raw.decode("utf-8", errors="replace"))

            except (ConnectionResetError, BrokenPipeError, OSError):
                break

        if self.running:
            self.set_status("Disconnected")
        self.running = False

    def send_message(self, *_):
        message = self.message_input.text.strip()
        if not message:
            return

        if not self.conn or not self.running:
            self.show_error("Connect to someone first.")
            return

        try:
            self.conn.sendall((message + "\n").encode("utf-8"))
            self.add_message("You", message)
            self.message_input.text = ""
        except (BrokenPipeError, ConnectionResetError, OSError):
            self.set_status("Connection lost")
            self.disconnect()

    def disconnect(self, *_):
        self.running = False
        try:
            if self.conn:
                self.conn.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            if self.conn:
                self.conn.close()
        except Exception:
            pass
        self.conn = None

        try:
            if self.sock:
                self.sock.close()
        except Exception:
            pass
        self.sock = None

        self.set_status("Disconnected")

    def cleanup_socket(self):
        try:
            if self.sock:
                self.sock.close()
        except Exception:
            pass
        self.sock = None

    def show_error(self, message):
        def popup(dt):
            Popup(
                title="Edy P2P Chat",
                content=Label(text=message),
                size_hint=(0.85, 0.35),
            ).open()
        Clock.schedule_once(popup)

    def on_stop(self):
        self.disconnect()


if __name__ == "__main__":
    ChatApp().run()
