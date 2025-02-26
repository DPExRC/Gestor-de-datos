from tkinter import messagebox


def show_message(title, message):
    """Muestra un mensaje de información."""
    messagebox.showinfo(title, message)

def show_error(title, message):
    """Muestra un mensaje de error."""
    messagebox.showerror(title, message)

def show_warning(title, message):
    """Muestra un mensaje de advertencia."""
    messagebox.showwarning(title, message)