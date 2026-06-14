import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------- DATABASE ---------------- #
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    note TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ---------------- #
def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    note = note_entry.get()

    if not date or not category or not amount:
        messagebox.showerror("Error", "Please fill all required fields")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Date Error", "Use YYYY-MM-DD format")
        return

    cursor.execute(
        "INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
        (date, category, amount, note)
    )
    conn.commit()
    clear_entries()
    load_expenses()

def load_expenses():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    calculate_total()

def edit_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an item to edit")
        return
    values = tree.item(selected[0])["values"]

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Expense")
    edit_window.geometry("300x300")

    tk.Label(edit_window, text="Date (YYYY-MM-DD)").pack()
    e_date = tk.Entry(edit_window)
    e_date.pack()
    e_date.insert(0, values[1])

    tk.Label(edit_window, text="Category").pack()
    e_cat = tk.Entry(edit_window)
    e_cat.pack()
    e_cat.insert(0, values[2])

    tk.Label(edit_window, text="Amount").pack()
    e_amt = tk.Entry(edit_window)
    e_amt.pack()
    e_amt.insert(0, values[3])

    tk.Label(edit_window, text="Note").pack()
    e_note = tk.Entry(edit_window)
    e_note.pack()
    e_note.insert(0, values[4])

    def update():
        cursor.execute("""
            UPDATE expenses
            SET date=?, category=?, amount=?, note=?
            WHERE id=?
        """, (e_date.get(), e_cat.get(), e_amt.get(), e_note.get(), values[0]))
        conn.commit()
        edit_window.destroy()
        load_expenses()

    tk.Button(edit_window, text="Update", command=update).pack(pady=10)

def delete_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an expense first")
        return
    expense_id = tree.item(selected[0])["values"][0]
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    load_expenses()

def calculate_total():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]
    if total is None:
        total = 0
    total_label.config(text=f"Total Expense: ₹ {total:.2f}")

def monthly_analysis():
    month = month_box.get()
    year = year_box.get()
    if not month or not year:
        messagebox.showerror("Error", "Select month and year")
        return

    month_num = datetime.strptime(month, "%B").strftime("%m")

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE strftime('%m', date)=? AND strftime('%Y', date)=?
        GROUP BY category
    """, (month_num, year))

    data = cursor.fetchall()
    if not data:
        messagebox.showinfo("No Data", f"No expenses for {month} {year}")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(6,6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.title(f"Expense Distribution - {month} {year}")
    plt.show()

def clear_entries():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)
    date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

# ---------------- UI ---------------- #
root = tk.Tk()
root.title("Advanced Personal Expense Tracker")
root.geometry("900x600")
root.resizable(False, False)

title = tk.Label(root, text="💰 Advanced Personal Expense Tracker",
                 font=("Arial", 20, "bold"))
title.pack(pady=10)

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
tk.Label(input_frame, text="Category").grid(row=0, column=1)
tk.Label(input_frame, text="Amount").grid(row=0, column=2)
tk.Label(input_frame, text="Note").grid(row=0, column=3)

date_entry = tk.Entry(input_frame)
category_entry = tk.Entry(input_frame)
amount_entry = tk.Entry(input_frame)
note_entry = tk.Entry(input_frame)

date_entry.grid(row=1, column=0)
category_entry.grid(row=1, column=1)
amount_entry.grid(row=1, column=2)
note_entry.grid(row=1, column=3)
date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

tk.Button(input_frame, text="Add Expense", bg="green", fg="white",
          command=add_expense).grid(row=1, column=4, padx=10)

# Table
columns = ("ID", "Date", "Category", "Amount", "Note")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=140)
tree.pack(pady=10)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Edit Selected", command=edit_expense).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete Selected", command=delete_expense).grid(row=0, column=1, padx=5)

# Monthly Analysis Frame
analysis_frame = tk.Frame(root)
analysis_frame.pack(pady=10)

month_box = ttk.Combobox(
    analysis_frame,
    values=["January","February","March","April","May","June",
            "July","August","September","October","November","December"],
    width=12
)
month_box.grid(row=0, column=0, padx=5)

year_box = ttk.Combobox(
    analysis_frame,
    values=[str(y) for y in range(2020, 2035)],
    width=8
)
year_box.grid(row=0, column=1, padx=5)

tk.Button(
    analysis_frame,
    text="Show Pie Chart",
    bg="#34495e",
    fg="white",
    width=18,
    command=monthly_analysis
).grid(row=0, column=2, padx=10)

# Total Label
total_label = tk.Label(root, text="Total Expense: ₹ 0", font=("Arial",14,"bold"), fg="purple")
total_label.pack(pady=10)

# ---------------- LOAD DATA ---------------- #
load_expenses()

root.mainloop()