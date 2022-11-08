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
            return HttpResponseRedirect(reverse('url:shorten', args=(new_url.shorten_url,)))
        #return render(request, 'url/shorten.html', {'url' : new_url}) 
    return render(request, 'url/index.html', {'form': form})
    

def generate(shorten_url_length):
    shorten_url = ""
    for i in range(shorten_url_length):
        shorten_url += random.choice(string.ascii_letters)
    return shorten_url


def shorten(request, slug):
    url = get_object_or_404(Url, shorten_url=slug)
    return render(request, 'url/shorten.html', {'url' : url})
    

def redirect_outside(request, slug):
    url = get_object_or_404(Url, shorten_url=slug)
    url.count+=1
    url.last_access = timezone.now()
    url.save()
    return redirect("http://" + url.original_url)


 