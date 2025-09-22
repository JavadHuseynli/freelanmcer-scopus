
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='payment_list'),
    path('<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('create/<int:project_id>/', views.PaymentCreateView.as_view(), name='payment_create'),
    path('<int:pk>/confirm/', views.PaymentConfirmView.as_view(), name='payment_confirm'),
    path('dashboard/', views.PaymentDashboardView.as_view(), name='payment_dashboard'),
]