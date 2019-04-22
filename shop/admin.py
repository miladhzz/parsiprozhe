from django.contrib import admin
from shop import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.ImageGallery)
admin.site.register(models.City)
admin.site.register(models.Province)
admin.site.register(models.Product)
admin.site.register(models.FileGallery)
admin.site.register(models.Order)
admin.site.register(models.PaymentLog)
admin.site.register(models.OrderItem)
admin.site.register(models.Contact)
