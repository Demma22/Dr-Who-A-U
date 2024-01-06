#a form is an interface where a user creates data
from django.forms import ModelForm

#accessing our models such that we link them to the form
from .models import *

class AddForm(ModelForm):
    class Meta:
        model = Product
        fields =['received_quantity']

#we are modeling a form basing on our model for us to record a given product sale
class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['quantity', 'ammount_received', 'issued_to']