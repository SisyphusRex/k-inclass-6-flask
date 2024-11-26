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

    # Return the form for adding a new employee
    return render_template(
        "employee/employee_add.html",
    )
