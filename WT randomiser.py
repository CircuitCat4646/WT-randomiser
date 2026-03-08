import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import random

CSV_FILE = "vehicles.csv"
FIELDS = ["name", "type", "subtype", "nation", "br", "rank", "premium"]

NATION_NAMES = {
    "usa": "United States",
    "ger": "Germany",
    "ussr": "USSR",
    "uk": "Great Britan",
    "jap": "Japan",
    "chi": "China",
    "ita": "Italy",
    "fra": "France",
    "swe": "Sweden",
    "isr": "Israel",
}

VEHICLE_TYPES = {
    "air": "Aircraft",
    "ground": "Ground Vehicle",
}

SUBTYPE_OPTIONS = {
    "air":    ["fighter", "interceptor", "strike", "bomber"],
    "ground": ["light", "medium", "heavy", "td", "spaa"],
}

VEHICLE_SUBTYPES = {
    "fighter": "Fighter",
    "interceptor": "Interceptor",
    "strike": "Strike Aircraft",
    "bomber": "Bomber",
    "light": "Light Tank",
    "medium": "Medium Tank",
    "heavy": "Heavy Tank",
    "td": "Tank Destroyer",
    "spaa": "Anti-Air",
}

RANK_NAMES = {
    "1": "I",
    "2": "II",
    "3": "III",
    "4": "IV",
    "5": "V",
    "6": "VI",
    "7": "VII",
    "8": "VIII",
    "9": "IX",
}

def load_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
    rows = []
    with open(CSV_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def save_row(row):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(row)


def delete_row_from_csv(index):
    rows = load_csv()
    if 0 <= index < len(rows):
        rows.pop(index)
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)


class CSVManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("War Thunder Randomiser")
        self.root.geometry("1080x800")
        self.root.configure(bg="#1e1e2e")
        self._apply_styles()
        self._build_tabs()
        self.refresh_table()

    def _apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2a2a3e", foreground="#cdd6f4",
                        rowheight=26, fieldbackground="#2a2a3e",
                        font=("Consolas", 10))
        style.configure("Treeview.Heading",
                        background="#313244", foreground="#cba6f7",
                        font=("Consolas", 10, "bold"))
        style.map("Treeview", background=[("selected", "#45475a")])
        style.configure("TNotebook", background="#1e1e2e", borderwidth=0)
        style.configure("TNotebook.Tab",
                        background="#313244", foreground="#a6adc8",
                        font=("Consolas", 11, "bold"), padding=[18, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", "#1e1e2e")],
                  foreground=[("selected", "#cba6f7")])

    def _build_tabs(self):
        tk.Label(self.root, text="War Thunder Randomiser",
                 bg="#1e1e2e", fg="#cba6f7",
                 font=("Consolas", 16, "bold")).pack(pady=(14, 6))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.tab_manager = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(self.tab_manager, text="  📋  Vehicle Manager  ")
        self._build_manager_tab(self.tab_manager)

        self.tab_random = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(self.tab_random, text="  🎲  Randomiser  ")
        self._build_randomiser_tab(self.tab_random)

    # ── Tab 1: Manager ─────────────────────────────────────────

    def _build_manager_tab(self, parent):
        form_frame = tk.Frame(parent, bg="#1e1e2e")
        form_frame.pack(fill="x", padx=20, pady=10)

        self.entries = {}
        labels = {"name": "Name", "type": "Type", "subtype": "Subtype", "nation": "Nation",
                  "br": "BR", "rank": "Rank", "premium": "Premium"}

        for col, (field, label) in enumerate(labels.items()):
            tk.Label(form_frame, text=label, bg="#1e1e2e", fg="#a6adc8",
                     font=("Consolas", 9)).grid(row=0, column=col, padx=6, sticky="w")
            
            if field == "type":
                var = tk.StringVar(value="Choose")
                cb = ttk.Combobox(form_frame, textvariable=var,
                                  values=["air", "ground"], width=10, state="readonly")
                cb.grid(row=1, column=col, padx=6, pady=4)
                self.entries[field] = var
                cb.bind("<<ComboboxSelected>>", self._on_type_change)
            
            elif field == "subtype":
                var = tk.StringVar(value="Choose")
                cb = ttk.Combobox(form_frame, textvariable=var,
                                  values=[], width=10, state="readonly")
                cb.grid(row=1, column=col, padx=6, pady=4)
                self.entries[field] = var
                self.subtype_cb = cb
            
            elif field == "nation":
                var = tk.StringVar(value="Choose")
                cb = ttk.Combobox(form_frame, textvariable=var,
                                  values=["usa", "ger", "ussr", "uk", "jap", "chi", "ita", "fra", "swe", "isr"], width=10, state="readonly")
                cb.grid(row=1, column=col, padx=6, pady=4)
                self.entries[field] = var
            
            elif field == "rank":
                var = tk.StringVar(value="Choose")
                cb = ttk.Combobox(form_frame, textvariable=var,
                                  values=["1", "2", "3", "4", "5", "6", "7", "8", "9"], width=10, state="readonly")
                cb.grid(row=1, column=col, padx=6, pady=4)
                self.entries[field] = var

            elif field == "premium":
                var = tk.StringVar(value="Choose")
                cb = ttk.Combobox(form_frame, textvariable=var,
                                  values=["TRUE", "FALSE"], width=10, state="readonly")
                cb.grid(row=1, column=col, padx=6, pady=4)
                self.entries[field] = var

            else:
                entry = tk.Entry(form_frame, bg="#313244", fg="#cdd6f4",
                                 insertbackground="#cdd6f4",
                                 font=("Consolas", 10), width=13,
                                 relief="flat", bd=4)
                entry.grid(row=1, column=col, padx=6, pady=4)
                self.entries[field] = entry

        btn_frame = tk.Frame(parent, bg="#1e1e2e")
        btn_frame.pack(pady=6)

        tk.Button(btn_frame, text="➕  Add Entry", command=self.add_entry,
                  bg="#a6e3a1", fg="#1e1e2e", font=("Consolas", 10, "bold"),
                  relief="flat", padx=14, pady=6, cursor="hand2").pack(side="left", padx=8)
        tk.Button(btn_frame, text="🗑  Delete Selected", command=self.delete_entry,
                  bg="#f38ba8", fg="#1e1e2e", font=("Consolas", 10, "bold"),
                  relief="flat", padx=14, pady=6, cursor="hand2").pack(side="left", padx=8)
        tk.Button(btn_frame, text="✖  Clear Fields", command=self.clear_fields,
                  bg="#89b4fa", fg="#1e1e2e", font=("Consolas", 10, "bold"),
                  relief="flat", padx=14, pady=6, cursor="hand2").pack(side="left", padx=8)

        table_frame = tk.Frame(parent, bg="#1e1e2e")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(4, 16))

        self.tree = ttk.Treeview(table_frame, columns=FIELDS,
                                 show="headings", selectmode="browse")
        col_widths = {"name": 160, "type": 110, "subtype": 110, "nation": 110,
                      "br": 70, "rank": 70, "premium": 80}
        for field in FIELDS:
            self.tree.heading(field, text=field.capitalize())
            self.tree.column(field, width=col_widths.get(field, 100), anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    # ── Tab 2: Randomiser ──────────────────────────────────────

    def _build_randomiser_tab(self, parent):
        tk.Label(parent, text="Vehicle Randomiser",
                 bg="#1e1e2e", fg="#cba6f7",
                 font=("Consolas", 14, "bold")).pack(pady=(18, 4))
        tk.Label(parent,
                 text="Filter by any combination of fields, then roll a random vehicle.",
                 bg="#1e1e2e", fg="#6c7086",
                 font=("Consolas", 9)).pack(pady=(0, 14))

        # Filters
        filter_frame = tk.LabelFrame(parent, text="  Filters  ",
                                     bg="#1e1e2e", fg="#89b4fa",
                                     font=("Consolas", 10, "bold"),
                                     relief="groove", bd=2, labelanchor="nw")
        filter_frame.pack(padx=40, fill="x", pady=(0, 16))

        self.filter_vars = {}
        filter_fields = [
            ("type",    "Type",    ["Any"]),
            ("subtype", "Subtype", ["Any"]),
            ("nation",  "Nation",  ["Any"]),
            ("br_min",  "BR Min",  ["Any"]),
            ("br_max",  "BR Max",  ["Any"]),
            ("rank",    "Rank",    ["Any"]),
            ("premium", "Premium", ["Any", "TRUE", "FALSE"]),
        ]

        for col, (field, label, base_values) in enumerate(filter_fields):
            tk.Label(filter_frame, text=label, bg="#1e1e2e", fg="#a6adc8",
                     font=("Consolas", 9)).grid(row=0, column=col, padx=16, pady=(10, 2), sticky="w")
            var = tk.StringVar(value="Any")
            cb = ttk.Combobox(filter_frame, textvariable=var,
                              values=base_values, width=14, state="readonly")
            cb.grid(row=1, column=col, padx=16, pady=(0, 12))
            self.filter_vars[field] = (var, cb)
            
            if field == "type":
                cb.bind("<<ComboboxSelected>>", self._on_filter_type_change)
            if field == "br_min":
                cb.bind("<<ComboboxSelected>>", self._on_br_min_change)

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

        # Buttons
        roll_frame = tk.Frame(parent, bg="#1e1e2e")
        roll_frame.pack(pady=6)

        tk.Button(roll_frame, text="🎲  Roll Random Vehicle",
                  command=self.roll_random,
                  bg="#cba6f7", fg="#1e1e2e",
                  font=("Consolas", 12, "bold"),
                  relief="flat", padx=20, pady=10, cursor="hand2").pack(side="left", padx=8)
        tk.Button(roll_frame, text="🔄  Reset Filters",
                  command=self.reset_filters,
                  bg="#45475a", fg="#cdd6f4",
                  font=("Consolas", 10),
                  relief="flat", padx=14, pady=10, cursor="hand2").pack(side="left", padx=8)

        # Result card
        result_outer = tk.Frame(parent, bg="#1e1e2e")
        result_outer.pack(padx=40, fill="both", expand=True, pady=(16, 0))

        tk.Label(result_outer, text="Result", bg="#1e1e2e", fg="#89b4fa",
                 font=("Consolas", 10, "bold")).pack(anchor="w")

        result_card = tk.Frame(result_outer, bg="#2a2a3e",
                               relief="flat", bd=0, padx=20, pady=16)
        result_card.pack(fill="x", pady=(4, 0))

        self.result_name = tk.Label(result_card, text="—",
                                    bg="#2a2a3e", fg="#cdd6f4",
                                    font=("Consolas", 18, "bold"))
        self.result_name.pack(anchor="w")

        self.result_details = tk.Label(result_card, text="",
                                       bg="#2a2a3e", fg="#a6adc8",
                                       font=("Consolas", 10))
        self.result_details.pack(anchor="w", pady=(4, 0))

        self.result_premium = tk.Label(result_card, text="",
                                       bg="#2a2a3e", fg="#f9e2af",
                                       font=("Consolas", 10, "bold"))
        self.result_premium.pack(anchor="w", pady=(2, 0))

        # History
        tk.Label(result_outer, text="Roll History", bg="#1e1e2e", fg="#89b4fa",
                 font=("Consolas", 10, "bold")).pack(anchor="w", pady=(16, 4))

        hist_frame = tk.Frame(result_outer, bg="#1e1e2e")
        hist_frame.pack(fill="both", expand=True, pady=(0, 16))

        self.history_box = tk.Listbox(hist_frame, bg="#2a2a3e", fg="#a6adc8",
                                      font=("Consolas", 9),
                                      selectbackground="#45475a",
                                      relief="flat", bd=0)
        hist_scroll = ttk.Scrollbar(hist_frame, orient="vertical",
                                    command=self.history_box.yview)
        self.history_box.configure(yscrollcommand=hist_scroll.set)
        self.history_box.pack(side="left", fill="both", expand=True)
        hist_scroll.pack(side="right", fill="y")

    # ── Randomiser logic ───────────────────────────────────────

    def _on_br_min_change(self, event):
        min_val = self.filter_vars["br_min"][0].get()
        max_var, max_cb = self.filter_vars["br_max"]
        rows = load_csv()
        all_br = sorted(set(r["br"] for r in rows if r.get("br")), key=lambda x: float(x))
        if min_val == "Any":
            filtered_br = all_br
        else:
            filtered_br = [br for br in all_br if float(br) >= float(min_val)]
        max_cb["values"] = ["Any"] + filtered_br
        # Reset max if it's now invalid
        if max_var.get() != "Any" and max_var.get() not in filtered_br:
            max_var.set("Any")

    def _on_type_change(self, event):
        chosen_type = self.entries["type"].get()
        options = SUBTYPE_OPTIONS.get(chosen_type, [])
        self.subtype_cb["values"] = options
        self.entries["subtype"].set("Choose" if options else "")
    
    def _on_filter_type_change(self, event):
        chosen_type = self.filter_vars["type"][0].get()
        subtype_var, subtype_cb = self.filter_vars["subtype"]
        rows = load_csv()
        if chosen_type == "Any":
            # Show all subtypes actually in the CSV
            unique = sorted(set(r["subtype"] for r in rows if r.get("subtype")))
        else:
            # Show only subtypes in the CSV that belong to the chosen type
            unique = sorted(set(r["subtype"] for r in rows if r.get("subtype") and r.get("type") == chosen_type))
        subtype_cb["values"] = ["Any"] + unique
        subtype_var.set("Any")

    def _on_tab_change(self, event):
        selected = self.notebook.index(self.notebook.select())
        if selected == 1:
            rows = load_csv()
            br_values = ["Any"] + sorted(set(r["br"] for r in rows if r.get("br")), key=lambda x: float(x))
            for field, (var, cb) in self.filter_vars.items():
                if field == "premium":
                    continue
                elif field in ("br_min", "br_max"):
                    cb["values"] = br_values
                    if var.get() not in cb["values"]:
                        var.set("Any")
                else:
                    unique = sorted(set(r[field] for r in rows if r.get(field)))
                    cb["values"] = ["Any"] + unique
                    if var.get() not in cb["values"]:
                        var.set("Any")

    def roll_random(self):
        rows = load_csv()
        if not rows:
            messagebox.showinfo("No Vehicles", "Add some vehicles first!")
            return
        filtered = rows
        for field, (var, _) in self.filter_vars.items():
            val = var.get()
            if val == "Any":
                continue
            if field == "br_min":
                filtered = [r for r in filtered if r.get("br") and float(r["br"]) >= float(val)]
            elif field == "br_max":
                filtered = [r for r in filtered if r.get("br") and float(r["br"]) <= float(val)]
            else:
                filtered = [r for r in filtered if r.get(field, "").lower() == val.lower()]
        if not filtered:
            messagebox.showinfo("No Results",
                                "No vehicles match the selected filters.\nTry broadening your filters.")
            return
        vehicle = random.choice(filtered)
        nation = NATION_NAMES.get(vehicle['nation'].lower(), vehicle['nation'])
        type = VEHICLE_TYPES.get(vehicle['type'].lower(), vehicle['type'])
        subtype = VEHICLE_SUBTYPES.get(vehicle['subtype'].lower(), vehicle['subtype'])
        rank = RANK_NAMES.get(vehicle['rank'].lower(), vehicle['rank'])
        self.result_name.config(text=vehicle.get("name", "Unknown"))
        self.result_details.config(
            text=f"Type: {type}   •   Subtype: {subtype}   •   Nation: {nation}   •   "
                 f"BR: {vehicle.get('br', '—')}   •   Rank: {rank}"
        )
        premium = vehicle.get("premium", "FALSE")
        self.result_premium.config(text="⭐ Premium Vehicle" if premium == "TRUE" else "")
        summary = (f"{vehicle.get('name')}  [{nation} / {type} / {subtype} / BR {vehicle.get('br')}]")
        self.history_box.insert(0, summary)

    def reset_filters(self):
        for _, (var, _) in self.filter_vars.items():
            var.set("Any")

    # ── Manager actions ────────────────────────────────────────

    def get_entry_value(self, field):
        return self.entries[field].get().strip()

    def add_entry(self):
        row = {f: self.get_entry_value(f) for f in FIELDS}
        if not row["name"]:
            messagebox.showwarning("Missing Field", "Name is required.")
            return
        save_row(row)
        self.refresh_table()
        self.clear_fields()

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Select a row to delete.")
            return
        index = self.tree.index(selected[0])
        if messagebox.askyesno("Confirm Delete", "Delete the selected entry?"):
            delete_row_from_csv(index)
            self.refresh_table()
            self.clear_fields()

    def clear_fields(self):
        for field, widget in self.entries.items():
            if field in ("type", "subtype", "nation", "rank", "premium"):
                widget.set("Choose" if field != "premium" else "FALSE")
            else:
                widget.delete(0, tk.END)
        # Also reset subtype options when clearing
        self.subtype_cb["values"] = []

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in load_csv():
            self.tree.insert("", "end", values=[row.get(f, "") for f in FIELDS])

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        for i, field in enumerate(FIELDS):
            widget = self.entries[field]
            if field == "premium":
                widget.set(values[i] if values[i] else "FALSE")
            else:
                widget.delete(0, tk.END)
                widget.insert(0, values[i])


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVManagerApp(root)
    root.mainloop()