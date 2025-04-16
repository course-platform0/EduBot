import requests
from django.contrib import messages
from django.shortcuts import render, redirect

from product.models import Product, ProductContent, ContentCategory

from user.models import Users, Purchases

from utils.utils import send_sms

from .forms import AddCardByCard


def product(request, slug):
    # my_product = Product.objects.get(slug=slug)
    my_products = ProductContent.objects.filter(product__slug=slug)
    my_product = my_products.first().product
    is_purchased = False
    if my_product.price != 0:
        if request.user.is_authenticated:
            user = Users.objects.get(user_email=request.user.email)
            purchased = Purchases.objects.filter(user=user, product=my_product)
            if purchased.exists():
                is_purchased = True
            else:
                is_purchased = False
        else:
            #todo باید یوزر لاگین نبود حرکت صحیحی انجام شود
            pass
    else:
        is_purchased = True

    content_category = ContentCategory.objects.filter(product=my_product)

    return render(request, 'product.html', {'product': my_product, 'product_content': my_products,
                                            'content_category': content_category, 'is_purchased': is_purchased})


def pay(request, slug):
    # user = Users.objects.get(user_email=request.user.email)
    # phone = user.user_phone
    # name = user.user_name
    # my_product = Product.objects.filter(slug=slug).first()
    # price = my_product.price
    # print(price, "پرداخت شد")
    # print(phone)
    # send_sms(phone, name, '3123123', 'taavoni')
    return redirect('home')


def add_cardbycard(request):
    if request.method == 'POST':
        form = AddCardByCard(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            token = form.cleaned_data.get('token')
            product_id = form.cleaned_data.get('product_id')
            price = 0
            # post method
            data = {
                'phone': phone,
                'price': 1000,
                'secret_key': token,
                'product_id': product_id,
            }

            response = requests.post('https://apiv2.dsrapp.ir/product/add_card_by_card', json=data)
            print(response.status_code)  # وضعیت پاسخ
            if response.status_code == 201:
                messages.success(request, 'Your card has been added.')
            else:
                messages.error(request, 'call to danehkar albate ebteda chek kon ghablan sabt nashode bashe')

    else:
        form = AddCardByCard()

    return render(request, 'add-card-by-card.html', {'form': form})
