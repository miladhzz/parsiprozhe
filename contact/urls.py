from django.urls import path
from . import views


urlpatterns = [
    path('contact/', views.ContactMe.as_view(), name='contact'),
]
