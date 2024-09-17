from django.shortcuts import render,redirect
from .models import *

# Create your views here.
def index(request):
    return render(request, 'seller/index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if SellerRegistration.objects.filter(email=email, password=password).exists():
            return redirect('seller:dashboard')
        else:
            return render(request, 'seller/index.html', {'msg': 'Invalid email or password'})
    return render(request, 'seller/login.html')



def dashboard(request):
    categories = Category.objects.all()  # Fetch all categories
    
    if request.method == 'POST':
        name = request.POST.get('pdt_name')
        price = request.POST.get('pdt_price')
        description = request.POST.get('pdt_description')
        category1 = request.POST.get('pdt_category')
        image = request.FILES.get('pdt_image')
        
        # Get the category object by id
        cat = Category.objects.get(id=category1)
        
        # Save the new product
        Product(name=name, price=price, description=description, category=cat, image=image).save()
        
        return render(request, 'seller/dashboard.html', {'categories': categories, 'msg': 'Product added successfully!'})
    
    # Render the dashboard with the categories context
    return render(request, 'seller/dashboard.html', {'categories': categories})

def view_products(request):
    products = Product.objects.all()
    return render(request, 'seller/view_products.html', {'products': products})

def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('seller:view_products')

def edit_product(request, id):
    product = Product.objects.get(id=id)
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('pdt_name')
        price = request.POST.get('pdt_price')
        description = request.POST.get('pdt_description')
        category1 = request.POST.get('pdt_category')
        image = request.FILES.get('pdt_image')

        # Get the category object by id
        cat = Category.objects.get(id=category1)

        # Update the product
        product.name = name
        product.price = price
        product.description = description
        product.category = cat
        if image:
            product.image = image
        product.save()

        return redirect('seller:view_products')
    return render(request, 'seller/edit_product.html', {'product': product, 'categories': categories})