# ============================================================
# EMPLOYEE MANAGEMENT SYSTEM - OOP IMPLEMENTATION
# ============================================================

# ------------------------------------------------------------
# 1. PARENT & CHILD CLASSES (OOP)
# ------------------------------------------------------------

class Employee:
    def __init__(self, emp_id, name, age, department, phone, email, bonus=0.0, deduction=0.0):
        self.emp_id = emp_id
        self.name = name
        self.age = age
        self.department = department
        self.phone = phone
        self.email = email
        self.bonus = bonus
        self.deduction = deduction

    def calculate_salary(self):
        pass

    def to_file_string(self):
        # Base format for file saving
        pass


class FullTimeEmployee(Employee):
    def __init__(self, emp_id, name, age, department, phone, email, basic_salary, bonus=0.0, deduction=0.0, absent_days=0, late_days=0):
        super().__init__(emp_id, name, age, department, phone, email, bonus, deduction)
        self.basic_salary = basic_salary
        self.absent_days = absent_days
        self.late_days = late_days
        self.emp_type = "Full-Time"

    def calculate_salary(self):
        absence_deduction = self.absent_days * 200
        late_deduction = self.late_days * 50
        final_salary = self.basic_salary + self.bonus - self.deduction - absence_deduction - late_deduction
        return max(0.0, final_salary)

    def to_file_string(self):
        return f"FullTime,{self.emp_id},{self.name},{self.age},{self.department},{self.phone},{self.email},{self.basic_salary},{self.bonus},{self.deduction},{self.absent_days},{self.late_days}\n"


class PartTimeEmployee(Employee):
    def __init__(self, emp_id, name, age, department, phone, email, hourly_rate, working_hours=0, bonus=0.0, deduction=0.0):
        super().__init__(emp_id, name, age, department, phone, email, bonus, deduction)
        self.hourly_rate = hourly_rate
        self.working_hours = working_hours
        self.emp_type = "Part-Time"

    def calculate_salary(self):
        base_earned = self.hourly_rate * self.working_hours
        final_salary = base_earned + self.bonus - self.deduction
        return max(0.0, final_salary)

    def to_file_string(self):
        return f"PartTime,{self.emp_id},{self.name},{self.age},{self.department},{self.phone},{self.email},{self.hourly_rate},{self.working_hours},{self.bonus},{self.deduction}\n"


class Freelancer(Employee):
    def __init__(self, emp_id, name, age, department, phone, email, project_rate, completed_projects=0, bonus=0.0, deduction=0.0):
        super().__init__(emp_id, name, age, department, phone, email, bonus, deduction)
        self.project_rate = project_rate
        self.completed_projects = completed_projects
        self.emp_type = "Freelancer"

    def calculate_salary(self):
        base_earned = self.project_rate * self.completed_projects
        final_salary = base_earned + self.bonus - self.deduction
        return max(0.0, final_salary)

    def to_file_string(self):
        return f"Freelancer,{self.emp_id},{self.name},{self.age},{self.department},{self.phone},{self.email},{self.project_rate},{self.completed_projects},{self.bonus},{self.deduction}\n"


# Global list to store employees
employees_list = []
FILENAME = "employees.txt"


# ------------------------------------------------------------
# 2. FILE HANDLING FUNCTIONS (TXT & WRITE)
# ------------------------------------------------------------

def load_employees():
    global employees_list
    employees_list = []
    try:
        file = open(FILENAME, "r")
        lines = file.readlines()
        file.close()
        
        if not lines:
            return

        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            emp_type = parts[0]

            try:
                if emp_type == "FullTime":
                    emp = FullTimeEmployee(parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7], parts[8], parts[9], parts[10], parts[11])
                    employees_list.append(emp)
                elif emp_type == "PartTime":
                    emp = PartTimeEmployee(parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7], parts[8], parts[9], parts[10])
                    employees_list.append(emp)
                elif emp_type == "Freelancer":
                    emp = Freelancer(parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7], parts[8], parts[9], parts[10])
                    employees_list.append(emp)
            except Exception:
                continue
    except FileNotFoundError:
        print("Employee file not found.")
        print("A new employee database will be created.")
    except Exception:
        print("Error while loading employee data. Please check the employee file.")


