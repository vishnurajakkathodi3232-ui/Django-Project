from django.contrib import admin
from .models import Product, Order, OrderItem, Cart, CartItem, UserProfile

# =========================
# PRODUCT ADMIN
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('price',)

# =========================
# CART ADMIN
# =========================
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('subtotal_display',)

    def subtotal_display(self, obj):
        return f"₹{obj.subtotal():,.2f}"
    subtotal_display.short_description = 'Subtotal'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'total_display')
    inlines = [CartItemInline]

    def total_display(self, obj):
        return f"₹{obj.total_price():,.2f}"
    total_display.short_description = 'Total Price'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'subtotal_display')

    def subtotal_display(self, obj):
        return f"₹{obj.subtotal():,.2f}"
    subtotal_display.short_description = 'Subtotal'

# =========================
# ORDER ADMIN
# =========================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'status', 'total_amount')
    list_filter = ('status',)
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')

# =========================
# USER PROFILE ADMIN
# =========================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'phone')
