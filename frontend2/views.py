from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def places(request):
    return render(request, 'places.html')