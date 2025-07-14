from django.shortcuts import render


def home(request):
    return render(request, 'test/home.html')

def setting(request):
    return render(request, 'test/setting.html')