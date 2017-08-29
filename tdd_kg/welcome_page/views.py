from django.shortcuts import render
from welcome_page.models import MediaAppearance


def welcome_page(request):
    media_appearances = MediaAppearance.objects.all()
    return render(request, 'home.html', {'media_appearances': media_appearances})
