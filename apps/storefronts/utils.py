from django.utils.text import slugify
from .models.storefront_slug import StorefrontSlug


def generate_unique_slug(name):
    base_slug = slugify(name) or "storefront"
    slug = base_slug
    counter = 2

    while StorefrontSlug.objects.filter(slug=slug).exists():
        slug = f"{base_slug}--{counter}"
        counter += 1

    return slug