def save_employees():
    try:
        file = open(FILENAME, "w")
        for emp in employees_list:
            file.write(emp.to_file_string())
        file.close()
        print("\nEmployee data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")


# ------------------------------------------------------------
# 3. VALIDATION FUNCTIONS
# ------------------------------------------------------------

def validate_employee_id(emp_id_str):
    try:
        emp_id = int(emp_id_str)
        if emp_id <= 0:
            print("Error: Employee ID must be a positive number.")
            return None
        for emp in employees_list:
            if emp.emp_id == emp_id:
                print("Error: Employee ID already exists.")
                return None
        return emp_id
    except ValueError:
        print("Error: Employee ID must be a number.")
        return None


def validate_age(age_str):
    try:
        age = int(age_str)
        if 18 <= age <= 65:
            return age
        print("Invalid input. Age must be between 18 and 65.")
        return None
    except ValueError:
        print("Invalid input. Age must be a number.")
        return None


def validate_positive_number(value_str, field_name="Value"):
    try:
        val = float(value_str)
        if val < 0:
            print(f"Error: {field_name} cannot be negative.")
            return None
        return val
    except ValueError:
        print(f"Invalid input. {field_name} must be a number.")
        return None


def validate_salary(val_str):
    try:
        val = float(val_str)
        if val <= 0:
            print("Salary must be greater than zero.")
            return None
        return val
    except ValueError:
        print("Invalid input. Salary must be a number.")
        return None


# ------------------------------------------------------------
# 4. CRUD OPERATIONS
# ------------------------------------------------------------

def add_employee():
    print("\nSelect Employee Type:")
    print("1. Full-Time")
    print("2. Part-Time")
    print("3. Freelancer")
    
    choice = input("Enter type: ")
    if choice not in ['1', '2', '3']:
        print("Invalid employee type.")
        return

    emp_id_input = input("Enter Employee ID: ")
    validated_id = validate_employee_id(emp_id_input)
    if validated_id is None:
        return

    name = input("Enter Name: ").strip()
    if not name:
        print("Name must not be empty.")
        return

    age_input = input("Enter Age: ")
    age = validate_age(age_input)
    if age is None:
        return

    department = input("Enter Department: ").strip()
    phone = input("Enter Phone: ").strip()
    email = input("Enter Email: ").strip()

    if choice == '1':
        salary_input = input("Enter Basic Salary: ")
        salary = validate_salary(salary_input)
        if salary is None:
            return
        emp = FullTimeEmployee(validated_id, name, age, department, phone, email, salary)
        employees_list.append(emp)
        print("\nEmployee added successfully.")

    elif choice == '2':
        rate_input = input("Enter Hourly Rate: ")
        rate = validate_salary(rate_input)
        if rate is None:
            return
        emp = PartTimeEmployee(validated_id, name, age, department, phone, email, rate)
        employees_list.append(emp)
        print("\nPart-Time employee added successfully.")

    elif choice == '3':
        rate_input = input("Enter Rate Per Project: ")
        rate = validate_salary(rate_input)
        if rate is None:
            return
        emp = Freelancer(validated_id, name, age, department, phone, email, rate)
        employees_list.append(emp)
        print("\nFreelancer added successfully.")

    save_employees()


def display_all_employees():
    if not employees_list:
        print("\nNo employees found.")
        return

    print("\n" + "-" * 70)
    print(f"{'ID':<8}{'-'*6:<18}{'Type':<14}{'Department':<18}{'Salary/Rate'}")
    print("-" * 70)
    for emp in employees_list:
        if isinstance(emp, FullTimeEmployee):
            rate_str = str(emp.basic_salary)
        elif isinstance(emp, PartTimeEmployee):
            rate_str = f"{emp.hourly_rate}/hour"
        else:
            rate_str = f"{emp.project_rate}/project"
        print(f"{emp.emp_id:<8}{emp.name:<18}{emp.emp_type:<14}{emp.department:<18}{rate_str}")
    print("-" * 70)
    print(f"Total Employees: {len(employees_list)}")


