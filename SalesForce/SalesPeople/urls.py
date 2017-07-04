# from SalesPeople.views import update_sale
from django.conf.urls import *

from SalesPeople import views
from SalesPeople.views import update_sale

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<first_name>\w+)/$', views.get_sales_person, name='sales_person'),
    url(r'^(?P<first_name>\w+)/AddSale/', views.add_sale, name='first_name'),
    url(r'^(?P<first_name>\w+)/AddMeeting/', views.add_meeting, name='first_name'),
    url(r'^(?P<first_name>\w+)/AddCompany/', views.add_company, name='first_name'),
    url(r'^(?P<first_name>\w+)/AddCompanyRepresentative/', views.add_company_representative),
    # url(r'^(?P<first_name>\w+)/sales/(?P<company_name>\w+)/$', views.get_sale, name='company_name'),
    url(r'^(?P<first_name>\w+)/ViewSales/', views.show_sales, name='first_name'),
    url(r'^(?P<first_name>\w+)/EditSale/(?P<pk>[\w-]+)$', update_sale.as_view(), name='update_sale'),
]
