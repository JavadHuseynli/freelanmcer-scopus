
from django.urls import path
from . import views

app_name = 'bids'

urlpatterns = [
    path('', views.BidListView.as_view(), name='bid_list'),
    path('create/<int:project_id>/', views.BidCreateView.as_view(), name='bid_create'),
    path('<int:pk>/', views.BidDetailView.as_view(), name='bid_detail'),
    path('<int:pk>/accept/', views.AcceptBidView.as_view(), name='accept_bid'),
    path('<int:pk>/reject/', views.RejectBidView.as_view(), name='reject_bid'),
    path('<int:pk>/withdraw/', views.WithdrawBidView.as_view(), name='withdraw_bid'),
    path('public/', views.PublicBidListView.as_view(), name='public_bid_list'),

]