from django import forms
from .models import Order, Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

PRODUCT_COUNT_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    count = forms.TypedChoiceField(choices=PRODUCT_COUNT_CHOICES,
                                   coerce=int,
                                   initial=1,
                                   widget=forms.HiddenInput
                                   )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class CartUpdateProductForm(forms.Form):
    count = forms.TypedChoiceField(choices=PRODUCT_COUNT_CHOICES,
                                   coerce=int,
                                   initial=1,
                                   )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class OrderCheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'family', 'email', 'mobile', 'is_accept_agreement')
        labels = { 
            'name': 'نام',
            'family': 'نام خانوادگی',
            'mobile': 'موبایل',
            'email': 'ایمیل',
            'is_accept_agreement': 'با قوانین پارسی پروژه موافقم'
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'mobile', 'email', 'message']
        labels = { 
            'name': 'نام',
            'mobile': 'موبایل',
            'email': 'ایمیل',
            'message': 'متن پیام'
        }


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'رمز عبور'
        self.fields['password2'].label = 'تکرار رمز عبور'
        self.fields['password1'].help_text = ' '
        self.fields['password2'].help_text = ' '

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
        }
        help_texts = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': '',
            'password1': '',
            'password2': '',
        }
        '''error_messages = {
            'password1': {
                'max_length': "This mmmmm writer's name is too long.",
            },
        }'''