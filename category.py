from tkinter import *
from tkinter import ttk
import sqlite3

from ui_theme import PALETTE, FONT, configure_root, create_card, apply_page_background
from ui_widgets import AppDialog, action_button


class categoryclass:
    def __init__(self, root):
        self.root = root
        configure_root(self.root, "Inventory Optimisation | Categories", "1270x650+250+110")
        self.root.focus_force()

        self.var_cat_id = StringVar()
        self.var_name = StringVar()
        self.showcase_offset = 0
        self.showcase_direction = 1

        apply_page_background(
            self.root,
            top="#fff8ef",
            bottom="#fde7c8",
            orbs=[
                ((-120, -80, 250, 240), "#ffe8c8"),
                ((980, -20, 1340, 250), "#fff1da"),
                ((930, 400, 1330, 760), "#ffe0b5"),
            ],
        )
        self._build_ui()
        self.show()
        self.animate_showcase()

    def _build_ui(self):
        hero = create_card(self.root, bg=PALETTE["dark"])
        hero.place(x=18, y=18, width=1234, height=92)
        Label(hero, text="Category Studio", bg=PALETTE["dark"], fg="white", font=("Georgia", 26, "bold")).place(x=22, y=18)
        Label(hero, text="Organize product categories in a lighter and more visual workspace.", bg=PALETTE["dark"], fg="#aabadd", font=FONT["body"]).place(x=24, y=56)

        control = create_card(self.root, bg=PALETTE["surface"])
        control.place(x=18, y=128, width=430, height=170)
        Label(control, text="Create category", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=20, y=18)
        Label(control, text="Category name", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["body_bold"]).place(x=20, y=74)
        Entry(control, textvariable=self.var_name, font=("Segoe UI", 12), relief=FLAT, bg=PALETTE["surface_alt"]).place(x=20, y=104, width=220, height=32)
        action_button(control, "Add", self.add, 256, 104, 72, 32, PALETTE["success"], "#168557")
        action_button(control, "Delete", self.delete, 340, 104, 72, 32, PALETTE["danger"], "#be2430")

        table_card = create_card(self.root, bg=PALETTE["surface"])
        table_card.place(x=464, y=128, width=788, height=170)
        Label(table_card, text="Existing categories", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=20, y=18)
        scrolly = Scrollbar(table_card, orient=VERTICAL)
        scrollx = Scrollbar(table_card, orient=HORIZONTAL)
        self.category_Table = ttk.Treeview(table_card, columns=("cid", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set, style="Inventory.Treeview")
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.category_Table.xview)
        scrolly.config(command=self.category_Table.yview)
        self.category_Table.heading("cid", text="C ID")
        self.category_Table.heading("name", text="NAME")
        self.category_Table["show"] = "headings"
        self.category_Table.column("cid", width=90)
        self.category_Table.column("name", width=200)
        self.category_Table.pack(fill=BOTH, expand=1, padx=20, pady=(58, 16))
        self.category_Table.bind("<ButtonRelease-1>", self.get_data)

        gallery = create_card(self.root, bg=PALETTE["surface"])
        gallery.place(x=18, y=316, width=1234, height=316)
        Label(gallery, text="Category showcase", bg=PALETTE["surface"], fg=PALETTE["text"], font=FONT["title"]).place(x=20, y=18)
        self.showcase_canvas = Canvas(gallery, bg="#fff4df", highlightthickness=0, bd=0)
        self.showcase_canvas.place(x=22, y=72, width=1190, height=222)
        self.showcase_canvas.create_oval(48, 36, 270, 186, fill="#ffd28c", outline="")
        self.showcase_canvas.create_oval(920, 34, 1135, 188, fill="#ffdca6", outline="")
        self.showcase_canvas.create_rectangle(210, 92, 980, 162, fill="#f6b85f", outline="")
        self.showcase_canvas.create_rectangle(250, 74, 330, 162, fill="#ffffff", outline="")
        self.showcase_canvas.create_rectangle(440, 74, 520, 162, fill="#ffffff", outline="")
        self.showcase_canvas.create_rectangle(630, 74, 710, 162, fill="#ffffff", outline="")
        self.showcase_canvas.create_rectangle(820, 74, 900, 162, fill="#ffffff", outline="")
        self.showcase_canvas.create_text(596, 48, text="Category flow", fill="#915d12", font=("Georgia", 22, "bold"))
        self.showcase_canvas.create_text(596, 196, text="Simple animated showcase for organizing product groups", fill="#915d12", font=FONT["body_bold"])
        self.folder_a = self.showcase_canvas.create_rectangle(300, 82, 390, 154, fill="#fffbf4", outline="#d89d47", width=2)
        self.folder_b = self.showcase_canvas.create_rectangle(490, 82, 580, 154, fill="#fffbf4", outline="#d89d47", width=2)
        self.folder_c = self.showcase_canvas.create_rectangle(680, 82, 770, 154, fill="#fffbf4", outline="#d89d47", width=2)

    def animate_showcase(self):
        step = self.showcase_direction * 3
        for item in (self.folder_a, self.folder_b, self.folder_c):
            self.showcase_canvas.move(item, step, 0)
        coords = self.showcase_canvas.coords(self.folder_c)
        if coords[2] >= 840 or self.showcase_canvas.coords(self.folder_a)[0] <= 280:
            self.showcase_direction *= -1
        self.root.after(70, self.animate_showcase)

    def add(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                AppDialog.error(self.root, "Missing Name", "Category name is required.")
            else:
                cur.execute("select * from category where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    AppDialog.error(self.root, "Duplicate Category", "That category already exists.")
                else:
                    cur.execute("Insert into category (name) values(?)", (self.var_name.get(),))
                    con.commit()
                    AppDialog.info(self.root, "Category Saved", "Category added successfully.")
                    self.var_name.set("")
                    self.show()
        except Exception as ex:
            AppDialog.error(self.root, "Database Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            cur.execute("select * from category")
            rows = cur.fetchall()
            self.category_Table.delete(*self.category_Table.get_children())
            for row in rows:
                self.category_Table.insert("", END, values=row)
        except Exception as ex:
            AppDialog.error(self.root, "Load Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def get_data(self, ev):
        f = self.category_Table.focus()
        content = self.category_Table.item(f)
        row = content["values"]
        if not row:
            return
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con = sqlite3.connect(database=r"io.db")
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                AppDialog.error(self.root, "Select Category", "Please select a category from the list.")
            else:
                cur.execute("select * from category where cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row is None:
                    AppDialog.error(self.root, "Missing Record", "That category no longer exists.")
                else:
                    op = AppDialog.confirm(self.root, "Delete Category", "Do you really want to delete this category?")
                    if op is True:
                        cur.execute("delete from category where cid=?", (self.var_cat_id.get(),))
                        con.commit()
                        AppDialog.info(self.root, "Category Deleted", "Category deleted successfully.")
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            AppDialog.error(self.root, "Delete Error", f"Error due to: {str(ex)}")
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = categoryclass(root)
    root.mainloop()
