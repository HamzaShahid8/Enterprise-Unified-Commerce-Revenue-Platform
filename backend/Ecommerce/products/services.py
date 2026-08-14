from django.db import transaction

from .models import Product, ProductVariant


class ProductService:

    @staticmethod
    @transaction.atomic
    def create(validated_data):
        variants = validated_data.pop("product_variants", [])

        product = Product.objects.create(**validated_data)

        ProductVariant.objects.bulk_create(
            [
                ProductVariant(
                    product=product,
                    **variant
                )
                for variant in variants
            ]
        )

        return product

    @staticmethod
    @transaction.atomic
    def update(product, validated_data):
        variants = validated_data.pop("product_variants", None)

        for key, value in validated_data.items():
            setattr(product, key, value)

        product.save()

        if variants is not None:
            product.product_variants.update(is_deleted=True)

            ProductVariant.objects.bulk_create(
                [
                    ProductVariant(
                        product=product,
                        **variant
                    )
                    for variant in variants
                ]
            )

        return product

    @staticmethod
    @transaction.atomic
    def delete(instance):
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted'])
        return instance

    @staticmethod
    @transaction.atomic
    def bulk_create(products_data):
        products = []

        for data in products_data:
            variants = data.pop("product_variants", [])

            product = Product.objects.create(**data)

            ProductVariant.objects.bulk_create(
                [
                    ProductVariant(
                        product=product,
                        **variant
                    )
                    for variant in variants
                ]
            )

            products.append(product)

        return products