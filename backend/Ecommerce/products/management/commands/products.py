from django.core.management.base import BaseCommand
from products.models import Product, Category, Brand


class Command(BaseCommand):
    help = "Seed Products"

    def handle(self, *args, **kwargs):

        products = [
            {
                "name": "iPhone 16 Pro",
                "category": "Mobiles",
                "brand": "Apple",
                "stock": 50,
                "description": "Apple flagship smartphone",
            },
            {
                "name": "Galaxy S25 Ultra",
                "category": "Mobiles",
                "brand": "Samsung",
                "stock": 40,
                "description": "Samsung flagship smartphone",
            },
            {
                "name": "MacBook Pro M4",
                "category": "Laptops",
                "brand": "Apple",
                "stock": 25,
                "description": "Apple professional laptop",
            },
            {
                "name": "Dell XPS 15",
                "category": "Laptops",
                "brand": "Dell",
                "stock": 30,
                "description": "Dell premium laptop",
            },
        ]

        for data in products:

            category = Category.objects.get(
                name=data["category"]
            )

            brand = Brand.objects.get(
                name=data["brand"]
            )

            product, created = Product.all_objects.get_or_create(
                name=data["name"],
                defaults={
                    "category": category,
                    "brand": brand,
                    "stock": data["stock"],
                    "description": data["description"],
                    "is_deleted": False,
                },
            )

            if created:

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Product '{product.name}' created with stock {product.stock}."
                    )
                )

            elif product.is_deleted:

                product.is_deleted = False
                product.category = category
                product.brand = brand
                product.stock = data["stock"]
                product.description = data["description"]
                product.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Product '{product.name}' restored with stock {product.stock}."
                    )
                )

            else:

                self.stdout.write(
                    self.style.WARNING(
                        f"Product '{product.name}' already exists."
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("Products seeded successfully.")
        )