def find_employee_by_id_obj(emp_id):
    for emp in employees_list:
        if emp.emp_id == emp_id:
            return emp
    return None


def search_employee():
    while True:
        print("\n------------------------")
        print("SEARCH EMPLOYEE")
        print("------------------------")
        print("1. Search by ID")
        print("2. Search by Name")
        print("3. Search by Department")
        print("4. Display by Employee Type")
        print("0. Back")
        
        choice = input("\nEnter your choice: ")
        if choice == '1':
            try:
                emp_id = int(input("Enter Employee ID: "))
                emp = find_employee_by_id_obj(emp_id)
                if emp:
                    print("\nEmployee Found\n")
                    print(f"Employee ID: {emp.emp_id}")
                    print(f"Name: {emp.name}")
                    print(f"Age: {emp.age}")
                    print(f"Department: {emp.department}")
                    print(f"Type: {emp.emp_type}")
                    print(f"Phone: {emp.phone}")
                    print(f"Email: {emp.email}")
                    if isinstance(emp, FullTimeEmployee):
                        print(f"Basic Salary: {emp.basic_salary} EGP")
                        print(f"Absent Days: {emp.absent_days}")
                        print(f"Late Days: {emp.late_days}")
                    elif isinstance(emp, PartTimeEmployee):
                        print(f"Hourly Rate: {emp.hourly_rate} EGP")
                        print(f"Working Hours: {emp.working_hours}")
                    else:
                        print(f"Project Rate: {emp.project_rate} EGP")
                        print(f"Completed Projects: {emp.completed_projects}")
                    print(f"Bonus: {emp.bonus} EGP")
                    print(f"Deduction: {emp.deduction} EGP")
                else:
                    print("\nError: Employee not found.")
            except ValueError:
                print("Invalid ID format.")
        elif choice == '2':
            name_q = input("Enter Name to search: ").lower()
            found = False
            for emp in employees_list:
                if name_q in emp.name.lower():
                    print(f"Found: ID: {emp.emp_id}, Name: {emp.name}, Type: {emp.emp_type}")
                    found = True
            if not found:
                print("No employees matched that name.")
        elif choice == '3':
            dept_q = input("Enter Department: ").lower()
            found = False
            for emp in employees_list:
                if dept_q in emp.department.lower():
                    print(f"Found: ID: {emp.emp_id}, Name: {emp.name}, Dept: {emp.department}")
                    found = True
            if not found:
                print("No employees found in this department.")
        elif choice == '4':
            print("1. Full-Time\n2. Part-Time\n3. Freelancer")
            t_choice = input("Select type: ")
            t_map = {'1': 'Full-Time', '2': 'Part-Time', '3': 'Freelancer'}
            if t_choice in t_map:
                target = t_map[t_choice]
                for emp in employees_list:
                    if emp.emp_type == target:
                        print(f"ID: {emp.emp_id}, Name: {emp.name}, Dept: {emp.department}")
            else:
                print("Invalid choice.")
        elif choice == '0':
            break
        else:
            print("Invalid menu option. Please try again.")


def update_employee():
    try:
        emp_id = int(input("Enter Employee ID: "))
        emp = find_employee_by_id_obj(emp_id)
        if not emp:
            print("Error: Employee not found.")
            return

        print(f"\nEmployee Found:\n{emp.name}")
        print("\nSelect field to update:")
        print("1. Name\n2. Age\n3. Department\n4. Phone\n5. Email\n6. Salary / Rate\n0. Cancel")
        
        choice = input("\nEnter choice: ")
        if choice == '1':
            emp.name = input("Enter New Name: ")
        elif choice == '2':
            new_age = validate_age(input("Enter New Age: "))
            if new_age: emp.age = new_age
        elif choice == '3':
            emp.department = input("Enter New Department: ")
        elif choice == '4':
            emp.phone = input("Enter New Phone: ")
        elif choice == '5':
            emp.email = input("Enter New Email: ")
        elif choice == '6':
            if isinstance(emp, FullTimeEmployee):
                print(f"Current Salary: {emp.basic_salary}")
                val = validate_salary(input("Enter New Salary: "))
                if val: emp.basic_salary = val
            elif isinstance(emp, PartTimeEmployee):
                print(f"Current Hourly Rate: {emp.hourly_rate}")
                val = validate_salary(input("Enter New Hourly Rate: "))
                if val: emp.hourly_rate = val
            elif isinstance(emp, Freelancer):
                print(f"Current Project Rate: {emp.project_rate}")
                val = validate_salary(input("Enter New Project Rate: "))
                if val: emp.project_rate = val
        elif choice == '0':
            return
        else:
            print("Invalid choice.")
            return

        print("\nEmployee updated successfully.")
        save_employees()
    except ValueError:
        print("Invalid input format.")


