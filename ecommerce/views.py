from django.shortcuts import render
from .forms import ContactForm
from django.http import JsonResponse, HttpResponse


def home_page(request):
    return render(request, "home.html", {})


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'form': contact_form
    }
    if request.is_ajax():
        if contact_form.is_valid():
            return JsonResponse({'message': 'Thank you.'}, status=200)
        if contact_form.errors:
            return HttpResponse(contact_form.errors.as_json(), status=400, content_type='application/json')
    return render(request, "contact.html", context)
