# -*- coding: utf-8 -*-
# تعيين الترميز لضمان التعامل الصحيح مع النصوص باللغة العربية
# مكتبات الـ MVC Framework
from flask import Flask, render_template, request, Response, redirect, send_file, session, url_for, flash
from flask_login import LoginManager, login_required, UserMixin, current_user, login_user, logout_user
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
# مكتبات التعامل مع الصور والفيديو
import cv2  # استيراد OpenCV لمعالجة الصور وتحليل الوجوه
import dlib  # استيراد مكتبة dlib للكشف عن الوجوه واستخدام نماذج الكشف
import face_recognition  # استيراد face_recognition لتقنية التعرف على الوجه
from deepface import DeepFace  # استيراد DeepFace لتسهيل تنفيذ عمليات التعرف على الوجه
from imutils import face_utils  # استيراد face_utils من مكتبة imutils لمساعدة في تيسير عمليات معالجة الوجه
# مكتبات التعامل مع البيانات والرسوم البيانية
import numpy as np  # استيراد NumPy للتعامل مع البيانات بشكل علمي
import pandas as pd  # استيراد pandas للتعامل مع البيانات في هيكل DataFrame
import plotly  # استيراد plotly لرسم الرسوم البيانية التفاعلية
import plotly.express as px  # استيراد plotly.express لرسم الرسوم البيانية بشكل مبسط
import json  # استيراد json للتعامل مع بيانات JSON
# مكتبات الوقت والقياس
from datetime import datetime  # استيراد datetime للتعامل مع التواريخ والأوقات
import timeit  # استيراد timeit لقياس الوقت
import time  # استيراد وحدة الوقت للتحكم في التوقيت
# مكتبات مساعدة
import os  # استيراد وحدة os للتفاعل مع نظام التشغيل
import arabic_reshaper  # استيراد arabic_reshaper لإعادة تشكيل النصوص العربية
from bidi.algorithm import get_display  # استيراد get_display لدعم الكتابة من اليمين إلى اليسار
from PIL import ImageFont, Image, ImageDraw  # استيراد مكتبة PIL للتعامل مع الصور والنصوص
# مكتبات مساعدة إضافية
from random import randint  # استيراد وحدة randint من مكتبة random لإنشاء أرقام عشوائية

from chatbot import setup_routes as chatbot_routes
from AttendanceSheet import setup_attendance_routes as attendance_routes
app = Flask(__name__)
chatbot_routes(app)
# ربط مراجعات AttendanceSheet بالتطبيق
attendance_routes(app)
# configurations for database and mail
# إعدادات لقاعدة البيانات والبريد الإلكتروني
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///EmployeeDB.db"  # تحديد موقع قاعدة البيانات ونوعها (SQLite في هذه الحالة)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # تعطيل تتبع التعديلات لتجنب إشعارات غير ضرورية
app.config['SECRET_KEY'] = 'mysecretkey'  # تعيين مفتاح سري لتوقيع الجلسات في التطبيق
db = SQLAlchemy(app)  # إعداد كائن قاعدة البيانات باستخدام Flask-SQLAlchemy
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # تحديد خادم البريد الإلكتروني
app.config['MAIL_PORT'] = 587  # تحديد منفذ البريد الإلكتروني
app.config['MAIL_USE_TLS'] = True  # تمكين استخدام TLS لتشفير الاتصال
app.config['MAIL_USERNAME'] = 'alfifi115@gmail.com'  # اسم مستخدم البريد الإلكتروني
app.config['MAIL_PASSWORD'] = 'tebx okao jwft qlic'  # كلمة مرور البريد الإلكتروني
login_manager = LoginManager()  # إعداد كائن لإدارة تسجيل الدخول باستخدام Flask-Login
login_manager.init_app(app)  # تهيئة التطبيق لاستخدام إدارة تسجيل الدخول
login_manager.login_view = 'login'  # تحديد عرض تسجيل الدخول
mail_ = Mail(app)  # إعداد كائن البريد الإلكتروني باستخدام Flask-Mail
# تحميل ملف توقع الشكل
shape_predictor_path = 'templates/shape_predictor_68_face_landmarks.dat'
predictor = dlib.shape_predictor(shape_predictor_path)
# تحميل ملف نموذج التعرف على الوجه
face_recognition_model_path = 'templates/dlib_face_recognition_resnet_model_v1.dat'
face_recognition_model = dlib.face_recognition_model_v1(face_recognition_model_path)
faceCascade = cv2.CascadeClassifier('templates/frontalface.xml')
# تحديد مسار مجلد الصور التدريبية
path = 'static/TrainingImages'
file_paths = ['static/records.csv', 'static/todayAttendance.csv']
# تحميل المستخدم عند الطلب باستخدام Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return users.query.get(user_id)
# نموذج لقاعدة بيانات الموظفين
class employee(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    hiringDate = db.Column(db.String(10), default=datetime.now().strftime("%d-%m-%Y"))
    def __repr__(self) -> str:
        return f"{self.id} - {self.name} - {self.department} - {self.email} - {self.hiringDate}"
# نموذج لقاعدة بيانات المستخدمين/المالك
class users(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=True)
    mail = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(80), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(20), nullable=True)
    def __repr__(self):
        return '<User {}>'.format(self.username)
