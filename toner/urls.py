from django.urls import path
from . import views

urlpatterns = [
    path('toner_requests/', views.TonerRequestsView.as_view(), name='toner_requests'),
    path('toner_requests/<int:pk>/', views.TonerRequestsDetailView.as_view(), name='toner_request_detail'),
    path('toners/', views.TonersView.as_view(), name='toners'),
    path('toners/<pk_or_name>/', views.TonerDetailView.as_view(), name='toner_detail'),
    path('printers/', views.PrintersView.as_view(), name='printers'),
    path('printers/<pk_or_name>/', views.PrintersDetailView.as_view(), name='printer_detail'),
    path('departments/', views.DepartmentsView.as_view(), name='departments'),
    path('departments/<pk_or_name>/', views.DepartmentsDetailView.as_view(), name='department_detail'),

    path('locations/', views.LocationsView.as_view(), name='locations'),
    path('locations/<pk_or_name>/', views.LocationssDetailView.as_view(), name='location_detail'),
    # path('users/', views.Userall_view, name='users'),
    # path('users/<int:pk>/', views.User_detail, name='user_detail'),
    # path('routes/', views.getRoutes, name='get_routes'),
]
