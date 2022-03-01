# Controls what databases are able to be viewed on the admin site ("localhost:8000/admin/")
from django.contrib import admin

# Register models.
from .models import Restaurant, Review, Tag, Contact_us
admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Contact_us)