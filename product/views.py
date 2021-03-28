from django.shortcuts import render,redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm,EditProductForm
from .models import Product
from django.views import generic

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



    