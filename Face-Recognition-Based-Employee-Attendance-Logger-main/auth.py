from flask import Blueprint, redirect
from flask_login import login_required, logout_user

# ÅäÔÇÁ Blueprint
auth = Blueprint('auth', __name__)

# ÊÚÑíİ ØÑíŞ ÇáÎÑæÌ
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()  # Şã ÈÊÓÌíá ÎÑæÌ ÇáãÓÊÎÏã
    return redirect('/')  # ÅÚÇÏÉ ÊæÌíå ÇáãÓÊÎÏã Åáì ÇáÕİÍÉ ÇáÑÆíÓíÉ
