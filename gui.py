import tkinter as tk
from tkinter import simpledialog, messagebox

from core.user_mgmt import verificar_credenciais, guardar_utilizador
from core.blockchain import add_action
from main import enviar_mensagem


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VPN Demo")
        self.geometry("300x200")
        self.username = None
        self.role = None
        self._show_login()

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _show_login(self):
        self._clear()
        tk.Label(self, text="Username:").pack()
        username_entry = tk.Entry(self)
        username_entry.pack()
        tk.Label(self, text="Password:").pack()
        password_entry = tk.Entry(self, show="*")
        password_entry.pack()

        def do_login():
            uname = username_entry.get()
            pwd = password_entry.get()
            role = verificar_credenciais(uname, pwd)
            if role:
                self.username = uname
                self.role = role
                add_action(f"login_gui:{uname}")
                self._show_main()
            else:
                messagebox.showerror("Erro", "Credenciais inválidas")

        tk.Button(self, text="Login", command=do_login).pack(pady=10)

    def _show_main(self):
        self._clear()
        tk.Label(self, text=f"Bem-vindo {self.username}").pack()
        msg_entry = tk.Entry(self)
        msg_entry.pack(fill="x", padx=10)

        def send():
            msg = msg_entry.get()
            if msg:
                enviar_mensagem_gui(msg)
                msg_entry.delete(0, tk.END)

        tk.Button(self, text="Enviar", command=send).pack(pady=5)
        tk.Button(self, text="Sair", command=self.destroy).pack(pady=5)


def enviar_mensagem_gui(msg: str) -> None:
    enviar_mensagem = __import__('main').enviar_mensagem
    add_action(f"send_message_gui:{msg}")
    # wrap enviar_mensagem to avoid interactive loop
    import socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destino = ("127.0.0.1", 8888)
    udp_sock.sendto(msg.encode(), destino)
    udp_sock.close()


if __name__ == "__main__":
    app = App()
    app.mainloop()
