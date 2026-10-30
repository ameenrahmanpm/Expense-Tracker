import json
import os
from datetime import date, datetime

FILE = "expense_data.json"
expenses = []

def load_expenses():
    global expenses
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            expenses = json.load(f)

def save_expenses():
    with open(FILE, "w") as f:
        json.dump(expenses, f)

def add_expense():
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Enter a valid number.")
        return
    category = input("Category (food, travel, etc.): ").lower()
    d = input("Date (DD-MM-YYYY, press Enter for today): ").strip()
    if d == "":
        d = date.today().strftime("%d-%m-%Y")
    else:
        try:
            datetime.strptime(d, "%d-%m-%Y")
        except ValueError:
            print("Invalid date. Use DD-MM-YYYY, e.g. 05-11-2026.")
            return
    expenses.append({"amount": amount, "category": category, "date": d})
    save_expenses()
    print("Added.")

def view_expenses():
    if not expenses:
        print("No expenses yet.")
        return
    for i, e in enumerate(expenses, start=1):
        print(f"{i}. {e['date']} | {e['category']} - Rs {e['amount']}")

def overall_summary():
    total = 0
    by_category = {}
    for e in expenses:
        total += e["amount"]
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]
    print("\n=== OVERALL SUMMARY ===")
    print(f"Total: Rs {total}")
    for cat, amt in by_category.items():
        print(f"  {cat}: Rs {amt}")

def date_summary():
    by_date = {}
    for e in expenses:
        day = by_date.setdefault(e["date"], {"total": 0, "cats": {}})
        day["total"] += e["amount"]
        day["cats"][e["category"]] = day["cats"].get(e["category"], 0) + e["amount"]
    print("\n=== SUMMARY BY DATE ===")
    for d in sorted(by_date, key=lambda x: datetime.strptime(x, "%d-%m-%Y")):
        print(f"\n{d}: Rs {by_date[d]['total']}")
        for cat, amt in by_date[d]["cats"].items():
            print(f"  {cat}: Rs {amt}")

def show_summary():
    if not expenses:
        print("No expenses yet.")
        return
    overall_summary()
    date_summary()

load_expenses()

while True:
    print("\n1. Add expense")
    print("2. View expenses")
    print("3. Summary")
    print("4. Exit")
    choice = input("Choose: ")
    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        show_summary()
    elif choice == "4":
        break
    else:
        print("Invalid choice.")