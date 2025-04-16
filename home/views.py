from django.shortcuts import render

from product.models import Product


# 1.میخواهیم لیست محصولات را به صفحه home.html ارسال کنیم.
# مهم هست بدانیم چه اطلاعاتی را لازم داریم تا ارسال کنیم؟
# لوگو و آیدی دوره را باید ارسال کنم....
# Create your views here.

def home(request):
    products = Product.objects.filter(status=1)
    result = list(products.values('id', 'logo', 'slug'))

    context = {
        'products': result
    }
    return render(request, 'home.html', context)