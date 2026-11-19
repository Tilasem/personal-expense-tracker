from datetime import datetime
import sqlite3
import os

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
db_path=os.path.join(BASE_DIR, "expenses.db")
#connect to SQLite database 
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
#Create expenses table 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL, 
        description TEXT,
        date TEXT NOT NULL
    )
""")
conn.commit()
#Load expenses from database 
cursor.execute("SELECT * FROM expenses")
rows=cursor.fetchall()

expenses=[]

for row in rows:
    expense={
        "id": row[0],
        "amount": row[1],
        "category": row[2],
        "description": row[3],
        "date": row[4]
    }
    expenses.append(expense)

while True:
    print(
    "========= Personal Expense Tracker ========="
    "\n             Main Menu                   "
    "\n 1.Add expense" 
    "\n 2. View all expenses" 
    "\n 3. Show total expenses" #сумма всех расходов
    "\n 4. Search by category" #поиск расходов по категории
    "\n 5. Sort expenses and search by date" #сортировка расходов по сумме и дате и поиск по дате
    "\n 6. Manage expenses" 
    "\n 7. Exit"
    )
    choice = input("Enter your choice (1-7): ")
        
    if choice == '1':
        while True:
            try:
                amount = float(input("Enter the expense amount: "))

                if amount <= 0:
                    print("Amount must be greater than zero.")
                    continue 
                break
            except ValueError:
                print("Invalid input. Please enter numbers only.")

        categories = []
        for expense in expenses:
            if expense['category'] not in categories:
                categories.append(expense['category'])
        if categories:
            print("==========Available Categories==========")

            count = 1
            for cat in categories:
                print(f"{count}. {cat}")
                count += 1
            category_choice = input(
                "Choose a category number or enter a new category:"
            )
            if category_choice.isdigit() and 1 <= int (category_choice) <= len(categories):
                category = categories[int(category_choice) - 1]
            else:
                category = category_choice.strip()
        else:
            category = input("Enter the expense category:").strip()
        while not category:
            print("Category cannot be empty!")
            category = input("Enter the expense category: ").strip()
            
        description = input("Enter a description for the expense: ")
        while True:
            input_date = input("Enter the date (DD-MM) or press Enter for today: ")
            if input_date == "":
                date = datetime.today().date().isoformat()
                break
            try:
                today=datetime.today().date()
                date=datetime.strptime(f"{input_date}-{today.year}", "%d-%m-%Y").date().isoformat()
                break
            except ValueError:
                print("Invalid date format. Please try again (DD-MM)")
        expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date":date
    }
        cursor.execute("""
            INSERT INTO expenses (amount, category, description, date)
            VALUES (?,?,?,?)
        """, (
            expense['amount'],
            expense['category'],
            expense['description'],
            expense['date']
        ))

        conn.commit()
        expense['id'] = cursor.lastrowid
        expenses.append(expense)
        print("Expense added successfully!")


    elif choice == '2':

        if not expenses:
            print("No expenses found. Please add an expense first.")
        else:
            print("=========All expenses=========")
            count = 1
            for expense in expenses:
                print(f"Expense {count}:")
                print(f"Amount: {expense['amount']}")
                print(f"Category: {expense['category']}")
                print(f"Description: {expense['description']}")
                print(f"Date: {expense['date']}")
                print("================================")
                count += 1

    elif choice == '3':
        
        if not expenses:
            print("No expenses found. Please add an expense first.")
        else: 
            total = 0
            count = 1
            print("=========Total Expenses=========")
            for expense in expenses:
                print(f"Expense {count} = {expense['amount']}")
                total += expense['amount']
                count += 1
            print("================================")
            print(f"Number of Expenses: {len(expenses)}")
            print(f"Total Expenses: {total}")
            print("================================")

    elif choice == '4':
        category_search = input("Enter category to search:").lower()

        found = False
        count = 1

        for expense in expenses:
         
            if category_search == expense['category'].lower():
                found = True 
                print(f"Expense {count}")
                print(f"Amount: {expense['amount']}")
                print(f"Category: {expense['category']}")
                print(f"Description: {expense['description']}")
                print(f"Date: {expense['date']}")
                count += 1
        if not found:
            print(f"No expenses found in category '{category_search}'.")
        print("================================")

    elif choice == '5':
        if not expenses:
            print("No expenses found. PLease add an expense first.")
        else:
            while True:
                sort_choice= input(
                    "=============== Sort Expenses and Search by Date ==============="
                    "\nChoose an option to sort expenses:" 
                    "\n  1. Sort by amount ascending" #сортировка по возрастанию
                    "\n  2. Sort by amount descending" # сортировка по убыванию
                    "\n  3. Sort by date " # сортировка по дате 
                    "\n  4. Search by date" # поиск по дате
                    "\n  5. Back to main menu "
                    "\n Choose an option: "
                    )
                if sort_choice == '1':
                    sorted_expenses = sorted(expenses, key = lambda x: x['amount'])
                    print("=========Expenses sorted by amount (ascending)=========")

                elif sort_choice == '2':
                    sorted_expenses = sorted(expenses, key = lambda x: x['amount'], reverse=True)
                    print("=========Expenses sorted by amount (descending)=========")
                elif sort_choice == '3':
                    sorted_expenses = sorted(expenses, key = lambda x: x['date'])
                    print("=========Expenses sorted by date=========")
                elif sort_choice == '4':
                    search_date = input ("Enter the date to search (DD-MM): ")
                    try:
                        today = datetime.today().date()
                        search_date = datetime.strptime(
                            f"{search_date}-{today.year}", "%d-%m-%Y"
                        ).date().isoformat()

                        found = False
                    
                        print("\n========== Search by Date ==========")
                        for count, expense in enumerate(expenses, start=1):
                            if expense['date'] == search_date:
                                found = True
                                print(f"\nExpense {count}:")
                                print(f"Amount: {expense['amount']}")
                                print(f"Category: {expense['category']}")
                                print(f"Description: {expense['description']}")
                                print(f"Date: {expense['date']}")
                            
                        if not found:
                            print(f"No expenses found for date '{search_date}'.")
                    except ValueError:
                        print("Invalid date format. Please enter the date in DD-MM format.")
                elif sort_choice == '5':
                    print("Returning to main menu.")
                    break
                else:
                    print("Invalid choice. Please select 1-5.")
                if sort_choice in ['1','2','3']:
                    for count, expense in enumerate(sorted_expenses, start=1):
                        print(f"\nExpense {count}:")
                        print(f"Amount: {expense['amount']}")
                        print(f"Category: {expense['category']}")
                        print(f"Description: {expense['description']}")
                        print(f"Date: {expense['date']}")
                    print("================================")  
    elif choice == '6':
      while True:
          print(
              "\n========= Manage Expenses ========="
                "\n 1. Edit an expense"
                "\n 2. Delete an expense"
                "\n 3. Back to main menu"
          )
          manage_choice = input("Choose an option (1-3):")
          if manage_choice == '1':
              if not expenses:
                  print("No expenses found. Please add an expense first.")
              else: 
                  print("\n========= Select Expense to Edit =========")

                  for i, expense in enumerate(expenses, start=1):
                      print(f"\nExpense{i}")
                      print((f"Amount: {expense['amount']}"))
                      print(f"Category: {expense['category']}")
                      print(f"Description: {expense['description']}")
                      print(f"Date: {expense['date']}")
                  while True:
                      expense_number = input(
                          "\nEnter expense number to edit (or 0 to go back):"
                      )
                      if expense_number == '0':
                          break
                      if expense_number.isdigit() and 1 <= int(expense_number) <= len(expenses):
                          expense_index = int(expense_number) - 1
                          break
                      else:
                          print("Invalid number! Please try again.")
                  if expense_number != '0':
                      while True:
                          print("\n========== Edit Expense ===========")
                          print("1. Edit amount")
                          print("2. Edit category")
                          print("3. Edit description")
                          print("4. Edit date")
                          print("5. Back to Manage Expenses")

                          edit_choice = input("Choose an option (1-5):")

                          if edit_choice == '1':
                              while True:
                                 try:
                                    new_amount = float(input("Enter new amount: "))

                                    if new_amount <= 0:
                                        print("Amount must be greater than zero.")
                                        continue
                                    expenses[expense_index]['amount']=new_amount
                                    print("Amount updated successfully!")
                                    break
                                 except ValueError:
                                     print("Invalid amount! Please enter numbers only.")
                          elif edit_choice == '2':
                              new_category = input("Enter new category: ").strip()

                              if new_category:
                                  expenses[expense_index]['category']=new_category 
                                  print("Category updated successfully!")
                              else: 
                                  print("Category cannot be empty.")
                          elif edit_choice == '3':
                              new_description = input("Enter new description: ").strip()

                              if new_description:
                                  expenses[expense_index]['description']=new_description
                                  print("Description updated successfully!")
                              else:
                                  print("Description cannot be empty.")
                          elif edit_choice == '4':
                              while True:
                                  input_date = input(
                                      "Enter new date (DD-MM) or press Enter for today: "
                                  ).strip()

                                  try:
                                    if input_date == "":
                                      new_date = datetime.today().date().isoformat()
                                    else:
                                      today = datetime.today().date()
                                      new_date = datetime.strptime(
                                          f"{input_date}-{today.year}", "%d-%m-%Y"
                                      ).date().isoformat()

                                    expenses[expense_index]['date']=new_date
                                    print("Date updated successfully!")
                                    break 
                                  except ValueError:
                                      print("Invalid date! Please try again (DD-MM).")
                          elif edit_choice == '5':
                                print("Returning to Manage Expenses...")
                                break
                          else: 
                                print("Invalid choice! Please select 1 to 5.")
          elif manage_choice == '2':
            if not expenses:    
                  print("No expenses found. Please add an expense first.")
            else:
                  print("\n========== Select Expense to Delete ==========")

                  for i, expense in enumerate(expenses, start=1):
                      print(f"\nExpense {i}")
                      print(f"Amount: {expense['amount']}")
                      print(f"Category: {expense['category']}")
                      print(f"Description: {expense['description']}")
                      print(f"Date: {expense['date']}")
                  while True:
                      expense_number = input(
                          "\nEnter expense number to delete (or 0 to go back):"
                      )

                      if expense_number == '0':
                          break
                      if expense_number.isdigit() and 1 <= int(expense_number) <= len(expenses):
                          expense_index = int(expense_number) - 1
                          break
                      else:
                          print("Invalid number! Please try again.")

                  if expense_number != '0':
                    while True:
                        confirm = input(
                            "Are you sure you want to delete this expense? (yes/no): "
                        ).lower().strip()

                        if confirm == 'yes':
                            expenses.pop(expense_index)                                                                                                                                                                                                                        
                            print("Expense deleted successfully!")
                            break
                        elif confirm == 'no':
                            print("Deletion cancelled.")
                            break
                        else: 
                            print("Please enter yes or no.")
          elif manage_choice == '3':
              print("Returning to main menu...")
              break
          else:
              print("Invalid choice! Please select 1,2 or 3.")
    elif choice == '7':
        print("Goodbye!")
        print(" Thank you for using the Personal Expense Tracker.")
        break
    else: 
        print("Invalid choice! Please select a number from 1 to 7.")
        