from django.shortcuts import render,redirect
from .models import *
from seller.models import *
 

# Create your views here.
def home(request):
    return render(request, 'customer/home.html')

def signup(request):
    if request.method == 'POST':
        name1=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        customer=CustomerRegistration(name=name1,email=email,password=password)
        customer.save()
        return redirect('customer:login')
    return render(request, 'customer/signup.html')


def login(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        name=request.POST.get('name')
        password=request.POST.get('password')
        try:
            cust=CustomerRegistration.objects.get(email=email, password=password, name=name)
            request.session['customer'] = cust.id
            return redirect('customer:view_products')
        except CustomerRegistration.DoesNotExist:
            return render(request, 'customer/login.html', {'error':'Invalid Credentials'})
        # if customer:
        #     return redirect('customer:view_products')
        # else:
        #     return render(request, 'customer/login.html', {'error':'Invalid Credentials'})
    return render(request, 'customer/login.html')

def view_products(request):
    if 'customer' in request.session:
        products = Product.objects.all()
        return render(request, 'customer/view_products.html', {'products': products})
    else:
        return render(request,'customer/home.html')
# def cart(request):
#     cart_items = Cart.objects.all()
#     total_price = sum(item.product.price * item.quantity for item in cart_items)
#     total_price_per_item=[]
#     grand_total=0
#     for item in cart_items:
#         item_total=item.product.price * item.quantity
#         total_price_per_item.append({'item':item,'total':item_total})
#         grand_total+=item_total
#     return render(request, 'customer/cart.html',{'cart_items':cart_items,'grand_total':grand_total,'total_price':total_price})
def cart(request):
    if 'customer' in request.session:
    # Get all items in the cart
        cart_items = Cart.objects.all()
    
    # Calculate the total price and total quantity
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        total_quantity = sum(item.quantity for item in cart_items)
    
    # Prepare a list to store the total price per item
        total_price_per_item = []
        grand_total = 0
    
    # Loop through the cart items and calculate totals
        for item in cart_items:
            item_total = item.product.price * item.quantity
            total_price_per_item.append({'item': item, 'total': item_total})
            grand_total += item_total
    
    # Render the cart template with the cart items, totals, and total quantity
        return render(request, 'customer/cart.html', {
            'cart_items': cart_items,
            'grand_total': grand_total,
            'total_price': total_price,
            'total_price_per_item': total_price_per_item,
            'total_quantity': total_quantity  
        })
    else:
        return render(request, 'customer/home.html')
    


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item,created = Cart.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()
    cart_item.save()
    return redirect('customer:cart')


def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item = Cart.objects.get(product=product)
    cart_item.delete()
    return redirect('customer:cart')

def logout(request):
    if 'customer' in request.session:
        del request.session['customer']
        return redirect('customer:home')
    else:
      return render(request, 'customer/logout.html')
    

def search(request):
    products = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(name__icontains=keyword)
    
    return render(request, 'customer/view_products.html', {'products': products})
