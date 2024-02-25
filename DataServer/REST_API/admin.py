from django.contrib import admin
from .models import Transaction, ImportSchema

admin.site.register(Transaction)
admin.site.register(ImportSchema)
