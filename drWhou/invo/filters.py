import django_filters
from .models import Category, Product

#creating a class to filter from our models 

class Product_filter(django_filters.FilterSet):
#class meta is used to alter manipulate) contents of another class
    class Meta:
        model = Product
        fields = ['item_name']

class Category_filter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ['name']