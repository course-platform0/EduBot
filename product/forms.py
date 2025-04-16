from django import forms


class AddCardByCard(forms.Form):
    token = forms.CharField(label="توکن خود را وارد کنید", widget=forms.TextInput(attrs={'class': 'form-control '}))
    phone = forms.CharField(label="شماره موبایل مورد نظر را وارد کنید",
                               widget=forms.TextInput(attrs={'class': 'form-control '}))
    product_id = forms.IntegerField(label="شماره محصول خود را واردکنید",
                                      widget=forms.TextInput(attrs={'class': 'form-control '}))
