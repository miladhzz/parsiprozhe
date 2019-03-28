from django import forms
from .models import Order, Contact

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


