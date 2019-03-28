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


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'mobile', 'email', 'message']


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

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
