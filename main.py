import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

def main():
    root = tk.Tk()
    root.title("Demo GUI App")
    root.geometry("560x420")
    root.minsize(520, 380)

    # --- Style (simple modern-ish look) ---
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    root.configure(bg="#f3f4f6")

    style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
    style.configure("Sub.TLabel", font=("Segoe UI", 10), foreground="#555")
    style.configure("Card.TFrame", background="#ffffff")
    style.configure("CardTitle.TLabel", font=("Segoe UI", 11, "bold"), background="#ffffff")
    style.configure("CardBody.TLabel", font=("Segoe UI", 10), background="#ffffff")
    style.configure("Accent.TButton", padding=(12, 6))
    style.configure("TButton", padding=(10, 6))

    # --- State ---
    name_var = tk.StringVar(value="")
    status_var = tk.StringVar(value="Ready.")
    todo_var = tk.StringVar(value="")

    # Theme state
    is_dark = {"value": False}

    def set_status(msg: str):
        status_var.set(f"{msg}  •  {datetime.now().strftime('%H:%M:%S')}")

    def say_hello():
        name = name_var.get().strip() or "there"
        set_status(f"Hello, {name}!")

    def clear_name():
        name_var.set("")
        set_status("Cleared name.")

    # --- To-do / Notes feature ---
    def add_todo():
        text = todo_var.get().strip()
        if not text:
            set_status("Nothing to add.")
            return
        todo_list.insert("end", text)
        todo_var.set("")
        set_status("Added item.")

    def delete_selected():
        sel = list(todo_list.curselection())
        if not sel:
            set_status("No item selected.")
            return
        # delete from bottom to top so indexes stay valid
        for idx in reversed(sel):
            todo_list.delete(idx)
        set_status("Deleted selected item(s).")

    def edit_selected(_event=None):
        sel = todo_list.curselection()
        if not sel:
            return
        idx = sel[0]
        current = todo_list.get(idx)
        new_text = simpledialog.askstring("Edit item", "Update text:", initialvalue=current, parent=root)
        if new_text is None:
            return
        new_text = new_text.strip()
        if not new_text:
            messagebox.showinfo("Edit item", "Item cannot be empty.")
            return
        todo_list.delete(idx)
        todo_list.insert(idx, new_text)
        set_status("Updated item.")

    def clear_all():
        if todo_list.size() == 0:
            set_status("List already empty.")
            return
        if messagebox.askyesno("Clear all", "Clear all items?", parent=root):
            todo_list.delete(0, "end")
            set_status("Cleared all items.")

    # --- Theme toggle ---
    def apply_theme(dark: bool):
        bg = "#0f172a" if dark else "#f3f4f6"
        fg_header = "#e5e7eb" if dark else "#111827"
        fg_sub = "#9ca3af" if dark else "#555"
        card_bg = "#111827" if dark else "#ffffff"
        card_fg_title = "#e5e7eb" if dark else "#111827"
        card_fg_body = "#cbd5e1" if dark else "#374151"

        root.configure(bg=bg)
        header.configure(background=bg, foreground=fg_header)
        sub.configure(background=bg, foreground=fg_sub)

        style.configure("Card.TFrame", background=card_bg)
        style.configure("CardTitle.TLabel", background=card_bg, foreground=card_fg_title)
        style.configure("CardBody.TLabel", background=card_bg, foreground=card_fg_body)

        # Some widgets (Listbox) are tk widgets, so style them directly:
        todo_list.configure(
            bg=("#0b1220" if dark else "#ffffff"),
            fg=("#e5e7eb" if dark else "#111827"),
            highlightbackground=card_bg,
            selectbackground=("#334155" if dark else "#c7d2fe"),
            selectforeground=("#ffffff" if dark else "#111827"),
        )

    def toggle_theme():
        is_dark["value"] = not is_dark["value"]
        apply_theme(is_dark["value"])
        set_status("Theme toggled.")

    # --- Layout ---
    container = ttk.Frame(root)
    container.pack(fill="both", expand=True, padx=18, pady=16)

    header = ttk.Label(container, text="Demo Dashboard", style="Header.TLabel")
    header.pack(anchor="w")
    header.configure(background=root.cget("bg"), foreground="#111827")

    sub = ttk.Label(container, text="A short, simple GUI for presentation/demo purposes.", style="Sub.TLabel")
    sub.pack(anchor="w", pady=(2, 12))
    sub.configure(background=root.cget("bg"), foreground="#555")

    # Card 1: Quick Action
    card1 = ttk.Frame(container, style="Card.TFrame")
    card1.pack(fill="x", padx=2, pady=2)

    inner1 = ttk.Frame(card1, padding=14, style="Card.TFrame")
    inner1.pack(fill="x")

    ttk.Label(inner1, text="Quick Action", style="CardTitle.TLabel").pack(anchor="w")
    ttk.Label(
        inner1,
        text="Enter your name and click “Greet”. Try toggling theme for a nicer demo.",
        style="CardBody.TLabel",
        wraplength=520,
        justify="left",
    ).pack(anchor="w", pady=(6, 10))

    row1 = ttk.Frame(inner1, style="Card.TFrame")
    row1.pack(fill="x", pady=(0, 10))

    entry = ttk.Entry(row1, textvariable=name_var)
    entry.pack(side="left", fill="x", expand=True)
    entry.focus_set()

    ttk.Button(row1, text="Greet", style="Accent.TButton", command=say_hello).pack(side="left", padx=(10, 0))

    btns1 = ttk.Frame(inner1, style="Card.TFrame")
    btns1.pack(fill="x")

    ttk.Button(btns1, text="Toggle Theme", command=toggle_theme).pack(side="left")
    ttk.Button(btns1, text="Clear Name", command=clear_name).pack(side="left", padx=(8, 0))
    ttk.Button(btns1, text="Quit", command=root.destroy).pack(side="right")

    # Card 2: To-do / Notes
    card2 = ttk.Frame(container, style="Card.TFrame")
    card2.pack(fill="both", expand=True, padx=2, pady=(12, 2))

    inner2 = ttk.Frame(card2, padding=14, style="Card.TFrame")
    inner2.pack(fill="both", expand=True)

    ttk.Label(inner2, text="To‑Do / Notes", style="CardTitle.TLabel").pack(anchor="w")
    ttk.Label(
        inner2,
        text="Add small demo notes. Double‑click an item to edit it.",
        style="CardBody.TLabel",
    ).pack(anchor="w", pady=(6, 10))

    row2 = ttk.Frame(inner2, style="Card.TFrame")
    row2.pack(fill="x")

    todo_entry = ttk.Entry(row2, textvariable=todo_var)
    todo_entry.pack(side="left", fill="x", expand=True)

    ttk.Button(row2, text="Add", style="Accent.TButton", command=add_todo).pack(side="left", padx=(10, 0))

    # List + scrollbar
    list_frame = ttk.Frame(inner2, style="Card.TFrame")
    list_frame.pack(fill="both", expand=True, pady=(10, 10))

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
    todo_list = tk.Listbox(
        list_frame,
        height=8,
        activestyle="none",
        bd=0,
        highlightthickness=1,
        yscrollcommand=scrollbar.set,
        selectmode="extended",
    )
    scrollbar.config(command=todo_list.yview)

    todo_list.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    todo_list.bind("<Double-Button-1>", edit_selected)

    # To-do buttons
    btns2 = ttk.Frame(inner2, style="Card.TFrame")
    btns2.pack(fill="x")

    ttk.Button(btns2, text="Edit", command=edit_selected).pack(side="left")
    ttk.Button(btns2, text="Delete Selected", command=delete_selected).pack(side="left", padx=(8, 0))
    ttk.Button(btns2, text="Clear All", command=clear_all).pack(side="right")

    # Status bar
    status = ttk.Label(container, textvariable=status_var)
    status.pack(fill="x", pady=(12, 0))
    set_status("Ready.")

    # Key bindings
    root.bind("<Return>", lambda _e: say_hello())
    todo_entry.bind("<Return>", lambda _e: add_todo())
    root.bind("<Delete>", lambda _e: delete_selected())

    # Apply initial theme
    apply_theme(False)

    root.mainloop()

if __name__ == "__main__":
    main()