import random
import string

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import *
from .forms import *


def index(request):
    """Path: domain/ The main page, with input form to get original_url with POST, when got, redirect to shorten_url page"""
    form = UrlForm(request.POST or None)
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            new_url = form.save(commit=False)
            new_url.save()
            return HttpResponseRedirect(reverse("url:shorten", args=(new_url.shorten_url,)))
    return render(request, "url/index.html", {"form": form})


def shorten(request, slug):
    """Path: domain/shorten/shorten_url The page to show generated shorten_url and original_url"""
    url = get_object_or_404(Url, shorten_url=slug)
    return render(request, "url/shorten.html", {"url": url})


def redirect_outside(request, slug):
    """Path: domain/shorten_url Redirect to original_url and updates Url model"""
    url = get_object_or_404(Url, shorten_url=slug)
    url.count += 1
    url.last_access = timezone.now()
    url.save()
    return redirect(url.original_url_link)
