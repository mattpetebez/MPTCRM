# from SalesPeople.views import update_sale
from django.conf.urls import *

from SalesPeople import views
from SalesPeople.views import UpdateSale, DeleteSale, UpdateMeeting, DeleteMeeting

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<first_name>\w+)/$', views.get_sales_person, name='sales_person'),
    url(r'^(?P<first_name>\w+)/AddSale/', views.add_sale, name='first_name'),
    url(r'^(?P<first_name>\w+)/AddMeeting/', views.add_meeting, name='first_name'),
    url(r'^(?P<first_name>\w+)/AddCompany/', views.add_company, name='first_name'),
    url(r'^(?P<first_name>\w+)/AddCompanyRepresentative/', views.add_company_representative),
    url(r'^(?P<first_name>\w+)/ViewSales/', views.show_sales, name='first_name'),
    url(r'^(?P<first_name>\w+)/ViewMeetings/', views.show_meetings, name='first_name'),
    url(r'^(?P<first_name>\w+)/EditSale/(?P<pk>[\w-]+)$', UpdateSale.as_view(), name='update_sale'),
    url(r'^(?P<first_name>\w+)/DeleteSale/(?P<pk>[\w-]+)$', DeleteSale.as_view()),
    url(r'^(?P<first_name>\w+)/EditMeeting/(?P<pk>[\w-]+)$', UpdateMeeting.as_view(), name='update_meeting'),
    url(r'^(?P<first_name>\w+)/DeleteMeeting/(?P<pk>[\w-]+)$', DeleteMeeting.as_view()),
    url(r'^(?P<first_name>\w+)/ViewPendingSales/', views.view_pending_sales, name='first_name'),
    url(r'^(?P<first_name>\w+)/ViewCompletedSales/', views.view_completed_sales, name='first_name'),
    url(r'^ViewTeam/(?P<pk>[\w-]+)', views.view_team),
    url(r'^(?P<first_name>\w+)/AddTeam/', views.add_team),
]
