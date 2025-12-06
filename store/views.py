from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import logout
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile

# ----------------- USER VIEWS -----------------
def index(request):
    recently_viewed = request.session.get('recently_viewed', [])
    latest_products = Product.objects.order_by('-id')[:5]
    return render(request, 'index.html', {'recently_viewed': recently_viewed, 'latest_products': latest_products})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('store:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('store:register')

        user = User.objects.create(username=username, email=email, password=make_password(password))
        UserProfile.objects.create(user=user)
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('store:login')
    return render(request, 'register.html')

@login_required(login_url='store:login')
def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'orders': orders})

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    recently_viewed = request.session.get('recently_viewed', [])
    if product_id not in recently_viewed:
        recently_viewed.append(product_id)
        if len(recently_viewed) > 5:
            recently_viewed = recently_viewed[-5:]
        request.session['recently_viewed'] = recently_viewed
    return render(request, 'product_detail.html', {'product': product})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('store:login')

# ----------------- CART -----------------
@login_required(login_url='store:login')
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    total = sum(item.subtotal() for item in items)
    return render(request, 'cart.html', {'cart': cart, 'items': items, 'total': total})

@login_required(login_url='store:login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity <= 0:
        messages.error(request, "Invalid quantity.")
        return redirect('store:products')
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect('store:view_cart')

@login_required(login_url='store:login')
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            cart_item.delete()
            messages.info(request, "Item removed from cart.")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated.")
    return redirect('store:view_cart')

@login_required(login_url='store:login')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('store:view_cart')

# ----------------- ADMIN PRODUCT CRUD -----------------
@user_passes_test(lambda u: u.is_staff)
def admin_product_list(request):
    products = Product.objects.all()
    return render(request, 'admin_products.html', {'products': products})

@user_passes_test(lambda u: u.is_staff)
def admin_add_product(request):
    if request.method == "POST":
        Product.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
            image_url=request.POST.get("image_url")
        )
        messages.success(request, "Product added successfully.")
        return redirect('store:admin_product_list')
    return render(request, 'admin_add_product.html')

@user_passes_test(lambda u: u.is_staff)
def admin_edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.image_url = request.POST.get("image_url")
        product.save()
        messages.success(request, "Product updated successfully.")
        return redirect('store:admin_product_list')
    return render(request, 'admin_edit_product.html', {'product': product})

@user_passes_test(lambda u: u.is_staff)
def admin_delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('store:admin_product_list')

# ----------------- USER PROFILE -----------------
@login_required(login_url='store:login')
def view_profile(request):
    
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required(login_url='store:login')
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.phone = request.POST.get("phone", profile.phone)
        profile.address = request.POST.get("address", profile.address)
        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('store:view_profile')
    return render(request, 'edit_profile.html', {'profile': profile})

# ----------------- ORDERS -----------------
@login_required(login_url='store:login')
def user_order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})

@user_passes_test(lambda u: u.is_staff)
def admin_order_list(request):
    orders = Order.objects.all()
    return render(request, 'admin_orders.html', {'orders': orders})

@user_passes_test(lambda u: u.is_staff)
def admin_update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.status = request.POST.get("status", order.status)
        order.save()
        messages.success(request, "Order status updated.")
        return redirect('store:admin_order_list')
    return render(request, 'admin_order_detail.html', {'order': order})

@user_passes_test(lambda u: u.is_staff)
def admin_delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Order deleted successfully.")
    return redirect('store:admin_order_list')

@login_required(login_url='store:login')
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    total = sum(item.subtotal() for item in items)
    
    # Simple form-handling for "Place Order"
    if request.method == "POST":
        # Create order
        order = Order.objects.create(user=request.user, total_amount=total, status="Pending")
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()  # Empty the cart
        messages.success(request, "Order placed successfully!")
        return redirect('store:my_orders')
    
    return render(request, 'checkout.html', {'cart': cart, 'items': items, 'total': total})

@login_required(login_url='store:login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.select_related('product').all()  # Or use order.orderitem_set.all() if using related_name
    return render(request, 'order_detail.html', {'order': order, 'items': items})
