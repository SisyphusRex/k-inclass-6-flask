"""Employee Views"""

# Third-party imports
from flask import flash, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# First-party imports
from models.employee import Employee

engine = create_engine("sqlite:///db.sqlite3", echo=False)
Session = sessionmaker(bind=engine)
db_session = Session()


def employee_list_view():
    """Display a list of employees from the database"""
    employees = db_session.query(Employee).all()

    return render_template(
        "employee/employee_list.html",
        employees=employees,  # template context; any variables needed by template
    )


def employee_add_view():
    """allow adding a new employee to the database"""

    errors = []

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        weekly_salary = request.form["weekly_salary"]

        if not first_name:
            errors.append("The first name is required.")
        if not last_name:
            errors.append("The last name is required.")
        if not weekly_salary:
            errors.append("The weekly salary is required.")

        if not errors:
            # Create the new Employee
            new_employee = Employee(first_name, last_name, weekly_salary)

            db_session.add(
                new_employee
            )  # if trying to pass letter as float for salary, application crashes here
            db_session.commit()

            flash("User added successfully!", "success")

            return redirect(url_for("employee_list_view"))

    # Return the form for adding a new employee
    return render_template(
        "employee/employee_add.html",
        errors=errors,
    )


def employee_edit_view(pk):
    """allow editing an existing employee to the database"""

    errors = []

    employee = db_session.get(Employee, pk)

    if not employee:
        flash(f"Unknown employee with pk of {pk}", "danger")
        return redirect(url_for("employee_list_view"))

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        weekly_salary = request.form["weekly_salary"]

        if not first_name:
            errors.append("The first name is required.")
        if not last_name:
            errors.append("The last name is required.")
        if not weekly_salary:
            errors.append("The weekly salary is required.")

        if not errors:
            # Create the new Employee
            employee.first_name = first_name
            employee.last_name = last_name
            employee.weekly_salary = weekly_salary
            db_session.commit()

            flash("User updated successfully!", "success")

            return redirect(url_for("employee_list_view"))

    # Return the form for adding a new employee
    return render_template(
        "employee/employee_edit.html",
        employee=employee,
        errors=errors,
    )


def employee_delete_view(pk):
    """show page for deleting an existing employee"""
    errors = []

    employee = db_session.get(Employee, pk)

    if not employee:
        flash(f"Unknown employee with pk of {pk}", "danger")
        return redirect(url_for("employee_list_view"))

    if employee and request.method == "POST":
        db_session.delete(employee)
        db_session.commit()

        flash("User deleted successfully!", "success")

        return redirect(url_for("employee_list_view"))

    return render_template(
        "employee/employee_delete.html",
        employee=employee,
        errors=errors,
    )


def employee_list_api():
    """returns json of employees from the databas"""
    employees = db_session.query(Employee).all()
    return [e.to_dict() for e in employees]


def employee_api(pk):
    """returns json of a single employee identified by pk from database"""
    employee = db_session.get(Employee, pk)
    return employee.to_dict()
