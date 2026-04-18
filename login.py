import os, sys
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
from tkinter import *
from PIL import ImageTk
import sqlite3

from ui_theme import PALETTE, FONT, configure_root, create_card, draw_vertical_gradient, pulse_label
from ui_widgets import AppDialog, add_hover


class Login_system:
    def __init__(self, root):
        self.root = root
        configure_root(self.root, "Inventory Optimisation | Login", "1530x780+0+0")

        self.employee_id = StringVar()
        self.password = StringVar()

        self.taglines = [
            "Track stock. Move faster. Sell smarter.",
            "A brighter front desk for your inventory team.",
            "Modern inventory control with a friendlier workflow.",
        ]
        self.tagline_index = 0

        self.im1 = ImageTk.PhotoImage(file="images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/im2.png")
        self.im3 = ImageTk.PhotoImage(file="images/im3.png")
        self.carousel_images = [self.im1, self.im2, self.im3]
        self.carousel_index = 0

        self.phone_image = ImageTk.PhotoImage(file="images/phone.png")

        self._build_background()
        self._build_layout()
        self.animate_showcase()
        self.rotate_tagline()
        pulse_label(self.login_hint, [PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"]], 900)

    def _build_background(self):
        self.bg_canvas = Canvas(self.root, highlightthickness=0, bd=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_canvas.bind(
            "<Configure>",
            lambda e: draw_vertical_gradient(self.bg_canvas, "#09111f", "#183867"),
        )
        self.orb_a = self.bg_canvas.create_oval(70, 80, 350, 360, fill="#204ea8", outline="")
        self.orb_b = self.bg_canvas.create_oval(1040, 70, 1400, 430, fill="#13a7a0", outline="")
        self.orb_c = self.bg_canvas.create_oval(1160, 480, 1490, 760, fill="#f18f4e", outline="")
        self.orb_step = 1
        self.animate_orbs()

    def _build_layout(self):
        hero = Frame(self.root, bg=PALETTE["bg"], bd=0, highlightthickness=0)
        hero.place(x=88, y=90, width=610, height=580)

        Label(
            hero,
            text="INVENTORY OPTIMISATION SUITE",
            bg=PALETTE["bg"],
            fg="#a9c6ff",
            font=("Segoe UI Semibold", 11, "bold"),
        ).place(x=0, y=16)

        Label(
            hero,
            text="Clean login.\nFaster start.",
            bg=PALETTE["bg"],
            fg="white",
            justify=LEFT,
            font=FONT["display"],
        ).place(x=0, y=48)

        self.tagline_label = Label(
            hero,
            text=self.taglines[0],
            bg=PALETTE["bg"],
            fg="#d7e4ff",
            justify=LEFT,
            font=("Segoe UI", 14),
        )
        self.tagline_label.place(x=0, y=146)

        showcase_shell = create_card(hero, bg="#f8fbff")
        showcase_shell.place(x=0, y=220, width=520, height=286)
        Frame(showcase_shell, bg="#dce7ff", bd=0, highlightthickness=0).place(x=18, y=18, width=484, height=250)
        self.showcase_phone = Label(showcase_shell, image=self.phone_image, bg="#f8fbff", bd=0)
        self.showcase_phone.place(x=40, y=18)
        self.lbl_change_image = Label(showcase_shell, bg="#f8fbff", bd=0)
        self.lbl_change_image.place(x=58, y=82, width=210, height=180)
        Label(
            showcase_shell,
            text="Inventory at a glance",
            bg="#f8fbff",
            fg=PALETTE["text"],
            font=("Segoe UI Semibold", 12, "bold"),
        ).place(x=316, y=48)
        Label(
            showcase_shell,
            text="A simpler welcome screen keeps the focus on signing in while still giving the app a polished first impression.",
            bg="#f8fbff",
            fg=PALETTE["muted"],
            justify=LEFT,
            wraplength=160,
            font=FONT["body"],
        ).place(x=316, y=82)

        login_card = create_card(self.root, bg="white")
        login_card.place(x=902, y=120, width=430, height=500)

        Label(login_card, text="Welcome back", bg="white", fg=PALETTE["primary"], font=("Segoe UI Semibold", 13, "bold")).place(x=42, y=38)
        Label(login_card, text="Sign in to continue", bg="white", fg=PALETTE["text"], font=("Georgia", 26, "bold")).place(x=42, y=72)
        Label(
            login_card,
            text="Use your employee ID and password to open the admin dashboard or billing desk.",
            bg="white",
            fg=PALETTE["muted"],
            justify=LEFT,
            font=FONT["body"],
            wraplength=330,
        ).place(x=42, y=122)

        Label(login_card, text="Employee ID", bg="white", fg=PALETTE["text"], font=FONT["body_bold"]).place(x=42, y=198)
        self.employee_entry = Entry(
            login_card,
            textvariable=self.employee_id,
            font=("Segoe UI", 14),
            relief=FLAT,
            bg=PALETTE["surface_alt"],
            fg=PALETTE["text"],
            insertbackground=PALETTE["text"],
        )
        self.employee_entry.place(x=42, y=232, width=340, height=42)

        Label(login_card, text="Password", bg="white", fg=PALETTE["text"], font=FONT["body_bold"]).place(x=42, y=295)
        self.password_entry = Entry(
            login_card,
            textvariable=self.password,
            show="*",
            font=("Segoe UI", 14),
            relief=FLAT,
            bg=PALETTE["surface_alt"],
            fg=PALETTE["text"],
            insertbackground=PALETTE["text"],
        )
        self.password_entry.place(x=42, y=329, width=340, height=42)

        self.login_hint = Label(
            login_card,
            text="Tip: Admin opens the dashboard, employee opens billing.",
            bg="white",
            fg=PALETTE["primary"],
            font=FONT["small"],
        )
        self.login_hint.place(x=42, y=386)

        login_button = Button(
            login_card,
            text="Log In",
            command=self.login,
            relief=FLAT,
            bd=0,
            cursor="hand2",
            bg=PALETTE["primary"],
            activebackground="#1747d1",
            activeforeground="white",
            fg="white",
            font=("Segoe UI Semibold", 14, "bold"),
        )
        login_button.place(x=42, y=430, width=340, height=46)
        add_hover(login_button, PALETTE["primary"], "#1747d1")

        footer_strip = create_card(login_card, bg=PALETTE["primary_soft"])
        footer_strip.place(x=42, y=442, width=340, height=36)
        Label(
            footer_strip,
            text="Secure sign-in for dashboard and billing access.",
            bg=PALETTE["primary_soft"],
            fg=PALETTE["text"],
            font=FONT["small"],
        ).pack(expand=True)

        self.root.bind("<Return>", lambda event: self.login())

    def animate_orbs(self):
        dx = self.orb_step
        self.bg_canvas.move(self.orb_a, dx, 0)
        self.bg_canvas.move(self.orb_b, -dx, 0)
        self.bg_canvas.move(self.orb_c, 0, dx)
        coords = self.bg_canvas.coords(self.orb_a)
        if coords and (coords[0] <= 40 or coords[2] >= 390):
            self.orb_step *= -1
        self.root.after(60, self.animate_orbs)

    def animate_showcase(self):
        self.lbl_change_image.config(image=self.carousel_images[self.carousel_index])
        self.carousel_index = (self.carousel_index + 1) % len(self.carousel_images)
        self.lbl_change_image.after(2400, self.animate_showcase)

    def rotate_tagline(self):
        self.tagline_index = (self.tagline_index + 1) % len(self.taglines)
        self.tagline_label.config(text=self.taglines[self.tagline_index])
        self.root.after(2600, self.rotate_tagline)

    def login(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                AppDialog.error(self.root, "Missing Fields", "All fields are required.")
            else:
                cur.execute(
                    "select utype from employee where eid=? AND pass=?",
                    (self.employee_id.get(), self.password.get()),
                )
                user = cur.fetchone()
                if user is None:
                    AppDialog.error(self.root, "Login Failed", "Invalid username or password.")
                else:
                    self.root.destroy()
                    if user[0] == "Admin":
                        from Dashboard import IO
                        new_root = Tk()
                        IO(new_root)
                        new_root.mainloop()
                    else:
                        from billing import BillClass
                        new_root = Tk()
                        BillClass(new_root)
                        new_root.mainloop()
        except Exception as ex:
            AppDialog.error(self.root, "Login Error", f"Error due to: {str(ex)}")
        finally:
            con.close()


root = Tk()
obj = Login_system(root)
root.mainloop()
