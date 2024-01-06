from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Product,Sale
from .filters import Product_filter
from .forms import AddForm, SaleForm

#here we include the models so that the views can use these models incase of posting 


##Handling redirection after deletion
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

'''It takes a request object as its parameter, which represents the incoming HTTP 
request from the client. The request object contains information such as the HTTP 
method, URL, headers, and any data submitted in the request.'''
def index(request):
    products = Product.objects.all().order_by('-id')
    product_filters = Product_filter(request.GET,queryset = products)
    products = product_filters.qs
    return render(request, 'products/index.html',{'products':products,'product_filters':product_filters})

'''render() function is used to render an HTML template with data and generate an HTTP 
response. The request parameter is the incoming HTTP request object, and the second 
parameter 'products/aboutDrWhoU.html' specifies the template to be rendered.'''
@login_required
def home(request):
    return render(request, 'products/aboutDrWhoU.html')

#Crete aview for product_detail
@login_required
def product_detail(request, product_id):
    product = Product.objects.get(id = product_id)
    return  render(request, 'products/product_detail.html', {'product':product})

@login_required
def issue_item(request,pk):
    issued_item = Product.objects.get(id = pk)
    sales_form = SaleForm(request.POST)

    if request.method == 'POST':
        #checks if the input is as its supposed to be
        if sales_form.is_valid():
            new_sale = sales_form.save(commit = False)
            new_sale.item = issued_item
            new_sale.unit_price = issued_item.unit_price
            new_sale.save()
            #to keep track of the remaining stock after sales
            issued_quantity = int(request.POST['quantity'])
            issued_item.total_quantity -= issued_quantity
            issued_item.save
            print(issued_item.item_name)
            print(request.POST['quantity'])
            print(issued_item.total_quantity)

            return redirect('receipt')
        
    return render(request, 'products/issue_item.html', {'sales_form': sales_form})   

#this handles receipt issuing
@login_required
def receipt(request):
    sales = Sale.objects.all().order_by('-id')
    return render(request,'products/receipt.html', {'sales':sales})

#a view to handle items added to tock 
@login_required
def add_to_stock(request, pk):
    '''pk is a variable that holds the primary key value of the record to be retrieved.
      The get() method is used to retrieve a single record based on a filter condition, 
      in this case, id=pk'''
    issue_item = Product.objects.get(id = pk)
    form = AddForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            added_quantity = int(request.POST['received_quantity'])
            issue_item.total_quantity += added_quantity
            issue_item.save()
        #to add to the remaining stock bcz quantity is reducing
            print(added_quantity)
            print(issue_item.total_quantity)
            return redirect('home')
    return render(request, 'products/add_to_stock.html',{'form':form})    

#a view to display allsales 
@login_required
def all_sales(request):
    '''line below retrieves all the objects (i.e., records or rows) from the Sale model in the database.'''
    sales = Sale.objects.all()
    #add all ammount received for items and adds all chane given out
    total = sum([items.ammount_received for items in sales])
    change = sum([items.get_change() for items in sales])
    #gets net from total-change
    net = total - change
    return render(request, 'products/all_sales.html',{
        'sales':sales,
        'total':total,
        'net':net,
        'change':change
    })

#a view to render receipt detail page
@login_required
def receipt_detail(request,receipt_id):
    receipt = Sale.objects.get(id = receipt_id)
    return render(request, 'products/receipt_detail.html', {'receipt':receipt})

#a view to delete a product and its objects
@login_required
def delete_detail(request, product_id):
    delete = Product.objects.get(id = product_id)
    delete.delete()
    return HttpResponseRedirect(reverse('index'))