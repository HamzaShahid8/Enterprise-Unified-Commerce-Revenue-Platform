from decimal import Decimal
import uuid
from django.core.management.base import BaseCommand
from products.models import Product, ProductVariant


class Command(BaseCommand):
    help = "Seed Product Variants"

    def handle(self, *args, **kwargs):

        variants = [
            {
                "product": "iPhone 16 Pro",
                "price": Decimal("299999.00"),
                "color": "Black",
                "size": "256GB",
            },
            {
                "product": "iPhone 16 Pro",
                "price": Decimal("349999.00"),
                "color": "White",
                "size": "512GB",
            },
            {
                "product": "Galaxy S25 Ultra",
                "price": Decimal("279999.00"),
                "color": "Titanium",
                "size": "256GB",
            },
        ]

        for data in variants:
            product = Product.objects.get(name=data["product"])

            variant, created = ProductVariant.all_objects.get_or_create(
                product=product,
                color=data["color"],
                size=data["size"],
                defaults={
                    "price": data["price"],
                    "is_deleted": False,
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Variant for '{product.name}' created."
                    )
                )

            elif variant.is_deleted:
                variant.is_deleted = False
                variant.price = data["price"]
                variant.save(
                    update_fields=[
                        "price",
                        "is_deleted",
                    ]
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Variant for '{product.name}' restored."
                    )
                )

            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Variant for '{product.name}' already exists."
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Product variants seeded successfully."
            )
        )