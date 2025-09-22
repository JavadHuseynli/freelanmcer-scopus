from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.ReviewListView.as_view(), name='review_list'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('create/<int:project_id>/', views.ReviewCreateView.as_view(), name='review_create'),
]