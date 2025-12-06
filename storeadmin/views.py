from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from store.models import Product, Order

from storeadmin.models import StoreAdmin

# -----------------
# CUSTOM ADMIN LOGIN / LOGOUT
# -----------------
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            admin_user = StoreAdmin.objects.get(username=username)
        except StoreAdmin.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect("storeadmin:admin_login")

        if admin_user.check_password(password):
            if not admin_user.is_active:
                messages.error(request, "Admin account is disabled.")
                return redirect("storeadmin:admin_login")

            request.session["store_admin_id"] = admin_user.id
            request.session["store_admin_username"] = admin_user.username
            return redirect("storeadmin:admin_dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("storeadmin:admin_login")

    return render(request, "loginadmin.html")

def admin_logout(request):
    request.session.pop("store_admin_id", None)
    request.session.pop("store_admin_username", None)
    return redirect("storeadmin:admin_login")


# -----------------
# CUSTOM ADMIN AUTH DECORATOR
# -----------------
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if "store_admin_id" not in request.session:
            return redirect("storeadmin:admin_login")
        return view_func(request, *args, **kwargs)
    return wrapper


# -----------------
# DASHBOARD
# -----------------
@admin_required
def admin_dashboard(request):
    context = {
        "product_count": Product.objects.count(),
        "order_count": Order.objects.count(),
        "admin_user": request.session.get("store_admin_username"),
    }
    return render(request, "admindashboard.html", context)


# -----------------
# PRODUCT CRUD
# -----------------
@admin_required
def admin_products(request):
    products = Product.objects.all()
    return render(request, "admin_products.html", {"products": products})

@admin_required
def admin_add_product(request):
    if request.method == "POST":
        Product.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
            image_url=request.POST.get("image_url"),
        )
        messages.success(request, "Product added successfully!")
        return redirect("storeadmin:admin_products")
    return render(request, "admin_add_product.html")

@admin_required
def admin_edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.image_url = request.POST.get("image_url")
        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect("storeadmin:admin_products")
    return render(request, "admin_add_product.html", {"product": product, "edit": True})

@admin_required
def admin_delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("storeadmin:admin_products")


# -----------------
# ORDER MANAGEMENT
# -----------------
@admin_required
def admin_orders(request):
    orders = Order.objects.all().order_by("-id")
    return render(request, "admin_orders.html", {"orders": orders})

@admin_required
def admin_order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    items = order.items.all()
    total = sum(item.product.price * item.quantity for item in items if item.product)
    return render(request, "admin_order_detail.html", {"order": order, "items": items, "total": total})

@admin_required
def admin_update_order_status(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == "POST":
        order.status = request.POST.get("status")
        order.save()
        messages.success(request, "Order status updated successfully!")
        return redirect("storeadmin:admin_orders")
    return render(request, "admin_update_order_status.html", {"order": order})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from store.models import Order

@admin_required
def admin_delete_order(request, id):
    order = get_object_or_404(Order, id=id)
    order.delete()
    messages.success(request, "Order deleted successfully!")
    return redirect("storeadmin:admin_orders")
