from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = "Seed Categories"

    def handle(self, *args, **kwargs):
        categories = [
            "Electronics",
            "Mobiles",
            "Laptops",
            "Computers",
            "Tablets",
            "Accessories",
            "Audio",
            "Cameras",
            "Gaming",
        ]

        for category_name in categories:
            category, created = Category.all_objects.get_or_create(
                name=category_name,
                defaults={"is_deleted": False},
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Category '{category_name}' created."
                    )
                )

            elif category.is_deleted:
                category.is_deleted = False
                category.save(update_fields=["is_deleted"])

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Category '{category_name}' restored."
                    )
                )

            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Category '{category_name}' already exists."
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("Categories seeded successfully.")
        )