# الكود التالي يعرف مسارات ووظائف في تطبيق ويب Flask:
@app.route('/admin-only')
@login_required
def admin_only_route():
    if current_user.role != 'admin':
        # إعادة توجيه المستخدمين غير الأدمن إلى صفحة أخرى أو عرض رسالة خطأ
        return redirect(url_for('index'))
# هذا المسار يتعامل مع الصفحة الرئيسية للتطبيق.
@app.route('/')
def index():
    try:
        # محاولة إلغاء تشغيل كائن التقاط الكاميرا الأول (cap)
        cap.release()
    except:
        pass
    try:
        # محاولة إلغاء تشغيل كائن التقاط الكاميرا الثاني (cap2)
        cap2.release()
    except:
        pass
    # إرجاع قالب HTML المقابل لصفحة الرئيسية
    return render_template('index.html')
# هذا المسار يتعامل مع وظيفة تسجيل الدخول، سواء عرض نموذج تسجيل الدخول أو معالجة طلبات تسجيل الدخول.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.query.filter_by(username=username).first()
        if user is not None and user.password == password:
            otp = randint(100000, 999999)  # توليد رمز OTP
            sendResetMail(user.mail, otp)  # إرسال رمز OTP إلى البريد الإلكتروني للمستخدم
            session['user_id_temp'] = user.id  # حفظ معرف المستخدم مؤقتًا
            session['otp'] = otp  # حفظ الرمز المؤقت في الجلسة
            return redirect(url_for('verifyOTP'))  # توجيه المستخدم إلى صفحة التحقق من OTP
        else:
            return render_template('login.html', incorrect=True)
    return render_template('login.html')
def sendResetMail(mail, otp):
    msg = Message('إعادة تسجيل ', recipients=[mail], sender='your_email@example.com')
    msg.body = f'''كلمة المرور الخاصة بك هي {str(otp)}. '''
    mail_.send(msg)
# إضافة مسار للتحقق من صحة الرمز المؤقت
@app.route('/verifyOTP', methods=['GET', 'POST'])
def verifyOTP():
    if request.method == 'POST':
        user_otp = int(request.form['otp'])
        if 'otp' in session and session['otp'] == user_otp:
            user_id = session.pop('user_id_temp', None)
            user = users.query.filter_by(id=user_id).first()
            if user:
                login_user(user)  # تسجيل دخول المستخدم
                return redirect('/')  # توجيه المستخدم إلى الصفحة الرئيسية
            else:
                return redirect(url_for('login'))
        else:
            return render_template('OTP.html', incorrect=True)
    return render_template('OTP.html')
# هذا المسار يتعامل مع خروج المستخدم. يتطلب من المستخدم أن يكون قد قام بتسجيل الدخول.
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # قم بتسجيل خروج المستخدم وإعادة توجيهه إلى الصفحة الرئيسية
    logout_user()
    return redirect('/')
