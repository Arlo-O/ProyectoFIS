import tkinter as tk
from typing import Tuple, Optional


class LoginForm:
    def __init__(self, parent: tk.Widget, config: dict):
        self.parent = parent
        self.config = config
        self._user_entry: tk.Entry = None
        self._pass_entry: tk.Entry = None
        
    def create_widgets(self, parent_frame: tk.Frame, font: tuple, bg_color: str, 
                      placeholder_color: str, text_color: str) -> None:
        tk.Label(parent_frame, text="Usuario:", bg=bg_color, fg=text_color, font=font).pack(anchor="w")
        self._user_entry = tk.Entry(parent_frame, font=font, fg=placeholder_color, bg="#ffffff", bd=0)
        self._user_entry.pack(fill="x", pady=(0, 15), ipady=8)
        self._setup_placeholder(self._user_entry, "Ingrese su usuario", is_password=False)
        
        tk.Label(parent_frame, text="Contraseña:", bg=bg_color, fg=text_color, font=font).pack(anchor="w")
        self._pass_entry = tk.Entry(parent_frame, font=font, fg=placeholder_color, bg="#ffffff", bd=0)
        self._pass_entry.pack(fill="x", pady=(0, 20), ipady=8)
        self._setup_placeholder(self._pass_entry, "Ingrese su contraseña", is_password=True)

    def _setup_placeholder(self, entry: tk.Entry, placeholder: str, is_password: bool = False) -> None:
        entry.placeholder = placeholder
        entry.is_password = is_password
        
        def on_focus_in(event):
            if entry.get() == entry.placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="#333333")
                if entry.is_password:
                    entry.config(show="*")
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, entry.placeholder)
                entry.config(fg="#aaaaaa")
                if entry.is_password:
                    entry.config(show="")
        
        on_focus_out(None)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def get_credentials(self) -> Tuple[str, str]:
        user = self._user_entry.get().lower()
        password = self._pass_entry.get()
        return user, password

    def is_empty(self) -> bool:
        user = self._user_entry.get()
        password = self._pass_entry.get()
        
        return (user == self._user_entry.placeholder.lower() or 
                user == "" or 
                password == self._pass_entry.placeholder or 
                password == "")

    def clear(self) -> None:
        self._user_entry.delete(0, tk.END)
        self._pass_entry.delete(0, tk.END)
        self._user_entry.insert(0, self._user_entry.placeholder)
        self._pass_entry.insert(0, self._pass_entry.placeholder)
        self._user_entry.config(fg="#aaaaaa")
        self._pass_entry.config(fg="#aaaaaa", show="")
