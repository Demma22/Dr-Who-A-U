from django.contrib import admin
from .models import *
# Register your models here.

#Here am creating models to appear on the admin dashboard
admin.site.register(Category)
admin.site.register(Product)
#providing admin with acces to sale
admin.site.register(Sale)