# تسجيل المستخدم
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.role != 'admin':
        flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
        # إعادة توجيه المستخدمين الذين ليسوا أدمن
        return redirect(url_for('index'))
    if request.method == 'POST':
        # استرجاع بيانات التسجيل من إرسال النموذج
        id = request.form['id']
        username = request.form['username']
        name = request.form['name']
        mail = request.form['mail']
        pass1 = request.form['pass']
        pass2 = request.form['pass2']
        # التحقق من فرادة معرف المالك واسم المستخدم
        user = users.query.filter_by(username=username).first()
        user2 = users.query.filter_by(id=id).first()
        # إذا لم تكن فريدة أو لم تتطابق كلمات المرور، عد إلى صفحة التسجيل مع رسالة توضيحية، وإلا قم بتسجيل المستخدم
        if user is not None or user2 is not None:
            return render_template('signup.html', incorrect=True,msg='المستخدم بنفس المعرف أو اسم المستخدم موجود بالفعل')
        elif pass1 != pass2:
            return render_template('signup.html', incorrect=True, msg="كلمة المرور غير مطابقة")
        else:
            # إنشاء مستخدم جديد وإضافته إلى قاعدة البيانات
            new_user = users(id=id, name=name, mail=mail, username=username, password=pass1)
            db.session.add(new_user)
            db.session.commit()
            # إرسال بريد إلكتروني للمستخدم بعد التسجيل الناجح
            msg = f'''مرحبًا {new_user.name}
لقد تم إنشاء حساب جديد
شكرًا لك.
'''
            sendResetMail(new_user.mail, msg)
            # إعادة توجيه المستخدم إلى صفحة تسجيل الدخول بعد التسجيل الناجح
            return render_template('login.html', registered=True)
    # إذا كانت طريقة الطلب هي GET، عرض صفحة التسجيل
    return render_template('signup.html')
# إضافة موظف جديد إلى قاعدة بيانات الموظفين
@app.route("/add", methods=['GET', 'POST'])
@login_required
def add():
    if current_user.role == 'user':
        flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
        # إعادة توجيه المستخدمين بدور 'user' إلى صفحة أخرى
        return redirect(url_for('index'))
    try:
        # إلغاء تشغيل كائن التقاط الكاميرا الثاني (cap2) إذا كان قائمًا
        cap2.release()
    except:
        pass
    invalid = 0  # 0 لا يوجد مشكلة، 1 إذا كان المعرف غير فريد، 2 إذا لم يتم تحميل الصورة
    if request.method == 'POST':
        # استرجاع بيانات الموظف من إرسال النموذج
        id = request.form['id']
        name = request.form['name']
        dept = request.form['dept']
        mail = request.form['mail']
        # في الكود أدناه، يُعين invalid = 0 لا يوجد مشكلة، invalid = 1 إذا كان المعرف غير فريد،
        # و invalid = 2 إذا لم يتم تحميل الصورة.
        # إذا تم إنشاء الحساب بنجاح، قم بإرسال بريد إلكتروني إلى الموظف، وإلا قم بالتراجع عن آخر إرسال.
        try:
            invalid = 1
            emp = employee(id=id, name=name, department=dept, email=mail)
            db.session.add(emp)
            db.session.commit()
            fileNm = id + '.jpg'
            msg = f'''مرحبًا {dept},
. لقد تم تسجيلك بنجاح في قاعدة بيانات الموظفين.
شكرًا لك.
مسجل حضور الموظف القائم على التعرف على الوجه'''
            sendResetMail(mail, msg)
            try:
                # محاولة حفظ الصورة إذا تم تحميلها
                photo = request.files['photo']
                photo.save(os.path.join(path, fileNm))
            except:
                invalid = 2
                # إذا لم يتم تحميل الصورة، استخدم صورة افتراضية أو احذف المتغير العالمي الخاص بالصورة (pic) إذا كان معرفًا
                cv2.imwrite(os.path.join(path, fileNm), pic)
                del globals()['pic']
            invalid = 0  # إذا وصلت إلى هذا النقطة، فإن العملية تمر بدون مشاكل
        except:
            # إذا حدث أي خطأ، تراجع آخر إرسال
            db.session.rollback()
    # استعراض جميع الصفوف في قاعدة بيانات الموظفين
    allRows = employee.query.all()
    # عرض صفحة إدخال جديدة مع قائمة بكل الصفوف وعلامة تحديد للمشكلة (invalid)
    return render_template("insertPage.html", allRows=allRows, invalid=invalid)
