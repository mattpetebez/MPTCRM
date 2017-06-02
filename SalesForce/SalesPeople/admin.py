from django.contrib import admin

from .models import SalesPerson, Sale, Company, Meeting, CompanyRepresentative

# Register your models here.
admin.site.register(Sale)
admin.site.register(SalesPerson)
admin.site.register(CompanyRepresentative)
admin.site.register(Meeting)
admin.site.register(Company)
