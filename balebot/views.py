import json
import random
import re

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import requests

from balebot.balebot import *
from balebot.models import UserVisit
from product.models import Product, ProductContent, ContentCategory
from user.models import Register, Users
from utils.utils import send_sms


# Create your views here.
@csrf_exempt
def get_updates(request):
    if request.method == 'POST':
        main_data = json.loads(request.body)

        # اگر داده دریافتی از نوع callback_query باشد
        # یعنی کاربر روی دکمه‌ای شیشه‌ای کلیک کرده است
        if "callback_query" in main_data:
           

            chat_id = main_data["callback_query"]['message']['chat']['id']
            message_id = main_data["callback_query"]['message']['message_id']
            data = main_data["callback_query"].get('data', "")

            isLogin = is_login(chat_id)
            if "visit" in data:
                user_visit(chat_id, data[5:])
            elif data == "python_bootcamp":
                get_python_bootcamp(chat_id, message_id)
            elif "python_term" in data:
                get_term(chat_id, data[11:])
            elif "python_day" in data :
                get_day(chat_id, data[10:])    
            elif "back_main" == data:
                get_start_action(chat_id, isLogin)    
        else:

            # پردازش پیام دریافتی
            chat_id = main_data['message']['chat']['id']
            text = main_data['message'].get('text', '')
            name = main_data['message']['from'].get('firs_name', '')
            contact = ''
            user_id = ''
            try:
                contact = main_data['message']['contact'].get('phone_number', '')
                user_id = main_data['message']['contact'].get('user_id', '')
            except KeyError as e:
                pass

            isLogin = is_login(chat_id)

            if text == '/start':
                get_start_action(chat_id, isLogin)
            #تست شود بعدا...       todo
            #عملیات لاگین با ارسال شماره توسط بله
            elif contact != '' and user_id != '':
                phone = "0" + contact[2:]
                register_with_bale(user_id, phone, name)
            #ورود با شماره دیگر اینجا ارسال پیام داریم.
            #todo سعی کنیم مانع ارسال پیامکهای بیجا شویم.
            #ایده میتوانیم لاگ بگیریم یک chatid بیش از حد از ما پیامک نگیرد
            elif text == "ورود با شماره دیگر" or text == "ثبت نام با شماره دیگر" or text == "لاگین" or text == "ورود":
                send_message(chat_id, "لطفا شماره موبایل مد نظر خود را وارد کنید")
            # باید متوجه شوم شماره تماس ارسال شده
            elif is_valid_iranian_mobile(text):
                verify_phone(text, chat_id)
            #آیا یک کد فعال ۵ رقمی برای ما آمده یا خیر
            elif has_exactly_five_digits(text):
                register(chat_id, text, name)
            elif text == "بوتکمپ پایتون":
                if isLogin:
                    get_python_bootcamp(chat_id)
                else:
                    send_message(chat_id, "شما لاگین نیستید لطفا شماره خود را ارسال کنید.")
            elif "ترم" in text:
                get_term(chat_id, text)
            elif "تمرین جلسات ۱ تا ۵" in text:
                send_message(chat_id, "این تمرین را با دقت ببینید....\n\n   "
                                      "https://my.uupload.ir/p/5L5M2Oy8")
            elif "روز" in text:
                get_day(chat_id, text)
            elif "بازگشت" in text:
                if text == MAIN_BACK:
                    get_start_action(chat_id, isLogin)
                elif text == BACK_TO_PYTHON:
                    get_python_bootcamp(chat_id)
            else:

                send_message(chat_id, "عبارت شما برای ربات ناخواناست")
    return HttpResponse('Hello from bale bot!')


def register(chat_id, text, name):
    is_valid_code = Register.objects.filter(user_email=chat_id, code=text)
    if is_valid_code.exists():
        phone = is_valid_code.first().user_phone
        is_valid_code.delete()
        user = Users.objects.filter(user_phone=phone)
        if user.exists():
            user = user.first()
            user.chat_id = chat_id
            user.name = name
            user.save()
        else:
            Users.objects.create(chat_id=chat_id, name=name, user_phone=phone)
        get_start_action(chat_id, is_login(chat_id))

    else:
        send_message(chat_id, "کد وارد شده صحیح نیست. فرصت باقی‌مانده -1")


def register_with_bale(chat_id, phone, name):
    user = Users.objects.filter(user_phone=phone)
    if user.exists():
        user = user.first()
        user.chat_id = chat_id
        user.name = name
        user.save()
    else:
        Users.objects.create(chat_id=chat_id, name=name, user_phone=phone)
    get_start_action(chat_id, is_login(chat_id))


def verify_phone(phone, chat_id):
    #todo اعتبار سنجی شماره موبایل وارد شده

    random_code = random.randint(10000, 99999)
    reg = Register(user_phone=phone, user_email=chat_id, code=random_code)
    reg.save()
    #todo async
    send_message(chat_id, "پیامک کد فعالسازی ارسال شد لطفا فقط کد را وارد کنید.")
    send_sms(phone, random_code, '', '', 'mgh21-verify')


# ------------------------توابع مخصوص ربات -----------------------
#متد ارسال پیام به ربات با چت آیدی
def send_message(chat_id, text, keyboard=None):
    send_message_url = f"https://tapi.bale.ai/bot{BALE_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': keyboard
    }
    requests.post(send_message_url, json=payload)

    return JsonResponse({'status': 'ok'})


