# 💰 Advanced Personal Expense Tracker

## Overview

Advanced Personal Expense Tracker is a Python-based desktop application that helps users manage and analyze their daily expenses efficiently. The application provides a user-friendly graphical interface built with Tkinter and stores expense records using SQLite.

Users can add, edit, delete, and monitor expenses while generating monthly expense distribution reports through graphical visualizations.

---

## Features

* Add new expense records
* Edit existing expenses
* Delete expense entries
* Store data using SQLite database
* View total expenses automatically
* Monthly expense analysis
* Expense distribution pie charts using Matplotlib
* User-friendly graphical interface using Tkinter
* Automatic date handling

---

## Technologies Used

* Python
* Tkinter
* SQLite3
* Matplotlib

---

## Project Structure

Expense-Tracker/

├── main.py

├── expenses.db

└── README.md

---

## Database Schema

Table: expenses

| Column   | Type    |
| -------- | ------- |
| id       | INTEGER |
| date     | TEXT    |
| category | TEXT    |
| amount   | REAL    |
| note     | TEXT    |

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/vsdevikrishna111/Expense-Tracker.git
```

2. Navigate to the project folder

```bash
cd Expense-Tracker
```

3. Install dependencies

```bash
pip install matplotlib
```

4. Run the application

```bash
python main.py
```

---

## How It Works

1. Enter expense details including date, category, amount, and notes.
2. Click **Add Expense** to save records.
3. View all expenses in the table.
4. Edit or delete records as required.
5. Select a month and year to generate expense distribution charts.
6. Track total expenses dynamically.

---

## Learning Outcomes

* GUI development using Tkinter
* Database integration using SQLite
* Data visualization using Matplotlib
* CRUD operations in Python
* Event-driven programming

---

## Future Enhancements

* Export reports to Excel/PDF
* User authentication system
* Budget tracking and alerts
* Search and filtering options
* Cloud database integration

---

## Author

V S DeviKrishna

B.Tech Computer Science and Engineering

LBS Institute of Technology for Women
