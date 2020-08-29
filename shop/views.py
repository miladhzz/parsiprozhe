from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.utils.encoding import uri_to_iri
from .models import Product, OrderItem, Order
from django.views.generic.base import ContextMixin
from django.views.decorators.http import require_POST
from . import forms
from .cart import Cart
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from zeep import Client
from django.http import HttpResponse
from parsiprozhe.settings import MERCHANT
from logger import statistic


class FormMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        ctx = super(FormMixin, self).get_context_data(**kwargs)
        ctx['cart_product_from'] = forms.CartAddProductForm()
        return ctx


class TopSelMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        ctx = super(TopSelMixin, self).get_context_data(**kwargs)
        ctx['top_sel'] = Product.objects.all()[9:12]
        return ctx


class RecentlyMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        ctx = super(RecentlyMixin, self).get_context_data(**kwargs)
        ctx['recently_view'] = Product.objects.all()[3:9]
        return ctx


class LatestMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        ctx = super(LatestMixin, self).get_context_data(**kwargs)
        ctx['latest_product'] = Product.objects.all()[3:9]
        return ctx


class ProductList(FormMixin, ListView):
    model = Product
    template_name = 'product_list.html'
    paginate_by = 12
    queryset = Product.objects.all()


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=uri_to_iri(slug))
    comments = product.comment_set.filter(is_active=True)

    new_comment = None
    if request.method == 'POST':
        comment_form = forms.CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()
    else:
        comment_form = forms.CommentForm()

    statistic.log(request)
    return render(request, 'product_detail.html', {'product': product,
                                                   'cart_product_from': forms.CartAddProductForm(),
                                                   'comments': comments,
                                                   'comment_form': comment_form,
                                                   'new_comment': new_comment })


class Home(TopSelMixin, RecentlyMixin, LatestMixin, FormMixin, ListView):
    model = Product
    template_name = "home.html"


def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = forms.OrderCheckoutForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         count=item['count'])
            # Clear the cart
            cart.clear()
            return redirect('to_bank', order_id=order.random_order_id)

    else:
        form = forms.OrderCheckoutForm()
    return render(request, 'checkout.html', {'cart': cart,
                                             'form': form})


client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = 'http://parsiprozhe.ir/callback/'


def to_bank(request, order_id):
    order = get_object_or_404(Order, random_order_id=order_id)
    description = "خرید فایل از پارسی پروژه"  # Required
    email = order.email
    mobile = order.mobile
    order_items = OrderItem.objects.filter(order=order)
    amount = 0
    for item in order_items:
        amount += item.price
    if amount == 0:
        return render(request, 'bank.html', {'order_items': order_items})
    order.amount = amount
    order.save()
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100 and len(result.Authority) == 36:
        order.authority = int(result.Authority)
        order.save()
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(int(result.Authority)))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


def callback(request):
    statistic.log(request)
    if request.GET.get('Status') == 'OK':
        authority = int(request.GET['Authority'])
        order = get_object_or_404(Order, authority=authority)
        result = client.service.PaymentVerification(MERCHANT, authority, order.amount)
        if result.Status == 100:
            order_items = OrderItem.objects.filter(order=order)
            order.order_status = 1  # Complete
            order.refId = result.RefID
            order.save()
            return render(request, 'callback.html', {'order_items': order_items,
                                                     'refId': order.refId})
        elif result.Status == 101:
            order_items = OrderItem.objects.filter(order=order)
            return render(request, 'callback.html', {'order_items': order_items,
                                                     'refId': order.refId})
        else:
            return HttpResponse('تراکنش ناموفق.\nStatus: ' + str(result.Status) +
                                '<a href="http://parsiprozhe.ir">بازگشت</a>')
    else:
        return HttpResponse('پرداخت توسط کاربر لغو شد' + '<a href="http://parsiprozhe.ir">بازگشت</a>')


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = forms.CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 count=cd['count'],
                 update_count=cd['update'])
    return redirect('cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = forms.CartUpdateProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 count=cd['count'],
                 update_count=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_count_from'] = forms.CartUpdateProductForm(initial={'count': item['count'],
                                                                   'update': True})
    return render(request, 'cart.html', {'cart': cart})


class CategoryProductList(ListView):
    model = Product
    template_name = 'category_product_list.html'

    def get_queryset(self):
        queryset = Product.objects.filter()
        return queryset


class SignUp(CreateView):
    template_name = 'registration/register.html'
    form_class = forms.RegisterForm
    success_url = '../login'


@login_required
def logout_user(request):
    logout(request)
    return render(request, 'registration/logout.html')
