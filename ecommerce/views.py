from django.shortcuts import render
from .forms import ContactForm


def home_page(request):
    return render(request, "home.html", {})


def contact_page(request):
    context = {
        'form': ContactForm()
    }
    return render(request, "contact.html", context)