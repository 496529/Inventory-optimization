from tkinter import *
from billing import BillClass
import os

from ui_theme import PALETTE, FONT, configure_root, create_card, apply_page_background
from ui_widgets import AppDialog, action_button


class salesclass:
    def __init__(self, root):
        self.root = root
        configure_root(self.root, "Inventory Optimisation | Sales", "1270x650+250+110")
        self.root.focus_force()
        apply_page_background(
            self.root,
            top="#f2f7ff",
            bottom="#e7eefc",
            orbs=[
                ((-100, -30, 220, 220), "#dbe6ff"),
                ((930, -50, 1280, 250), "#ffe8d8"),
                ((920, 410, 1310, 760), "#dff8ef"),
            ],
        )

        self.var_invoice = StringVar()
        self.bill_list = []

        self._build_ui()
        self.show()

    def _build_ui(self):
        hero = create_card(self.root, bg=PALETTE["dark"])
        hero.place(x=18, y=18, width=1234, height=92)
        Label(hero, text="Sales Archive", bg=PALETTE["dark"], fg="white", font=("Georgia", 26, "bold")).place(x=22, y=18)
        Label(hero, text="Browse saved bills, preview invoice text, and jump straight into a new billing session.", bg=PALETTE["dark"], fg="#aabadd", font=FONT["body"]).place(x=24, y=56)

        tools = create_card(self.root, bg=PALETTE["surface"])
        tools.place(x=18, y=128, width=1234, height=74)
        Label(tools, text="Invoice search", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["heading"]).place(x=20, y=14)
        Entry(tools, textvariable=self.var_invoice, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=20, y=38, width=220, height=28)
        action_button(tools, "Search", self.search, 254, 38, 96, 28, PALETTE["primary"], "#1747d1")
        action_button(tools, "Clear", self.clear, 362, 38, 96, 28, "#9aa4bd", "#7d89a7")
        action_button(tools, "Generate Bill", self.billing, 1066, 24, 150, 34, PALETTE["accent"], "#e67722", fg="white")

        list_card = create_card(self.root, bg=PALETTE["surface"])
        list_card.place(x=18, y=220, width=280, height=412)
        Label(list_card, text="Saved invoices", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=20, y=18)
        scrolly = Scrollbar(list_card, orient=VERTICAL)
        self.sales_list = Listbox(
            list_card,
            font=("Segoe UI", 11),
            bg=PALETTE["surface_alt"],
            fg=PALETTE["text"],
            relief=FLAT,
            yscrollcommand=scrolly.set,
            selectbackground=PALETTE["primary"],
            selectforeground="white",
        )
        scrolly.pack(side=RIGHT, fill=Y, pady=(60, 18))
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH, expand=1, padx=20, pady=(60, 18))
        self.sales_list.bind("<ButtonRelease-1>", self.get_data)

        preview_card = create_card(self.root, bg=PALETTE["surface"])
        preview_card.place(x=316, y=220, width=936, height=412)
        Label(preview_card, text="Customer bill area", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=20, y=18)
        scrolly2 = Scrollbar(preview_card, orient=VERTICAL)
        self.bill_area = Text(
            preview_card,
            bg="#0f1730",
            fg="#f5f7ff",
            relief=FLAT,
            font=("Consolas", 11),
            yscrollcommand=scrolly2.set,
            insertbackground="white",
        )
        scrolly2.pack(side=RIGHT, fill=Y, pady=(60, 18))
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1, padx=20, pady=(60, 18))

    def show(self):
        del self.bill_list[:]
        self.sales_list.delete(0, END)
        for i in os.listdir("bill"):
            if i.split(".")[-1] == "txt":
                self.sales_list.insert(END, i)
                self.bill_list.append(i.split(".")[0])

    def get_data(self, ev):
        index_ = self.sales_list.curselection()
        if not index_:
            return
        file_name = self.sales_list.get(index_[0])
        self.bill_area.delete("1.0", END)
        fp = open(f"bill/{file_name}", "r")
        for i in fp:
            self.bill_area.insert(END, i)
        fp.close()

    def search(self):
        if self.var_invoice.get() == "":
            AppDialog.error(self.root, "Search Input", "Invoice number is required.")
        else:
            if self.var_invoice.get() in self.bill_list:
                fp = open(f"bill/{self.var_invoice.get()}.txt", "r")
                self.bill_area.delete("1.0", END)
                for i in fp:
                    self.bill_area.insert(END, i)
                fp.close()
                self.sales_list.selection_clear(0, END)
                if f"{self.var_invoice.get()}.txt" in self.sales_list.get(0, END):
                    idx = self.sales_list.get(0, END).index(f"{self.var_invoice.get()}.txt")
                    self.sales_list.selection_set(idx)
                    self.sales_list.activate(idx)
            else:
                AppDialog.error(self.root, "Invalid Invoice", "No bill exists with that invoice number.")

    def clear(self):
        self.var_invoice.set("")
        self.show()
        self.bill_area.delete("1.0", END)

    def billing(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = BillClass(self.new_win)


if __name__ == "__main__":
    root = Tk()
    obj = salesclass(root)
    root.mainloop()
