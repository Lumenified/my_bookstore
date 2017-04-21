from flask import render_template, abort
from flask_login import login_required, current_user

from . import home

@home.route('/')
def anasayfa():
    """
    for homepage
    """

    return render_template('home/index.html', title="welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    not admin is the one can only reach that page, everone does
    """
    if current_user.is_admin:
        abort(403)

    return render_template('home/dashboard.html', title="Dashboard")

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")
