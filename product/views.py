from django.shortcuts import render,redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm
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
    return render(request,'product/edit_product.html')


@login_required
def view_product(request):

    context = {'product_list':Product.objects.all()}
    return render(request, 'product/view_product.html', context)

# class ViewProduct(generic.DetailView):
#     template_name = "product/view_product.html"
#     model = Product
#     context_object_name = "product_list"

#     def get_queryset(self):
#         return Product.objects.all()

    