from flask import Blueprint, redirect
from flask_login import login_required, logout_user

# ����� Blueprint
auth = Blueprint('auth', __name__)

# ����� ���� ������
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()  # �� ������ ���� ��������
    return redirect('/')  # ����� ����� �������� ��� ������ ��������
