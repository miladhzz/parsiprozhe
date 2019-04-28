from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from shop import views
'''
from django.conf.urls import url, include
if settings.DEBUG:
    import debug_toolbar
'''


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('shop/', views.ProductList.as_view(), name='product'),
    path('shop/<str:slug>/', views.product_detail, name='product-detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>', views.cart_add, name='cart_add'),
    path('cart/update/<int:product_id>', views.cart_update, name='cart_update'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('to_bank/<int:order_id>', views.to_bank, name='to_bank'),
    path('category/<slug>', views.CategoryProductList.as_view(), name='category'),
    path('contact/', views.ContactMe.as_view(), name='contact'),
    path('registration/register/', views.SignUp.as_view(), name='register'),
    path('registration/login/', auth_views.LoginView.as_view(), name="login"),
    path('registration/logout/', views.logout_user, name="logout"),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
urlpatterns += [
    url(r'^__debug__/', include(debug_toolbar.urls)),
]
'''