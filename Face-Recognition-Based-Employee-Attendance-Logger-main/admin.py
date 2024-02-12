from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__)
@admin_bp.route('/admin-only')
@login_required
def admin_only_route():
    if current_user.role != 'admin':
        flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
        return redirect(url_for('index'))
