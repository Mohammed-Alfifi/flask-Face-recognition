# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_file, redirect, url_for, flash
from flask_login import login_required, current_user
import csv
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)


def clean_old_records():
    # مسار ملف CSV
    file_path = 'static/records.csv'

    # قراءة البيانات من ملف CSV
    df = pd.read_csv(file_path, encoding='UTF-8')

    # تحويل عمود التاريخ إلى نوع datetime
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")

    # الحصول على التاريخ الحالي
    now = datetime.now()

    # تحديد الحد الأقصى للتاريخ (أسبوع واحد)
    cutoff_date = now - timedelta(days=7)

    # فلترة السجلات للحفاظ على السجلات من آخر أسبوع فقط
    df_filtered = df[df['Date'] > cutoff_date]

    # كتابة البيانات المحدثة إلى ملف CSV
    df_filtered.to_csv(file_path, index=False, encoding='UTF-8')


def setup_attendance_routes(app):
    # عرض سجلات الحضور
    @app.route("/AttendanceSheet")
    @login_required
    def AttendanceSheet():
        if current_user.role == 'user':
            flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
            return redirect(url_for('index'))
        rows = []
        with open('static/todayAttendance.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
        fieldnames = ['Id', 'Name', 'Department', 'Time', 'Date', 'Status']
        return render_template('RecordsPage.html', allrows=rows, fieldnames=fieldnames, len=len)

    # تنزيل جميع السجلات (مدمجة لجميع التواريخ)
    @app.route("/resetToday")
    @login_required
    def resetToday():
        df = pd.read_csv('static/records.csv')
        df = df[df['Date'] != datetime.now().strftime("%d-%m-%Y")]
        df.to_csv("static/records.csv", index=False)
        return redirect('/AttendanceSheet')
    @app.route("/downloadAll")
    def downloadAll():
        if current_user.role == 'user':
            flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
            return redirect(url_for('index'))
        return send_file('static/todayAttendance.csv', as_attachment=True)

    # تنزيل سجلات الحضور لليوم فقط
    @app.route("/downloadToday")
    def downloadToday():
        if current_user.role == 'user':
            flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
            return redirect(url_for('index'))

        try:
            df = pd.read_csv("static/records.csv", encoding='UTF-8')
            # تحديث التنسيق هنا ليطابق التنسيق في ملف CSV
            df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y")

            today = datetime.now().strftime("%d-%m-%Y")
            df_today = df[df['Date'].dt.strftime("%d-%m-%Y") == today]

            if df_today.empty:
                flash('لا توجد سجلات لليوم.', 'info')
                return redirect(url_for('AttendanceSheet'))

            today_file_path = "static/todayAttendance.csv"
            df_today.to_csv(today_file_path, index=False, encoding='ISO-8859-1', date_format="%d-%m-%Y")
            return send_file(today_file_path, as_attachment=True)
        except Exception as e:
            flash(str(e), 'error')
            return redirect(url_for('AttendanceSheet'))
