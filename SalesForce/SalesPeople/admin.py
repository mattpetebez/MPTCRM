from django.contrib import admin

from .models import SalesPerson, Sale, Company, Activity, CompanyRepresentative, Goal, SalesTeam, Currency, SaleType

# Register your models here.
admin.site.register(Sale)
admin.site.register(SalesPerson)
admin.site.register(CompanyRepresentative)
admin.site.register(Activity)
admin.site.register(Company)
admin.site.register(Goal)
admin.site.register(SalesTeam)
admin.site.register(Currency)
admin.site.register(SaleType)
