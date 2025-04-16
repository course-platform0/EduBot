from django import forms


class UserRegisterForm(forms.Form):
    email = forms.EmailField(label="ایمیل خود را وارد کنید ", widget=forms.TextInput(attrs={'class': 'form-control m-1'}))
    phone = forms.CharField(label="شماره همراه خود را وارد کنید", max_length=15, widget=forms.TextInput(attrs={'class': 'form-control m-1'}))


class UserVerifyForm(forms.Form):
    code = forms.CharField(label="کد ارسال شده را وارد کنید", widget=forms.TextInput(attrs={'class': 'form-control '}))
    password = forms.CharField(label="یک رمز عبور برای خود انتخاب کنید",
                               widget=forms.PasswordInput(attrs={'class': 'form-control '}))
    name = forms.CharField(label='لطفا نام خود را وارد کنید', widget=forms.TextInput(attrs={'class': 'form-control '}))


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="ایمیل یا نام کاربری ", widget=forms.TextInput(attrs={'class': 'form-control m-1'}))
    password = forms.CharField(label="رمز عبور خودرا وارد کنید", widget=forms.PasswordInput(attrs={'class': 'form-control '}))


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control m-1'}))


#این فرم برای فعالسازی رمز جدید درنظر گرفته شده است.
class UserVerifyForgetForm(forms.Form):
    code = forms.CharField(label="کد ارسال شده را وارد کنید", widget=forms.TextInput(attrs={'class': 'form-control '}))
    password = forms.CharField(label="یک رمز عبور برای خود انتخاب کنید",
                               widget=forms.PasswordInput(attrs={'class': 'form-control '}))
    repeat_password = forms.CharField(label="لطفا رمز عبور خود را تکرار کنید.",
                                      widget=forms.PasswordInput(attrs={'class': 'form-control '}))
