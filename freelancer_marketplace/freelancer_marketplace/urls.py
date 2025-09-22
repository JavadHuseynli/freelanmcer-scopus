
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def home_view(request):
    """Ana səhifə view"""
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
    # path('projects/', include('projects.urls')),  # sonra əlavə edəcəyik
    path('bids/', include('bids.urls')),          # sonra əlavə edəcəyik
    path('payments/', include('payments.urls')),  # sonra əlavə edəcəyik
    path('reviews/', include('reviews.urls')),    # sonra əlavə edəcəyik
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