def delete_employee():
    try:
        emp_id = int(input("Enter Employee ID: "))
        emp = find_employee_by_id_obj(emp_id)
        if not emp:
            print("Error: Employee not found.")
            return

        conf = input(f"Are you sure you want to delete employee {emp.emp_id} ({emp.name})? (y/n): ").lower()
        if conf == 'y':
            employees_list.remove(emp)
            print("Employee deleted successfully.")
            save_employees()
        else:
            print("Deletion cancelled.")
    except ValueError:
        print("Invalid ID format.")


# ------------------------------------------------------------
# 5. ATTENDANCE & METRICS MANAGEMENT
# ------------------------------------------------------------

def attendance_menu():
    while True:
        print("\n------------------------")
        print("ATTENDANCE MANAGEMENT")
        print("------------------------")
        print("1. Mark Present")
        print("2. Mark Absent")
        print("3. Record Late Day")
        print("4. Add Working Hours")
        print("5. Add Completed Project")
        print("6. Display Attendance Report")
        print("0. Back")

        choice = input("\nEnter your choice: ")
        if choice in ['1', '2', '3', '4', '5']:
            try:
                emp_id = int(input("Enter Employee ID: "))
                emp = find_employee_by_id_obj(emp_id)
                if not emp:
                    print("Error: Employee not found.")
                    continue

                if choice == '1':
                    print(f"Attendance marked present for {emp.name}.")
                elif choice == '2':
                    if isinstance(emp, FullTimeEmployee):
                        emp.absent_days += 1
                        print("\nAbsence recorded successfully.")
                        print(f"Employee: {emp.name}\nTotal Absent Days: {emp.absent_days}")
                        save_employees()
                    else:
                        print("Error: Absence tracking is only for Full-Time employees.")
                elif choice == '3':
                    if isinstance(emp, FullTimeEmployee):
                        emp.late_days += 1
                        print("\nLate arrival recorded successfully.")
                        print(f"Employee: {emp.name}\nTotal Late Days: {emp.late_days}")
                        save_employees()
                    else:
                        print("Error: Late tracking is only for Full-Time employees.")
                elif choice == '4':
                    if isinstance(emp, PartTimeEmployee):
                        hrs = float(input("Enter Working Hours to Add: "))
                        if hrs < 0:
                            print("Hours cannot be negative.")
                        else:
                            emp.working_hours += hrs
                            print("\nWorking hours updated successfully.")
                            print(f"Employee: {emp.name}\nAdded Hours: {hrs}\nTotal Working Hours: {emp.working_hours}")
                            save_employees()
                    else:
                        print("Error: Working hours are only for Part-Time employees.")
                elif choice == '5':
                    if isinstance(emp, Freelancer):
                        projs = int(input("Enter Number of Completed Projects to Add: "))
                        if projs < 0:
                            print("Projects cannot be negative.")
                        else:
                            emp.completed_projects += projs
                            print("\nCompleted projects updated successfully.")
                            print(f"Employee: {emp.name}\nProjects Added: {projs}\nTotal Completed Projects: {emp.completed_projects}")
                            save_employees()
                    else:
                        print("Error: Projects tracking is only for Freelancers.")
            except ValueError:
                print("Invalid numeric input.")
        elif choice == '6':
            try:
                emp_id = int(input("Enter Employee ID: "))
                emp = find_employee_by_id_obj(emp_id)
                if emp:
                    print(f"\n--- Attendance Report: {emp.name} ({emp.emp_type}) ---")
                    if isinstance(emp, FullTimeEmployee):
                        print(f"Absent Days: {emp.absent_days}")
                        print(f"Late Days: {emp.late_days}")
                    elif isinstance(emp, PartTimeEmployee):
                        print(f"Total Working Hours: {emp.working_hours}")
                    else:
                        print(f"Completed Projects: {emp.completed_projects}")
                else:
                    print("Employee not found.")
            except ValueError:
                print("Invalid ID.")
        elif choice == '0':
            break
        else:
            print("Invalid menu option.")


