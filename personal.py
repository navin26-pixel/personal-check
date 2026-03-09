"""
LIFE MANAGER - Complete Python Program
A simple CLI app to manage tasks, money, and notes
"""

import json
from datetime import datetime
import os

# ====================================
# DATA STORAGE (all our lists)
# ====================================

tasks = []           # List for tasks
transactions = []    # List for money
notes = []           # List for notes

# File names for saving
TASKS_FILE = "tasks.json"
TRANSACTIONS_FILE = "transactions.json"
NOTES_FILE = "notes.json"

# ====================================
# FILE FUNCTIONS (save and load)
# ====================================

def load_all_data():
    """Load all data from files when program starts"""
    global tasks, transactions, notes
    
    # Load tasks
    try:
        with open(TASKS_FILE, 'r') as f:
            tasks = json.load(f)
        print(f"✅ Loaded {len(tasks)} tasks")
    except FileNotFoundError:
        print("📝 No existing tasks file - starting fresh")
        tasks = []
    
    # Load transactions
    try:
        with open(TRANSACTIONS_FILE, 'r') as f:
            transactions = json.load(f)
        print(f"✅ Loaded {len(transactions)} transactions")
    except FileNotFoundError:
        print("💰 No existing transactions file - starting fresh")
        transactions = []
    
    # Load notes
    try:
        with open(NOTES_FILE, 'r') as f:
            notes = json.load(f)
        print(f"✅ Loaded {len(notes)} notes")
    except FileNotFoundError:
        print("📝 No existing notes file - starting fresh")
        notes = []

def save_all_data():
    """Save all data to files"""
    # Save tasks
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)
    
    # Save transactions
    with open(TRANSACTIONS_FILE, 'w') as f:
        json.dump(transactions, f, indent=2)
    
    # Save notes
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=2)
    
    print("💾 All data saved!")

# ====================================
# TASK FUNCTIONS
# ====================================

