from tkinter import *
from tkinter import ttk
import sqlite3

from ui_theme import PALETTE, FONT, configure_root, create_card, apply_page_background
from ui_widgets import AppDialog, action_button


class supplierclass:
    def __init__(self, root):
        self.root = root
        configure_root(self.root, "Inventory Optimisation | Suppliers", "1270x650+250+110")
        self.root.focus_force()
        apply_page_background(
            self.root,
            top="#eef9f7",
            bottom="#d8efe9",
            orbs=[
                ((-100, 10, 250, 280), "#cdeee5"),
                ((840, -60, 1240, 230), "#e8fff8"),
                ((910, 380, 1330, 760), "#cfe7ff"),
            ],
        )

        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_emp_name = StringVar()
        self.var_emp_contact = StringVar()

        self._build_ui()
        self.show()

    def _build_ui(self):
        hero = create_card(self.root, bg=PALETTE["dark"])
        hero.place(x=18, y=18, width=1234, height=92)
        Label(hero, text="Supplier Management", bg=PALETTE["dark"], fg="white", font=("Georgia", 26, "bold")).place(x=22, y=18)
        Label(hero, text="Keep invoices, supplier contact details, and notes organized with a smoother workflow.", bg=PALETTE["dark"], fg="#aabadd", font=FONT["body"]).place(x=24, y=56)

        left = create_card(self.root, bg=PALETTE["surface"])
        left.place(x=18, y=128, width=620, height=504)
        Label(left, text="Supplier details", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=20, y=18)

        Label(left, text="Invoice No", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["body_bold"]).place(x=22, y=74)
        Entry(left, textvariable=self.var_sup_invoice, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=130, y=72, width=180, height=30)
        Label(left, text="Name", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["body_bold"]).place(x=22, y=126)
        Entry(left, textvariable=self.var_emp_name, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=130, y=124, width=260, height=30)
        Label(left, text="Contact", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["body_bold"]).place(x=22, y=178)
        Entry(left, textvariable=self.var_emp_contact, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=130, y=176, width=260, height=30)
        Label(left, text="Description", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["body_bold"]).place(x=22, y=230)
        self.txt_desc = Text(left, font=("Segoe UI", 10), relief=FLAT, bg=PALETTE["surface_alt"], fg=PALETTE["text"])
        self.txt_desc.place(x=130, y=230, width=450, height=140)

        action_button(left, "Save", self.add, 130, 400, 100, 34, PALETTE["primary"], "#1747d1")
        action_button(left, "Update", self.update, 242, 400, 100, 34, PALETTE["success"], "#168557")
        action_button(left, "Delete", self.delete, 354, 400, 100, 34, PALETTE["danger"], "#be2430")
        action_button(left, "Clear", self.clear, 466, 400, 100, 34, "#9aa4bd", "#7d89a7")

        right = create_card(self.root, bg=PALETTE["surface"])
        right.place(x=654, y=128, width=598, height=504)
        Label(right, text="Supplier records", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=20, y=18)
        Label(right, text="Search by invoice number to filter the list quickly.", bg=PALETTE["surface"], fg=PALETTE["muted"], font=FONT["body"]).place(x=20, y=56)

        Entry(right, textvariable=self.var_searchtxt, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=20, y=92, width=220, height=30)
        action_button(right, "Search", self.search, 254, 92, 96, 30, PALETTE["secondary"], "#0e9992")
        action_button(right, "Reset", self.clear, 362, 92, 96, 30, "#9aa4bd", "#7d89a7")

        table_wrap = create_card(right, bg="#f7f9ff")
        table_wrap.place(x=20, y=140, width=558, height=344)
        scrolly = Scrollbar(table_wrap, orient=VERTICAL)
        scrollx = Scrollbar(table_wrap, orient=HORIZONTAL)
        self.supplierTable = ttk.Treeview(
            table_wrap,
            columns=("invoice", "name", "contact", "desc"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set,
            style="Inventory.Treeview",
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        for key, text, width in [("invoice", "INVOICE", 90), ("name", "NAME", 120), ("contact", "CONTACT", 120), ("desc", "DESCRIPTION", 210)]:
            self.supplierTable.heading(key, text=text)
            self.supplierTable.column(key, width=width)
        self.supplierTable["show"] = "headings"
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

    def add(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                AppDialog.error(self.root, "Missing Invoice", "Invoice number is required.")
            else:
                cur.execute("select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is not None:
                    AppDialog.error(self.root, "Duplicate Invoice", "This invoice number already exists.")
                else:
                    cur.execute(
                        "Insert into supplier (invoice,name,contact,desc) values(?,?,?,?)",
                        (
                            self.var_sup_invoice.get(),
                            self.var_emp_name.get(),
                            self.var_emp_contact.get(),
                            self.txt_desc.get("1.0", END),
                        ),
                    )
                    con.commit()
                    AppDialog.info(self.root, "Supplier Saved", "Supplier added successfully.")
            self.show()
        except Exception as ex:
            AppDialog.error(self.root, "Database Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            cur.execute("select * from supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert("", END, values=row)
        except Exception as ex:
            AppDialog.error(self.root, "Load Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = self.supplierTable.item(f)
        row = content["values"]
        if not row:
            return
        self.var_sup_invoice.set(row[0])
        self.var_emp_name.set(row[1])
        self.var_emp_contact.set(row[2])
        self.txt_desc.delete("1.0", END)
        self.txt_desc.insert(END, row[3])

    def update(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                AppDialog.error(self.root, "Missing Invoice", "Invoice number is required.")
            else:
                cur.execute("select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    AppDialog.error(self.root, "Invalid Invoice", "No supplier exists with that invoice number.")
                else:
                    cur.execute(
                        "Update supplier set name=?,contact=?,desc=? where invoice=?",
                        (
                            self.var_emp_name.get(),
                            self.var_emp_contact.get(),
                            self.txt_desc.get("1.0", END),
                            self.var_sup_invoice.get(),
                        ),
                    )
                    con.commit()
                    AppDialog.info(self.root, "Supplier Updated", "Supplier updated successfully.")
                    self.show()
        except Exception as ex:
            AppDialog.error(self.root, "Update Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                AppDialog.error(self.root, "Missing Invoice", "Invoice number is required.")
            else:
                cur.execute("select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    AppDialog.error(self.root, "Invalid Invoice", "No supplier exists with that invoice number.")
                else:
                    op = AppDialog.confirm(self.root, "Delete Supplier", "Do you really want to delete this supplier?")
                    if op is True:
                        cur.execute("delete from supplier where invoice=?", (self.var_sup_invoice.get(),))
                        con.commit()
                        AppDialog.info(self.root, "Supplier Deleted", "Supplier deleted successfully.")
                        self.clear()
        except Exception as ex:
            AppDialog.error(self.root, "Delete Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_emp_name.set("")
        self.var_emp_contact.set("")
        self.txt_desc.delete("1.0", END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                AppDialog.error(self.root, "Search Input", "Invoice number is required for search.")
            else:
                cur.execute("select * from supplier where invoice=?", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row is not None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert("", END, values=row)
                else:
                    AppDialog.error(self.root, "No Record", "No supplier record was found.")
        except Exception as ex:
            AppDialog.error(self.root, "Search Error", f"Error due to: {str(ex)}")
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = supplierclass(root)
    root.mainloop()
