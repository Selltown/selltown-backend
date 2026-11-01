from django.contrib import admin
from .models.storefront import Storefront
from .models.storefront_slug import StorefrontSlug

admin.site.register(Storefront)
admin.site.register(StorefrontSlug)
