from django.core.management.base import BaseCommand
from products.models import Brand


class Command(BaseCommand):
    help = "Seed Brands"

    def handle(self, *args, **kwargs):

        brand_names = [
            "Samsung",
            "Apple",
            "Samsung",
            "Xiaomi",
            "OnePlus",
            "Google",
            "Oppo",
            "Apple",
            "Dell",
            "HP",
            "Lenovo",
            "Microsoft",
            "Dell",
            "HP",
            "Lenovo",
            "Apple",
            "Samsung",
            "Lenovo",
            "Huawei",
            "Xiaomi",
            "Microsoft",
            "JBL",
            "Canon",
            "Nikon",
            "Microsoft",
            "ASUS",
            "MSI",
            "Sony",
            "Logitech",
            "Anker",
            "LG",
        ]

        for name in set(brand_names):   # Duplicate names remove
            brand, created = Brand.all_objects.get_or_create(
                name=name,
                defaults={"is_deleted": False},
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Brand '{name}' created successfully."
                    )
                )

            elif brand.is_deleted:
                brand.is_deleted = False
                brand.save(update_fields=["is_deleted"])

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Brand '{name}' restored successfully."
                    )
                )

            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Brand '{name}' already exists."
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("Brands seeded successfully.")
        )