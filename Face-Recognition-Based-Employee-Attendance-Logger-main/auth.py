from flask import Blueprint, redirect
from flask_login import login_required, logout_user

# إنشاء Blueprint
auth = Blueprint('auth', __name__)

# تعريف طريق الخروج
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()  # قم بتسجيل خروج المستخدم
    return redirect('/')  # إعادة توجيه المستخدم إلى الصفحة الرئيسية
