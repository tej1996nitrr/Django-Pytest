from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.mail import send_mail
import stripe 
from django.shortcuts import redirect
from .models import Post
from .forms import PostForm
from django.views import generic
class HomeView(TemplateView):
    template_name = "birdie/home.html"


class AdminView(TemplateView):
    template_name = "birdie/admin.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminView, self).dispatch(request, *args, **kwargs)

class PostUpdateView(UpdateView):
    model = Post
    form_class=PostForm
    template_name = "birdie/update.html"
    success_url = "birdie/home.html"
    def post(self,request,*args,**kwargs):
        if getattr(request.user,'first_name',None)=='Python':
                raise Http404()
        return super(PostUpdateView,self).post(request,*args, **kwargs)

class PaymentView(generic.View):
    def post(self, request,*args, **kwargs):
        charge = stripe.Charge.create(
            amount=100,
            currency='sgd',
            description='',
            token=request.POST.get('token'),
        )
        send_mail(
            'Payment received',
            'Charge {} succeeded!'.format(charge),
            'server@example.com',
            ['admin@example.com'],
        )
        return redirect('/')