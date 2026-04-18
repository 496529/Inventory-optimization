from tkinter import *
from tkinter import ttk
import os
import sqlite3
import tempfile
import time

from ui_theme import PALETTE, FONT, configure_root, create_card, pulse_label, apply_page_background
from ui_widgets import AppDialog, add_hover


class BillClass:
    def __init__(self, root):
        self.root = root
        configure_root(self.root, "Inventory Optimisation | Billing", "1550x790+0+0")
        apply_page_background(
            self.root,
            top="#f2f7ff",
            bottom="#e7eefc",
            orbs=[
                ((-140, -60, 240, 260), "#dbe6ff"),
                ((1180, -20, 1560, 290), "#dff8ef"),
                ((1150, 430, 1560, 840), "#ffe8d8"),
            ],
        )

        self.cart_list = []
        self.chk_print = 0

        self._build_header()
        self._build_products_panel()
        self._build_customer_panel()
        self._build_center_panel()
        self._build_cart_controls()
        self._build_bill_panel()

        self.show()
        self.update_date_time()
        pulse_label(self.live_hint, [PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"]], 850)

    def _build_header(self):
        header = create_card(self.root, bg=PALETTE["dark"])
        header.place(x=0, y=0, relwidth=1, height=96)

        self.icon_title = PhotoImage(file="images/logo1.png")
        Label(
            header,
            image=self.icon_title,
            text="  Billing Studio",
            compound=LEFT,
            bg=PALETTE["dark"],
            fg="white",
            anchor="w",
            font=("Georgia", 28, "bold"),
        ).place(x=22, y=18)

        Label(
            header,
            text="Generate neat customer bills with a cleaner workspace.",
            bg=PALETTE["dark"],
            fg="#adc0e5",
            font=FONT["body"],
        ).place(x=80, y=58)

        self.lbl_clock = Label(
            header,
            text="",
            bg="#13213d",
            fg="white",
            font=("Segoe UI Semibold", 11, "bold"),
            padx=18,
            pady=10,
        )
        self.lbl_clock.place(x=1035, y=22, width=280, height=40)

        logout_btn = Button(
            header,
            text="Logout",
            command=self.logout,
            relief=FLAT,
            bd=0,
            cursor="hand2",
            bg=PALETTE["danger"],
            activebackground=PALETTE["danger"],
            activeforeground="white",
            fg="white",
            font=("Segoe UI Semibold", 11, "bold"),
        )
        logout_btn.place(x=1338, y=22, width=160, height=40)
        add_hover(logout_btn, PALETTE["danger"], "#be2430")

    def _build_products_panel(self):
        product_frame = create_card(self.root, bg=PALETTE["surface"])
        product_frame.place(x=18, y=116, width=430, height=646)

        Label(product_frame, text="Products", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=22, y=18)
        Label(product_frame, text="Search active stock and add items to the bill.", bg=PALETTE["surface"], fg=PALETTE["muted"], font=FONT["body"]).place(x=22, y=58)

        self.var_search = StringVar()
        search_wrap = create_card(product_frame, bg="#f7f9ff")
        search_wrap.place(x=18, y=92, width=394, height=92)
        Label(search_wrap, text="Product name", bg="#f7f9ff", fg=PALETTE["text"], font=FONT["body_bold"]).place(x=18, y=16)
        Entry(
            search_wrap,
            textvariable=self.var_search,
            font=("Segoe UI", 12),
            relief=FLAT,
            bg="white",
            fg=PALETTE["text"],
        ).place(x=18, y=44, width=190, height=30)
        search_btn = Button(
            search_wrap,
            text="Search",
            command=self.search,
            relief=FLAT,
            bd=0,
            cursor="hand2",
            bg=PALETTE["primary"],
            activebackground=PALETTE["primary"],
            activeforeground="white",
            fg="white",
            font=("Segoe UI Semibold", 10, "bold"),
        )
        search_btn.place(x=225, y=44, width=74, height=30)
        add_hover(search_btn, PALETTE["primary"], "#1747d1")
        show_btn = Button(
            search_wrap,
            text="Show All",
            command=self.show,
            relief=FLAT,
            bd=0,
            cursor="hand2",
            bg=PALETTE["secondary"],
            activebackground=PALETTE["secondary"],
            activeforeground="white",
            fg="white",
            font=("Segoe UI Semibold", 10, "bold"),
        )
        show_btn.place(x=309, y=44, width=70, height=30)
        add_hover(show_btn, PALETTE["secondary"], "#0e9992")

        table_wrap = create_card(product_frame, bg="#f7f9ff")
        table_wrap.place(x=18, y=198, width=394, height=394)
        scrolly = Scrollbar(table_wrap, orient=VERTICAL)
        scrollx = Scrollbar(table_wrap, orient=HORIZONTAL)
        self.product_Table = ttk.Treeview(
            table_wrap,
            columns=("Pid", "name", "price", "qty", "status"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set,
            style="Inventory.Treeview",
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.heading("Pid", text="Pid")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="Qty")
        self.product_Table.heading("status", text="Status")
        self.product_Table["show"] = "headings"
        self.product_Table.column("Pid", width=45)
        self.product_Table.column("name", width=110)
        self.product_Table.column("price", width=84)
        self.product_Table.column("qty", width=48)
        self.product_Table.column("status", width=88)
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)

        Label(
            product_frame,
            text="Tip: enter 0 quantity to remove an item from the cart.",
            bg=PALETTE["surface"],
            fg=PALETTE["danger"],
            font=FONT["small"],
        ).place(x=20, y=605)

    def _build_customer_panel(self):
        customer_frame = create_card(self.root, bg=PALETTE["surface"])
        customer_frame.place(x=464, y=116, width=454, height=110)

        Label(customer_frame, text="Customer details", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["heading"]).place(x=22, y=18)
        Label(customer_frame, text="Fill in customer info before generating the final bill.", bg=PALETTE["surface"], fg=PALETTE["muted"], font=FONT["small"]).place(x=22, y=46)

        self.var_cname = StringVar()
        self.var_contact = StringVar()

        Label(customer_frame, text="Name", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["body_bold"]).place(x=22, y=74)
        Entry(customer_frame, textvariable=self.var_cname, font=("Segoe UI", 12), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=76, y=72, width=160, height=28)

        Label(customer_frame, text="Contact", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["body_bold"]).place(x=256, y=74)
        Entry(customer_frame, textvariable=self.var_contact, font=("Segoe UI", 12), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=323, y=72, width=108, height=28)

    def _build_center_panel(self):
        center_panel = create_card(self.root, bg=PALETTE["surface"])
        center_panel.place(x=464, y=242, width=454, height=390)

        Label(center_panel, text="Order flow", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=22, y=18)
        self.live_hint = Label(center_panel, text="Live total updates while you edit the cart.", bg=PALETTE["surface"], fg=PALETTE["primary"], font=FONT["small"])
        self.live_hint.place(x=22, y=54)

        info_panel = create_card(center_panel, bg="#13213d")
        info_panel.place(x=20, y=88, width=208, height=280)
        Frame(info_panel, bg="#1b315e", bd=0, highlightthickness=0).place(x=16, y=16, width=176, height=74)
        Label(info_panel, text="Billing guide", bg="#13213d", fg="white", font=("Georgia", 18, "bold")).place(x=24, y=38)
        Label(info_panel, text="1. Search a product", bg="#13213d", fg="#c8d5ef", font=FONT["body_bold"]).place(x=24, y=118)
        Label(info_panel, text="2. Choose quantity", bg="#13213d", fg="#c8d5ef", font=FONT["body_bold"]).place(x=24, y=150)
        Label(info_panel, text="3. Add or update cart", bg="#13213d", fg="#c8d5ef", font=FONT["body_bold"]).place(x=24, y=182)
        Label(info_panel, text="4. Generate and print bill", bg="#13213d", fg="#c8d5ef", font=FONT["body_bold"]).place(x=24, y=214)
        Label(info_panel, text="Simple flow, fewer distractions.", bg="#13213d", fg="#8fc3ff", font=FONT["small"]).place(x=24, y=248)

        cart_frame = create_card(center_panel, bg="#f7f9ff")
        cart_frame.place(x=244, y=88, width=192, height=280)
        self.cartTitle = Label(cart_frame, text="Cart | Total Products [0]", bg="#f7f9ff", fg=PALETTE["text"], font=FONT["body_bold"])
        self.cartTitle.pack(side=TOP, fill=X, pady=(10, 4))

        scrolly = Scrollbar(cart_frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_frame, orient=HORIZONTAL)
        self.cartTable = ttk.Treeview(
            cart_frame,
            columns=("Pid", "name", "price", "qty"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set,
            style="Inventory.Treeview",
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)
        self.cartTable.heading("Pid", text="Pid")
        self.cartTable.heading("name", text="Name")
        self.cartTable.heading("price", text="Price")
        self.cartTable.heading("qty", text="Qty")
        self.cartTable["show"] = "headings"
        self.cartTable.column("Pid", width=40)
        self.cartTable.column("name", width=92)
        self.cartTable.column("price", width=78)
        self.cartTable.column("qty", width=48)
        self.cartTable.pack(fill=BOTH, expand=1, padx=8, pady=(0, 10))
        self.cartTable.bind("<ButtonRelease-1>", self.get_data_cart)

    def _build_cart_controls(self):
        controls = create_card(self.root, bg=PALETTE["surface"])
        controls.place(x=464, y=646, width=454, height=116)

        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        Label(controls, text="Product", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["body_bold"]).place(x=18, y=18)
        Entry(controls, textvariable=self.var_pname, state="readonly", relief=FLAT, bg=PALETTE["surface_alt"], font=("Segoe UI", 11)).place(x=18, y=44, width=170, height=30)

        Label(controls, text="Price", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["body_bold"]).place(x=202, y=18)
        Entry(controls, textvariable=self.var_price, state="readonly", relief=FLAT, bg=PALETTE["surface_alt"], font=("Segoe UI", 11)).place(x=202, y=44, width=90, height=30)

        Label(controls, text="Qty", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["body_bold"]).place(x=306, y=18)
        Entry(controls, textvariable=self.var_qty, relief=FLAT, bg=PALETTE["surface_alt"], font=("Segoe UI", 11)).place(x=306, y=44, width=56, height=30)

        self.lbl_instock = Label(controls, text="In Stock", bg=PALETTE["surface"], fg=PALETTE["muted"], font=FONT["small"])
        self.lbl_instock.place(x=20, y=84)

        clear_btn = Button(controls, text="Clear", command=self.clear_cart, relief=FLAT, bd=0, cursor="hand2", bg="#d9deea", fg=PALETTE["text"], font=("Segoe UI Semibold", 10, "bold"))
        clear_btn.place(x=208, y=80, width=90, height=28)
        add_hover(clear_btn, "#d9deea", "#bcc6dc", PALETTE["text"], PALETTE["text"])
        add_btn = Button(controls, text="Add | Update", command=self.add_update_cart, relief=FLAT, bd=0, cursor="hand2", bg=PALETTE["accent"], fg="white", activebackground=PALETTE["accent"], activeforeground="white", font=("Segoe UI Semibold", 10, "bold"))
        add_btn.place(x=308, y=80, width=128, height=28)
        add_hover(add_btn, PALETTE["accent"], "#e67722")

    def _build_bill_panel(self):
        bill_panel = create_card(self.root, bg=PALETTE["surface"])
        bill_panel.place(x=936, y=116, width=596, height=646)

        Label(bill_panel, text="Customer Bill", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=22, y=18)
        Label(bill_panel, text="Preview, save, and print the generated invoice here.", bg=PALETTE["surface"], fg=PALETTE["muted"], font=FONT["body"]).place(x=22, y=56)

        preview_wrap = create_card(bill_panel, bg="#0f1730")
        preview_wrap.place(x=20, y=92, width=556, height=410)
        scrolly = Scrollbar(preview_wrap, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        self.txt_bill_area = Text(
            preview_wrap,
            yscrollcommand=scrolly.set,
            bg="#0f1730",
            fg="#f5f7ff",
            insertbackground="white",
            relief=FLAT,
            font=("Consolas", 11),
        )
        self.txt_bill_area.pack(fill=BOTH, expand=1, padx=14, pady=14)
        scrolly.config(command=self.txt_bill_area.yview)

        totals = create_card(bill_panel, bg="#f7f9ff")
        totals.place(x=20, y=520, width=556, height=108)

        self.lbl_amount = Label(totals, text="Bill Amount\n0", bg="#dbe6ff", fg=PALETTE["text"], font=FONT["body_bold"])
        self.lbl_amount.place(x=10, y=12, width=170, height=42)
        self.lbl_discount = Label(totals, text="Discount\n5%", bg="#dff8ef", fg=PALETTE["text"], font=FONT["body_bold"])
        self.lbl_discount.place(x=192, y=12, width=170, height=42)
        self.lbl_net_pay = Label(totals, text="Net Pay\n0", bg="#ffe8d8", fg=PALETTE["text"], font=FONT["body_bold"])
        self.lbl_net_pay.place(x=374, y=12, width=170, height=42)

        print_btn = Button(totals, text="Print", command=self.print_bill, relief=FLAT, bd=0, cursor="hand2", bg=PALETTE["secondary"], fg="white", activebackground=PALETTE["secondary"], activeforeground="white", font=("Segoe UI Semibold", 10, "bold"))
        print_btn.place(x=10, y=68, width=170, height=28)
        add_hover(print_btn, PALETTE["secondary"], "#0e9992")
        clear_all_btn = Button(totals, text="Clear All", command=self.clear_all, relief=FLAT, bd=0, cursor="hand2", bg="#9aa4bd", fg="white", activebackground="#9aa4bd", activeforeground="white", font=("Segoe UI Semibold", 10, "bold"))
        clear_all_btn.place(x=192, y=68, width=170, height=28)
        add_hover(clear_all_btn, "#9aa4bd", "#7d89a7")
        generate_btn = Button(totals, text="Generate Bill", command=self.generate_bill, relief=FLAT, bd=0, cursor="hand2", bg=PALETTE["primary"], fg="white", activebackground=PALETTE["primary"], activeforeground="white", font=("Segoe UI Semibold", 10, "bold"))
        generate_btn.place(x=374, y=68, width=170, height=28)
        add_hover(generate_btn, PALETTE["primary"], "#1747d1")

        summary_chip = create_card(bill_panel, bg=PALETTE["primary_soft"])
        summary_chip.place(x=404, y=14, width=154, height=60)
        Label(summary_chip, text="Bill preview", bg=PALETTE["primary_soft"], fg=PALETTE["primary"], font=FONT["body_bold"]).place(x=18, y=10)
        Label(summary_chip, text="Clean receipt layout", bg=PALETTE["primary_soft"], fg=PALETTE["text"], font=FONT["small"]).place(x=18, y=30)

    def show(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows = cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert("", END, values=row)
        except Exception as ex:
            AppDialog.error(self.root, "Load Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                AppDialog.error(self.root, "Search Input", "Search input is required.")
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%" + self.var_search.get() + "%' and status='Active'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert("", END, values=row)
                else:
                    AppDialog.error(self.root, "No Record", "No matching product record was found.")
        except Exception as ex:
            AppDialog.error(self.root, "Search Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def get_data(self, ev):
        f = self.product_Table.focus()
        content = self.product_Table.item(f)
        row = content["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set("1")

    def get_data_cart(self, ev):
        f = self.cartTable.focus()
        content = self.cartTable.item(f)
        row = content["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def add_update_cart(self):
        if self.var_pid.get() == "":
            AppDialog.error(self.root, "Select Product", "Please select a product from the list.")
        elif self.var_qty.get() == "":
            AppDialog.error(self.root, "Missing Quantity", "Quantity is required.")
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            AppDialog.error(self.root, "Invalid Quantity", "Quantity cannot be greater than stock.")
        else:
            price_cal = self.var_price.get()
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]
            present = "no"
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = "yes"
                    break
                index_ += 1
            if present == "yes":
                op = AppDialog.confirm(self.root, "Update Cart", "Product already exists in the cart. Do you want to update or remove it?")
                if op is True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][3] = self.var_qty.get()
            else:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amt = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.bill_amt = self.bill_amt + (float(row[2]) * int(row[3]))
        self.discount = (self.bill_amt * 5) / 100
        self.net_pay = self.bill_amt - self.discount
        self.lbl_amount.config(text=f"Bill Amount\nRs. {str(self.bill_amt)}")
        self.lbl_net_pay.config(text=f"Net Pay\nRs. {str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart | Total Products [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_list:
                self.cartTable.insert("", END, values=row)
        except Exception as ex:
            AppDialog.error(self.root, "Cart Error", f"Error due to: {str(ex)}")

    def generate_bill(self):
        if self.var_cname.get() == "" or self.var_contact.get() == "":
            AppDialog.error(self.root, "Customer Details", "Customer details are required.")
        elif len(self.cart_list) == 0:
            AppDialog.error(self.root, "Empty Cart", "Add product to the cart first.")
        else:
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()

            fp = open(f"bill/{str(self.invoice)}.txt", "w")
            fp.write(self.txt_bill_area.get("1.0", END))
            fp.close()
            AppDialog.info(self.root, "Bill Saved", "Bill has been generated successfully.")
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f"""
\t\t\t\t MY INVENTORY
    \t\t YOUR BILL !!!
{str("=" * 68)}
  Customer Name: {self.var_cname.get()}
  Ph no. :{self.var_contact.get()}
  Bill No. {str(self.invoice)}\t\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("=" * 68)}
   Product Name\t\t\t\tQTY\t\t Price
{str("=" * 68)}
     """
        self.txt_bill_area.delete("1.0", END)
        self.txt_bill_area.insert("1.0", bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp = f"""
{str("=" * 68)}
 Bill Amount\t\t\t\t\t\tRs.{self.bill_amt}
 Discount\t\t\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\t\t\tRs.{self.net_pay}
{str("=" * 68)}\n
    """
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def bill_middle(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                qty = int(row[4]) - int(row[3])
                if int(row[3]) == int(row[4]):
                    status = "Inactive"
                if int(row[3]) != int(row[4]):
                    status = "Active"
                price = float(row[2]) * int(row[3])
                price = str(price)
                self.txt_bill_area.insert(END, "\n  " + name + "\t\t\t\t" + row[3] + "\t\tRs." + price)
                cur.execute(
                    "Update product set qty=?,status=? where pid=?",
                    (
                        qty,
                        status,
                        pid,
                    ),
                )
                con.commit()
            self.show()
        except Exception as ex:
            AppDialog.error(self.root, "Billing Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_instock.config(text="In Stock")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set("")
        self.var_contact.set("")
        self.txt_bill_area.delete("1.0", END)
        self.cartTitle.config(text="Cart | Total Products [0]")
        self.var_search.set("")
        self.clear_cart()
        self.show()
        self.show_cart()
        self.bill_update()

    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S %p")
        date_ = time.strftime("%d %b %Y")
        self.lbl_clock.config(text=f"{date_}   |   {time_}")
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            AppDialog.info(self.root, "Print", "Please wait while printing.")
            new_file = tempfile.mktemp(".txt")
            open(new_file, "w").write(self.txt_bill_area.get("1.0", END))
            os.startfile(new_file, "print")
        else:
            AppDialog.info(self.root, "Print", "Please generate a bill before printing the receipt.")

    def logout(self):
        self.root.destroy()
        from login import Login_system
        new_root = Tk()
        Login_system(new_root)
        new_root.mainloop()


if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