def send_photo(chat_id, caption, img_url, keyboard=None):
    send_photo_url = f"https://tapi.bale.ai/bot{BALE_BOT_TOKEN}/sendPhoto"
    payload = {
        'chat_id': chat_id,
        'caption': caption,
        'photo': img_url,
        'reply_markup': keyboard
    }
    requests.post(send_photo_url, json=payload)

    return JsonResponse({'status': 'ok'})


def set_keyboard_markup(keyboard):
    return {'keyboard': keyboard}


def set_keyboard_inline(keyboard):
    keyboard.append([{"text": "بازگشت به منوی اصلی", "callback_data": "back_main"}])
    return {'inline_keyboard': keyboard}


def edit_message(chat_id, message_id, text, keyboard=None):
    edit_message_url = f"https://tapi.bale.ai/bot{BALE_BOT_TOKEN}/editMessageText"
    payload = {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'reply_markup': keyboard
    }
    requests.post(edit_message_url, json=payload)

    return JsonResponse({'status': 'ok'})

# ------------------------توابع مخصوص ربات -----------------------


def get_start_action(chat_id, isLogin):
    if isLogin:
        #todo balebot.py change 
        BALE_MAIN_KEYBOARD_LOGINq = [

                    [{"text": "بوتکمپ پایتون", "callback_data":"python_bootcamp"}, {"text": "بوتکمپ کسب وکار", "callback_data":"business"}],
                    [{"text": "بوتکمپ فضای مجازی", "callback_data":"onlinework"}],
                    [{"text": "تمرین جلسات ۱ تا ۵", "callback_data":"tamrin1-5"}],
                ]
        keyboard = set_keyboard_inline(BALE_MAIN_KEYBOARD_LOGINq)
        send_message(chat_id, TEXT_WELCOME, keyboard)

    else:
         #todo balebot.py change 

        keyboard = [
            [{"text": "ثبت نام یا ورود  با همین شماره بله", "request_contact": True, "callback_data": "login-with-bale"}],
            [{"text": "ثبت نام با شماره دیگر", "callback_data": "login"}, {"text": "ورود با شماره دیگر", "callback_data": "login"}],
        ]
        keyboard = set_keyboard_inline(keyboard)
        send_message(chat_id, TEXT_REGISTER, keyboard)


#آیا یک شماره موبایل صحیح ایرانی به من داده شده یا خیر
def is_valid_iranian_mobile(phone):
    pattern = r"^(?:(?:0|\\+?98)?(?:\\s)?(9(?:[0-9]{9})))$"
    return bool(re.fullmatch(pattern, phone))


#آیا کد فعالسازی برای من ارسال شده یا خیر
def has_exactly_five_digits(text):
    pattern = r'^\d{5}$'
    return bool(re.fullmatch(pattern, text))


#آیا کاربر در سرور من وجود دارد یا خیر
def is_login(chat_id):
    user = Users.objects.filter(chat_id=chat_id)
    if user.exists():
        return True
    return False


# توابع مربوط به اپلیکیشن آکادمی دانه کار
def get_python_bootcamp(chat_id, message_id=None):
    products = Product.objects.all()
    keyboard = []
    row = []
    for i, product in enumerate(products):
        my_dict = {'text': product.name, "callback_data": "python_term"+product.slug}
        row.append(my_dict)
        if len(row) == 2:
            keyboard.append(row)
            row = []
        #برای چک کردن فرد بودن تعداد اعضا آخری را تکی اضافه میکنیم
        elif i == len(products) - 1:
            keyboard.append(row)
            row = []
    keyboard = set_keyboard_inline(keyboard)
    if message_id is not None:
        edit_message(chat_id, message_id, "یکی از ترمهای بوتکمپ را انتخاب کنید.", keyboard)
    else:
        send_message(chat_id, "یکی از ترمهای بوتکمپ را انتخاب کنید.", keyboard)

def get_term(chat_id, text):
    product = Product.objects.filter(slug=text)
    if product.exists():
        product_contents = ContentCategory.objects.filter(product=product[0])
        keyboard = []
        row = []
        for i, content in enumerate(product_contents):
            my_dict = {'text': content.name, "callback_data": "python_day"+ str(content.id)}
            row.append(my_dict)
            if len(row) == 2:
                keyboard.append(row)
                row = []
            # برای چک کردن فرد بودن تعداد اعضا آخری را تکی اضافه میکنیم
            elif i == len(product_contents) - 1:
                keyboard.append(row)
                row = []
        

        keyboard = set_keyboard_inline(keyboard)
        send_photo(chat_id, "یکی از روزهای بوتکمپ را انتخاب کنید.", content.product.logo , keyboard)


def get_day(chat_id, text):
    content_category = ContentCategory.objects.filter(id=text)

    if content_category.exists():

        product_contents = ProductContent.objects.filter(content_category=content_category[0])
        content_category_id = ""
        link = "با سلام لینک ویدئوهای شما 👇: " + "\n\n"
        for product_link in product_contents:
            content_category_id = product_link.content_category_id
            link += (product_link.video_link + "\n\n ")
        keyboard = [
            [{"text": "مشاهده کردم", "callback_data": "visit " + str(content_category_id)}],
        ]
        keyboard = set_keyboard_inline(keyboard)
        send_message(chat_id, link, keyboard)


def user_visit(chat_id, data):
    content_category = ContentCategory.objects.filter(id=data)
    if content_category.exists():

        content_category = content_category[0]
    user = Users.objects.filter(chat_id=chat_id)
    if user.exists():
        user = user.first()

    UserVisit.objects.create(user=user, product=content_category.product,
                             content_category=content_category)

    send_message(chat_id, "شما با موفقیت این روز را سپری کردید ثبت شد.")