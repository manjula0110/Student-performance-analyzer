"""
main.py
-------
Student Performance Analyzer - Tkinter GUI
Run with:  python main.py
"""

import tkinter as tk
from tkinter import messagebox

from analyzer import (
    SUBJECTS,
    validate_name,
    validate_mark,
    analyze,
    format_number,
)

# ---------- Colours and fonts ----------
BG_COLOR = "#EEF2F7"        # light grey-blue page
CARD_COLOR = "#FFFFFF"      # white panels
TEXT_COLOR = "#1F2A44"      # dark navy text
MUTED_TEXT = "#5A6478"
PRIMARY = "#2E5AAC"         # blue buttons
PRIMARY_DARK = "#234785"
PASS_COLOR = "#1E8449"      # green
FAIL_COLOR = "#C0392B"      # red

TITLE_FONT = ("Segoe UI", 18, "bold")
LABEL_FONT = ("Segoe UI", 11)
BOLD_FONT = ("Segoe UI", 11, "bold")
SMALL_FONT = ("Segoe UI", 9)


class StudentAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Analyzer")
        self.root.geometry("820x520")
        self.root.minsize(760, 500)
        self.root.configure(bg=BG_COLOR)

        self.mark_entries = {}     # subject -> Entry widget
        self.result_labels = {}    # field name -> Label widget

        self.build_header()

        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.build_input_panel(main_frame)
        self.build_result_panel(main_frame)

        self.name_entry.focus_set()
        # Pressing Enter anywhere runs the analysis
        self.root.bind("<Return>", lambda event: self.calculate())

    # ---------- Layout ----------
    def build_header(self):
        header = tk.Frame(self.root, bg=BG_COLOR)
        header.pack(fill="x", padx=20, pady=(18, 12))

        tk.Label(header, text="Student Performance Analyzer",
                 font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w")
        tk.Label(header, text="Enter marks out of 100 for each subject, then click Analyze.",
                 font=LABEL_FONT, bg=BG_COLOR, fg=MUTED_TEXT).pack(anchor="w")

    def build_input_panel(self, parent):
        panel = tk.Frame(parent, bg=CARD_COLOR, padx=20, pady=16,
                         highlightbackground="#D5DCE6", highlightcolor="#D5DCE6",
                         highlightthickness=1)
        panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(panel, text="Student details", font=BOLD_FONT,
                 bg=CARD_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=2,
                                                    sticky="w", pady=(0, 10))

        tk.Label(panel, text="Student name", font=LABEL_FONT,
                 bg=CARD_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, sticky="w", pady=6)
        self.name_entry = tk.Entry(panel, font=LABEL_FONT, width=22)
        self.name_entry.grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=6)

        # One row per subject, created with a loop
        row = 2
        for subject in SUBJECTS:
            tk.Label(panel, text=subject, font=LABEL_FONT,
                     bg=CARD_COLOR, fg=TEXT_COLOR).grid(row=row, column=0, sticky="w", pady=6)
            entry = tk.Entry(panel, font=LABEL_FONT, width=22)
            entry.grid(row=row, column=1, sticky="ew", padx=(12, 0), pady=6)
            self.mark_entries[subject] = entry
            row += 1

        panel.columnconfigure(1, weight=1)

        button_frame = tk.Frame(panel, bg=CARD_COLOR)
        button_frame.grid(row=row, column=0, columnspan=2, sticky="w", pady=(14, 0))

        tk.Button(button_frame, text="Analyze", font=BOLD_FONT,
                  bg=PRIMARY, fg="white", activebackground=PRIMARY_DARK,
                  activeforeground="white", relief="flat", padx=18, pady=6,
                  cursor="hand2", command=self.calculate).pack(side="left", padx=(0, 10))

        tk.Button(button_frame, text="Clear", font=LABEL_FONT,
                  bg="#E3E8EF", fg=TEXT_COLOR, activebackground="#D0D7E2",
                  relief="flat", padx=18, pady=6,
                  cursor="hand2", command=self.clear_all).pack(side="left")

    def build_result_panel(self, parent):
        panel = tk.Frame(parent, bg=CARD_COLOR, padx=20, pady=16,
                         highlightbackground="#D5DCE6", highlightcolor="#D5DCE6",
                         highlightthickness=1)
        panel.pack(side="left", fill="both", expand=True, padx=(10, 0))

        tk.Label(panel, text="Result", font=BOLD_FONT,
                 bg=CARD_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=2,
                                                    sticky="w", pady=(0, 10))

        fields = [
            ("name", "Student"),
            ("total", "Total marks"),
            ("average", "Average"),
            ("percentage", "Percentage"),
            ("grade", "Grade"),
            ("status", "Result"),
            ("top", "Highest subject"),
        ]

        row = 1
        for key, label_text in fields:
            tk.Label(panel, text=label_text, font=LABEL_FONT,
                     bg=CARD_COLOR, fg=MUTED_TEXT).grid(row=row, column=0, sticky="nw", pady=5)
            value = tk.Label(panel, text="-", font=BOLD_FONT, bg=CARD_COLOR,
                             fg=TEXT_COLOR, anchor="w", justify="left", wraplength=220)
            value.grid(row=row, column=1, sticky="w", padx=(12, 0), pady=5)
            self.result_labels[key] = value
            row += 1

        # Performance message shown in a coloured strip at the bottom
        self.message_label = tk.Label(panel, text="Results will appear here.",
                                      font=BOLD_FONT, bg="#F3F5F9", fg=MUTED_TEXT,
                                      pady=10, padx=10, anchor="w",
                                      justify="left", wraplength=320)
        self.message_label.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(14, 0))

        self.note_label = tk.Label(panel, text="", font=SMALL_FONT, bg=CARD_COLOR,
                                   fg=FAIL_COLOR, anchor="w", justify="left", wraplength=320)
        self.note_label.grid(row=row + 1, column=0, columnspan=2, sticky="w", pady=(6, 0))

        panel.columnconfigure(1, weight=1)

    # ---------- Actions ----------
    def calculate(self):
        # 1. Validate name
        name = self.name_entry.get()
        error = validate_name(name)
        if error:
            messagebox.showerror("Invalid input", error)
            self.name_entry.focus_set()
            return

        # 2. Validate every mark and store them in a dictionary
        marks = {}
        for subject in SUBJECTS:
            entry = self.mark_entries[subject]
            mark, error = validate_mark(subject, entry.get())
            if error:
                messagebox.showerror("Invalid input", error)
                entry.focus_set()
                entry.select_range(0, tk.END)
                return
            marks[subject] = mark

        # 3. Calculate and show results
        result = analyze(name, marks)
        self.show_result(result)

    def show_result(self, result):
        self.result_labels["name"].config(text=result["name"])
        self.result_labels["total"].config(
            text=f"{format_number(result['total'])} / {result['max_total']}")
        self.result_labels["average"].config(text=f"{result['average']:.2f}")
        self.result_labels["percentage"].config(text=f"{result['percentage']:.2f}%")
        self.result_labels["grade"].config(text=result["grade"])

        status_color = PASS_COLOR if result["status"] == "Pass" else FAIL_COLOR
        self.result_labels["status"].config(text=result["status"], fg=status_color)

        top_text = ", ".join(result["top_subjects"]) + f" ({format_number(result['top_mark'])})"
        self.result_labels["top"].config(text=top_text)

        message = result["message"]
        if message == "Excellent Performance":
            bg, fg = "#E3F4EA", PASS_COLOR
        elif message == "Good Performance":
            bg, fg = "#E6EEFB", PRIMARY
        else:
            bg, fg = "#FBE9E7", FAIL_COLOR
        self.message_label.config(text=message, bg=bg, fg=fg)

        if result["weak_subjects"]:
            self.note_label.config(
                text="Below 40 in: " + ", ".join(result["weak_subjects"]))
        else:
            self.note_label.config(text="")

    def clear_all(self):
        self.name_entry.delete(0, tk.END)
        for entry in self.mark_entries.values():
            entry.delete(0, tk.END)

        for label in self.result_labels.values():
            label.config(text="-", fg=TEXT_COLOR)

        self.message_label.config(text="Results will appear here.",
                                  bg="#F3F5F9", fg=MUTED_TEXT)
        self.note_label.config(text="")
        self.name_entry.focus_set()


def main():
    root = tk.Tk()
    StudentAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
