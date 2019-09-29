from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.utils.encoding import uri_to_iri
from .models import Product, OrderItem, Order
from django.views.generic.base import ContextMixin
from django.views.decorators.http import require_POST
from .forms import CartAddProductForm, CartUpdateProductForm, OrderCheckoutForm, ContactForm, RegisterForm
from .cart import Cart
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from zeep import Client
from django.http import HttpResponse


class FormMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        ctx = super(FormMixin, self).get_context_data(**kwargs)
        ctx['cart_product_from'] = CartAddProductForm()
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
    return render(request, 'product_detail.html', {'product': product,
                                                   'cart_product_from':CartAddProductForm() })


class Home(TopSelMixin, RecentlyMixin, LatestMixin, FormMixin, ListView):
    model = Product
    template_name = "home.html"


def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCheckoutForm(request.POST)
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
        form = OrderCheckoutForm()
    return render(request, 'checkout.html', {'cart': cart,
                                             'form': form})


MERCHANT = ''
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = 'http://127.0.0.1:8000/callback/'


def to_bank(request, order_id):
    description = "تست جنگو"  # Required
    email = 'miladhzz@gmail.com'  # Optional
    mobile = '09384677005'  # Optional
    order_items = OrderItem.objects.filter(order__random_order_id=order_id)
    amount = 0
    for item in order_items:
        amount += item.price
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100 and len(result.Authority) == 36:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + int(str(result.Status)))


def callback(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], 1000)
        if result.Status == 100:
            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
            order_items = OrderItem.objects.filter(order__random_order_id=1)
            return render(request, 'bank.html', {'order_items': order_items})
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
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
    form = CartUpdateProductForm(request.POST)
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
        item['update_count_from'] = CartUpdateProductForm(initial={'count': item['count'],
                                                                   'update': True})
    return render(request, 'cart.html', {'cart': cart})


class CategoryProductList(ListView):
    model = Product
    template_name = 'category_product_list.html'

    def get_queryset(self):
        queryset = Product.objects.filter()
        return queryset


class ContactMe(CreateView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '.'


class SignUp(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = '../login'


@login_required
def logout_user(request):
    logout(request)
    return render(request, 'registration/logout.html')


