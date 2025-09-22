
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .forms import CustomUserCreationForm


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

@login_required
@require_POST
@csrf_protect
def logout_view(request):
    """Təhlükəsiz logout view - yalnız POST method"""
    logout(request)
    messages.success(request, 'Hesabınızdan uğurla çıxış etdiniz!')
    return redirect('home')

def register_view(request):
    """İstifadəçi qeydiyyatı səhifəsi"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hesab {username} üçün yaradıldı! İndi daxil ola bilərsiniz.')
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm(request.POST)
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    """İstifadəçi profil səhifəsi"""
    return render(request, 'users/profile.html', {'user': request.user})

class FreelancerListView(ListView):
    """Freelancerlərin siyahısı"""
    model = User
    template_name = 'users/freelancer_list.html'
    context_object_name = 'freelancers'
    paginate_by = 12
    
    def get_queryset(self):
        return User.objects.filter(
            role='freelancer', 
            is_active=True
        ).order_by('-created_at')

class FreelancerDetailView(DetailView):
    """Freelancerin təfərrüatlı məlumatları"""
    model = User
    template_name = 'users/freelancer_detail.html'
    context_object_name = 'freelancer'
    
    def get_queryset(self):
        return User.objects.filter(role='freelancer')