# ------------------------------------------------------------
# 6. SALARY & BONUS/DEDUCTION MANAGEMENT
# ------------------------------------------------------------

def salary_menu():
    while True:
        print("\n------------------------")
        print("SALARY MANAGEMENT")
        print("------------------------")
        print("1. Calculate Employee Salary")
        print("2. Display Salary Details")
        print("3. Add Bonus")
        print("4. Add Deduction")
        print("5. Calculate Total Payroll")
        print("6. Display Highest Paid Employee")
        print("7. Display Lowest Paid Employee")
        print("0. Back")

        choice = input("\nEnter your choice: ")
        if choice == '1' or choice == '2':
            try:
                emp_id = int(input("Enter Employee ID: "))
                emp = find_employee_by_id_obj(emp_id)
                if not emp:
                    print("Error: Employee not found.")
                    continue

                final_sal = emp.calculate_salary()
                print("\n========================================")
                print("SALARY DETAILS")
                print("========================================")
                print(f"Employee: {emp.name}")
                print(f"Employee Type: {emp.emp_type}")
                if isinstance(emp, FullTimeEmployee):
                    print(f"Basic Salary:             {emp.basic_salary} EGP")
                    print(f"Bonus:                     {emp.bonus} EGP")
                    print(f"Manual Deduction:           {emp.deduction} EGP")
                    print(f"Absent Days:                  {emp.absent_days}")
                    print(f"Absence Deduction:           {emp.absent_days * 200} EGP")
                    print(f"Late Days:                    {emp.late_days}")
                    print(f"Late Deduction:               {emp.late_days * 50} EGP")
                elif isinstance(emp, PartTimeEmployee):
                    print(f"Hourly Rate:              {emp.hourly_rate} EGP")
                    print(f"Working Hours:            {emp.working_hours}")
                    print(f"Bonus:                     {emp.bonus} EGP")
                    print(f"Deduction:                 {emp.deduction} EGP")
                else:
                    print(f"Project Rate:             {emp.project_rate} EGP")
                    print(f"Completed Projects:       {emp.completed_projects}")
                    print(f"Bonus:                     {emp.bonus} EGP")
                    print(f"Deduction:                 {emp.deduction} EGP")
                print("-" * 40)
                print(f"Final Salary:             {final_sal} EGP")
                print("========================================")
            except ValueError:
                print("Invalid ID.")
        elif choice == '3':
            try:
                emp_id = int(input("Enter Employee ID: "))
                emp = find_employee_by_id_obj(emp_id)
                if not emp:
                    print("Error: Employee not found.")
                    continue
                amt = float(input("Enter Bonus Amount: "))
                if amt < 0:
                    print("Bonus cannot be negative.")
                else:
                    emp.bonus += amt
                    print("\nBonus added successfully.")
                    print(f"Employee: {emp.name}\nBonus Added: {amt} EGP\nTotal Bonus: {emp.bonus} EGP")
                    save_employees()
            except ValueError:
                print("Invalid input.")
        elif choice == '4':
            try:
                emp_id = int(input("Enter Employee ID: "))
                emp = find_employee_by_id_obj(emp_id)
                if not emp:
                    print("Error: Employee not found.")
                    continue
                amt = float(input("Enter Deduction Amount: "))
                if amt < 0:
                    print("Deduction cannot be negative.")
                else:
                    emp.deduction += amt
                    print("\nDeduction added successfully.")
                    print(f"Employee: {emp.name}\nDeduction Added: {amt} EGP\nTotal Deduction: {emp.deduction} EGP")
                    save_employees()
            except ValueError:
                print("Invalid input.")
        elif choice == '5':
            total = sum(emp.calculate_salary() for emp in employees_list)
            print(f"\nTotal Payroll: {total} EGP")
        elif choice == '6':
            if not employees_list:
                print("No employees available.")
            else:
                highest = max(employees_list, key=lambda e: e.calculate_salary())
                print(f"\nHighest Paid Employee:\n{highest.name} - {highest.calculate_salary()} EGP")
        elif choice == '7':
            if not employees_list:
                print("No employees available.")
            else:
                lowest = min(employees_list, key=lambda e: e.calculate_salary())
                print(f"\nLowest Paid Employee:\n{lowest.name} - {lowest.calculate_salary()} EGP")
        elif choice == '0':
            break
        else:
            print("Invalid choice.")


