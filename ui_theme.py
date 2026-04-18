from tkinter import Canvas, Frame, ttk


PALETTE = {
    "bg": "#0b1020",
    "bg_alt": "#111936",
    "surface": "#ffffff",
    "surface_alt": "#eef3ff",
    "card": "#f7f9ff",
    "primary": "#2962ff",
    "primary_soft": "#dbe6ff",
    "secondary": "#11b5ae",
    "accent": "#ff8a3d",
    "text": "#16213e",
    "muted": "#5c6884",
    "success": "#1f9d6a",
    "warning": "#ffb703",
    "danger": "#e63946",
    "dark": "#16213e",
    "dark_alt": "#1d2747",
}

FONT = {
    "display": ("Georgia", 28, "bold"),
    "title": ("Bahnschrift SemiBold", 22, "bold"),
    "heading": ("Bahnschrift SemiBold", 16, "bold"),
    "body": ("Segoe UI", 11),
    "body_bold": ("Segoe UI Semibold", 11, "bold"),
    "small": ("Segoe UI", 10),
    "mono": ("Consolas", 11),
}


def configure_root(root, title, geometry):
    root.title(title)
    root.geometry(geometry)
    root.configure(bg=PALETTE["bg"])
    style_ttk(root)


def style_ttk(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(
        "Inventory.Treeview",
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        fieldbackground=PALETTE["surface"],
        rowheight=30,
        borderwidth=0,
        font=FONT["body"],
    )
    style.configure(
        "Inventory.Treeview.Heading",
        background=PALETTE["dark"],
        foreground="white",
        relief="flat",
        padding=(10, 8),
        font=FONT["body_bold"],
    )
    style.map(
        "Inventory.Treeview",
        background=[("selected", PALETTE["primary"])],
        foreground=[("selected", "white")],
    )
    style.map(
        "Inventory.Treeview.Heading",
        background=[("active", PALETTE["primary"])],
    )
    style.configure(
        "Inventory.TCombobox",
        fieldbackground=PALETTE["surface"],
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        borderwidth=0,
        arrowsize=16,
        padding=6,
        font=FONT["body"],
    )


def create_card(parent, bg=None, bd=0):
    return Frame(
        parent,
        bg=bg or PALETTE["surface"],
        bd=bd,
        highlightthickness=0,
    )


def draw_vertical_gradient(canvas, top, bottom):
    canvas.update_idletasks()
    width = max(canvas.winfo_width(), 2)
    height = max(canvas.winfo_height(), 2)
    canvas.delete("gradient")

    r1, g1, b1 = canvas.winfo_rgb(top)
    r2, g2, b2 = canvas.winfo_rgb(bottom)

    r_ratio = float(r2 - r1) / height
    g_ratio = float(g2 - g1) / height
    b_ratio = float(b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f"#{nr // 256:02x}{ng // 256:02x}{nb // 256:02x}"
        canvas.create_line(0, i, width, i, tags=("gradient",), fill=color)

    canvas.lower("gradient")


def pulse_label(label, colors, delay=700, index=0):
    label.configure(fg=colors[index % len(colors)])
    label.after(delay, lambda: pulse_label(label, colors, delay, index + 1))


def animate_counter(label, prefix, value, suffix="", start=0, step=1, delay=15):
    if start >= value:
        label.configure(text=f"{prefix}{value}{suffix}")
        return
    label.configure(text=f"{prefix}{start}{suffix}")
    label.after(delay, lambda: animate_counter(label, prefix, value, suffix, start + step, step, delay))


def rounded_badge(parent, text, bg, fg="white"):
    badge = Frame(parent, bg=bg, bd=0, highlightthickness=0)
    badge_label = ttk.Label(badge, text=text)
    badge_label.configure(background=bg, foreground=fg, font=FONT["small"])
    badge_label.pack(padx=10, pady=4)
    return badge


def add_orb(canvas, x1, y1, x2, y2, color, alpha_tag):
    return canvas.create_oval(x1, y1, x2, y2, fill=color, outline="", tags=alpha_tag)


def apply_page_background(root, top="#eef3ff", bottom="#dce7ff", orbs=None):
    canvas = Canvas(root, highlightthickness=0, bd=0)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.bind("<Configure>", lambda e: draw_vertical_gradient(canvas, top, bottom))
    for coords, color in (orbs or []):
        canvas.create_oval(*coords, fill=color, outline="")
    return canvas
