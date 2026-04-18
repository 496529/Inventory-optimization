import tkinter

from  tkinter import *
from tkinter import ttk
import sqlite3

from ui_theme import PALETTE, FONT, configure_root, create_card, apply_page_background
from ui_widgets import AppDialog, action_button


class emploeeclass:
    def __init__(self, root):
        self.root = root
        configure_root(self.root, "Inventory Optimisation | Employees", "1270x650+250+110")
        self.root.focus_force()
        apply_page_background(
            self.root,
            top="#eef3ff",
            bottom="#dde8ff",
            orbs=[
                ((-80, -50, 250, 220), "#d8e6ff"),
                ((920, -40, 1280, 220), "#e3f8ef"),
                ((980, 420, 1340, 760), "#ffe8dc"),
            ],
        )

        self.var_searchby = StringVar(value="Select")
        self.var_searchtxt = StringVar()
        self.var_emp_id = StringVar()
        self.var_emp_gender = StringVar(value="Select")
        self.var_emp_contact = StringVar()
        self.var_emp_name = StringVar()
        self.var_emp_doj = StringVar()
        self.var_emp_email = StringVar()
        self.var_emp_pass = StringVar()
        self.var_emp_utype = StringVar(value="Select")
        self.var_emp_dob = StringVar()
        self.var_emp_salary = StringVar()

        self._build_ui()
        self.show()

    def _build_ui(self):
        hero = create_card(self.root, bg=PALETTE["dark"])
        hero.place(x=18, y=18, width=1234, height=92)
        Label(hero, text="Employee Management", bg=PALETTE["dark"], fg="white", font=("Georgia", 26, "bold")).place(x=22, y=18)
        Label(hero, text="Create, update, search, and review employee records in one clean workspace.", bg=PALETTE["dark"], fg="#aabadd", font=FONT["body"]).place(x=24, y=56)

        search_card = create_card(self.root, bg=PALETTE["surface"])
        search_card.place(x=18, y=128, width=1234, height=74)
        Label(search_card, text="Search employees", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["heading"]).place(x=20, y=14)
        self.cmb_search = ttk.Combobox(search_card, textvariable=self.var_searchby, values=("Select", "email", "name", "contact"), state="readonly", justify=CENTER, style="Inventory.TCombobox", font=FONT["body"])
        self.cmb_search.place(x=20, y=38, width=180, height=28)
        Entry(search_card, textvariable=self.var_searchtxt, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=218, y=38, width=260, height=28)
        action_button(search_card, "Search", self.search, 494, 38, 110, 28, PALETTE["primary"], "#1747d1")
        action_button(search_card, "Reset", self.clear, 618, 38, 110, 28, PALETTE["secondary"], "#0e9992")

        form_card = create_card(self.root, bg=PALETTE["surface"])
        form_card.place(x=18, y=220, width=1234, height=190)
        Label(form_card, text="Employee details", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["heading"]).place(x=20, y=16)

        labels = [
            ("Emp ID", 20, 56), ("Gender", 328, 56), ("Contact", 636, 56),
            ("Name", 20, 104), ("D.O.B", 328, 104), ("D.O.J", 636, 104),
            ("Email", 20, 152), ("Password", 328, 152), ("User Type", 636, 152),
            ("Address", 944, 56), ("Salary", 944, 152),
        ]
        for text, x, y in labels:
            Label(form_card, text=text, bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["body_bold"]).place(x=x, y=y)

        Entry(form_card, textvariable=self.var_emp_id, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=108, y=54, width=180, height=28)
        self.cmb_gender = ttk.Combobox(form_card, textvariable=self.var_emp_gender, values=("Select", "Male", "Female", "Other"), state="readonly", justify=CENTER, style="Inventory.TCombobox", font=FONT["body"])
        self.cmb_gender.place(x=416, y=54, width=180, height=28)
        Entry(form_card, textvariable=self.var_emp_contact, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=724, y=54, width=180, height=28)
        Entry(form_card, textvariable=self.var_emp_name, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=108, y=102, width=180, height=28)
        Entry(form_card, textvariable=self.var_emp_dob, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=416, y=102, width=180, height=28)
        Entry(form_card, textvariable=self.var_emp_doj, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=724, y=102, width=180, height=28)
        Entry(form_card, textvariable=self.var_emp_email, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=108, y=150, width=180, height=28)
        Entry(form_card, textvariable=self.var_emp_pass, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=416, y=150, width=180, height=28)
        self.cmb_usertype = ttk.Combobox(form_card, textvariable=self.var_emp_utype, values=("Select", "Admin", "Employee"), state="readonly", justify=CENTER, style="Inventory.TCombobox", font=FONT["body"])
        self.cmb_usertype.place(x=724, y=150, width=180, height=28)
        self.txt_address = Text(form_card, font=("Segoe UI", 10), relief=FLAT, bg=PALETTE["surface_alt"], fg=PALETTE["text"])
        self.txt_address.place(x=1014, y=54, width=190, height=74)
        Entry(form_card, textvariable=self.var_emp_salary, font=("Segoe UI", 11), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=1014, y=150, width=190, height=28)

        actions = create_card(self.root, bg=PALETTE["surface"])
        actions.place(x=18, y=426, width=1234, height=60)
        action_button(actions, "Save", self.add, 20, 14, 110, 32, PALETTE["primary"], "#1747d1")
        action_button(actions, "Update", self.update, 144, 14, 110, 32, PALETTE["success"], "#168557")
        action_button(actions, "Delete", self.delete, 268, 14, 110, 32, PALETTE["danger"], "#be2430")
        action_button(actions, "Clear", self.clear, 392, 14, 110, 32, "#9aa4bd", "#7d89a7")

        table_card = create_card(self.root, bg=PALETTE["surface"])
        table_card.place(x=18, y=502, width=1234, height=130)
        scrolly = Scrollbar(table_card, orient=VERTICAL)
        scrollx = Scrollbar(table_card, orient=HORIZONTAL)
        self.EmployeeTable = ttk.Treeview(
            table_card,
            columns=("eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set,
            style="Inventory.Treeview",
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        headings = [("eid", "EMP ID", 80), ("name", "NAME", 120), ("email", "EMAIL", 140), ("gender", "GENDER", 90), ("contact", "CONTACT", 110), ("dob", "DOB", 100), ("doj", "DOJ", 100), ("pass", "PASS", 100), ("utype", "TYPE", 90), ("address", "ADDRESS", 180), ("salary", "SALARY", 100)]
        for key, text, width in headings:
            self.EmployeeTable.heading(key, text=text)
            self.EmployeeTable.column(key, width=width)
        self.EmployeeTable["show"] = "headings"
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

    def add(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                AppDialog.error(self.root, "Missing ID", "Employee ID is required.")
            elif self.var_emp_pass.get() == "":
                AppDialog.error(self.root, "Missing Password", "Password is required.")
            else:
                cur.execute("select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    AppDialog.error(self.root, "Duplicate Employee", "This employee ID is already assigned. Try a different one.")
                else:
                    cur.execute(
                        "Insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            self.var_emp_id.get(),
                            self.var_emp_name.get(),
                            self.var_emp_email.get(),
                            self.var_emp_gender.get(),
                            self.var_emp_contact.get(),
                            self.var_emp_dob.get(),
                            self.var_emp_doj.get(),
                            self.var_emp_pass.get(),
                            self.var_emp_utype.get(),
                            self.txt_address.get("1.0", END),
                            self.var_emp_salary.get(),
                        ),
                    )
                    con.commit()
                    AppDialog.info(self.root, "Employee Saved", "Employee added successfully.")
            self.show()
        except Exception as ex:
            AppDialog.error(self.root, "Database Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            cur.execute("select * from employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert("", END, values=row)
        except Exception as ex:
            AppDialog.error(self.root, "Load Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = self.EmployeeTable.item(f)
        row = content["values"]
        if not row:
            return
        self.var_emp_id.set(row[0])
        self.var_emp_name.set(row[1])
        self.var_emp_email.set(row[2])
        self.var_emp_gender.set(row[3])
        self.var_emp_contact.set(row[4])
        self.var_emp_dob.set(row[5])
        self.var_emp_doj.set(row[6])
        self.var_emp_pass.set(row[7])
        self.var_emp_utype.set(row[8])
        self.txt_address.delete("1.0", END)
        self.txt_address.insert(END, row[9])
        self.var_emp_salary.set(row[10])

    def update(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                AppDialog.error(self.root, "Missing ID", "Employee ID is required.")
            else:
                cur.execute("select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    AppDialog.error(self.root, "Invalid Employee", "No employee exists with that ID.")
                else:
                    cur.execute(
                        "Update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",
                        (
                            self.var_emp_name.get(),
                            self.var_emp_email.get(),
                            self.var_emp_gender.get(),
                            self.var_emp_contact.get(),
                            self.var_emp_dob.get(),
                            self.var_emp_doj.get(),
                            self.var_emp_pass.get(),
                            self.var_emp_utype.get(),
                            self.txt_address.get("1.0", END),
                            self.var_emp_salary.get(),
                            self.var_emp_id.get(),
                        ),
                    )
                    con.commit()
                    AppDialog.info(self.root, "Employee Updated", "Employee updated successfully.")
                    self.show()
        except Exception as ex:
            AppDialog.error(self.root, "Update Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                AppDialog.error(self.root, "Missing ID", "Employee ID is required.")
            else:
                cur.execute("select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    AppDialog.error(self.root, "Invalid Employee", "No employee exists with that ID.")
                else:
                    op = AppDialog.confirm(self.root, "Delete Employee", "Do you really want to delete this employee?")
                    if op is True:
                        cur.execute("delete from employee where eid=?", (self.var_emp_id.get(),))
                        con.commit()
                        AppDialog.info(self.root, "Employee Deleted", "Employee deleted successfully.")
                        self.clear()
        except Exception as ex:
            AppDialog.error(self.root, "Delete Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def clear(self):
        self.var_emp_id.set("")
        self.var_emp_name.set("")
        self.var_emp_email.set("")
        self.var_emp_gender.set("Select")
        self.var_emp_contact.set("")
        self.var_emp_dob.set("")
        self.var_emp_doj.set("")
        self.var_emp_pass.set("")
        self.var_emp_utype.set("Select")
        self.txt_address.delete("1.0", END)
        self.var_emp_salary.set("")
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
                cur.execute("select * from employee where " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert("", END, values=row)
                else:
                    AppDialog.error(self.root, "No Record", "No matching employee record was found.")
        except Exception as ex:
            AppDialog.error(self.root, "Search Error", f"Error due to: {str(ex)}")
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = emploeeclass(root)
    root.mainloop()
