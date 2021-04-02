from django.shortcuts import render,redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm,EditProductForm,TransactionForm
from .models import Product,Transaction
from django.views import generic
from django.contrib.auth.models import User
from .checks import *
from django.http import HttpResponse
from .utils import render_to_pdf
import datetime



@user_passes_test(lambda u: u.is_superuser)
def home(request):
    return render(request,'product/home.html')

@user_passes_test(lambda u: u.is_superuser)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        # {'name':"rice", 'price':150}
        if form.is_valid():
            form.save()
            messages.success(request, f'Product added!')
            return redirect('product-home')

    else:
        form = ProductForm()
    return render(request,'product/add_product.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def edit_product(request):

    context = {'product_list': Product.objects.all()}
    return render(request,'product/edit_product.html',context)


@user_passes_test(lambda u: u.is_superuser)
def edit_util(request,p_id):
    if request.method == 'POST':
        form = EditProductForm(request.POST)
        product = Product.objects.get(pk = p_id)
        if form.is_valid():
            product.quantity = form.cleaned_data['quantity']
            product.selling_price = form.cleaned_data['selling_price']
            product.cost_price = form.cleaned_data['cost_price']
            
            if product.selling_price<product.cost_price:
                context = {'form':form,'product':product,'my_error_message':"Selling Price cannot be less than Cost Price!"}
                return render(request,'product/edit_util.html',context)

            product.save()
            messages.success(request, f'{product.name} has been edited!')
            return redirect('product-edit')
            
        else:
            context = {'form':form,'product':product}
            return render(request,'product/edit_util.html',context)


    product = Product.objects.get(pk=p_id)
    form = EditProductForm(initial={'cost_price':product.cost_price,'quantity':product.quantity,'selling_price':product.selling_price})
    context = {'form':form,'product':product}
    return render(request,'product/edit_util.html',context)

@login_required
def view_product(request):
    form = ProductForm()
    context = {'product_list':Product.objects.all(),'form':form}
    return render(request, 'product/view_product.html', context)

@login_required
def new_transaction(request):

    if request.method == 'POST':
    
        form = TransactionForm(request.POST)

        if form.is_valid():
            
            p_name = form.cleaned_data['Product_name']
            p_id = form.cleaned_data['product_id']

            if p_id==None and len(p_name)==0 :
                product_list = []
                for key in request.session['my_dict'].keys():
                    p = Product.objects.get(name=key)
                    product_list.append(p)
                context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'Enter a valid ID and / or Product Name'}
                return render(request,'product/transaction.html',context)
            
            if p_id!=None and len(p_name) == 0 :
                temp = Product.objects.filter(pk=p_id)

                if  len(temp)==0 :
                    product_list = []
                    for key in request.session['my_dict'].keys():
                        p = Product.objects.get(name=key)
                        product_list.append(p)

                    context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'Please enter a valid ID!'}
                    return render(request,'product/transaction.html',context)
                
                p_name = Product.objects.get(pk=p_id).name 
            
            elif p_id==None and len(p_name)!=0 :
                pass
            
            elif p_id!=None and len(p_name)!=0 :
                temp = Product.objects.filter(pk=p_id)
                if  len(temp)==0 :
                    product_list = []
                    for key in request.session['my_dict'].keys():
                        p = Product.objects.get(name=key)
                        product_list.append(p)
                    context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'Please enter a valid ID!'}
                    return render(request,'product/transaction.html',context)

                if p_name != Product.objects.get(pk=p_id).name :
                    product_list = []
                    for key in request.session['my_dict'].keys():
                        p = Product.objects.get(name=key)
                        product_list.append(p)

                    context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'Name: {p_name} and ID: {p_id} are mismatched!'}
                    return render(request,'product/transaction.html',context)
                  

            # product_exist check...
            if not product_exist(p_name):
                product_list = []
                for key in request.session['my_dict'].keys():
                    p = Product.objects.get(name=key)
                    product_list.append(p)

                context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'{p_name} is not available!'}
                return render(request,'product/transaction.html',context)

            p = Product.objects.filter(name__exact = p_name)[0]
            
            if 'my_dict' not in request.session:
                request.session['my_dict'] = {}

            
            # check if current product is not in 'my_dict'
            if p_name not in request.session['my_dict'].keys():

                if form.cleaned_data['quantity'] > p.quantity:
                
                    product_list = []
                    for key in request.session['my_dict'].keys():
                        temp = Product.objects.get(name=key)
                        product_list.append(temp)

                    context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'Only {p.quantity} item(s) left in stock'}
                    return render(request,'product/transaction.html',context)
                
                else:
                    request.session['my_dict'][p_name] = 0 
                
                
                
            # checks if entered quantity exceeds the stock limit...
            if quantity_check(p.id, form.cleaned_data['quantity'] + request.session['my_dict'][p_name]):            

                if 'my_dict' not in request.session:
                    request.session['my_dict'] = {}

                if p_name in request.session['my_dict'].keys():
                    request.session['my_dict'][p_name] += form.cleaned_data['quantity'] 
                    
                else:
                    request.session['my_dict'][p_name] = form.cleaned_data['quantity']

                return redirect('product-transaction')
                
            else:

                if 'my_dict' not in request.session:
                    request.session['my_dict'] = {}
                
                product_list = []
                for key in request.session['my_dict'].keys():
                    p = Product.objects.get(name=key)
                    product_list.append(p)

                context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'Only {p.quantity} item(s) left in stock'}
                return render(request,'product/transaction.html',context)
    
    form = TransactionForm()
    # t = Transaction.objects.filter(user=request.user).order_by('-created_at')[0]
    if 'my_dict' not in request.session:
        request.session['my_dict'] = {}

    product_list = []
    for key in request.session['my_dict'].keys():
        p = Product.objects.get(name=key)
        product_list.append(p)

    context = {'form':form, 'product_dict':request.session['my_dict'], 'product_list':product_list}
    return render(request, 'product/transaction.html', context)

# def generate_pdf(request):
# Before rendering out the pdf, make sure to decrease the size of the inventory...

def generate_pdf(request):

    transaction_dict = request.session['my_dict']

    total_amount = 0

    product_list = []

    for key,val in transaction_dict.items():
        p = Product.objects.get(name__exact=key)
        p.quantity -= val
        p.save()
        total_amount += p.selling_price*val
        product_list.append(p)

    t = Transaction.objects.create(user=request.user, data=transaction_dict, amount = total_amount)
    
    del request.session['my_dict']


    data = {
             'product_list': product_list,
             'amount': total_amount,
             'today': datetime.date.today(), 
             'product_dict': transaction_dict,
             'order_id': t.id,
        }
    pdf = render_to_pdf('product/invoice.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def complete_transaction(request):
    return render(request, 'product/complete_transaction.html')


def clear(request):
    del request.session['my_dict']
    return redirect('product-transaction')