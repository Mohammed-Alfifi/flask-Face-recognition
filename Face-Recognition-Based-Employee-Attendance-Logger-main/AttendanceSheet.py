# -*- coding: utf-8 -*-


from flask import Flask, render_template, send_file, redirect, url_for, flash
from flask_login import login_required, current_user
import csv
import pandas as pd
from datetime import datetime

def setup_attendance_routes(app):
# عرض سجلات الحضور
    @app.route("/AttendanceSheet")
    @login_required
    def AttendanceSheet():
        if current_user.role == 'user':
            flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
        # إعادة توجيه المستخدمين بدور 'user' إلى صفحة أخرى
            return redirect(url_for('index'))
        rows = []
    # فتح ملف السجلات وقراءة البيانات منه
        with open('static/records.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
        fieldnames = ['Id', 'Name', 'Department', 'Time', 'Date', 'Status']
    # إعادة تقديم البيانات لصفحة HTML
        return render_template('RecordsPage.html', allrows=rows, fieldnames=fieldnames, len=len)


# تنزيل جميع السجلات (مدمجة لجميع التواريخ)
    @app.route("/downloadAll")
    def downloadAll():
        if current_user.role == 'user':
            flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
        # إعادة توجيه المستخدمين بدور 'user' إلى صفحة أخرى
            return redirect(url_for('index'))

    # إرسال ملف السجلات كتنزيل مضغوط
        return send_file('static/records.csv', as_attachment=True)


# تنزيل سجلات الحضور لليوم فقط
    @app.route("/downloadToday")
    def downloadToday():
        if current_user.role == 'user':
            flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
        # إعادة توجيه المستخدمين بدور 'user' إلى صفحة أخرى
            return redirect(url_for('index'))

    # استخراج سجلات اليوم فقط وتصديرها إلى ملف CSV
        df = pd.read_csv("static/records.csv", encoding='ISO-8859-1')
        df = df[df['Date'] == datetime.now().strftime("%d-%m-%Y")]
        df.to_csv("static/todayAttendance.csv", index=False, encoding='ISO-8859-1')
    # إرسال ملف الحضور لليوم كتنزيل مضغوط
        return send_file('static/todayAttendance.csv', as_attachment=True)


# إعادة تعيين حضور اليوم
    @app.route("/resetToday")
    @login_required
    def resetToday():
        if current_user.role == 'user':
            flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
        # إعادة توجيه المستخدمين بدور 'user' إلى صفحة أخرى
            return redirect(url_for('index'))

    # قراءة ملف السجلات وإزالة الحضور لليوم الحالي
        df = pd.read_csv("static/records.csv", encoding='ISO-8859-1')
        df = df[df['Date'] != datetime.now().strftime("%d-%m-%Y")]
        df.to_csv("static/records.csv", index=False)
        # إعادة توجيه المستخدم إلى صفحة سجلات الحضور
        return redirect('/AttendanceSheet')
