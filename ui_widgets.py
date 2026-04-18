from tkinter import *

from ui_theme import PALETTE, FONT, create_card


def add_hover(button, normal_bg, hover_bg, normal_fg="white", hover_fg="white"):
    def on_enter(_event):
        button.configure(bg=hover_bg, fg=hover_fg)

    def on_leave(_event):
        button.configure(bg=normal_bg, fg=normal_fg)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    return button


def action_button(parent, text, command, x, y, width, height, bg, hover_bg, fg="white"):
    btn = Button(
        parent,
        text=text,
        command=command,
        relief=FLAT,
        bd=0,
        cursor="hand2",
        bg=bg,
        activebackground=hover_bg,
        activeforeground=fg,
        fg=fg,
        font=("Segoe UI Semibold", 10, "bold"),
    )
    btn.place(x=x, y=y, width=width, height=height)
    add_hover(btn, bg, hover_bg, fg, fg)
    return btn


class AppDialog:
    @staticmethod
    def _base(parent, title, message, accent):
        dialog = Toplevel(parent)
        dialog.title(title)
        dialog.transient(parent)
        dialog.grab_set()
        dialog.configure(bg=PALETTE["bg"])
        dialog.resizable(False, False)
        dialog.geometry("430x220")

        shell = create_card(dialog, bg=PALETTE["surface"])
        shell.place(x=16, y=16, width=398, height=188)

        accent_bar = Frame(shell, bg=accent, bd=0, highlightthickness=0)
        accent_bar.place(x=0, y=0, relwidth=1, height=12)

        Label(shell, text=title, bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=24, y=28)
        Label(
            shell,
            text=message,
            bg=PALETTE["surface"],
            fg=PALETTE["muted"],
            justify=LEFT,
            wraplength=340,
            font=FONT["body"],
        ).place(x=24, y=74)
        return dialog, shell

    @staticmethod
    def info(parent, title, message):
        dialog, shell = AppDialog._base(parent, title, message, PALETTE["secondary"])
        action_button(shell, "OK", dialog.destroy, 268, 140, 100, 32, PALETTE["primary"], "#1747d1")
        dialog.wait_window()

    @staticmethod
    def error(parent, title, message):
        dialog, shell = AppDialog._base(parent, title, message, PALETTE["danger"])
        action_button(shell, "Close", dialog.destroy, 250, 140, 118, 32, PALETTE["danger"], "#be2430")
        dialog.wait_window()

    @staticmethod
    def confirm(parent, title, message):
        result = {"value": False}
        dialog, shell = AppDialog._base(parent, title, message, PALETTE["accent"])

        def accept():
            result["value"] = True
            dialog.destroy()

        action_button(shell, "Cancel", dialog.destroy, 146, 140, 100, 32, "#c5cede", "#aeb9cd", fg=PALETTE["text"])
        action_button(shell, "Yes", accept, 258, 140, 100, 32, PALETTE["accent"], "#e67722")
        dialog.wait_window()
        return result["value"]


def top_section(parent, title, subtitle, width, height):
    section = create_card(parent, bg=PALETTE["surface"])
    section.place(x=18, y=18, width=width, height=height)
    Label(section, text=title, bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=20, y=18)
    Label(section, text=subtitle, bg=PALETTE["surface"], fg=PALETTE["muted"], font=FONT["body"]).place(x=20, y=54)
    return section
