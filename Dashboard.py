from tkinter import *
from PIL import Image, ImageTk
import os
import sqlite3
import time

from employee import emploeeclass
from supplier import supplierclass
from category import categoryclass
from product import productclass
from sales import salesclass
from ui_theme import PALETTE, FONT, configure_root, create_card
from ui_widgets import add_hover, AppDialog


class IO:
    def __init__(self, root):
        self.root = root
        configure_root(self.root, "Inventory Optimisation | Dashboard", "1550x790+0+0")

        self.current_highlight = 0
        self.metric_cards = []

        self._build_shell()
        self._build_sidebar()
        self._build_topbar()
        self._build_metrics()
        self._build_panels()
        self.animate_metrics()
        self.update_content()

    def _build_shell(self):
        self.sidebar = Frame(self.root, bg=PALETTE["dark"], bd=0, highlightthickness=0)
        self.sidebar.place(x=0, y=0, width=270, relheight=1)

        self.main_panel = Frame(self.root, bg="#eef3ff", bd=0, highlightthickness=0)
        self.main_panel.place(x=270, y=0, relwidth=1, relheight=1)

    def _build_sidebar(self):
        self.icon_title = PhotoImage(file="images/logo1.png")
        self.menu_logo = Image.open("images/menu_im.png")
        self.menu_logo = self.menu_logo.resize((170, 170), Image.LANCZOS)
        self.menu_logo = ImageTk.PhotoImage(self.menu_logo)

        Label(
            self.sidebar,
            image=self.icon_title,
            bg=PALETTE["dark"],
            bd=0,
        ).place(x=24, y=24)
        Label(
            self.sidebar,
            text="MY INVENTORY",
            bg=PALETTE["dark"],
            fg="white",
            anchor="w",
            font=("Georgia", 22, "bold"),
        ).place(x=84, y=28)

        Label(
            self.sidebar,
            text="Inventory control with a sharper visual rhythm.",
            bg=PALETTE["dark"],
            fg="#9fb3d9",
            justify=LEFT,
            wraplength=210,
            font=FONT["body"],
        ).place(x=24, y=86)

        Label(self.sidebar, image=self.menu_logo, bg=PALETTE["dark"]).place(x=48, y=145)

        menu_wrap = create_card(self.sidebar, bg=PALETTE["dark_alt"])
        menu_wrap.place(x=20, y=345, width=230, height=330)

        Label(
            menu_wrap,
            text="Workspace",
            bg=PALETTE["dark_alt"],
            fg="#dce6ff",
            font=("Segoe UI Semibold", 13, "bold"),
        ).place(x=18, y=18)

        buttons = [
            ("Employees", self.employee, "#5b8cff"),
            ("Suppliers", self.supplier, "#11b5ae"),
            ("Categories", self.category, "#ff8a3d"),
            ("Products", self.product, "#7c6cff"),
            ("Sales", self.sales, "#1fbf75"),
            ("Logout", self.logout, "#e24d5f"),
        ]

        y = 58
        for text, command, color in buttons:
            btn = Button(
                menu_wrap,
                text=text,
                command=command,
                cursor="hand2",
                relief=FLAT,
                bd=0,
                bg=color,
                activebackground=color,
                activeforeground="white",
                fg="white",
                font=("Segoe UI Semibold", 12, "bold"),
            )
            btn.place(x=18, y=y, width=194, height=38)
            add_hover(btn, color, "#16376d" if text != "Logout" else "#be2430")
            y += 46

    def _build_topbar(self):
        hero = create_card(self.main_panel, bg=PALETTE["surface"])
        hero.place(x=28, y=26, width=1218, height=124)

        Label(
            hero,
            text="Inventory Dashboard",
            bg=PALETTE["surface"],
            fg=PALETTE["text"],
            font=("Georgia", 28, "bold"),
        ).place(x=28, y=22)

        Label(
            hero,
            text="Monitor stock, suppliers, and sales from one calm command center.",
            bg=PALETTE["surface"],
            fg=PALETTE["muted"],
            font=FONT["body"],
        ).place(x=30, y=67)

        self.lbl_clock = Label(
            hero,
            text="",
            bg=PALETTE["primary_soft"],
            fg=PALETTE["primary"],
            font=("Segoe UI Semibold", 11, "bold"),
            padx=18,
            pady=10,
        )
        self.lbl_clock.place(x=866, y=26, width=320, height=44)

        self.status_chip = Label(
            hero,
            text="Live sync with local database",
            bg="#dff8ef",
            fg=PALETTE["success"],
            font=FONT["small"],
            padx=14,
            pady=8,
        )
        self.status_chip.place(x=916, y=78, width=270, height=30)

    def _build_metrics(self):
        cards = [
            ("Employees", "#dce7ff"),
            ("Suppliers", "#d8f6f2"),
            ("Categories", "#ffe8d8"),
            ("Products", "#ebe5ff"),
            ("Sales", "#dff8ef"),
        ]
        self.metric_vars = {}

        x = 28
        for title, card_bg in cards:
            card = create_card(self.main_panel, bg=PALETTE["surface"])
            card.place(x=x, y=175, width=224, height=145)

            accent = Frame(card, bg=card_bg, bd=0, highlightthickness=0)
            accent.place(x=16, y=16, width=52, height=52)

            Label(card, text=title, bg=PALETTE["surface"], fg=PALETTE["muted"], font=FONT["body_bold"]).place(x=18, y=83)
            value_label = Label(card, text="0", bg=PALETTE["surface"], fg=PALETTE["text"], font=("Georgia", 24, "bold"))
            value_label.place(x=18, y=105)

            note = Label(card, text="Updated live", bg=PALETTE["surface"], fg=PALETTE["muted"], font=FONT["small"])
            note.place(x=140, y=112)

            self.metric_cards.append((card, accent, card_bg))
            self.metric_vars[title.lower()] = value_label
            x += 244

    def _build_panels(self):
        quick_actions = create_card(self.main_panel, bg=PALETTE["surface"])
        quick_actions.place(x=28, y=345, width=580, height=385)

        Label(quick_actions, text="Quick actions", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=24, y=20)
        Label(
            quick_actions,
            text="Jump straight into the records your team updates most often.",
            bg=PALETTE["surface"],
            fg=PALETTE["muted"],
            font=FONT["body"],
        ).place(x=24, y=58)

        action_specs = [
            ("Manage employees", "Open employee records and credentials", self.employee, "#2962ff"),
            ("Manage suppliers", "Review contact details and vendor notes", self.supplier, "#11b5ae"),
            ("Manage categories", "Organize stock groups with clarity", self.category, "#ff8a3d"),
            ("Manage products", "Update pricing, quantity, and status", self.product, "#7c6cff"),
            ("Review sales", "Browse stored bills and invoices", self.sales, "#1fbf75"),
        ]

        y = 102
        for title, desc, command, color in action_specs:
            box = create_card(quick_actions, bg="#f7f9ff")
            box.place(x=24, y=y, width=532, height=46)
            btn = Button(
                box,
                text=title,
                command=command,
                relief=FLAT,
                bd=0,
                cursor="hand2",
                bg=color,
                activebackground=color,
                activeforeground="white",
                fg="white",
                font=("Segoe UI Semibold", 11, "bold"),
            )
            btn.place(x=0, y=0, width=180, height=46)
            add_hover(btn, color, "#16376d")
            Label(box, text=desc, bg="#f7f9ff", fg=PALETTE["muted"], font=FONT["small"]).place(x=198, y=14)
            y += 56

        insight_panel = create_card(self.main_panel, bg=PALETTE["surface"])
        insight_panel.place(x=634, y=345, width=612, height=385)

        Label(insight_panel, text="Today at a glance", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=24, y=20)
        Label(
            insight_panel,
            text="A polished overview of your current system state.",
            bg=PALETTE["surface"],
            fg=PALETTE["muted"],
            font=FONT["body"],
        ).place(x=24, y=58)

        highlight = create_card(insight_panel, bg=PALETTE["dark"])
        highlight.place(x=24, y=100, width=564, height=114)
        Label(highlight, text="Operational Focus", bg=PALETTE["dark"], fg="#8fc3ff", font=FONT["body_bold"]).place(x=22, y=18)
        self.insight_text = Label(
            highlight,
            text="Dashboard ready. Watching records and bill files in real time.",
            bg=PALETTE["dark"],
            fg="white",
            justify=LEFT,
            wraplength=500,
            font=("Segoe UI", 14),
        )
        self.insight_text.place(x=22, y=48)

        stat_grid = create_card(insight_panel, bg="#f7f9ff")
        stat_grid.place(x=24, y=236, width=564, height=122)

        self.snapshot_a = Label(stat_grid, text="Admin view\nBright, organized, and live", bg="#f7f9ff", fg=PALETTE["text"], justify=LEFT, font=FONT["body_bold"])
        self.snapshot_a.place(x=22, y=22)
        self.snapshot_b = Label(stat_grid, text="Bills folder\nTracking completed sales files", bg="#f7f9ff", fg=PALETTE["text"], justify=LEFT, font=FONT["body_bold"])
        self.snapshot_b.place(x=220, y=22)
        self.snapshot_c = Label(stat_grid, text="Clock sync\nTimestamp updates every moment", bg="#f7f9ff", fg=PALETTE["text"], justify=LEFT, font=FONT["body_bold"])
        self.snapshot_c.place(x=395, y=22)

    def animate_metrics(self):
        for index, (card, accent, card_bg) in enumerate(self.metric_cards):
            card.configure(bg=PALETTE["surface"] if index != self.current_highlight else "#f1f6ff")
            accent.configure(bg=card_bg if index != self.current_highlight else PALETTE["primary_soft"])
        self.current_highlight = (self.current_highlight + 1) % len(self.metric_cards)
        self.root.after(850, self.animate_metrics)

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = emploeeclass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierclass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryclass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productclass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesclass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            product = cur.fetchall()
            self.metric_vars["products"].config(text=str(len(product)))

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.metric_vars["suppliers"].config(text=str(len(supplier)))

            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.metric_vars["employees"].config(text=str(len(employee)))

            cur.execute("select * from category")
            category = cur.fetchall()
            self.metric_vars["categories"].config(text=str(len(category)))

            bill = len(os.listdir("bill"))
            self.metric_vars["sales"].config(text=str(bill))

            time_ = time.strftime("%I:%M:%S %p")
            date_ = time.strftime("%d %b %Y")
            self.lbl_clock.config(text=f"{date_}    |    {time_}")

            self.insight_text.config(
                text=f"You currently have {len(product)} products, {len(supplier)} suppliers, {len(employee)} employees, and {bill} saved bill files."
            )

            self.root.after(500, self.update_content)
        except Exception as ex:
            AppDialog.error(self.root, "Dashboard Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def logout(self):
        self.root.destroy()
        from login import Login_system
        new_root = Tk()
        Login_system(new_root)
        new_root.mainloop()


if __name__ == "__main__":
    root = Tk()
    obj = IO(root)
    root.mainloop()
