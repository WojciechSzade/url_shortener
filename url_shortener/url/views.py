import random
import string
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from django.urls import reverse
from urllib.request import urlopen
from django.utils import timezone



def index(request):
    form = UrlForm(request.POST or None)
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            new_url = form.save(commit=False)
            new_url.shorten_url = generate(5)
            new_url.pub_date = timezone.now()
            new_url.count = 0
            new_url.save()

        context = {'original_url' : new_url.original_url, 'shorten_url' : new_url.shorten_url}
        return render(request, 'url/shorten.html', {'url' : new_url}) 
        # return HttpResponseRedirect('/url/shorten/' + new_url.shorten_url)
        # shorten(request, new_url.shorten_url, context)
        # return HttpResponse(f"Your shorten url is: {new_url.shorten_url}") 
    return render(request, 'url/index.html', {'form': form})
    

def generate(shorten_url_length):
    shorten_url = ""
    for i in range(shorten_url_length):
        shorten_url += random.choice(string.ascii_letters)
    return shorten_url


def shorten(request, slug, context):
    return render(request, 'url/shorten.html', { 'url': context})  

def redirect_outside(request, slug):
    url = get_object_or_404(Url, shorten_url=slug)
    url.count+=1
    url.save()
    #TODO count redirects
    # return HttpResponse(f"Redirecting to {url.original_url}")
    # return render(request, 'url/redirect.html', {'url': url})
    return redirect(url.original_url)


 