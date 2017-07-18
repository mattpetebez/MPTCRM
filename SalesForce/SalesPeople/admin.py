from django.contrib import admin

from .models import SalesPerson, Sale, Company, Activity, CompanyRepresentative, Goal, SalesTeam

# Register your models here.
admin.site.register(Sale)
admin.site.register(SalesPerson)
admin.site.register(CompanyRepresentative)
admin.site.register(Activity)
admin.site.register(Company)
admin.site.register(Goal)
admin.site.register(SalesTeam)
