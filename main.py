import tkinter as tk
from tkinter import ttk
from datetime import datetime

def main():
    root = tk.Tk()
    root.title("Demo GUI App")
    root.geometry("520x320")
    root.minsize(480, 300)

    # --- Style (simple modern-ish look) ---
    style = ttk.Style(root)
    # Use a native theme when available
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
    style.configure("Sub.TLabel", font=("Segoe UI", 10), foreground="#555")
    style.configure("Card.TFrame", background="#ffffff")
    style.configure("CardTitle.TLabel", font=("Segoe UI", 11, "bold"), background="#ffffff")
    style.configure("CardBody.TLabel", font=("Segoe UI", 10), background="#ffffff")
    style.configure("Accent.TButton", padding=(12, 6))
    style.configure("TButton", padding=(10, 6))

    root.configure(bg="#f3f4f6")

    # --- State ---
    name_var = tk.StringVar(value="")
    status_var = tk.StringVar(value="Ready.")

    def set_status(msg: str):
        status_var.set(f"{msg}  •  {datetime.now().strftime('%H:%M:%S')}")

    def say_hello():
        name = name_var.get().strip() or "there"
        set_status(f"Hello, {name}!")

    def clear():
        name_var.set("")
        set_status("Cleared.")

    def toggle_theme():
        # Quick light/dark-ish toggle by swapping root background + card
        bg = root.cget("bg")
        dark = (bg != "#0f172a")
        root.configure(bg="#0f172a" if dark else "#f3f4f6")
        header.configure(background=root.cget("bg"), foreground="#e5e7eb" if dark else "#111827")
        sub.configure(background=root.cget("bg"), foreground="#9ca3af" if dark else "#555")

        card_bg = "#111827" if dark else "#ffffff"
        card.configure(style="Card.TFrame")
        style.configure("Card.TFrame", background=card_bg)
        style.configure("CardTitle.TLabel", background=card_bg, foreground="#e5e7eb" if dark else "#111827")
        style.configure("CardBody.TLabel", background=card_bg, foreground="#cbd5e1" if dark else "#374151")

        set_status("Theme toggled.")

    # --- Layout ---
    container = ttk.Frame(root)
    container.pack(fill="both", expand=True, padx=18, pady=16)
    container.configure(style="TFrame")

    header = ttk.Label(container, text="Demo Dashboard", style="Header.TLabel")
    header.pack(anchor="w")
    header.configure(background=root.cget("bg"), foreground="#111827")

    sub = ttk.Label(container, text="A short, simple GUI for presentation/demo purposes.", style="Sub.TLabel")
    sub.pack(anchor="w", pady=(2, 12))
    sub.configure(background=root.cget("bg"), foreground="#555")

    # Card
    card = ttk.Frame(container, style="Card.TFrame")
    card.pack(fill="x", padx=2, pady=2)

    # Fake "card shadow" effect using outer padding + bg
    card_pad = ttk.Frame(container)
    card_pad.pack(fill="x")
    card_pad.pack_propagate(False)

    inner = ttk.Frame(card, padding=14, style="Card.TFrame")
    inner.pack(fill="x")

    title = ttk.Label(inner, text="Quick Action", style="CardTitle.TLabel")
    title.pack(anchor="w")

    body = ttk.Label(
        inner,
        text="Enter your name and click “Greet”. Try toggling theme for a nicer demo.",
        style="CardBody.TLabel",
        wraplength=460,
        justify="left",
    )
    body.pack(anchor="w", pady=(6, 10))

    row = ttk.Frame(inner, style="Card.TFrame")
    row.pack(fill="x", pady=(0, 10))

    entry = ttk.Entry(row, textvariable=name_var)
    entry.pack(side="left", fill="x", expand=True)
    entry.focus_set()

    greet_btn = ttk.Button(row, text="Greet", style="Accent.TButton", command=say_hello)
    greet_btn.pack(side="left", padx=(10, 0))

    # Buttons
    btns = ttk.Frame(inner, style="Card.TFrame")
    btns.pack(fill="x")

    ttk.Button(btns, text="Toggle Theme", command=toggle_theme).pack(side="left")
    ttk.Button(btns, text="Clear", command=clear).pack(side="left", padx=(8, 0))
    ttk.Button(btns, text="Quit", command=root.destroy).pack(side="right")

    # Status bar
    status = ttk.Label(container, textvariable=status_var)
    status.pack(fill="x", pady=(12, 0))
    set_status("Ready.")

    # Enter key triggers greet
    root.bind("<Return>", lambda _e: say_hello())

    root.mainloop()

if __name__ == "__main__":
    main()