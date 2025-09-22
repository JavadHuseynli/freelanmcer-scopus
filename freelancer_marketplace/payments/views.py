
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from .models import Payment
from .forms import PaymentForm
from projects.models import Project

class PaymentListView(LoginRequiredMixin, ListView):
    """İstifadəçinin ödəniş tarixçəsi"""
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 15
    
    def get_queryset(self):
        # İstifadəçinin roluna görə ödənişləri filtrləyir
        if self.request.user.is_customer:
            # Customer öz etdiyi ödənişləri görür
            return Payment.objects.filter(payer=self.request.user).order_by('-created_at')
        else:
            # Freelancer aldığı ödənişləri görür
            return Payment.objects.filter(receiver=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_customer:
            # Customer statistikaları
            context['total_paid'] = self.get_queryset().filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
            context['pending_payments'] = self.get_queryset().filter(status='pending').count()
        else:
            # Freelancer statistikaları
            context['total_earned'] = self.get_queryset().filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
            context['pending_earnings'] = self.get_queryset().filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0
        
        return context

class PaymentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Ödəniş təfərrüatları"""
    model = Payment
    template_name = 'payments/payment_detail.html'
    context_object_name = 'payment'
    
    def test_func(self):
        payment = self.get_object()
        # Yalnız payer və ya receiver görə bilər
        return (self.request.user == payment.payer or 
                self.request.user == payment.receiver)

class PaymentCreateView(LoginRequiredMixin, CreateView):
    """Yeni ödəniş yaratmaq"""
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment_create.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Layihəni yoxlayaq
        self.project = get_object_or_404(Project, pk=kwargs['project_id'])
        
        # Yalnız layihə sahibi ödəniş yarada bilər
        if request.user != self.project.customer:
            messages.error(request, 'Yalnız layihə sahibi ödəniş yarada bilər.')
            return redirect('projects:project_detail', pk=self.project.pk)
        
        # Layihə in_progress və ya completed statusunda olmalıdır
        if self.project.status not in ['in_progress', 'completed']:
            messages.error(request, 'Ödəniş üçün layihə icrada və ya tamamlanmış olmalıdır.')
            return redirect('projects:project_detail', pk=self.project.pk)
        
        # Təyin edilmiş freelancer olmalıdır
        if not self.project.assigned_freelancer:
            messages.error(request, 'Layihəyə freelancer təyin edilməyib.')
            return redirect('projects:project_detail', pk=self.project.pk)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context
    
    def form_valid(self, form):
        form.instance.project = self.project
        form.instance.payer = self.request.user
        form.instance.receiver = self.project.assigned_freelancer
        messages.success(self.request, 'Ödəniş qeydiyyatı yaradıldı!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('payments:payment_detail', kwargs={'pk': self.object.pk})

class PaymentConfirmView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Ödənişi təsdiqləmək"""
    
    def test_func(self):
        payment = get_object_or_404(Payment, pk=self.kwargs['pk'])
        # Yalnız payer təsdiqləyə bilər
        return self.request.user == payment.payer
    
    def post(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=kwargs['pk'])
        
        if payment.status != 'pending':
            messages.error(request, 'Yalnız gözləmədə olan ödənişlər təsdiqlənə bilər.')
            return redirect('payments:payment_detail', pk=payment.pk)
        
        # Ödənişi təsdiqlə
        payment.status = 'paid'
        payment.paid_at = timezone.now()
        payment.transaction_id = f"TXN_{payment.pk}_{timezone.now().strftime('%Y%m%d%H%M%S')}"
        payment.save()
        
        # Layihə statusunu yenilə
        if payment.project.status == 'in_progress':
            payment.project.status = 'completed'
            payment.project.save()
        
        messages.success(request, 'Ödəniş uğurla təsdiqləndi!')
        return redirect('payments:payment_detail', pk=payment.pk)

class PaymentDashboardView(LoginRequiredMixin, TemplateView):
    """Ödəniş dashboard"""
    template_name = 'payments/payment_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_customer:
            # Customer dashboard
            payments = Payment.objects.filter(payer=user)
            context.update({
                'total_spent': payments.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0,
                'pending_payments': payments.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0,
                'completed_projects': user.my_projects.filter(status='completed').count(),
                'active_projects': user.my_projects.filter(status='in_progress').count(),
                'recent_payments': payments.order_by('-created_at')[:5]
            })
        else:
            # Freelancer dashboard
            payments = Payment.objects.filter(receiver=user)
            context.update({
                'total_earned': payments.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0,
                'pending_earnings': payments.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0,
                'completed_projects': user.assigned_projects.filter(status='completed').count(),
                'active_projects': user.assigned_projects.filter(status='in_progress').count(),
                'recent_payments': payments.order_by('-created_at')[:5]
            })
        
        return context