# لحذف موظف موجود
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    if current_user.role == 'user':
        flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
        # إعادة توجيه المستخدمين بدور 'user' إلى صفحة أخرى
        return redirect(url_for('index'))
    # حذف من قاعدة البيانات
    emp = employee.query.filter_by(id=id).first()
    db.session.delete(emp)
    db.session.commit()
    fn = id + ".jpg"
    # حذف الصورة المخزنة في صور التدريب
    try:
        os.unlink(os.path.join(path, fn))
    except:
        pass
    # تحديث حالة الموظف كمُنهي في سجلات الحضور للموظف المحذوف
    df = pd.read_csv("static/records.csv", encoding='ISO-8859-1')
    df.loc[df["Id"] == id, "Status"] = "Terminated"
    df.to_csv("static/records.csv", index=False)
    return redirect("/add")
# لتحديث موظف موجود
@app.route("/update", methods=['GET', 'POST'])
@login_required
def update():
    if current_user.role == 'user':
        flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
        # إعادة توجيه المستخدمين بدور 'user' إلى صفحة أخرى
        return redirect(url_for('index'))
    id = request.form['id']
    emp = employee.query.filter_by(id=id).first()
    # تحديث في قاعدة البيانات
    emp.name = request.form['name']
    emp.department = request.form['dept']
    emp.email = request.form['mail']
    db.session.commit()
    # تحديث الصورة
    fileNm = id + '.jpg'
    try:
        try:
            photo = request.files['photo']
            photo.save(os.path.join(path, fileNm))
        except:
            cv2.imwrite(os.path.join(path, fileNm), pic)
            del globals()['pic']
    except:
        pass
    # تحديث في سجلات الحضور
    df = pd.read_csv("static/records.csv", encoding='ISO-8859-1')
    df.loc[(df["Id"] == id) & (df['Status'] == 'On Service'), ['Name', 'Department']] = [emp.name, emp.department]
    df.to_csv("static/records.csv", index=False)
    return redirect("/add")
