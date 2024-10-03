from django.shortcuts import render

def menu_home_page(request):
    return render(request, 'index.html')
