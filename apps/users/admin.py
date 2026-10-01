from django.contrib import admin
from .models.user import CustomUser
from .models.artisan import ArtisanProfile
from .models.customer import CustomerProfile

admin.site.register(CustomUser)
admin.site.register(ArtisanProfile)
admin.site.register(CustomerProfile)