# إنشاء إطارات لالتقاط الصورة
def gen_frames_takePhoto():
    start = timeit.default_timer()
    flag = False
    num = -1
    while True:
        ret, frame = cap2.read()  # قراءة الإطار من الكاميرا
        if ret:
            # تغيير حجم الإطار وتحويله إلى اللون الرمادي
            frameS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            frameS = cv2.cvtColor(frameS, cv2.COLOR_BGR2RGB)
            # البحث عن مواقع الوجوه
            facesLoc = face_recognition.face_locations(frameS)
            # إذا لم يتم العثور على وجه، لا تقم بالتقاط الصورة
            if not facesLoc:
                continue
            if num == 0:
                # إذا تم الانتهاء من الترقيم لالتقاط الصورة، قم بإطلاق الكاميرا وحفظ الصورة
                global pic
                pic = frame
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                # playsound("static/cameraSound.wav")
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                cap2.release()
                break
            # إذا كان هناك أكثر من شخص في الإطار، فلا تنظر إلى ذلك
            if len(facesLoc) > 1:
                cv2.putText(frame, "Only one person allowed", (100, 150),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                flag = False
                continue
            for faceLoc in facesLoc:
                # analyze the frame and look for emotion attribute and save it in a result
                result = DeepFace.analyze(
                    frame, actions=['emotion'], enforce_detection=False)
                # face locations
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                # if the smotion is happy, start numbering and check same for 3 upcoming frames
                if result and timeit.default_timer() - start > 5:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    if flag:
                        cv2.putText(frame, str(num), (150, 200), cv2.FONT_HERSHEY_SIMPLEX, 6, (255, 255, 255), 20)
                        time.sleep(1)
                        num = num - 1
                    else:
                        flag = True
                        num = 3
                else:
                    flag = False
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # pass the frame to show on html page
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
# تمرير الإطارات المولدة إلى صفحة HTML
@app.route('/takePhoto', methods=['GET', 'POST'])
def takePhoto():
    if current_user.role == 'user':
        flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
        # إعادة توجيه المستخدمين بدور 'user' إلى صفحة أخرى
        return redirect(url_for('index'))
    # بدء الكاميرا
    global cap2
    cap2 = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    return Response(gen_frames_takePhoto(), mimetype='multipart/x-mixed-replace; boundary=frame')
# ترميز الوجوه المعروفة
@app.route("/encode")
@login_required
def encode():
    images=[]
    myList= os.listdir(path)
    global encodedList
    global imgNames
    # دالة لحفظ أسماء الصور أي معرفات الموظفين في imgNames
    def findClassNames(myList):
        cNames = []
        for l in myList:
            curImg = cv2.imread(f'{path}/{l}')
            images.append(curImg)
            cNames.append(os.path.splitext(l)[0])
        return cNames
    # دالة لحفظ ترميزات الوجوه في encodedList
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            try:
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            except:
                pass
        return encodeList
    imgNames = findClassNames(myList)
    encodedList = findEncodings(images)
    return render_template("recogPage.html")
# إنشاء إطارات للمعرف
def gen_frames():
    global encodedList
    oldIds = []
    cap = cv2.VideoCapture(0)
    # دالة لتسجيل الحضور
    def markEntry(id):
        with app.app_context():
            with open('static/records.csv', 'r+') as f:
                # استخراج الحضور لليوم الحالي
                myDataList = [
                    line for line in f if datetime.now().strftime('%d-%m-%Y') in line]
                idList = []
                for line in myDataList:
                    entry = line.split(',')
                    idList.append(entry[0])
                # وضع علامة للحضور فقط إذا لم يتم تسجيل الحضور بالفعل للموظف
                if (id not in idList):
                    now = datetime.now()
                    date = now.strftime("%d-%m-%Y")
                    dtime = now.strftime('%H:%M:%S')
                    emp = employee.query.filter_by(id=id).first()
                    f.writelines(
                        f'\n{id},{emp.name},{emp.department}, {dtime},{date},{"On Service"}')
    # التقاط الإطارات من كاميرا الويب
    while True:
        success, img = cap.read()
        if success is True:
            img = cv2.flip(img, 1)
            # تغيير حجم وتحويل الإطار إلى RGB
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            # وضع التاريخ على الإطار
            cv2.putText(img, datetime.now().strftime("%D %H:%M:%S"), (10, 15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (0, 0, 255), 1)
            # استخدام dlib لاكتشاف الوجوه والعلامات الأرضية
            facesCurFrame = face_recognition.face_locations(imgS)
            # لكل وجه في الإطار
            for faceLoc in facesCurFrame:
                # الحصول على العلامات الأرضية الوجهية(shape_predictor_68_face_landmarks.dat:)
                shape = predictor(imgS, dlib.rectangle(*faceLoc))
                # تحويل العلامات إلى مصفوفة numpy
                landmarks = face_utils.shape_to_np(shape)
                # (dlib_face_recognition_resnet_model_v1.dat)الحصول على ترميز الوجه باستخدام dlib
                encodeFace = face_recognition.face_encodings(imgS, [faceLoc])[0]
                # مقارنة ترميز الوجه مع ترميزات الوجوه المعروفة
                threshold = 0.5  #  للتشابه قيمة الحد المرغوبة
                matches = face_recognition.compare_faces(encodedList, encodeFace, tolerance=threshold)
                faceDis = face_recognition.face_distance(encodedList, encodeFace)
                # الشخص ذو المسافة الأقل أقل
                matchIndex = np.argmin(faceDis)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                # إذا كان الشخص معروفًا ، فأظهر الهوية والاسم بلون أخضر وقم بتسجيل الحضور إذا كان يظهر للمرة الأولى في اليوم
                if ((matches[matchIndex]) & (faceDis[matchIndex] < 0.5)):
                    Id = imgNames[matchIndex]
                    with app.app_context():
                        emp = employee.query.filter_by(id=Id).first()
                        cv2.putText(img, Id, (x1, y2 + 25), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (255, 255, 255), 2)
                        reshapedTxt = arabic_reshaper.reshape(emp.name)
                        bidiTxt = get_display(reshapedTxt)
                        fontPath = "alfont_com_arial-1.ttf"
                        font = ImageFont.truetype(fontPath, 32)
                        imgPil = Image.fromarray(img)
                        draw = ImageDraw.Draw(imgPil)
                        draw.text((x1, y2 + 30), bidiTxt, font=font)
                        img = np.array(imgPil)
                        cv2.rectangle(img, (x1, y1), (x2, y2 - 4), (0, 255, 0), 2)
                        markEntry(Id)
                        cv2.rectangle(img, (x1, y1), (x2, y2 - 4), (255, 255, 255), 2)
                        if Id in oldIds:
                            pass
                        else:
                            markEntry(Id)
                            oldIds.append(Id)
                # إذا لم يتطابق ، فأظهر "غير معروف" بلون أحمر
                else:
                    cv2.putText(img, 'unknown', (x1, y2 + 25), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0, 0, 255), 2)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            # إرسال الإطار ليظهر على صفحة HTML
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
# passing generated frames to html page 'recogPage.html'
@app.route('/video', methods=['GET', 'POST'])
def video():
    global cap
    cap = cv2.VideoCapture(0)
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
# بعض الإحصائيات على سجلات الحضور
@app.route("/stats")
@login_required
def stats():
    if current_user.role == 'user':
        flash('ليس لديك صلاحية الوصول إلى هذه الصفحة.', 'warning')
        # إعادة توجيه المستخدمين بدور 'user' إلى صفحة أخرى
        return redirect(url_for('index'))
    # جلب البيانات من ملف csv للحضور وقاعدة بيانات الموظفين
    df = pd.read_csv("static/records.csv", encoding='ISO-8859-1')
    rows = employee.query.all()
    db = [str(row) for row in rows]
    db = pd.DataFrame(db)
    db = pd.DataFrame(data=list(map(lambda x: x.split(" - "), db[0])),columns=['Id', 'Name', 'Department', 'Mail', 'Hiring Date'])
    # إنشاء إطار بيانات يحتوي على عدد الموظفين المسجلين والحاضرين اليومين حسب قسمهم
    today = df[(df["Date"] == datetime.now().strftime("%d-%m-%Y")) & (df['Status'] == 'On Service')]
    today_counts = pd.DataFrame(today.groupby(['Department']).count()['Id'])
    db_counts = pd.DataFrame(db.groupby(['Department']).count()['Id'])
    attendance = pd.merge(db_counts, today_counts,how='outer', left_index=True, right_index=True)
    attendance.columns = ["Registered", "Present"]
    attendance = attendance.fillna(0).astype(int)
    attendance['Absent'] = attendance['Registered'] - attendance['Present']
    # حضور اليوم حسب القسم
    fig1 = px.bar(attendance, x=attendance.index, y=attendance.columns, barmode='group',labels={'value': 'عدد السجناء '},title='قسم الحضور  اليوم', color_discrete_sequence=px.colors.qualitative.T10,template='presentation')
    # حضور القسم بالنسبة المئوية والعدد
    fig2 = []
    for d in db['Department'].unique():
        present = len(today[today['Department'] == d])
        fig2.append(px.pie(df, values=[present, len(db[db['Department'] == d]) - present],names=['Present', 'Absent'], hole=.4, title=d + ' Department',color_discrete_sequence=px.colors.qualitative.T10))
    # حضور السبعة أيام الأخيرة
    dates = df['Date'].unique()[-7:]
    df_last7 = df[df['Date'].isin(dates)]
    fig3 = px.histogram(df_last7, x='Date', color="Department", title='التاريخ والحضور حسب القسم',color_discrete_sequence=px.colors.qualitative.T10, template='presentation')
    # نسبة الحضور الفردية
    hiringDates = [datetime.date(datetime.strptime(d, '%d-%m-%Y')) for d in db['Hiring Date']]
    daysInJob = [(datetime.date(datetime.now()) - d).days + 1 for d in hiringDates]
    presentDays = [len(df[(df['Id'] == id) & (df['Status'] == 'On Service')]) for id in db['Id']]
    db['Attendance(%)'] = [round(presentDays[i] * 100 / daysInJob[i], 2) for i in range(0, len(db))]
    # تحويل الرسوم البيانية إلى JSON للتمريرها إلى الصفحة HTML
    JSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    JSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    JSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    # إرسال البيانات إلى صفحة HTML
    return render_template('statsPage.html', JSON1=JSON1, JSON2=JSON2, JSON3=JSON3,
    depts=db['Department'].unique(),td=[sum(attendance['Registered']), sum(attendance['Present'])],titles=db.columns.values,data=list(db.sort_values(by='Attendance(%)', ascending=False, kind="mergesort").values.tolist()), len=len)
# قاعدة البيانات
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
