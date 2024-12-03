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
