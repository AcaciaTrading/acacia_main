from django.contrib import admin

from billing.models import Plan, Customer, Invoice

# Register your models here.
admin.site.register(Plan)
admin.site.register(Customer)
admin.site.register(Invoice)