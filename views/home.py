"""Home and static views"""

# Third party imports
from flask import render_template



def home_view():
    """Home view"""
    return render_template("home.html")


def contact_view():
    """contact view"""
    return render_template("contact.html")