from accounts.models import *
from roles_permissions.models import *
from profiles.models import *
from products.models import *
from orders.models import *
from billing.models import *
from stripe_payment.models import *
from django.db import transaction

class DashboardService:
    
    @staticmethod
    def get_data(user):
        
        if user.role.name == 'manager':
            
            total_users = User.objects.count()
            verified_emails = User.objects.filter(is_email_verified=True).count()
            customer_role = list(Roles.objects.filter(name = 'customer').values())
            employe_role = list(Roles.objects.filter(name='employe').values())
            permissions = list(Permissions.objects.values())
            customer_profiles = CustomerProfile.objects.count()
            employe_profiles = EmployeeProfile.objects.count()
            brands = list(Brand.objects.values())
            categories = list(Category.objects.values())
            products = Product.objects.count()
            product_stock = list(Product.objects.filter(stock__lte = 15).values())
            product_variants = ProductVariant.objects.count()
            total_orders = Order.objects.count()
            total_order_items = OrderItem.objects.count()
            delivered = Order.objects.filter(status = 'delivered').count()
            shipped = Order.objects.filter(status = 'shipped').count()
            cancelled = Order.objects.filter(status = 'cancelled').count()
            paid = Order.objects.filter(payment_status = 'paid').count()
            refunded = Order.objects.filter(payment_status='refunded').count()
            pending = Order.objects.filter(payment_status='pending').count()
            order_revenue = Order.objects.filter(status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
            invoices = Invoice.objects.count()
            
            return {
                'total_users': total_users,
                'verified_emails': verified_emails,
                'customer_role': customer_role,
                'employe_role': employe_role,
                'permissions': permissions,
                'customer_profiles': customer_profiles,
                'employe_profiles': employe_profiles,
                'brands': brands,
                'categories': categories,
                'products': products,
                'product_stock': product_stock,
                'product_variants': product_variants,
                'total_orders': total_orders,
                'total_order_items': total_order_items,
                'delivered': delivered,
                'shipped': shipped,
                'cancelled': cancelled,
                'paid': paid,
                'refunded': refunded,
                'pending': pending,
                'order_revenue': order_revenue,
                'invoices': invoices,
            }
            
        elif user.role.name == 'employe':
            
            customer_users = User.objects.filter(role__name='customer').count()
            employe_users = User.objects.filter(role__name='employe').count()
            customer_profiles = CustomerProfile.objects.count()
            employe_profiles = EmployeeProfile.objects.count()
            roles = Roles.objects.count()
            permissions = Permissions.objects.count()
            products = Product.objects.count()
            products_stock = Product.objects.filter(stock__lte = 20).values()
            product_variants = ProductVariant.objects.count()
            orders = Order.objects.count()
            delivered = Order.objects.filter(status = 'delivered').count()
            shipped = Order.objects.filter(status = 'shipped').count()
            cancelled = Order.objects.filter(status = 'cancelled').count()
            paid = Order.objects.filter(payment_status = 'paid').count()
            refunded = Order.objects.filter(payment_status='refunded').count()
            pending = Order.objects.filter(payment_status='pending').count()
            order_revenue = Order.objects.filter(status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
            invoices = Invoice.objects.count()
            
            return {
                'customer_users': customer_users,
                'employe_users': employe_users,
                'customer_profiles': customer_profiles,
                'employe_profiles': employe_profiles,
                'roles': roles,
                'permissions': permissions,
                'products': products,
                'products_stock': products_stock,
                'product_variants': product_variants,
                'orders': orders,
                'delivered': delivered,
                'shipped': shipped,
                'cancelled': cancelled,
                'paid': paid,
                'refunded': refunded,
                'pending': pending,
                'order_revenue': order_revenue,
                'invoices': invoices,
            }
            
        elif user.role.name == 'customer':
            
            pending_orders = Order.objects.filter(status='pending').count()
            paid_orders = Order.objects.filter(status='paid').count()
            shipped_orders = Order.objects.filter(status='shipped').count()
            cancelled_orders = Order.objects.filter(status='cancelled').count()
            customer_profile = CustomerProfile.objects.filter(user=user).values().first()
            
            return {
                'pending_orders': pending_orders,
                'paid_orders': paid_orders,
                'shipped_orders': shipped_orders,
                'cancelled_orders': cancelled_orders,
                'customer_profile': customer_profile,
            }
            
        else:
            return {
                'Message': 'Unknown role.'
            }