# ------------------------------------------------------------
# 7. REPORTS & STATISTICS
# ------------------------------------------------------------

def payroll_report():
    if not employees_list:
        print("No employees available for report.")
        return

    print("\n========================================")
    print("MONTHLY PAYROLL REPORT")
    print("========================================")
    print(f"{'ID':<8}{'Name':<16}{'Type':<14}{'Final Salary'}")
    print("-" * 50)
    
    total = 0.0
    highest = employees_list[0]
    lowest = employees_list[0]

    for emp in employees_list:
        sal = emp.calculate_salary()
        total += sal
        if sal > highest.calculate_salary(): highest = emp
        if sal < lowest.calculate_salary(): lowest = emp
        print(f"{emp.emp_id:<8}{emp.name:<16}{emp.emp_type:<14}{sal}")

    avg = total / len(employees_list)
    print("-" * 50)
    print(f"Total Payroll: {total} EGP")
    print(f"Average Salary: {round(avg, 2)} EGP\n")
    print(f"Highest Paid Employee:\n{highest.name} - {highest.calculate_salary()} EGP\n")
    print(f"Lowest Paid Employee:\n{lowest.name} - {lowest.calculate_salary()} EGP")
    print("========================================")


def employee_statistics():
    total_count = len(employees_list)
    ft_count = sum(1 for e in employees_list if e.emp_type == "Full-Time")
    pt_count = sum(1 for e in employees_list if e.emp_type == "Part-Time")
    fl_count = sum(1 for e in employees_list if e.emp_type == "Freelancer")

    total_payroll = sum(e.calculate_salary() for e in employees_list)
    avg_salary = total_payroll / total_count if total_count > 0 else 0

    print("\n========================================")
    print("EMPLOYEE STATISTICS")
    print("========================================")
    print(f"Total Employees: {total_count}\n")
    print(f"Full-Time Employees: {ft_count}")
    print(f"Part-Time Employees: {pt_count}")
    print(f"Freelancers: {fl_count}\n")
    print(f"Total Payroll: {total_payroll} EGP")
    print(f"Average Salary: {round(avg_salary, 2)} EGP")
    print("========================================")


# ------------------------------------------------------------
# 8. MAIN MENU LOOP
# ------------------------------------------------------------

def main():
    load_employees()
    while True:
        print("\n========================================")
        print("      EMPLOYEE MANAGEMENT SYSTEM        ")
        print("========================================")
        print("1. Add Employee")
        print("2. Display All Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Attendance Management")
        print("7. Bonus Management")
        print("8. Deduction Management")
        print("9. Calculate Employee Salary")
        print("10. Payroll Report")
        print("11. Employee Statistics")
        print("12. Save Data")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            add_employee()
        elif choice == '2':
            display_all_employees()
        elif choice == '3':
            search_employee()
        elif choice == '4':
            update_employee()
        elif choice == '5':
            delete_employee()
        elif choice == '6':
            attendance_menu()
        elif choice == '7' or choice == '8':
            salary_menu()
        elif choice == '9':
            salary_menu()
        elif choice == '10':
            payroll_report()
        elif choice == '11':
            employee_statistics()
        elif choice == '12':
            save_employees()
        elif choice == '0':
            print("\nSaving employee data...")
            save_employees()
            print("Thank you for using the Employee Management System.")
            print("Goodbye!")
            break
        else:
            print("Invalid menu option. Please try again.")

if __name__ == "__main__":
    main()

