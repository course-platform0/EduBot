import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from kavenegar import *

# important data
if True:
    kave_Api = 'YOUR_KAVE_API'


def send_email(to, subject, body):
    # اطلاعات حساب Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_user = "python.danehkar@gmail.com"  # ایمیل خود را اینجا وارد کنید
    email_password = "qlfu fwdw udbt valn"  # رمز عبور خود را اینجا وارد کنید

    # ایجاد ایمیل
    to_email = to  # ایمیل گیرنده
    subject = subject
    body = body

    # ساختار ایمیل
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = to_email
    msg['Subject'] = subject
    # اضافه کردن متن به ایمیل
    # msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(body, 'html'))

    try:
        # اتصال به سرور و ارسال ایمیل
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # استفاده از TLS
        server.login(email_user, email_password)  # ورود به حساب
        server.sendmail(email_user, to_email, msg.as_string())  # ارسال ایمیل
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()  # قطع اتصال


#کد فعالسازی را در یک قالب html برمی‌گردانیم...
def html_body(code):
    html = f'''
 

      <div >
        <img style="width:300px;height:300px;margin:auto"  src="https://s5.uupload.ir/files/dastyar/mysite/mysite_files/python_danekar_t1.jpg" />
    </div>
    <hr/>
    <b style="text-align: center"> سلام به بوتکمپ دانه‌کار خوش آمدید کد فعال سازی شما برابر است با</b>
    <hr/>
    <h2 style="text-align: center">{code}</h2>


            '''
    return html


def send_sms(to, token, token2, token3, template):
    try:
        api = KavenegarAPI(kave_Api)
        params = {
            'receptor': to,
            'template': template,
            'token': token,
            'token2': token2,
            'token3': token3,
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
