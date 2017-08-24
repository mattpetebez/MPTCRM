# from SalesPeople.views import update_sale
from django.conf.urls import *

from SalesPeople import views
from SalesPeople.views import UpdateSale, DeleteSale, UpdateActivity, DeleteActivity #UpdateProfile
from SalesPeople.views import activate_account

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ActivateAccount/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)$',
        activate_account, name='activate_account'),
    url(r'^(?P<first_name>\w+)/$', views.individual_dashboard, name='sales_person'),
    # url(r'^(?P<first_name>\w+)/EditProfile$', views.edit_profile),
    url(r'^(?P<first_name>\w+)/AddSaleType/', views.add_sale_type),
    url(r'^(?P<first_name>\w+)/AddSale/', views.add_sale, name='first_name'),
    url(r'^(?P<first_name>\w+)/AddActivity/', views.add_activity, name='first_name'),
    url(r'^(?P<first_name>\w+)/AddCompany/', views.add_company, name='first_name'),
    url(r'^(?P<first_name>\w+)/AddCompanyRepresentative/', views.add_company_representative),
    url(r'^(?P<first_name>\w+)/ViewSales/', views.show_sales, name='first_name'),
    url(r'^(?P<first_name>\w+)/ViewActivities/', views.show_activities, name='first_name'),
    url(r'^(?P<first_name>\w+)/EditSale/(?P<pk>[\w-]+)$', UpdateSale.as_view(), name='update_sale'),
    url(r'^(?P<first_name>\w+)/DeleteSale/(?P<pk>[\w-]+)$', DeleteSale.as_view()),
    url(r'^(?P<first_name>\w+)/EditActivity/(?P<pk>[\w-]+)$', UpdateActivity.as_view(), name='update_meeting'),
    url(r'^(?P<first_name>\w+)/DeleteActivity/(?P<pk>[\w-]+)$', DeleteActivity.as_view()),
    url(r'^(?P<first_name>\w+)/ViewPendingSales/', views.view_pending_sales, name='first_name'),
    url(r'^(?P<first_name>\w+)/ViewCompletedSales/', views.view_completed_sales, name='first_name'),
    url(r'^ViewTeam/(?P<pk>[\w-]+)', views.view_team),
    url(r'^ViewTeams/', views.view_all_teams),
    url(r'^(?P<first_name>\w+)/AddTeam/', views.add_team),
    url(r'^EditTeam/(?P<pk>[\w-]+)$', views.update_team),
]
