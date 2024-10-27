import csv
import os
from tabulate import tabulate
import sys
from datetime import datetime
import operator

def main():
    print()
    print("Welcome to the Expense Tracker!")
    print()
    print("Would you like to: ")
    print("1. Add new expenses")
    print("2. Remove expenses")
    print("3. View current spendings")
    print("4. Quit Program")
    selection = input("Choice: ")
    if selection == "1":
        #get user expense
        item, cost, category, date = get_user_expense()
        #write user expense to csv file
        write_csv(item, cost, category, date)
    elif selection == "2":
        remove_expense()
    elif selection == "3":
        summarize()
    elif selection == "4":
        sys.exit("Bye!")

def get_user_expense():
    item_name = input("Enter the name of the item you spent your money on: ")
    item_cost = float(input("Enter the cost of the item($): "))
    print("Choose from one of the categories below: ")
    print("1. Food")
    print("2. Personal Item")
    print("3. Activities")
    print("4. Other")
    item_category = input("What is your choice? (enter a number)")
    if item_category == "1":
        item_category = "Food"
    elif item_category == "2":
        item_category = "Personal Item"
    elif item_category == "3":
        item_category = "Activities"
    elif item_category == "4":
        item_category = "Other"
    date_str = input("Enter the date in which you spent your money on(month/day/year): ")
    date_format = '%m/%d/%Y'
    date_obj = datetime.strptime(date_str, date_format).date()
    return item_name, item_cost, item_category, date_obj

def write_csv(item, cost, category, date):
    current_month = str(datetime.now().date().month)
    current_year = str(datetime.now().date().year)
    exists = os.path.exists(f"{current_year}_{current_month}_expenses.csv")
    if not exists:
        with open(f"{current_year}_{current_month}_expenses.csv", "w") as new_file:
            headers = ["Date", "Item Name", "Cost($)", "Category"]
            writer = csv.DictWriter(new_file, fieldnames=headers)
            writer.writeheader()
            writer.writerow({"Date": date, "Item Name": item, "Cost($)": cost, "Category": category})
            print()
            print("Item added. Run the program again to view your spending summary.")

    else:
        with open(f"{current_year}_{current_month}_expenses.csv", "a") as file:
            headers = ["Date", "Item Name", "Cost($)", "Category"]
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writerow({"Date": date, "Item Name": item, "Cost($)": cost, "Category": category})
            print()
            print("Item added. Run the program again to view your spending summary.")

def summarize():
    spending_table = []
    cost_list = []
    print()
    date_option = input("For which year and month would you like to view your spendings?(month/year)")
    print()
    month, year = date_option.split("/")
    month_chart = {
        "1": "January",
        "2": "February",
        "3": "March",
        "4":"April",
        "5": "May",
        "6": "June",
        "7": "July",
        "8": "August",
        "9": "September",
        "10": "October",
        "11": "November",
        "12": "December"
        }
    exists = os.path.exists(f"{year}_{month}_expenses.csv")
    if exists:
        with open(f"{year}_{month}_expenses.csv", "r") as file:
            reader = csv.reader(file, delimiter=',')
            sort = sorted(reader, key=operator.itemgetter(0), reverse=True)
            for line in sort:
                spending_table.append(line)
                cost_list.append(line[2])

        del cost_list[0]

        total = 0
        for cost in cost_list:
            total += float(cost)

        print("Here is a table that summarizes your spendings in", month_chart[month], year + ":")
        print(tabulate(spending_table[1:], headers=spending_table[0], tablefmt="grid"))
        print(f"You have spent a total of ${total:.2f} this month.")

    if not exists:
        sys.exit("You haven't created an expenses table for that month yet.")

def remove_expense():
    spending_table = []
    cost_list = []
    print()
    date_option = input("For which year and month would you like to remove spending from?(month(single digit)/year)")
    print()
    month, year = date_option.split("/")
    month_chart = {
        "1": "January",
        "2": "February",
        "3": "March",
        "4":"April",
        "5": "May",
        "6": "June",
        "7": "July",
        "8": "August",
        "9": "September",
        "10": "October",
        "11": "November",
        "12": "December"
        }

    exists = os.path.exists(f"{year}_{month}_expenses.csv")
    if exists:
        with open(f"{year}_{month}_expenses.csv", "r") as file:
            reader = csv.reader(file, delimiter=',')
            sort = sorted(reader, key=operator.itemgetter(0), reverse=True)
            for line in sort:
                spending_table.append(line)
                cost_list.append(line[2])

        del cost_list[0]

        total = 0
        for cost in cost_list:
            total += float(cost)

        print("Here is a table that summarizes your spendings in", month_chart[month], year + ":")
        print(tabulate(spending_table[1:], headers=spending_table[0], tablefmt="grid"))

        item_removed = input("Which item would you like to remove from your spending list?")

        with open(f"{year}_{month}_expenses.csv", "r") as file:
            reader = csv.reader(file, delimiter=',')
            sort = sorted(reader, key=operator.itemgetter(0), reverse=True)
            new_rows = list(sort)
            for i, line in enumerate(sort):
                if item_removed in line:
                    del new_rows[i]

        with open(f"{year}_{month}_expenses.csv", "w") as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(new_rows)

        print("Item removed. Run the program again to view your newly updated spending list.")

    else:
        print("You haven't created a spending list for that month yet.")

if __name__ == "__main__":
    main()