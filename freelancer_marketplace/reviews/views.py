
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from projects.models import Project

class ReviewListView(LoginRequiredMixin, ListView):
    """İstifadəçinin rəyləri"""
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10
    
    def get_queryset(self):
        if self.request.user.is_customer:
            return Review.objects.filter(reviewer=self.request.user).order_by('-created_at')
        else:
            return Review.objects.filter(freelancer=self.request.user).order_by('-created_at')

class ReviewDetailView(LoginRequiredMixin, DetailView):
    """Rəy təfərrüatları"""
    model = Review
    template_name = 'reviews/review_detail.html'
    context_object_name = 'review'

class ReviewCreateView(LoginRequiredMixin, CreateView):
    """Yeni rəy yazmaq"""
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['project_id'])
        
        if request.user != self.project.customer:
            messages.error(request, 'Yalnız layihə sahibi rəy yaza bilər.')
            return redirect('projects:project_detail', pk=self.project.pk)
        
        if self.project.status != 'completed':
            messages.error(request, 'Yalnız tamamlanmış layihələr üçün rəy yaza bilərsiniz.')
            return redirect('projects:project_detail', pk=self.project.pk)
            
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context
    
    def form_valid(self, form):
        form.instance.project = self.project
        form.instance.reviewer = self.request.user
        form.instance.freelancer = self.project.assigned_freelancer
        messages.success(self.request, 'Rəyiniz uğurla əlavə edildi!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.project.pk})
