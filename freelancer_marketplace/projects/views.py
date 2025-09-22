
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Project
from .forms import ProjectForm

class ProjectListView(ListView):
    """Bütün açıq layihələrin siyahısı"""
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Project.objects.filter(status='open').order_by('-created_at')
        
        # Axtarış funksiyası
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(skills_required__icontains=search)
            )
        
        # Kateqoriya filtri
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Project.CATEGORY_CHOICES
        context['search'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context

class ProjectDetailView(DetailView):
    """Layihənin təfərrüatlı məlumatları"""
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    project = self.get_object()
    
    # İstifadəçinin bu layihəyə təklif göndərib-göndərmədiyi
    if self.request.user.is_authenticated and self.request.user.is_freelancer:
        user_bid = project.bids.filter(freelancer=self.request.user).first()
        context['user_has_bid'] = user_bid is not None
        if user_bid:
            context['user_bid'] = user_bid
    else:
        context['user_has_bid'] = False
    
    return context
   

class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Yeni layihə yaratmaq (yalnız customer üçün)"""
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_create.html'
    success_url = reverse_lazy('projects:project_list')
    
    def dispatch(self, request, *args, **kwargs):
        # Yalnız customer-lər layihə yarada bilər
        if not request.user.is_authenticated or request.user.role != 'customer':
            messages.error(request, 'Layihə yaratmaq üçün müştəri rolunda olmalısınız.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.customer = self.request.user
        messages.success(self.request, 'Layihə uğurla yaradıldı!')
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Layihə yeniləmək (yalnız sahib üçün)"""
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_update.html'
    
    def test_func(self):
        project = self.get_object()
        return self.request.user == project.customer
    
    def form_valid(self, form):
        messages.success(self.request, 'Layihə uğurla yeniləndi!')
        return super().form_valid(form)

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Layihə silmək (yalnız sahib üçün)"""
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:project_list')
    
    def test_func(self):
        project = self.get_object()
        return self.request.user == project.customer
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Layihə uğurla silindi!')
        return super().delete(request, *args, **kwargs)