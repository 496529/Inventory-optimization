from tkinter import *
from tkinter import ttk
import sqlite3

from ui_theme import PALETTE, FONT, configure_root, create_card, apply_page_background
from ui_widgets import AppDialog, action_button


class productclass:
    def __init__(self, root):
        self.root = root
        configure_root(self.root, "Inventory Optimisation | Products", "1270x650+250+110")
        self.root.focus_force()
        apply_page_background(
            self.root,
            top="#f2f6ff",
            bottom="#e3eaff",
            orbs=[
                ((-120, -40, 210, 230), "#dbe6ff"),
                ((880, -40, 1260, 250), "#ede5ff"),
                ((930, 420, 1320, 760), "#dff8ef"),
            ],
        )

        self.var_searchby = StringVar(value="Select")
        self.var_searchtxt = StringVar()
        self.var_cat = StringVar()
        self.var_pid = StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar(value="Active")

        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sup()

        self._build_ui()
        self.show()

    def _build_ui(self):
        hero = create_card(self.root, bg=PALETTE["dark"])
        hero.place(x=18, y=18, width=1234, height=92)
        Label(hero, text="Product Control", bg=PALETTE["dark"], fg="white", font=("Georgia", 26, "bold")).place(x=22, y=18)
        Label(hero, text="Manage product stock, status, supplier relationships, and pricing from a more refined layout.", bg=PALETTE["dark"], fg="#aabadd", font=FONT["body"]).place(x=24, y=56)

        left = create_card(self.root, bg=PALETTE["surface"])
        left.place(x=18, y=128, width=420, height=504)
        Label(left, text="Product details", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=20, y=18)

        fields = [("Category", 20, 78), ("Supplier", 20, 138), ("Name", 20, 198), ("Price", 20, 258), ("Quantity", 20, 318), ("Status", 20, 378)]
        for text, x, y in fields:
            Label(left, text=text, bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["body_bold"]).place(x=x, y=y)

        self.cmb_cat = ttk.Combobox(left, textvariable=self.var_cat, values=self.cat_list, state="readonly", justify=CENTER, style="Inventory.TCombobox", font=FONT["body"])
        self.cmb_cat.place(x=120, y=76, width=250, height=30)
        self.cmb_sup = ttk.Combobox(left, textvariable=self.var_sup, values=self.sup_list, state="readonly", justify=CENTER, style="Inventory.TCombobox", font=FONT["body"])
        self.cmb_sup.place(x=120, y=136, width=250, height=30)
        Entry(left, textvariable=self.var_name, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=120, y=196, width=250, height=30)
        Entry(left, textvariable=self.var_price, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=120, y=256, width=250, height=30)
        Entry(left, textvariable=self.var_qty, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=120, y=316, width=250, height=30)
        self.cmb_status = ttk.Combobox(left, textvariable=self.var_status, values=("Active", "Inactive"), state="readonly", justify=CENTER, style="Inventory.TCombobox", font=FONT["body"])
        self.cmb_status.place(x=120, y=376, width=250, height=30)

        action_button(left, "Save", self.add, 20, 444, 88, 34, PALETTE["primary"], "#1747d1")
        action_button(left, "Update", self.update, 118, 444, 88, 34, PALETTE["success"], "#168557")
        action_button(left, "Delete", self.delete, 216, 444, 88, 34, PALETTE["danger"], "#be2430")
        action_button(left, "Clear", self.clear, 314, 444, 88, 34, "#9aa4bd", "#7d89a7")

        right = create_card(self.root, bg=PALETTE["surface"])
        right.place(x=454, y=128, width=798, height=504)
        Label(right, text="Product records", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=20, y=18)
        Label(right, text="Search by supplier, category, or product name to narrow the table.", bg=PALETTE["surface"], fg=PALETTE["muted"], font=FONT["body"]).place(x=20, y=56)

        self.cmb_search = ttk.Combobox(right, textvariable=self.var_searchby, values=("Select", "Supplier", "Category", "name"), state="readonly", justify=CENTER, style="Inventory.TCombobox", font=FONT["body"])
        self.cmb_search.place(x=20, y=92, width=190, height=30)
        Entry(right, textvariable=self.var_searchtxt, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=224, y=92, width=250, height=30)
        action_button(right, "Search", self.search, 488, 92, 92, 30, PALETTE["secondary"], "#0e9992")
        action_button(right, "Reset", self.clear, 592, 92, 92, 30, "#9aa4bd", "#7d89a7")

        table_wrap = create_card(right, bg="#f7f9ff")
        table_wrap.place(x=20, y=140, width=758, height=344)
        scrolly = Scrollbar(table_wrap, orient=VERTICAL)
        scrollx = Scrollbar(table_wrap, orient=HORIZONTAL)
        self.product_table = ttk.Treeview(
            table_wrap,
            columns=("pid", "Category", "Supplier", "name", "price", "qty", "status"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set,
            style="Inventory.Treeview",
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        for key, text, width in [("pid", "P_ID", 70), ("Category", "CATEGORY", 120), ("Supplier", "SUPPLIER", 120), ("name", "NAME", 130), ("price", "PRICE", 90), ("qty", "QUANTITY", 90), ("status", "STATUS", 90)]:
            self.product_table.heading(key, text=text)
            self.product_table.column(key, width=width)
        self.product_table["show"] = "headings"
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

    def fetch_cat_sup(self):
        self.cat_list = ["Empty"]
        self.sup_list = ["Empty"]
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            cur.execute("select name from category")
            cat = cur.fetchall()
            if len(cat) > 0:
                self.cat_list = ["Select"] + [i[0] for i in cat]

            cur.execute("select name from supplier")
            sup = cur.fetchall()
            if len(sup) > 0:
                self.sup_list = ["Select"] + [i[0] for i in sup]
        except Exception as ex:
            AppDialog.error(self.root, "Load Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def add(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_cat.get() in {"Select", "Empty", ""} or self.var_sup.get() in {"Select", "Empty", ""} or self.var_name.get() == "":
                AppDialog.error(self.root, "Missing Fields", "Category, supplier, and product name are required.")
            else:
                cur.execute("select * from product where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    AppDialog.error(self.root, "Duplicate Product", "That product already exists.")
                else:
                    cur.execute(
                        "Insert into product (Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",
                        (
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                        ),
                    )
                    con.commit()
                    AppDialog.info(self.root, "Product Saved", "Product added successfully.")
                    self.show()
        except Exception as ex:
            AppDialog.error(self.root, "Database Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert("", END, values=row)
        except Exception as ex:
            AppDialog.error(self.root, "Load Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def get_data(self, ev):
        f = self.product_table.focus()
        content = self.product_table.item(f)
        row = content["values"]
        if not row:
            return
        self.var_pid.set(row[0])
        self.var_sup.set(row[2])
        self.var_cat.set(row[1])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])

    def update(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                AppDialog.error(self.root, "Select Product", "Select a product from the list first.")
            else:
                cur.execute("select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    AppDialog.error(self.root, "Invalid Product", "No product exists with that ID.")
                else:
                    cur.execute(
                        "Update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",
                        (
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                            self.var_pid.get(),
                        ),
                    )
                    con.commit()
                    AppDialog.info(self.root, "Product Updated", "Product updated successfully.")
                    self.show()
        except Exception as ex:
            AppDialog.error(self.root, "Update Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                AppDialog.error(self.root, "Select Product", "Select a product from the list first.")
            else:
                cur.execute("select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    AppDialog.error(self.root, "Invalid Product", "No product exists with that ID.")
                else:
                    op = AppDialog.confirm(self.root, "Delete Product", "Do you really want to delete this product?")
                    if op is True:
                        cur.execute("delete from product where pid=?", (self.var_pid.get(),))
                        con.commit()
                        AppDialog.info(self.root, "Product Deleted", "Product deleted successfully.")
                        self.clear()
        except Exception as ex:
            AppDialog.error(self.root, "Delete Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                AppDialog.error(self.root, "Search Option", "Select a search option first.")
            elif self.var_searchtxt.get() == "":
                AppDialog.error(self.root, "Search Input", "Enter something to search.")
            else:
                cur.execute("select * from product where " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert("", END, values=row)
                else:
                    AppDialog.error(self.root, "No Record", "No matching product record was found.")
        except Exception as ex:
            AppDialog.error(self.root, "Search Error", f"Error due to: {str(ex)}")
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = productclass(root)
    root.mainloop()
