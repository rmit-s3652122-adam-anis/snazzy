from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'shop/home.html')

def about(request):
    return render(request, 'shop/about.html', {'title': 'About'})