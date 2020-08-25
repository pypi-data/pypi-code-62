from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.conf import settings
from django.contrib import messages
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator
from .models import Post
import requests
import json

# Create your views here.

def index(request):
    return render(request,'index.html')


def emailView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            from_email = settings.EMAIL_HOST_USER
            header = 'Coronavirus Information'
            if name and message and email:
                msg = 'Name : '+name + '\nEmail : ' + email + '\nMessage : '+message

                try:
                    send_mail(name, msg, email, ['jubel8180@gmail.com','sushenbiswasaga@gmail.com'],fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                form = ContactForm()
                messages.success(request, 'Thanks for your message! You will reply quickly')

                return HttpResponseRedirect(request.path_info)
            return HttpResponse('Make sure all fields are entered and valid.')
    else:
        form = ContactForm()
    return render(request, 'index.html', {'form': form})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')


class PostView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'index.html'
    
    
    def get_queryset(self):
        return Post.objects.all().order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        # context['description'] = context['description'][300:]+'<span id="dots">...</span>'+context['description'][301:]
        # print(context['description'])
        context['world_info'] = koronaInfo()
        return context
    
def koronaInfo():
    response = requests.get("https://corona.lmao.ninja/countries?fbclid=IwAR361IpY2mbXU7twwKwwiYX3u6vMiDj3IGzgtNIFQhC0pI0UzaTS_Hq1Gh4")
    data = response.json() 
    return data
    
