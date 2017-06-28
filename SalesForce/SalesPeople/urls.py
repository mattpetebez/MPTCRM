from django.conf.urls import url

from SalesPeople import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<first_name>\w+)/$', views.get_sales_person, name='sales_person'),
    url(r'^(?P<first_name>\w+)/AddSale/', views.add_sale, name='first_name'),
    url(r'^(?P<first_name>\w+)/AddMeeting/', views.add_meeting, name='first_name'),
    url(r'^(?P<first_name>\w+)/AddCompany/', views.add_company, name='first_name'),
    url(r'^(?P<first_name>\w+)/AddCompanyRepresentative/', views.add_company_representative),
    url(r'^(?P<first_name>\w+)/sales/(?P<company_name>\w+)/$', views.get_sale, name='company_name'),
]