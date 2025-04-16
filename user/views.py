import random

from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserVerifyForm, UserLoginForm, ForgetPasswordForm, UserVerifyForgetForm
from .models import Register, Users, Purchases
# خودکار ایمپورت نمیکند...
# باگ موجود در پای چار برای فراخوانی توابع کمی دردسر درست کرد...
from utils.utils import send_email, html_body, send_sms
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.

#این تابع برای ثبت نام استفاده می‌شود.
def register(request):
    #------- وقتیست که فرم توسط کاربر پر می‌شود--------------
    if request.method == 'POST':
        # فرم زیر با فرم صفر فرق دارد چون در request.post موجود است
        form = UserRegisterForm(request.POST)
        # is_valid متد خود جنگو است که فرم را بررسی میکند
        if form.is_valid():
            #اطلاعات ما در cleaned_data به اینجا ارسال شده است
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            random_code = random.randint(10000, 99999)
            #تو این مرحله ایمیل کاربر و تلفن و کد را وارد دیتابیس موقت کنیم...
            reg = Register(user_phone=phone, user_email=email, code=random_code)
            reg.save()
            # ساخت یک نوشته برای ارسال کد به کاربر از طریق ایمیل
            html = html_body(random_code)
            send_email(email, "کد فعالسازی بوتکمپ دانه کار", html)
            return redirect(f"../verify?email={email}&phone={phone}")
        else:
            messages.error(request, "ایرادی در فرم شما وجود دارد.")
    # وقتی صفحه اولین بار لود میشود متد get صدا زده می‌شود پس فقط کافیست یک فرم صفر کیلومتر ساخته شود و تحویل قالب
    # داده شود
    elif request.method == 'GET':
        if request.user.is_authenticated:
            messages.error(request, "شما لاگین هستید")
            return redirect("home")
        form = UserRegisterForm()

    return render(request, 'register.html', {"form": form})


def verify(request):
    if request.method == 'POST':
        verify_form = UserVerifyForm(request.POST)
        if verify_form.is_valid():
            code = verify_form.cleaned_data.get('code')
            name = verify_form.cleaned_data.get('name')
            password = verify_form.cleaned_data.get('password')
            email = request.GET.get('email')
            phone = request.GET.get('phone')
            print(email)
            is_valid_code = Register.objects.filter(code=code, user_email=email).exists()
            if is_valid_code:
                user = Users(user_name=name, user_email=email, user_phone=phone)
                user.save()
                #یوزر بالا یوزر دستی ماست و یوزر پایین یوزر استاندارد جنگوست...
                #یوزرنیم را ایمیل قراردادیم
                user = User.objects.create_user(email, email, password)
                user.first_name = name
                user.save()
                user = authenticate(request, username=email, password=password)
                login(request, user)
                Register.objects.filter(user_email=email).delete()
            else:
                messages.warning(request, "کد وارد شده صحیح نیست...")
                verify_form = UserVerifyForm()
        else:
            messages.warning(request, "اطلاعات نادرست است لطفا مجدد تلاش کنید")
            verify_form = UserVerifyForm()

    elif request.method == 'GET':
        if request.GET.get("is_sms") == "1":
            verify_form = UserVerifyForm()
            messages.info(request, f"وارد کنید {request.GET.get('phone')}کد ارسال شده به موبایل : ")
            phone = request.GET.get('phone')
            try:
                random_code = (Register.objects.filter(user_phone=phone)
                               .order_by('-date_register').first().code)
                print(random_code)
                send_sms(phone, random_code, '', '', 'mgh21-verify')
            except Register.DoesNotExist:
                messages.error(request, "خطا در بازیابی اطلاعات لطفا از ابتدا لاگین کنید")
                send_sms("09128882737", phone, '', '', 'mgh21-verify')
        elif request.GET.get("phone") is not None:
            messages.info(request, f"وارد کنید {request.GET.get('email')}کد ارسال شده به ایمیل : ")
            verify_form = UserVerifyForm()
        else:
            messages.error(request, "مسیر غلط")
            return redirect("register")

    #این url را زمانیکه کاربر بخواهد sms ارسال کند صدا میزند
    my_url = f"../verify?email={request.GET.get('email')}&phone={request.GET.get('phone')}"
    return render(request, 'verify.html', {"form": verify_form, "my_url": my_url})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "شما با موفقیت وارد شدید")
                #todo ma bayad bebinim karbar koja booode bargardim anja
                return redirect('home')
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
                form = UserLoginForm()
    else:
        if request.user.is_authenticated:
            messages.error(request, "شما لاگین هستید")
            return redirect("home")
        form = UserLoginForm()
    return render(request, 'login.html', {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "شما با موفقیت از سایت خارج شدید")
    return redirect("home")


def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            code = random.randint(10000, 99999)
            reg = Register.objects.create(user_email=email, code=code)
            reg.save()
            html = html_body(code)
            send_email(email, "ارسال کد فراموشی", html)
            messages.success(request, "کد فعالسازی مجدد حساب برای شما ارسال شد.")
            return redirect(f"../verifyforgetpassword?email={email}")
    else:
        form = ForgetPasswordForm()
    return render(request, 'forget-pass.html', {"form": form})


def verify_forget_password(request):
    if request.method == 'POST':
        form = UserVerifyForgetForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            password = form.cleaned_data.get('password')
            repeat_password = form.cleaned_data.get('repeat_password')
            if password == repeat_password:
                reg = Register.objects.filter(code=code, user_email=request.GET.get('email'))
                if reg.exists():
                    user = User.objects.get(email=request.GET.get('email'))
                    user.set_password(password)
                    user.save()
                    reg.delete()
                    messages.success(request, "رمز عبور شما به روز شد لطفا وارد شوید.")
                    return redirect("login")
                else:
                    messages.error(request, "کد وارد شده صحیح نیست.")
            else:
                messages.error(request, "رمز عبور یکسان نیست....")

    else:
        form = UserVerifyForgetForm()

    return render(request, 'verify-forget-form.html', {"form": form})


def profile(request):
    email = request.user.email
    #لیست خریدهای کاربر با ایمیل بالا را دریافت می‌کنیم
    user = Users.objects.get(user_email=email)
    purchases = Purchases.objects.filter(user=user)
    #todo kharidhaye bishtar va mahsooolate bishtar az tarighe admin panel sabt shavad
    products = purchases.product
    return render(request, 'profile.html', {"products": products})


def testsms(request):
    email = request.user.email
    user = Users.objects.filter(user_email=email).first()
    phone = user.user_phone
    name = user.user_name
    send_sms(phone, name, '123', 'mgh21', 'update-app')
    return redirect("home")
