
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Bid
from .forms import BidForm
from projects.models import Project
def test_func(self):
    bid = self.get_object()
    # Artıq hamı bid detail görə bilər (yalnız əməliyyatlar məhdud)
    return True  # Əvvəllər yalnız bid.freelancer və bid.project.customer görə bilirdi
class PublicBidListView(ListView):
    """Bütün açıq təkliflərin siyahısı"""
    model = Bid
    template_name = 'bids/public_bid_list.html'
    context_object_name = 'bids'
    paginate_by = 20
    
    def get_queryset(self):
        # Yalnız açıq layihələrin aktiv təkliflərini göstər
        return Bid.objects.filter(
            project__status='open',
            status='active'
        ).select_related('project', 'freelancer').order_by('-created_at')

class BidListView(LoginRequiredMixin, ListView):
    """İstifadəçinin bid-lərinin siyahısı"""
    model = Bid
    template_name = 'bids/bid_list.html'
    context_object_name = 'bids'
    paginate_by = 10
    
    def get_queryset(self):
        if self.request.user.is_freelancer:
            # Freelancer öz göndərdiyi bid-ləri görür
            return Bid.objects.filter(freelancer=self.request.user).order_by('-created_at')
        else:
            # Customer öz layihələrinə gələn bid-ləri görür
            return Bid.objects.filter(project__customer=self.request.user).order_by('-created_at')

class BidDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Bid-in təfərrüatlı məlumatları"""
    model = Bid
    template_name = 'bids/bid_detail.html'
    context_object_name = 'bid'
    
    def test_func(self):
        bid = self.get_object()
        # Yalnız bid sahibi və ya layihə sahibi görə bilər
        return (self.request.user == bid.freelancer or 
                self.request.user == bid.project.customer)

class BidCreateView(LoginRequiredMixin, CreateView):
    """Yeni bid yaratmaq (yalnız freelancer üçün)"""
    model = Bid
    form_class = BidForm
    template_name = 'bids/bid_create.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Yalnız freelancer-lər bid göndərə bilər
        if not request.user.is_authenticated or request.user.role != 'freelancer':
            messages.error(request, 'Təklif göndərmək üçün freelancer rolunda olmalısınız.')
            return redirect('projects:project_list')
        
        # Layihəni yoxlayaq
        self.project = get_object_or_404(Project, pk=kwargs['project_id'])
        
        # Açıq layihəyə təklif göndərmək olar
        if self.project.status != 'open':
            messages.error(request, 'Bu layihə artıq açıq deyil.')
            return redirect('projects:project_detail', pk=self.project.pk)
        
        # Eyni freelancer eyni layihəyə yalnız bir təklif göndərə bilər
        existing_bid = Bid.objects.filter(
            project=self.project, 
            freelancer=request.user
        ).first()
        if existing_bid:
            messages.error(request, 'Bu layihəyə artıq təklif göndərmişsiniz.')
            return redirect('bids:bid_detail', pk=existing_bid.pk)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context
    
    def form_valid(self, form):
        form.instance.project = self.project
        form.instance.freelancer = self.request.user
        messages.success(self.request, 'Təklifiniz uğurla göndərildi!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.project.pk})

class AcceptBidView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Bid-i qəbul etmək (yalnız layihə sahibi üçün)"""
    
    def test_func(self):
        bid = get_object_or_404(Bid, pk=self.kwargs['pk'])
        return self.request.user == bid.project.customer
    
    def post(self, request, *args, **kwargs):
        bid = get_object_or_404(Bid, pk=kwargs['pk'])
        
        if bid.project.status != 'open':
            messages.error(request, 'Bu layihə artıq açıq deyil.')
            return redirect('projects:project_detail', pk=bid.project.pk)
        
        # Bid-i qəbul et
        bid.status = 'accepted'
        bid.save()
        
        # Layihəni in_progress statusuna çevir
        bid.project.status = 'in_progress'
        bid.project.assigned_freelancer = bid.freelancer
        bid.project.save()
        
        # Digər bid-ləri rədd et
        other_bids = Bid.objects.filter(
            project=bid.project, 
            status='active'
        ).exclude(pk=bid.pk)
        other_bids.update(status='rejected')
        
        messages.success(request, f'{bid.freelancer.username} təklifi qəbul edildi!')
        return redirect('projects:project_detail', pk=bid.project.pk)

class RejectBidView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Bid-i rədd etmək (yalnız layihə sahibi üçün)"""
    
    def test_func(self):
        bid = get_object_or_404(Bid, pk=self.kwargs['pk'])
        return self.request.user == bid.project.customer
    
    def post(self, request, *args, **kwargs):
        bid = get_object_or_404(Bid, pk=kwargs['pk'])
        bid.status = 'rejected'
        bid.save()
        
        messages.success(request, 'Təklif rədd edildi.')
        return redirect('projects:project_detail', pk=bid.project.pk)

class WithdrawBidView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Bid-i geri çəkmək (yalnız bid sahibi üçün)"""
    
    def test_func(self):
        bid = get_object_or_404(Bid, pk=self.kwargs['pk'])
        return self.request.user == bid.freelancer
    
    def post(self, request, *args, **kwargs):
        bid = get_object_or_404(Bid, pk=kwargs['pk'])
        
        if bid.status != 'active':
            messages.error(request, 'Yalnız aktiv təkliflər geri çəkilə bilər.')
            return redirect('bids:bid_detail', pk=bid.pk)
        
        bid.status = 'withdrawn'
        bid.save()
        
        messages.success(request, 'Təklifiniz geri çəkildi.')
        return redirect('bids:bid_list')