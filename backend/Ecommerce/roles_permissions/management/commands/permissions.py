from django.core.management import BaseCommand
from roles_permissions.models import Permissions

class Command(BaseCommand):
    help = 'Create permissions.'
    
    def handle(self, *args, **kwargs):
        PERMISSIONS = [
            'create_permission',
            'update_permission',
            'view_permission',
            'delete_permission',
            'create_role',
            'update_role',
            'view_role',
            'delete_role',
            'create_role_permission',
            'update_role_permission',
            'view_role_permission',
            'delete_role_permission',
            'create_customer_profile',
            'update_customer_profile',
            'view_customer_profile',
            'delete_customer_profile',
            'create_manager_profile',
            'update_manager_profile',
            'view_manager_profile',
            'delete_manager_profile',
            'create_employee_profile',
            'update_employee_profile',
            'view_employee_profile',
            'delete_employee_profile',
            'create_category',
            'update_category',
            'view_category',
            'delete_category',
            'create_brand',
            'update_brand',
            'view_brand',
            'delete_brand',
            'create_product',
            'update_product',
            'view_product',
            'delete_product',
            'create_product_variant',
            'update_product_variant',
            'view_product_variant',
            'delete_product_variant',
            'create_order',
            'update_order',
            'view_order',
            'delete_order',
            'create_order_item',
            'update_order_item',
            'view_order_item',
            'delete_order_item',
            'create_bill',
            'update_bill',
            'view_bill',
            'delete_bill',
            'create_payment',
            'view_payment',
            'cancel_payment',
            'create_activity_logs',
            'update_activity_logs',
            'view_activity_logs',
            'delete_activity_logs',
        ]
        
        for permission_names in PERMISSIONS:
            permission, created = Permissions.objects.get_or_create(name=permission_names)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Permissions created: {permission_names}'))
            
            else:
                self.stdout.write(self.style.WARNING(f'Permissions already exist: {permission_names}'))
                
        else:
            self.stdout.write(self.style.SUCCESS(f'Permissions successfully seeding: {permission_names}'))