def add_task():
    """Add a new task"""
    print("\n--- ADD NEW TASK ---")
    title = input("Task description: ")
    
    # Create task dictionary
    task = {
        "title": title,
        "done": False,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    tasks.append(task)
    print(f"✅ Task added: {title}")

def view_tasks():
    """Show all tasks"""
    print("\n--- YOUR TASKS ---")
    
    if not tasks:
        print("📭 No tasks yet")
        return
    
    for i, task in enumerate(tasks, 1):
        # Show [x] for done, [ ] for not done
        status = "✅" if task["done"] else "⬜"
        print(f"{i}. {status} {task['title']}")
        print(f"   📅 {task['created']}")

def complete_task():
    """Mark a task as complete"""
    print("\n--- COMPLETE TASK ---")
    
    if not tasks:
        print("📭 No tasks to complete")
        return
    
    # Show tasks with numbers
    for i, task in enumerate(tasks, 1):
        status = "✅" if task["done"] else "⬜"
        print(f"{i}. {status} {task['title']}")
    
    try:
        choice = int(input("\nTask number to complete: ")) - 1
        if 0 <= choice < len(tasks):
            tasks[choice]["done"] = True
            print(f"✅ Task completed: {tasks[choice]['title']}")
        else:
            print("❌ Invalid task number")
    except ValueError:
        print("❌ Please enter a number")

def delete_task():
    """Delete a task"""
    print("\n--- DELETE TASK ---")
    
    if not tasks:
        print("📭 No tasks to delete")
        return
    
    # Show tasks with numbers
    for i, task in enumerate(tasks, 1):
        status = "✅" if task["done"] else "⬜"
        print(f"{i}. {status} {task['title']}")
    
    try:
        choice = int(input("\nTask number to delete: ")) - 1
        if 0 <= choice < len(tasks):
            deleted = tasks.pop(choice)
            print(f"🗑️ Deleted: {deleted['title']}")
        else:
            print("❌ Invalid task number")
    except ValueError:
        print("❌ Please enter a number")

# ====================================
# MONEY FUNCTIONS
# ====================================

def add_income():
    """Add income transaction"""
    print("\n--- ADD INCOME ---")
    
    try:
        amount = float(input("Amount: $"))
        category = input("Category (salary/freelance/gift/etc): ")
        
        transaction = {
            "type": "income",
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        transactions.append(transaction)
        print(f"✅ Added income: ${amount} from {category}")
    
    except ValueError:
        print("❌ Please enter a valid number")

def add_expense():
    """Add expense transaction"""
    print("\n--- ADD EXPENSE ---")
    
    try:
        amount = float(input("Amount: $"))
        category = input("Category (food/transport/entertainment/etc): ")
        
        transaction = {
            "type": "expense",
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        transactions.append(transaction)
        print(f"✅ Added expense: ${amount} for {category}")
    
    except ValueError:
        print("❌ Please enter a valid number")

def view_transactions():
    """Show all transactions"""
    print("\n--- ALL TRANSACTIONS ---")
    
    if not transactions:
        print("📭 No transactions yet")
        return
    
    total_income = 0
    total_expense = 0
    
    for i, t in enumerate(transactions, 1):
        # Show + for income, - for expense
        sign = "+" if t["type"] == "income" else "-"
        print(f"{i}. {sign} ${t['amount']} | {t['category']} | {t['date']}")
        
        if t["type"] == "income":
            total_income += t["amount"]
        else:
            total_expense += t["amount"]
    
    print("-" * 40)
    print(f"Total Income:  +${total_income}")
    print(f"Total Expense: -${total_expense}")
    print(f"Balance:       ${total_income - total_expense}")

def show_financial_summary():
    """Show summary by category"""
    print("\n--- FINANCIAL SUMMARY ---")
    
    if not transactions:
        print("📭 No transactions yet")
        return
    
    # Dictionary to store category totals
    categories = {}
    
    for t in transactions:
        if t["type"] == "expense":
            cat = t["category"]
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += t["amount"]
    
    if categories:
        print("\nSpending by category:")
        for cat, amount in categories.items():
            print(f"  {cat}: ${amount}")
    else:
        print("No expenses recorded")

# ====================================
# NOTE FUNCTIONS
# ====================================

def add_note():
    """Add a quick note"""
    print("\n--- ADD NOTE ---")
    
    text = input("Note: ")
    
    note = {
        "text": text,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    notes.append(note)
    print(f"✅ Note added")

def view_notes():
    """Show all notes"""
    print("\n--- YOUR NOTES ---")
    
    if not notes:
        print("📭 No notes yet")
        return
    
    for i, note in enumerate(notes, 1):
        print(f"{i}. 📝 {note['text']}")
        print(f"   📅 {note['created']}")

def delete_note():
    """Delete a note"""
    print("\n--- DELETE NOTE ---")
    
    if not notes:
        print("📭 No notes to delete")
        return
    
    # Show notes with numbers
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['text']}")
    
    try:
        choice = int(input("\nNote number to delete: ")) - 1
        if 0 <= choice < len(notes):
            deleted = notes.pop(choice)
            print(f"🗑️ Deleted note")
        else:
            print("❌ Invalid note number")
    except ValueError:
        print("❌ Please enter a number")

# ====================================
# MAIN MENU FUNCTION
# ====================================

def show_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("          LIFE MANAGER")
    print("="*50)
    print("📋 TASKS")
    print("  1. Add Task")
    print("  2. View Tasks")
    print("  3. Complete Task")
    print("  4. Delete Task")
    print("\n💰 MONEY")
    print("  5. Add Income")
    print("  6. Add Expense")
    print("  7. View Transactions")
    print("  8. Financial Summary")
    print("\n📝 NOTES")
    print("  9. Add Note")
    print(" 10. View Notes")
    print(" 11. Delete Note")
    print("\n💾 SYSTEM")
    print(" 12. Save & Exit")
    print("="*50)

# ====================================
# MAIN PROGRAM
# ====================================

def main():
    """Main program loop"""
    print("\n🔥 WELCOME TO LIFE MANAGER 🔥")
    
    # Load existing data
    load_all_data()
    
    while True:
        show_menu()
        
        choice = input("\nEnter your choice (1-12): ")
        
        # Tasks
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        
        # Money
        elif choice == "5":
            add_income()
        elif choice == "6":
            add_expense()
        elif choice == "7":
            view_transactions()
        elif choice == "8":
            show_financial_summary()
        
        # Notes
        elif choice == "9":
            add_note()
        elif choice == "10":
            view_notes()
        elif choice == "11":
            delete_note()
        
        # System
        elif choice == "12":
            save_all_data()
            print("👋 Thanks for using Life Manager! Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-12")

# ====================================
# START THE PROGRAM
# ====================================

if __name__ == "__main__":
    main()